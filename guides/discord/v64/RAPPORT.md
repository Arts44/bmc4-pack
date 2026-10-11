# BMC-100 — Guides Discord v64 : rapport

Rédigé le 11 octobre 2026. Rien n'est publié. Les longueurs sont comptées comme Discord (UTF-16), sans le saut de ligne final.

## Les fichiers

| Fichier | Salon | Message | Longueur |
|---|---|---|---|
| `create-5-steam-n-rails.md` | #create | nouveau | 1 959 |
| `farmers-delight-kaleidoscope-3.md` | #farmers-delight | nouveau | 1 829 |
| `petits-mods-arrive-avec-la-v64.md` | #petits-mods | nouveau | 1 512 |
| `paladins-furniture-2-sa-place-dans-le-pack.md` | #paladins-furniture | remplace 1552649978336518165 | 1 944 |
| `presentation-le-jeu-en-factions.md` | #présentation | remplace 1549323902201626667 | 1 971 |
| `ftb-2-ce-qu-un-claim-protege.md` | #ftb | remplace 1552643914341814293 | 1 969 |
| `guide-4-les-guides-par-mod.md` | #guide | remplace 1552653532648181775 | 1 984 |

## À savoir avant de publier

### Le conducteur espion de Steam 'n' Rails (#create)

**Oui, il permet d'espionner une base à distance.** Ce qui suit vient du code du jar, sans essai en jeu.

- **Comment ça marche.**
  - On donne des lunettes d'ingénieur à un conducteur : il passe en mode espion.
  - Une Lentille à distance liée à ce conducteur montre ce qu'il voit, sans limite de distance dans la même dimension.
  - Le conducteur doit être chargé au départ.
- **Ce n'est pas qu'une vue.**
  - Les touches de déplacement le font marcher.
  - « Utiliser » lui fait actionner boutons, trappes et leviers, à environ 4,7 blocs, avec un faux joueur « [Conductor] ».
- **Le mod ne prévoit aucune protection.**
  - Aucune option, serveur ni commune, ne le coupe.
  - Rien ne vérifie le propriétaire : n'importe qui lie sa lentille à n'importe quel conducteur espion.
  - Rien dans Steam 'n' Rails ne consulte les claims.
  - Je n'ai pas lu le code de FTB Chunks pour savoir s'il bloque le faux joueur. Côté serveur : `fake_players: "check"`, et `allow_fake_players` est à faux pour les deux factions.
- **Le conducteur est difficile à neutraliser.**
  - Assis dans un wagon, il est invulnérable.
  - Accroupi, main vide, n'importe qui lui retire ses lunettes : c'est la parade écrite dans le guide.
- **Charge serveur.** Pendant la vue, le mod pose chaque tick des tickets de chunk forcés sur 21 × 21 chunks autour du conducteur (`view-distance=10`). Il ne les retire jamais dans son code.
- **Pour le couper.** Il n'y a pas d'option : il faudrait retirer la recette de la Lentille à distance (`railways:crafting/remote_lens`) par KubeJS ou par datapack.
- **Le guide tel qu'écrit.** Il décrit l'espion et sa parade. Si tu coupes la lentille, il faut retirer la section « Le conducteur espion ».

**Autre point :** `mustOwnBoundTrain = false`. N'importe qui peut lier un sifflet au conducteur d'un train adverse et appeler ce train s'il n'a pas d'horaire en cours. Le guide le dit.

### Kaleidoscope : ce que le datapack ne couvre pas (#farmers-delight)

Je n'en parle pas dans le guide. Ce sont des décisions pour toi.

- **Sculk Special** (cocktail) : effet Shriek Attack. C'est un rayon de 32 blocs dans la direction du regard, qui blesse aussi les joueurs (1,2 × une valeur de vie du buveur, avec recul).
- **Molotov Cocktail** : il se lance (lave seule dans le tonneau, 16 par tonneau). `InfiniteLavaFromTap = true` sur le serveur.
  - Je n'ai pas vérifié s'il abîme quoi que ce soit dans un claim.
- **Satiation Shield** (Cookery) : la jauge de faim absorbe 100 % des dégâts, jusqu'à 64. Le serveur garde la config par défaut.
- **Millstone** (Cookery) : 1 bloc de minerai donne 3 bruts de fer ou d'or, 5 de cuivre, 2 diamants, 7 redstone ou lapis. Il faut avoir les blocs de minerai, donc Toucher de soie.
- **Spirit Vision** (Glowflower Brew, Mojito) : il applique un effet aux entités proches, probablement Glowing (en surbrillance). Cela pourrait révéler les joueurs, ce qui contredit le radar privé.
- **Rum** : Mauvais présage V.

### Les claims (#présentation, #ftb)

**Les factions ne sont pas réglées comme les valeurs par défaut.** Lu dans `world/ftbteams/party/*.snbt` ; à ne pas publier :

| Réglage | Apex | Farmer's | Défaut serveur |
|---|---|---|---|
| Casser, poser | `private` | `allies` | `allies` |
| Interagir | `public` | **`allies`** | `public` |
| Visibilité du claim | `private` | `allies` | `public` |
| Position | `private` | `allies` | `private` |

