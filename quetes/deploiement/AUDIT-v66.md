# BMC-106, partie 3 — Audit de la v66

Tout vient du bytecode des jars, des issues publiques et de la lecture seule du
serveur. **Rien n'a tourné en jeu.**

## MrCrayfish's Furniture Mod: Refurbished 1.0.20

Framework : `[0.7.15,)` demandé, 0.8.0 dans le pack et sur le serveur, pas de mise à
jour.

**Décision d'Arthur du 30 octobre : tout fermer.** Le tableau reste le constat ; ce qui
est appliqué : `electricity.cheats.everythingIsPowered = true`, `mailing.deliveryQueueSize = 8`
(`config/refurbished_furniture.server.toml`, type `SERVER_SYNC` de Framework, comme
`backpacked.server.toml` sur le serveur) et les recettes `refurbished_furniture:wrench`,
`refurbished_furniture:constructing/computer` et `refurbished_furniture:television_remote`
retirées, avec celles des ventilateurs de plafond (`bmc4_v66_retraits.js`). Restent ouverts : l'envoi par Post Box (seulement borné) et
l'établi du mod en limite de claim.

**Ventilateurs de plafond : retirés.** `CeilingFanBlockEntity.moduleTick` appelle `performDamage` côté
serveur. Sa seule condition est `isNodePowered()`, donc toujours vraie avec `everythingIsPowered` ; le
clic sur le bloc ne bascule que `LIT`, sa lumière. Il frappe toute `LivingEntity` de sa zone :
`hurt(ceiling_fan, 0.5)`, joueurs compris. La zone est une tranche de 2,25 × 2,25 × 0,125 bloc,
centrée sur le ventilateur, dans sa hauteur. Avec les 10 ticks d'invulnérabilité de Minecraft, cela
fait **0,5 point toutes les demi-secondes, avant armure, sans limite** : mortel pour qui reste dedans.
Un ventilateur hors de portée de tête ne touche personne, mais un ventilateur mural ou bas forme un
piège sans redstone. Recettes retirées : 20 de l'établi, 10 de teinture. Seules sources elles aussi
(même crible, 366 308 fichiers) ; hors recettes : avancements, modèles, loot du bloc lui-même.

**Seule source de ces trois objets : ces recettes.** 407 jars, 366 301 fichiers, données, `.nbt`
décompressés et classes. Hors recettes : tags (`c:tools/wrench`, `electronics`, `items`),
avancements de recette et le loot du bloc ordinateur lui-même. Aucun loot de coffre, aucun échange.
Les classes qui citent ces objets ne les donnent pas (registres, onglet créatif, clé en main).
Non passés : les jars présents seulement sur le serveur.

**Ce que change `everythingIsPowered`** (`IModuleNode.updateNodePoweredState` force
`setNodePowered(true)`) :
- marchent sans générateur : cuisinière, micro-ondes, congélateur, grille-pain, Recycle Bin,
  établi du mod, sonnette, télévision ;
- lampes et plafonniers (`LightingBlockEntity`) : `POWERED` toujours vrai, **toujours allumés** ;
- ventilateur : **recettes retirées**, voir plus bas ;
- interrupteur : il bascule son propre état, sans lien il ne commande plus rien ;
- générateur : inutile.
Le commentaire du mod avertit que « certains blocs peuvent ne plus marcher comme prévu ».

