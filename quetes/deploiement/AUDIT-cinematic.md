# BMC-103, partie 1 — Audit de Cinematic Interactions (Forge 1.20.1)

Fork `Arts44/CinematicInteractions`, branche `bmc4`, commit `f88a182`, sur
`bb1bca1` (amont, 0.18.30, dernier commit au 30 octobre). SHA-1 du jar :
`1e997add34030ef010c7246fc63cff29a108f335`.

Tout vient de la lecture du code et des jars du pack (instance `BMC4 v65`).
**Rien n'a tourné en jeu ni sur un serveur** ; le projet n'a pas de tests
unitaires (`test NO-SOURCE`).

## 1. À trancher avant de déployer : l'établi

Le patch ne protège pas les objets posés sur un établi dans un claim :

- `minecraft:crafting_table` est dans `ftbchunks:interact_whitelist` (jar FTB
  Chunks 2001.3.8) : FTB Chunks laisse toujours passer, quel que soit
  `block_interact_mode`.
- `bmc4_garde.js` exempte ce même tag (`TOUJOURS_OUVERTS`).
- Le patch demande donc l'avis de FTB et de la garde, qui répondent oui. Un
  ennemi ouvre la scène et prend les objets.
- Il existe un chemin sans la scène : `ServerPlayerMixin` → `TableActions.intoWindow`
  verse le contenu de la table dans toute fenêtre d'établi ouverte, même par un
  client sans le mod.

Visual Workbench, déjà dans le pack, pose le même problème aujourd'hui : il met
une BlockEntity sur l'établi et y garde la grille, exemptée par le même tag.

Solution proposée : dans `bmc4_garde.js`, traiter `minecraft:crafting_table`
comme un bloc à inventaire (fermé aux autres factions, sauf alliés et raid). Une
condition de plus dans `coffreInterdit`, avant le test des `TOUJOURS_OUVERTS`.
Effet : on ne peut plus crafter sur l'établi d'une autre faction. Le patch et la
fenêtre vanilla passent par la même garde, donc les deux chemins sont couverts.

## 2. Le patch (`f88a182`)

- `begin()` et `openWindow()` appellent `mayUse()` : `player.mayInteract`, puis
  un `RightClickBlock` serveur. Un refus envoie `SessionClosePayload`.
- **Écart avec la demande, volontaire.** Le mod a son propre écouteur de
  `RightClickBlock` (priorité NORMAL), qui annule l'événement côté serveur. Sans
  précaution, tout serait refusé. L'écouteur sert donc de point d'arrêt : pendant
  la sonde, il note qu'il a été atteint et annule. Refus si non atteint (une
  protection a annulé avant) ou si `getUseBlock() == DENY`.
- **Pourquoi l'arrêter là.** 50 mods du pack écoutent `RightClickBlock`
  (Create, Mowzie's, Zeta/Quark, Supplementaries…). L'événement ne doit pas leur
  faire jouer une seconde fois un usage. FTB Chunks et KubeJS passent par
  Architectury en priorité HIGH, donc avant le point d'arrêt.
- **Reste un effet de bord possible :** les écouteurs HIGH/HIGHEST et ceux en
  NORMAL enregistrés avant le mod voient l'événement deux fois. Car, contrairement
  à l'analyse de départ, le client envoie bien le paquet d'usage vanilla (lambda
  de `MultiPlayerGameMode.useItemOn`) : le serveur a déjà un événement réel. Cet
  événement réel n'est pas suffisant pour autant, car `BEGIN` peut arriver seul
  (touche du feu de camp, client modifié).
- `valid()` : aucune session n'est créée après un refus (`SESSIONS.put` vient
  après). Le refus dans `begin()` ferme en plus une session déjà ouverte ailleurs :
  sinon le client se fermait et le serveur la gardait.
- `openWindow()` n'a pas de face : `Direction.UP` (FTB et la garde ne la lisent pas).

### Les autres entrées serveur

| Entrée | Passe par | Vérification ajoutée |
|---|---|---|
| Feu de camp, touche H | `BEGIN` | oui, par `begin()` |
| PLACE, SPREAD, CLICK, PAINT, CRAFT, QUICK, CHOOSE | exigent une session | non nécessaire |
| Juke-box, bibliothèque sans scène | `WINDOW` → `vanillaUse` | oui, par `openWindow()` |
| `NeighborNotify` → `spill` | bloc déjà retiré par quelqu'un d'autre | non nécessaire |
| `intoWindow` | toute fenêtre d'établi | voir point 1 |

