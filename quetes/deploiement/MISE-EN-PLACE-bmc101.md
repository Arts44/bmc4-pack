# BMC-101 — Mise en place côté serveur

Lot : `/bmc4-depot/bmc101-<date>/`, déposé par
`sh quetes/deploiement/deposer.sh --lot bmc101-<date>`. Le dépôt ne met rien
en place : les déplacements et retouches se font avec les outils MineStrator.
`SHA1SUMS` donne l'empreinte de chaque fichier. Une action par ligne.

## Ce qui change, et comment ça se charge

| Fichier du lot | Effet | Pris en compte par |
|---|---|---|
| `kubejs/server_scripts/bmc4_v64_retraits.js` | plus de recette pour la Lentille à distance ni pour le Molotov Cocktail | `/reload` |
| `config/kaleidoscope_tavern-common.toml` | `InfiniteLavaFromTap = false` : le robinet vide le chaudron de lave | tout seul, dès l'écriture du fichier |
| `config/kaleidoscope_cookery-common.toml` | `SatiatedShieldAbsorbEnabled = false` : Satiation Shield n'absorbe plus rien | tout seul, dès l'écriture du fichier |
| `kubejs/startup_scripts/bmc4_v64_sculk.js` | cri du Sculk Special plafonné à 8 points contre un joueur, jamais mortel | **un redémarrage** (le quotidien de 5 h suffit) |

Le datapack `bmc4-taverne` ne change pas. Satiation Shield ne vient d'aucune
boisson : seuls les plats de Cookery le donnent (`ModFoods`, dans le code du
jar). Le datamap des boissons n'y peut donc rien, et c'est l'option de la
config qui le neutralise.

**Les deux configs se rechargent sans redémarrage**, à condition de modifier
le fichier en place.
- Forge 47.4.20 surveille chaque fichier de config. Au changement, il le relit, vide le cache des valeurs (`ForgeConfigSpec.afterReload`) et écrit en debug « Config file … changed, sending notifies ».
- Le mod relit l'option à chaque usage :
  - `LavaCauldronTapBehavior` lit `INFINITE_LAVA_FROM_TAP.get()` ;
  - `SatiatedShieldEvent` lit `SATIATED_SHIELD_ABSORB_ENABLED.get()` à chaque coup reçu.
- D'où `edit_file` sur la ligne, plutôt que de remplacer le fichier. Les fichiers du lot servent de référence : ils sont identiques à ceux du serveur, à cette valeur près (1 octet de plus chacun).

## Avant tout

1. `create_snapshot`, nom `avant-bmc101`. Attendre qu'il soit terminé.

## Recettes (sans redémarrage)

2. `move_files` : `/bmc4-depot/bmc101-<date>/kubejs/server_scripts/bmc4_v64_retraits.js` vers `/kubejs/server_scripts/`.
3. Console : `reload`.
4. `/logs/kubejs/server.log` (ou `latest.log`) : `bmc4_v64_retraits.js` est chargé sans erreur, et la ligne « Added … recipes, removed … recipes, … » de KubeJS (texte lu dans `RecipesEventJS`) compte au moins 2 retraits.
5. `latest.log` : pas d'erreur de rechargement.

## Robinet de lave (sans redémarrage)

6. `edit_file` sur `/config/kaleidoscope_tavern-common.toml` : `InfiniteLavaFromTap = true` devient `InfiniteLavaFromTap = false`.
7. `read_file` du même fichier : la ligne vaut `false`, et le fichier fait 853 octets.

## Satiation Shield (sans redémarrage)

8. `edit_file` sur `/config/kaleidoscope_cookery-common.toml` : `SatiatedShieldAbsorbEnabled = true` devient `SatiatedShieldAbsorbEnabled = false`.
9. `read_file` du même fichier : la ligne vaut `false`, et le fichier fait 1 201 octets.

## Cri du Sculk Special (redémarrage)

10. `move_files` : `/bmc4-depot/bmc101-<date>/kubejs/startup_scripts/bmc4_v64_sculk.js` vers `/kubejs/startup_scripts/`.
11. Redémarrer (`power_action restart`), ou attendre le redémarrage quotidien de 5 h. Jusque-là, le cri reste à pleine puissance.
12. Après le démarrage : `/logs/kubejs/startup.log` charge `bmc4_v64_sculk.js` sans erreur.

## Vérifications en jeu

13. EMI : la Lentille à distance et le Molotov Cocktail n'ont plus de recette.
14. Tonneau rempli de lave seule : il ne donne plus de Molotov.
15. Robinet sur un chaudron de lave : une bouteille tirée vide le chaudron.
16. Un plat de Cookery à Satiation Shield, puis un coup reçu : la vie baisse normalement.
17. À deux joueurs, après le redémarrage : le cri d'un Sculk Special bu à pleine vie retire 4 cœurs au plus, et laisse toujours au moins un demi-cœur.

## Retour arrière

- Recettes : déplacer `bmc4_v64_retraits.js` hors de `/kubejs/server_scripts/` (vers `/bmc4-depot/bmc101-<date>/`), puis `reload`.
- Configs : remettre la ligne à `true` avec `edit_file`.
- Cri : déplacer `bmc4_v64_sculk.js` hors de `/kubejs/startup_scripts/`, puis redémarrer.
- En dernier recours : `restore_snapshot avant-bmc101`.

## Ce que le lot ne couvre pas

- **Les objets déjà fabriqués** : les lentilles et Molotov qui existent dans le monde restent utilisables. La v64 tourne depuis le 11 octobre.
- **Les conducteurs déjà liés à une lentille existante.**
