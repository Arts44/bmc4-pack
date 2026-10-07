# BMC-94 — Mise en place côté serveur (temps 1 : serveur seul)

Lot : `/bmc4-depot/bmc94-<date>/`, déposé par
`sh quetes/deploiement/deposer.sh --lot bmc94-<date>` après un snapshot.
Rien n'est mis en place par le dépôt : les déplacements se font avec les
outils MineStrator. `SHA1SUMS` donne l'empreinte de chaque fichier.

Aucun de ces changements ne touche au pack client : un client v62 se
connecte comme avant (les jars Xaero sont ceux du pack v62, à l'octet près ;
tout le reste est script ou configuration du serveur).

## Étape A — tout de suite : le journal des commandes des ops

1. Copier `kubejs/server_scripts/bmc4_triche.js` dans `/kubejs/server_scripts/`.
2. Console : `kubejs reload server_scripts`.
3. Taper une commande d'op en jeu (par exemple `/time query daytime`) :
   moins d'une minute plus tard, `#console` affiche
   « 🛡️ **pseudo** · `/time query daytime` · HH:MM ».
4. `/prestige diagnostic` (op) : la ligne « mods du client » doit être OK.
   Si elle est en ÉCHEC, le refus des mods ne marche pas : le dire (aucun
   joueur n'est refusé dans ce cas, une alerte part dans `#anti-triche`).

## Étape B — avant le redémarrage automatique de 5 h

Remplacer ou ajouter (les dossiers absents se créent) :

| Fichier du lot | Destination sur le serveur |
|---|---|
| `kubejs/server_scripts/bmc4_garde.js` | `/kubejs/server_scripts/` (remplace) |
| `kubejs/startup_scripts/bmc4_teleportations.js` | `/kubejs/startup_scripts/` (nouveau dossier) |
| `mods/xaerominimap-forge-1.20.1-26.1.0.jar` | `/mods/` |
| `mods/xaeroworldmap-forge-1.20.1-1.41.0.jar` | `/mods/` |
| `config/xaero/minimap/server_profiles/default.cfg` | `/config/xaero/minimap/server_profiles/` (remplace) |
| `config/xaero/minimap/default_radar_categories_server.json` | `/config/xaero/minimap/` (remplace) |
| `config/xaero/world-map/server_profiles/default.cfg` | `/config/xaero/world-map/server_profiles/` (remplace) |
| `config/carryon-common.toml` | `/config/` (remplace) |
| `config/alexsmobs.toml` | `/config/` (remplace) |
| `world/serverconfig/ftbchunks-world.snbt` | `/world/serverconfig/` (remplace) |

Le redémarrage de 5 h charge le tout. Un redémarrage plus tôt est possible
sur demande d'Arthur.

## Étape C — après le redémarrage

1. Console : vérifier que KubeJS a chargé 5 scripts serveur et 1 script de
   démarrage, sans erreur (`latest.log`, « Loaded … KubeJS server scripts »
   et « startup scripts »).
2. L'équipe Farmer's est encore en `ftbchunks:location_mode allies` (le
   nouveau défaut ne vaut que pour les équipes à venir). Console :
   `ftbteams party settings_for <équipe> ftbchunks:location_mode private`
   — l'argument `<équipe>` se complète avec Tab (nom ou identifiant
   `161a78e2-eaf3-4456-9b35-34c6f8ed83a5`). Apex est déjà en `private`.
3. Les essais en jeu : `ESSAIS-BMC-94.md`.

## Retour arrière

Remettre les fichiers d'origine (snapshot du jour), retirer
`bmc4_triche.js`, `bmc4_teleportations.js` et les deux jars Xaero, puis
redémarrer.
