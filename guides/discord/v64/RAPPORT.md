# BMC-100 — Guides Discord v64 : rapport

Rédigé le 11 octobre 2026. Rien n'est publié. Les longueurs sont comptées comme Discord (UTF-16), sans le saut de ligne final.

## Les fichiers

| Fichier | Salon | Message | Longueur |
|---|---|---|---|
| `create-5-steam-n-rails.md` | #create | nouveau | 1 630 |
| `create-titres-1-a-4.md` | #create | première ligne des messages 1 à 4 | — |
| `farmers-delight-kaleidoscope-3-cuisine.md` | #farmers-delight | nouveau | 1 296 |
| `farmers-delight-kaleidoscope-4-taverne.md` | #farmers-delight | nouveau | 1 423 |
| `petits-mods-arrive-avec-la-v64.md` | #petits-mods | nouveau | 1 512 |
| `paladins-furniture-2-sa-place-dans-le-pack.md` | #paladins-furniture | remplace 1552649978336518165 | 1 944 |
| `presentation-le-jeu-en-factions.md` | #présentation | remplace 1549323902201626667 | 1 971 |
| `ftb-2-ce-qu-un-claim-protege.md` | #ftb | remplace 1552643914341814293 | 1 969 |
| `guide-4-les-guides-par-mod.md` | #guide | remplace 1552653532648181775 | 1 984 |

## BMC-101 (décisions du 11 octobre) : ce que les guides supposent

Les guides #create et #farmers-delight décrivent le serveur **après** la mise en place du lot `bmc101-2026-10-11` (`quetes/deploiement/MISE-EN-PLACE-bmc101.md`, branche `bmc101-retraits`) :

- **Lentille à distance** : recette retirée (`/reload`).
- **Molotov Cocktail** : recette retirée (`/reload`).
- **Robinet** : `InfiniteLavaFromTap = false` (rechargement automatique de la config).
- **Satiation Shield** : `SatiatedShieldAbsorbEnabled = false` (rechargement automatique de la config).
  - Il ne vient que des plats de Cookery, d'aucune boisson : le datapack `bmc4-taverne` n'y pouvait rien.
- **Cri du Sculk Special** : 8 points au plus contre un joueur, jamais mortel.
  - Script de démarrage : il ne s'applique qu'**après un redémarrage**.
  - **Ne publiez pas le message 4/4 avant.**

Vérifié dans les jars :
- **Spirit Vision** met bien **Glowing** (`MobEffects.f_19619_` = « glowing » dans le jar 1.20.1) toutes les 50 ticks, pour 60 ticks.
  - Cibles : toute entité vivante autre que le buveur, joueurs compris.
  - Portée : la boîte du buveur élargie de 6 × min(niveau, 3) blocs, soit 6, 12 ou 18.
- **Le cri** frappe dans l'axe du regard jusqu'à 32 blocs.
  - Dégâts : 1,2 × la vie actuelle du buveur (`getHealth`).
  - Type `sonic_boom`, qui figure dans `bypasses_armor`.

## À savoir avant de publier

### Le conducteur espion de Steam 'n' Rails

- **Résolu par BMC-101** : la recette de la Lentille à distance est retirée. Le guide le dit en une ligne.
- **Lentilles déjà fabriquées** : celles qui existent avant le retrait restent utilisables.
- **Sifflet** : `mustOwnBoundTrain = false`. N'importe qui peut appeler le train d'un autre, s'il n'a pas d'horaire en cours. Le guide le dit.

### Kaleidoscope

- **Gardés et décrits dans le 4/4** : Sculk Special (bridé), Spirit Vision, la meule (dans le 3/4).
- **Désactivés et signalés** : Molotov, robinet de lave infinie, Satiation Shield.
- **Non signalé dans le guide** : Rum donne Mauvais présage V.

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
- **#create :** titres des messages 1 à 4 en « /5 » dans `create-titres-1-a-4.md`.
- **#guide :** trois lignes complétées (Create, Farmer's Delight, Paladin's) et une ajoutée (#petits-mods).