| Point | FTB Chunks | Garde | Faille | Fermeture proposée |
|---|---|---|---|---|
| Post Box : envoi à distance | non | non | oui, moyenne | `mailing.deliveryQueueSize=8` (borne l'inondation) ; `=0` coupe tout envoi ; ou retirer la recette `refurbished_furniture:constructing/post_box` |
| Boîte d'un autre : lire, vider | selon le mode | oui hors alliés et raid | non en claim ; oui hors claim | consigne : boîtes dans un claim |
| Liens électriques, coupure, surcharge | non | non | oui, moyenne | `electricity.cheats.everythingIsPowered=true` et retrait de `refurbished_furniture:wrench` ; partiel : `powerableAreaRadius` |
| Home Control (bascule à distance via un lien) | non | non | oui, moyenne | retirer `refurbished_furniture:constructing/computer` |
| Établi du mod contre un coffre en limite de claim | non | non | oui, bords seulement | `BlockEvents.placed` en KubeJS, ou consigne |
| Télécommande TV, 16 blocs | non | non | oui, faible | retirer `refurbished_furniture:television_remote` |
| Entonnoir, comparateur | sans objet | sans objet | non | un entonnoir peut pousser dans un appareil en bord de claim |
| Recycle Bin | oui selon le mode | oui | non, destruction réelle | guide |
| Dupe par recyclage | - | - | non, aucune sortie d'objet | - |

### Post Box

- `sendMail` ne contrôle ni distance, ni dimension de l'expéditeur, ni claim ; seule
  la dimension de la boîte destinataire compte. L'ouverture d'une Post Box envoie
  la liste de **toutes** les boîtes du serveur (propriétaire et nom, sans coordonnées).
- Pendant une fuite, c'est un coffre instantané vers une boîte alliée. 41 colis d'un
  objet (9 emplacements + file de 32) bloquent une boîte : la victime n'a pas de filtre.
- `bannedItems` compare à la clé de traduction, pas à l'identifiant : il faudrait
  `item.minecraft.diamond`, pas `minecraft:diamond`. À confirmer sur un objet test.
- Boîte cassée : file jetée au sol. Stockage : SavedData de l'overworld.

### Liens électriques

- `LinkManager.MAX_LINK_LENGTH = 512` blocs, constante sans option. Clic à 4,5 blocs,
  à travers les murs. Aucun contrôle de propriétaire ni de claim.
- `WrenchItem.use` passe par l'usage d'objet : `ForgeEvents.onRightClickBlock` annule
  lui-même le clic de bloc, la garde ne voit donc rien de pertinent. FTB teste la
  position des yeux, et n'arrête que Farmer's avec un tag `right_click_blacklist`.
- `handleMessageDeleteLink` : clé en main, distance ≤ max(5, longueur du lien), aucun
  propriétaire : un lien adverse se coupe sans entrer.
- Surcharge : au-delà de 64 nœuds, le générateur adverse s'arrête.

### Ordinateur, sonnette, télévision

- Programmes installés : `paddle_ball` et `home_control`. Pas de caméra ni de vue.
- `HomeControl.toggleDevice` valide la position contre le réseau de l'ordinateur :
  pas de position arbitraire, mais un ordinateur lié au réseau adverse bascule frigos,
  cuisinières, Recycle Bin et interrupteurs sans clic sur eux.
- Sonnette : BlockEntity, refusée par la garde en claim étranger. Pas de position envoyée.
- Le paillasson est le seul « paint » (14 × 10, verrouillé après la pose).

### Poubelle (pour les guides)

La Recycle Bin a 3 emplacements. Elle détruit un objet toutes les 10 ticks **si** elle
est alimentée **et** allumée, s'arrête à 5 niveaux d'XP, et ne rend rien. Coupée, c'est
un conteneur. Les toilettes détruisent aussi les objets au sol dans la cuvette.

### Blocs à inventaire

Tous ont une BlockEntity : la garde les traite comme des coffres. Le jar n'ajoute aux
tags exemptés que `minecraft:fence_gates` (10 portillons, sans BlockEntity). Passent à
côté de la garde : s'asseoir (chaises, canapés, tabourets) et le clic gauche sur Storage
Jar et Cutting Board (qui sort un objet), mais FTB applique alors `block_edit_mode`.

### Taille à la connexion : notable

449 blocs, 470 objets, 32 BlockEntityType, 59 sons, 709 recettes, 44 fichiers de tags.
Estimation : 150 à 200 Ko bruts, 40 à 60 Ko compressés (non mesuré). Le paquet de
recettes pèse le plus lourd. Avec l'historique « VarInt too big » de la v64→v65 (Krypton),
**à vérifier sur une vraie connexion avant l'ouverture**.

**Every Compat : module coupé, décision d'Arthur du 30 octobre.** Son `RefurbishedFurnitureModule`
aurait ajouté 20 familles de meubles par essence moddée, plus une famille de feuilles, soit de
l'ordre de 1 500 blocs (déduit des 74 blocs du module Farmer's Delight, une famille).
`[module] blacklist = ["refurbished_furniture"]` dans `config/everycomp-hazardous.toml`, identique dans
le pack et le lot. L'identifiant est le bon : `EveryCompatCommon` appelle
`addIfLoaded("refurbished_furniture", …)`, et `EveryCompat.addIfLoaded` commence par
`MODULES_BLACKLIST.contains(modId)`. Le fichier avertit qu'un écart entre client et serveur
empêche de rejoindre.

