# BMC-103, partie 3 — Audit de la v66

Tout vient du bytecode des jars, des issues publiques et de la lecture seule du
serveur. **Rien n'a tourné en jeu.**

## MrCrayfish's Furniture Mod: Refurbished 1.0.20

Framework : `[0.7.15,)` demandé, 0.8.0 dans le pack et sur le serveur, pas de mise à
jour. Les fermetures sont **à proposer, aucune n'est appliquée**.

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
recettes pèse le plus lourd. Avec l'historique « VarInt too big » (BMC-104), **à mesurer
sur une vraie connexion avant l'ouverture**.

### Autres

Trampoline : 8 blocs de rebond, franchit les murs bas (`trampoline.maxBounceHeight`).
Ventilateur : 0,5 de dégât dans sa zone. Baignoire de lave : brûle. Pas de téléportation.

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

## Connector et Pulse Trims

**Aucune incompatibilité documentée ne vise Pulse Trims ni beta.49**. Le jar n'embarque
aucune liste ; Immersive Portals et Distant Horizons tournent en Forge natif.

| Mod | Éléments | État |
|---|---|---|
| Oculus | ConnectorExtras #52 | ouverte (11/2024) : crash Oculus 1.7 avec JEI et Quark, sans diagnostic ; combinaison déjà en v65 |
| Oculus | Connector #1083, #1504 | fermées |
| Xenon | aucune issue dédiée | - |
| Embeddium | #1777, #2061 | ouvertes, sur des mods absents du pack |
| Immersive Portals | #665, #1789, #1819 | fermées, version Fabric ou invalid |
| Distant Horizons 3.3.3 | aucune | - |
| Cinematic Interactions | aucune | - |

- **beta.48 → 49** : Fabric Loader passe de 0.16.5 à 0.19.3 sous le capot, 23 fichiers
  sur 1126. Forge inchangé (`[47,)`). Risque modéré, aucune régression signalée.
- **Forgified Fabric API** : aucune mise à jour exigée, reste 6885853.
- **Pulse Trims ne produira très probablement aucun effet** : son shader ne reconnaît
  que des atlas de 1024 ou 2048 de large, et l'atlas de trims du pack fait 4096
  (`logs/latest.log` de l'instance v65). Armure rendue normalement, pas de crash.
- Il écrase le core shader `rendertype_armor_cutout_no_cull` et remplace le set des
  sources de packs par un `HashSet`. Sans effet avec un shader Oculus actif.
- Distribution tierce de CurseForge non confirmée (API officielle sans clé).
- Connector 1.20.1 ne reçoit plus que des correctifs critiques (#2272).

## Touches

Aucune touche par défaut chez Refurbished et AFK Camera. Pulse Trims : `key.pulse-trims.config`,
non assignée. **Light Overlay est par défaut sur F7 (code 296), pas F4 : conflit avec Do a
Barrel Roll.** Mise sur F4, libre, dans `configureddefaults/options.txt`. ClickThrough Plus :
F9 par défaut, mis sur F10. Les joueurs migrés gardent leur fichier et voient ces conflits.

## Identifiants

Light Overlay est le projet **325492**, pas 312870 (Curse Maven : 200 contre 404).
Connector est 890127. Vérifiés sur Curse Maven (200) : Refurbished 897116/7110922, Light
Overlay 325492/4573178, ClickThrough Plus 1122678/6726028, Connector 890127/8367974, Pulse
Trims 1625738/8848576.