### Limite restante

`valid()` ne redemande pas la permission : une session ouverte pendant un raid
survit à la fin du raid tant que le joueur reste à moins de 6 blocs. La sonde à
chaque tick déclencherait les écouteurs à chaque fois, je ne l'ai pas ajoutée.

## 3. Audit dupes et pertes

Aucune duplication certaine trouvée. Les opérations se font sur le thread
serveur, et le paquet passe par `consumerMainThread` : deux joueurs sur un même
établi sont traités l'un après l'autre.

| Cas | Code | Verdict |
|---|---|---|
| Sauvegarde | `TableStore`, `setDirty` dans `finish`/`remove` | correct |
| Établi cassé ou explosé en scène | `onNeighborNotify` → `spill` → `dropContents`, `endAllAt` | objets au sol, une fois ; repli toutes les 40 ticks (`onLevelTick`) |
| Déconnexion | `onLogout` → `Sessions.end` : le curseur revient à l'inventaire | correct |
| Mort | `onDeath` → `end`, avant le butin | à vérifier avec YIGD en jeu |
| Deux joueurs, même case | `click`, séquentiel ; échange de piles | pas de dupe |
| `TableCrafting.craftOnce` | consomme la table, reste rendu sur place ou à l'inventaire | correct |
| Sortie du four | `takeResult` : `removeItem` puis copie au curseur | correct ; XP comme le slot vanilla |
| `FurnaceActions.quickMove` | `split`/`grow`, vérifie `canPlaceItem` | correct |
| `MenuActions.quickMove` | restaure l'inventaire si rien n'est entré | correct tant qu'un mod ne déplace pas vers autre chose qu'une slot de station (Easy Anvils, testé par l'auteur) |
| Feu de camp | `advanceStalledSlot`, garde par tick | correct |

Risques à connaître :

1. **Perte, retrait du mod** : `cinematic_tables.dat` n'est lu que par le mod.
2. **Perte, arrêt brutal** : l'objet tenu au curseur en scène n'est pas dans
   l'inventaire. `onServerStopped` fait `Sessions.clear()` sans le rendre. Sur un
   plantage, il est perdu, comme un curseur vanilla. L'arrêt normal passe par la
   déconnexion, non vérifié sur notre redémarrage de 5 h.
3. **Paquet trop gros** : `TableContentsPayload` envoie les neuf piles avec leur
   NBT à chaque joueur qui charge le chunk (`onChunkSent`). Neuf objets très
   chargés (boîtes pleines de livres écrits) pourraient dépasser la limite d'un
   paquet et déconnecter tout joueur qui approche. Non essayé.
4. **Visual Workbench** : deux stockages sur un même établi (BlockEntity et
   `TableStore`). `intoWindow` s'arrête si la grille n'est pas vide : les objets de
   la scène restent alors sur la table. Pas de dupe vue, à essayer.

## 4. Mixins (point 5)

Cible forge : 4 communs (`AbstractFurnaceBlockEntityMixin`,
`BrewingStandBlockEntityMixin`, `CraftingMenuAccess`, `ServerPlayerMixin`) et 10
clients (`CameraMixin`, `CampfireRendererMixin`, `ExperienceOrbRendererMixin`,
`FirstPersonHandsMixin`, `HumanoidArmorLayerMixin`, `HumanoidModelMixin`,
`ItemInHandLayerMixin`, `LecternRendererMixin`, `MouseHandlerMixin`,
`PlayerRendererMixin`). `required: true`, `defaultRequire: 1` : une injection
ratée fait planter le démarrage, ce qui se verra tout de suite.

Scan du pack : aucun `@Overwrite` sur ces classes.

| Mod | Ce qu'il touche | Évaluation |
|---|---|---|
| Oculus 1.8.0 | `ItemInHandRenderer.renderArmWithItem` | testé par l'auteur avec Embeddium 0.3.31 et Complementary |
| Xenon 0.3.31 | fork d'Embeddium | **non testé**, même base |
| Distant Horizons | lit la caméra au rendu | **douteux** : la scène déplace la caméra loin des yeux ; notre config met `useCameraPositionForQualityDropOff` à faux |
| Leawind | `MouseHandler.turnPlayer`, invoker caméra | scène en première personne forcée (`Scene.java:278`) ; **douteux** : Alt gauche (`FreeLook`) repasse en troisième personne |
| Do a Barrel Roll | `Camera.update`, souris | en vol seulement ; peu probable |
| Not Enough Animations | `renderPlayerArm`, modèle | **douteux** : bras vus par les autres joueurs |
| playerAnimator | `renderHandsWithItems` | **douteux** : même méthode que `FirstPersonHandsMixin`, annulée en HEAD |
| First-person Model | absent du pack | issue #12 sans objet |
| SecurityCraft | `evaluateWhichHandsToRender` | `CameraMixin` ne vise que `LocalPlayer` ; peu probable |
| Immersive Portals | `Camera.setup`, `isDetached` | **douteux** : `setup` tourne aussi pour le rendu des portails, et `CameraMixin` s'applique à chaque appel ; essayer une station à côté d'un portail |
| Amendments 2.2.6 | `BrewingStandBlockEntity` | issue #15 corrigée : le mixin ne porte plus `getUpdatePacket`, testé par l'auteur (`withAmendments`) |
| Iron's Spells | `LecternRenderer` | même `render` ; à regarder sur un lutrin |
| JEI | | issues #26 (curseur bloqué) et #29 (bras étirés) ouvertes sur d'autres versions ; à essayer |
| Easy Anvils, Easy Magic | menus remplacés | testés par l'auteur (`withEasyMods`), `MenuActions.isOpen` en `instanceof` |

## 5. Touches (point 6)

Défauts du mod : `key.cinematic.sit` sur H, `key.cinematic.look` sur Alt gauche.

- H sert déjà à 5 actions : `hide_icons`, jetpack, `cycleRight`, Aether Redux, inventaire du dragon.
- Alt gauche à 7 : sorts d'Iron, Deep Aether, Steam 'n' Rails (2), ramper, Create (2).

Proposé, pour `configureddefaults/options.txt` :

    key_key.cinematic.sit:key.keyboard.left.bracket
    key_key.cinematic.look:key.keyboard.backslash

Soit ^ et * sur AZERTY, libres dans les 269 assignations de l'instance et hors de
celles déjà réservées (ù, ², F7, F8, F9). Non vérifié en jeu. ConfiguredDefaults ne
sert qu'aux nouvelles instances : qui migre ses réglages garde H et Alt gauche.

## 6. Config (point 7)

`armStyle` vaut 0, « Stretched », par défaut (`Settings.java`). **Rien à livrer.**
Le fichier est `config/cinematic-client.toml`, côté client (`ModConfig.Type.CLIENT`).
**Il n'y a aucune config serveur.** Les joueurs peuvent choisir Natural Reach, dont
le bug de rendu est connu (`CHANGELOG.md`).

## 7. Livraison (point 8)

- Lot serveur prêt en local : `preparer-cinematic.sh`, `MISE-EN-PLACE-cinematic.md`.
  Non déposé.
- Zip client **non construit** : il faut une version v66 et le jar peut encore
  changer (point 1, et les suites du patch). La base serait la v65 ; `overrides/mods`
  pour le jar, `overrides/licenses/` pour la licence.
- Le jar d'origine a des espaces dans son nom, que `deposer.sh` refuse ; je l'ai
  renommé `…-0.18.30-bmc4.jar`. Il annonce toujours `0.18.30`, comme l'amont.

## 8. Blocage de connexion sur Forge 47.4.20 (point 9)

Seule trace dans le dépôt : `docs/ports/1.20.1-forge/TESTING.md`, candidat 0.18.28.
Serveur Forge 47.4.10 et jar construit : le client 47.4.0 passe ; le client 47.4.20
passe une fois, puis un second essai bloque avant l'apparition du joueur, avec
`lost connection: Disconnected` côté serveur. L'auteur écrit que la cause n'est pas
établie et qu'elle n'est pas confirmée dans le code du mod. Aucune issue n'en parle.
Notre cas diffère : serveur et client sont tous deux en 47.4.20. Essais par l'auteur
d'un jar complet sur client 47.4.20 en solo : 729 vérifications sans échec.
Ce qu'on surveille : voir `MISE-EN-PLACE-cinematic.md`.

## 9. Trouvé en passant, sans rapport avec ce mod

`KubeJSBlockEventHandler.rightClick` ne transmet pas l'événement aux scripts quand
l'objet en main est en recharge (`getCooldowns().isOnCooldown`). Une perle de l'Ender
en recharge en main ferait donc sauter `BlockEvents.rightClicked`, et avec elle la
règle des coffres de `bmc4_garde.js`. Lu dans le bytecode, pas essayé. À vérifier.