**Ce qui reste comme bois** : les blocs du mod lui-même, en 10 essences vanilla (chêne, sapin,
bouleau, jungle, acacia, chêne noir, palétuvier, cerisier, carmin, biscornu). Rien pour les essences
moddées, ni pour le bambou.

### Autres

Trampoline : 8 blocs de rebond, franchit les murs bas (`trampoline.maxBounceHeight`).
Baignoire de lave : brûle. Pas de téléportation.

**Non vérifiable** : tag `ftbchunks:right_click_blacklist` du serveur ; limite du paquet
d'ouverture de Post Box avec beaucoup de boîtes ; résultat d'établi obsolète entre deux
ticks (dupe plausible, non prouvé) ; sortie du `Seat` à travers un mur fin.

## Passthrough Signs : retiré de la v66

Décision d'Arthur du 30 octobre : fork ou retrait. **Licence : « All rights reserved »**
(`mods.toml`, `gradle.properties` du dépôt source, aucun fichier LICENSE) : pas de fork.
Le constat qui a mené là :

- `PassableHandler` écoute `RightClickBlock` en priorité NORMAL, sans `receiveCanceled`,
  puis appelle `Block.use` directement sur le bloc derrière : **aucun événement** sur le
  coffre. FTB et la garde ne jugent que la position du panneau.
- Panneau dans le claim ennemi : refusé par la garde (BlockEntity du panneau), à HIGH,
  avant le mod.
- **Trou 1, panneau hors claim** : un panneau mural posé hors claim contre un coffre en
  limite de claim (clic sur le sol, `StandingAndWallBlockItem` choisit le mur). Chunk du
  panneau non claimé : FTB et la garde laissent passer, le coffre s'ouvre.
- **Trou 2, cadres et tableaux** : `EntityInteract`. `entity_interact_mode` est `public`
  pour Apex et Farmer's, la garde n'a aucun gestionnaire d'entité. Tout cadre sur un
  coffre ouvrait ce coffre à tous.

Avec Quark, le panneau ne passe qu'en Maj + clic droit.

## ClickThrough Plus 3.5.1 : le remplaçant de Reach Behind

Décision d'Arthur du 30 octobre. Modrinth et CurseForge portent le même jar (SHA-1
`90211f07…`) : projet **1122678**, fichier **6726028**, donc manifeste. MIT.

- `ItemUseMixin` : `@Inject` dans `Minecraft.startUseItem`, avant `getItemInHand`. Il remplace
  `hitResult` par `ModHelpers.switchCrosshairTarget`. Le reste est le code vanilla :
  `useItemOn` envoie l'usage sur le coffre. Le serveur reçoit un `RightClickBlock` **sur
  le coffre** : FTB Chunks et la garde le voient. Cadre compris : la cible devient un bloc,
  il n'y a plus d'`EntityInteract`.
- **Aucun réseau** : aucune classe du mod ne référence un paquet, `MultiPlayerGameMode`
  ou `connection`. Les seuls appels de `ModHelpers` sont des lectures côté client.
- Donc un client qui triche ne gagne rien : le serveur juge le coffre, mod présent ou non.
- `mods.toml` : forge `[43,50)`, minecraft `[1.19.1,1.21)`, architectury `[6.6.92,)`, 9.2.14 dans
  le pack. Client seul (Modrinth : `server_side: unsupported`). Pas de canal réseau.
- Config `config/clickthrough.json` : `onlycontainers` vaut `true` par défaut (constructeur de
  `ModConfig`, champ en minuscules). Livrée telle quelle, avec la liste par défaut.
- **Touche** `key.clickthrough.toggle` : F9 par défaut (code 298), conflit avec l'animation des
  repas. Mise sur **F10**, libre.
- L'issue #11 (la touche plante le jeu) lit l'état maintenu ; ce jar utilise `consumeClick`.