- **Farmer's a fermé l'interaction à ses seuls alliés.** Ses portes, boutons et leviers sont donc fermés à Apex même pendant un raid : la garde peut restreindre, pas rouvrir.
- **Contradiction avec le règlement des raids.** Il dit « Portes, trappes… restent utilisables en tout temps ». Ce n'est vrai que pour une faction en `public`.
- **Ce que disent les guides.** #présentation dit « une faction peut aussi fermer ses portes ». #ftb le détaille, avec le piège du raid.
- **Le réglage PvP des équipes est sans effet.** `allow_pvp` est à faux pour les deux factions, mais `pvp_mode: "always"` l'emporte (lu dans l'infobulle du jar FTB Chunks).
- **Ancienne phrase fausse dans #présentation.** « Les revendications sont privées : chacun ne voit que les siennes » n'était pas vrai par défaut : c'est `public`, réglable par équipe.

## #ftb 2/2 : chaque valeur qui a changé

Ancienne valeur : guide du 24 septembre et sauvegarde `ftbchunks-world` du 29 septembre. Nouvelle valeur : `world/serverconfig/ftbchunks-world.snbt` et `bmc4_garde.js` en production (même taille que `origin/bmc94-serveur`).

| Ligne | Avant | Maintenant |
|---|---|---|
| Interagir avec les blocs (`def_block_interact`) | alliés seulement (`allies`) | `public` |
| Coffres et blocs à inventaire | suivaient l'interaction | fermés par la garde aux autres factions, sauf alliés ; ouverts aux deux factions engagées pendant un raid |
| Portes, trappes, portillons, boutons, leviers, plaques | alliés seulement | tous, sauf équipe en `allies` ou `private` |
| Position des joueurs (`def_player_visibility`) | `allies` | `private` |
| Suivi longue portée (`long_range_tracker_interval`) | 20 | 0, coupé |
| Minicarte FTB Chunks (`force_disable_minimap`) | `false` | `true`, coupée |
| Partage de carte entre alliés | « si l'ajout est réciproque » | option **Share Map with Allies** (`ftbchunks.gui.sync`) |

Inchangés et revérifiés :
- casser et poser : `allies` ;
- explosions, grief des mobs et pistons : bloqués ;
- visibilité du claim par défaut : `public` ;
- PvP : `pvp_mode always`, `def_pvp true` ;
- partage des waypoints : groupe, joueurs et serveur, tous `true` ;
- FTB Chunks : 40 chunks par équipe ;
- OPAC : 500 chunks par joueur, 10 forcés.

## Affirmations non vérifiées

- **Écrites dans les guides, prises dans le code sans essai en jeu :**
  - toute la mécanique du conducteur espion et du sifflet ;
  - la Voie en phantom invisible ;
  - l'aiguillage en laiton qui bascule seul ;
  - le vieillissement du vin (niveau 6 en 30 min, chunk chargé) ;
  - « F9 ou clic droit » joue l'animation puis le plat est mangé ;
  - la caméra de Leawind qui s'arrête aux murs ;
  - l'aide à la visée ;
  - la poussée de Do a Barrel Roll refusée sans le mod serveur.
- **Leawind, « Verr. Maj » pour changer d'épaule :** c'est le défaut du jar (code 280). Je n'ai pas vérifié le libellé affiché.
- **Leawind, l'aide à la visée « se coupe dans la config du mod » :** l'option existe (`enable_target_entity_predict`), mais je n'ai pas vérifié l'écran qui la montre.
- **#ftb, « FTB Chunks Properties » :** c'est le titre du groupe de réglages dans la lang. Je n'ai pas vérifié qui, dans l'équipe, peut les modifier.
- **Le datapack bmc4-taverne actif :** son dossier existe sur le serveur, mais je n'ai pas lancé `datapack list`. Tu dis qu'il tourne.
- **Ardent Heat qui contourne les claims :** c'est une déduction du code (`destroyBlock` direct). Le guide ne le dit pas.
- **Connectible Chains, portée de 7 blocs :** c'est la valeur sur le serveur, mais la config dit « sans effet en multijoueur ». Je ne l'ai pas écrite.
- **Just Outdoor Stuffs, les bancs :** on peut s'asseoir sur les chaises et les canapés (vérifié). Pour les bancs, je ne l'ai pas vérifié ; le guide dit seulement « sièges compris ».
- **Aucun des mods v64 n'a de traduction française,** sauf Steam 'n' Rails (partielle). Les guides le disent.
- **Textes existants recopiés :** je les ai repris à la main depuis les messages lus le 11 octobre. Claude côté Discord doit vérifier, avant de remplacer, que seules les parties voulues changent.

## Changements de forme à valider

- **#paladins-furniture 2/2 :** la section « Corrigé le 24 septembre » est retirée pour tenir sous 2 000 caractères. Le message 1/2 dit déjà « Le frigo ne conserve rien ».
- **#create :** la série passe à « 5/5 », mais les messages 1 à 4 portent encore « /4 ».
- **#guide :** trois lignes complétées (Create, Farmer's Delight, Paladin's) et une ajoutée (#petits-mods).
