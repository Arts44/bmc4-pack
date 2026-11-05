# BMC-108 — jar de diagnostic de Cinematic Interactions

Lot : `/bmc4-depot/bmc108-diag-<date>/`, déposé par `sh quetes/deploiement/deposer.sh
--lot bmc108-diag-<date>`. Le dépôt ne met rien en place. Une action par ligne.

Jar : fork `Arts44/CinematicInteractions`, branche `bmc4-diag`, commit `4ff4f16` (sur
`e492fee`), SHA-1 `269bb4bb1e8fec4e27acc029153fd9c0972fe803`. Il ne fait qu'écrire dans
`latest.log`, au niveau INFO, des lignes `[cinematic-diag]` côté serveur. Même canal et même
protocole (`12`) : les clients v66 ne changent pas.

## Mise en place

1. Arrêter le serveur (`power_action stop`).
2. `move_files` : `/mods/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4.jar` (SHA-1 `7347340d…`) vers `/bmc4-depot/bmc108-diag-<date>/ancien/`. Deux jars du même mod dans `/mods` empêchent le démarrage.
3. `move_files` : `/bmc4-depot/bmc108-diag-<date>/mods/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4-diag.jar` vers `/mods/`.
4. Démarrer le serveur (`power_action start`).
5. `latest.log` : une ligne `[cinematic-diag] sentinelles de la sonde enregistrées (HIGHEST à LOWEST, receiveCanceled)` au démarrage.

## Reproduire

6. Un joueur v66 ouvre une scène dans son propre claim : établi, puis four.
7. `search_in_file /logs/latest.log` sur `cinematic-diag`.

Ce qu'on y lit :
- `begin refusé, …` : la raison du refus (`kind.matches`, `sides vide`, `valid`/`usable` avec le détail, `mayUse faux`, `MenuActions.open`) ;
- `mayUse à … : probeReached=… isCanceled=… useBlock=… useItem=…` : le résultat de la sonde ;
- `sonde, fin de la tranche HIGHEST … LOWEST` : l'état de l'événement à la fin de chaque tranche de priorité. La première tranche où `isCanceled=true` apparaît est celle où un écouteur l'annule (ou une tranche avant, pour la première ligne) ;
- `session ouverte` puis `session fermée au tick` ou `action … refusée` : la scène s'ouvre mais se ferme ensuite, avec le détail de `valid` ;
- `Network.accepts faux` : le serveur ne voit pas le canal du client.

## Retour

1. Arrêter le serveur.
2. `move_files` : `/mods/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4-diag.jar` vers `/bmc4-depot/bmc108-diag-<date>/mods/`.
3. `move_files` : `/bmc4-depot/bmc108-diag-<date>/ancien/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4.jar` vers `/mods/`.
4. Démarrer le serveur.