**⚠️ Risque au lancement, à voir à l'import.** GlitchCore a un `@Redirect` sur le même appel
`getItemInHand` de `startUseItem`, et le Mixin du pack (0.8.5, celui de Connector) n'a pas d'ordre
d'injecteurs : il applique les mixins l'un après l'autre. Si GlitchCore passe avant, l'`@Inject` ne
trouve plus sa cible et `defaultRequire: 1` fait **planter le client au lancement**
(`Critical injection failure … switchCrosshairTargetItemUse`). À priorité égale, l'ordre suit celui
des configs, donc des fichiers de mods en minuscules : `clickthrough…` avant `glitchcore…`,
ce qui doit marcher. C'est une déduction de mémoire du code de FML, pas une observation.
Le repli ClickThrough Forge 1.0.0 vise le même appel, sans `defaultRequire` : il ne planterait pas,
mais il resterait sans effet dans le mauvais ordre. Il envoie aussi des paquets d'accroupissement.

## AFK Camera

Modrinth `1.0.0+1.20.1-forge`, SHA-1 identique (`d00be9f1…`) ; `mods.toml` dit
1.4.2+1.20.1-forge. Client seul, aucun canal réseau, aucune touche enregistrée. YACL est
`mandatory=false` : sans lui, `ModMenuIntegration` montre `NoConfigLibraryScreen`, il n'est
donc pas ajouté (pas d'écran de réglages). Licence CC BY-ND 4.0, sans modification : jar
tel quel, licence et crédit dans `overrides/licenses/`. Cinq mixins client avec
`defaultRequire: 1` : une injection ratée ferait planter le client, à voir à l'essai.

## Connector et Pulse Trims : hors v66

Décision d'Arthur du 30 octobre : Pulse Trims abandonné, Connector reste en beta.48 (fichier
7594389), Forgified Fabric API inchangé. Raison : son shader ne reconnaît que des atlas de
1024 ou 2048 de large, et l'atlas de trims du pack fait 4096.

## Glowing Trims

Modrinth 1.0.0+1.20.1, SHA-1 `a7e60bb3…`, MinionDude19, MIT. **Absent de CurseForge** : jar dans
`overrides/mods`, texte MIT dans `overrides/licenses/` (le jar n'en contient pas, la licence
est déclarée dans `mods.toml` et sur Modrinth). Client seul (`clientSideOnly`, `IGNORE_ALL_VERSION`),
aucune dépendance, aucun réseau, aucune touche.

Un seul mixin, `@ModifyArg` (index 2, la lumière) sur `Model.renderToBuffer` dans le `renderTrim` ajouté
par Forge à `HumanoidArmorLayer` (méthode présente dans 47.4.20). Il renvoie toujours 15728880.

| Mod | Sur `renderTrim` | Conflit |
|---|---|---|
| Glow Up | `@ModifyArg` sur le **même argument du même appel** | non : les deux s'enchaînent, et il rend la valeur reçue pour une armure sans son NBT |
| Oculus | `@Inject` HEAD et TAIL de `renderTrim` | non, pas sur cet appel |
| Structure Gel | `@ModifyVariable` | non, autre variable |
| Cinematic Interactions | rien : son mixin vise `renderArmorPiece` (`setPartVisibility`) | non |
| Xenon | ne vise pas `HumanoidArmorLayer` | non |

- Pas de `@Redirect` ni d'`@Overwrite` sur cet appel dans le pack : pas le cas de GlitchCore.
- **Glow Up** propose déjà des garnitures brillantes à l'encre luisante. Avec Glowing Trims,
  toutes brillent : cette fonction de Glow Up ne se voit plus.
- **En faction** : on verra mieux les garnitures des autres joueurs dans le noir, chez ceux qui
  ont le mod. Rien de plus qu'un rendu client.
- L'effet avec un shader Oculus actif n'est pas vérifié.

## Touches

Aucune touche par défaut chez Refurbished, AFK Camera et Glowing Trims. **Light Overlay est par défaut sur F7 (code 296), pas F4 : conflit avec Do a
Barrel Roll.** Mise sur F4, libre, dans `configureddefaults/options.txt`. ClickThrough Plus :
F9 par défaut, mis sur F10. Les joueurs migrés gardent leur fichier et voient ces conflits.

## Identifiants

Light Overlay est le projet **325492**, pas 312870 (Curse Maven : 200 contre 404).
Connector est 890127. Vérifiés sur Curse Maven (200) : Refurbished 897116/7110922, Light
Overlay 325492/4573178, ClickThrough Plus 1122678/6726028.
