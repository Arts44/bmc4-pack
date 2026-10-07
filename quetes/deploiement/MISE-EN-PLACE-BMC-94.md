# BMC-94 — Mise en place côté serveur (temps 1 : serveur seul)

Lot : `/bmc4-depot/bmc94-<date>/`, déposé par
`sh quetes/deploiement/deposer.sh --lot bmc94-<date>` après un snapshot.
Rien n'est mis en place par le dépôt : les déplacements se font avec les
outils MineStrator. `SHA1SUMS` donne l'empreinte de chaque fichier.

Aucun de ces changements ne touche au pack client : un client v62 se
connecte comme avant (les jars Xaero sont ceux du pack v62, à l'octet près ;
tout le reste est script ou configuration du serveur).

## Étape A — faite le 7 octobre à 16 h 02 (Cowork), à refaire avec la correction

`bmc4_triche.js` a été déplacé dans `/kubejs/server_scripts/` et rechargé
(5/5 scripts, 0 erreur). Mais le journal de KubeJS montre, dès la première
commande d'op (16 h 03) : « Cannot find function m_230896_ in object
…CommandSourceStack ». Sur ce serveur, Rhino ne connaît que les noms Mojang,
pas les noms SRG bruts : **le journal des ops n'écrit rien depuis**.

Le lot contient la version corrigée (noms Mojang : `getPlayer()`,
`hasPermission(2)`, `connection`). À faire **dès que possible**, sans
attendre 21 h 30 :

1. Copier `kubejs/server_scripts/bmc4_triche.js` du lot dans
   `/kubejs/server_scripts/` (remplace la version de 16 h 02).
2. Console : `kubejs reload server_scripts`.
3. Taper une commande d'op en jeu (par exemple `/time query daytime`) :
   moins d'une minute plus tard, `#console` affiche
   « 🛡️ **pseudo** · `/time query daytime` · HH:MM ».
4. `logs/kubejs/server.log` ne doit plus contenir « Cannot find function ».

Si l'étape A n'est pas refaite avant 21 h 30, faire le point 1 pendant
l'étape B : le démarrage le chargera.

## Étape B — pendant le redémarrage contrôlé de 21 h 30 (Cowork : arrêt, mise en place, démarrage)

Remplacer ou ajouter (les dossiers absents se créent) :

| Fichier du lot | Destination sur le serveur |
|---|---|
| `kubejs/server_scripts/bmc4_garde.js` | `/kubejs/server_scripts/` (remplace) |
| `kubejs/startup_scripts/bmc4_teleportations.js` | `/kubejs/startup_scripts/` (nouveau dossier) |
| `mods/xaerominimap-forge-1.20.1-26.1.0.jar` | `/mods/` |
| `mods/xaeroworldmap-forge-1.20.1-1.41.0.jar` | `/mods/` |
| `mods/createdupepatch-1.0.jar` | `/mods/` |
| `kubejs/server_scripts/bmc4_triche.js` | `/kubejs/server_scripts/` (remplace, si l'étape A n'a pas été refaite) |
| `config/xaero/minimap/server_profiles/default.cfg` | `/config/xaero/minimap/server_profiles/` (remplace) |
| `config/xaero/minimap/default_radar_categories_server.json` | `/config/xaero/minimap/` (remplace) |
| `config/xaero/world-map/server_profiles/default.cfg` | `/config/xaero/world-map/server_profiles/` (remplace) |
| `config/carryon-common.toml` | `/config/` (remplace) |
| `config/alexsmobs.toml` | `/config/` (remplace) |
| `world/serverconfig/ftbchunks-world.snbt` | `/world/serverconfig/` (remplace) |

Le démarrage charge le tout, y compris le script de démarrage
(`bmc4_teleportations.js`), qui exige un redémarrage complet.

## Étape C — après le redémarrage

1. `latest.log` : KubeJS a chargé 5 scripts serveur et 1 script de démarrage,
   sans erreur (« Loaded … KubeJS server scripts », « startup scripts ») ;
   le serveur a démarré avec `createdupepatch` dans la liste des mods, sans
   erreur de mixin.
2. L'équipe Farmer's est encore en `ftbchunks:location_mode allies` (le
   nouveau défaut ne vaut que pour les équipes à venir). Console :
   `ftbteams party settings_for <équipe> ftbchunks:location_mode private`
   — l'argument `<équipe>` se complète avec Tab (nom ou identifiant
   `161a78e2-eaf3-4456-9b35-34c6f8ed83a5`). Apex est déjà en `private`.
3. Les essais en jeu : `ESSAIS-BMC-94.md`.

## Retour arrière

Remettre les fichiers d'origine (snapshot du jour), retirer
`bmc4_triche.js`, `bmc4_teleportations.js`, les deux jars Xaero et
`createdupepatch-1.0.jar`, puis redémarrer.
