# BMC-108 — correctif de Cinematic Interactions : les scènes ne se ferment plus

Lot : `/bmc4-depot/bmc108-fix-<date>/`, déposé par `sh quetes/deploiement/deposer.sh
--lot bmc108-fix-<date>`. Le dépôt ne met rien en place. Une action par ligne.

Jar : fork `Arts44/CinematicInteractions`, branche `bmc4`, commit `e3938ef` (correctif
`86188b6`), SHA-1 `e1cb79d2f2e8e136223526cd452eb1d472d93a6f`. Cause : la sonde relisait
`useBlock` après sa propre annulation, que Forge 47.4.20 met à `DENY`. Le correctif ne change
que du code serveur ; canal `12` inchangé : les clients v66 gardent leur jar `7347340d…`.

## Mise en place

1. Arrêter le serveur (`power_action stop`).
2. Créer le dossier `/bmc4-depot/bmc108-fix-<date>/diag/`.
3. `move_files` : `/mods/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4-diag.jar` vers `/bmc4-depot/bmc108-fix-<date>/diag/`.
4. `move_files` : `/bmc4-depot/bmc108-fix-<date>/mods/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4.jar` vers `/mods/`.
5. Démarrer le serveur (`power_action start`).
6. `latest.log` : `cinematic` chargé, démarrage jusqu'à « Done », et **aucune** ligne `[cinematic-diag]`.

## Essai

7. Dans son propre claim, main vide : établi, puis four. La scène reste ouverte.
8. Chez une autre faction, hors raid et hors alliés : four. Refusé, la scène se ferme.
9. Reporter le résultat dans BMC-98.

## Retour

1. Arrêter le serveur.
2. `move_files` : `/mods/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4.jar` vers `/bmc4-depot/bmc108-fix-<date>/mods/`.
3. `move_files` : au choix, le jar de diagnostic depuis `/bmc4-depot/bmc108-fix-<date>/diag/`, ou l'ancien jar (`7347340d…`) depuis `/bmc4-depot/bmc108-diag-2026-11-05/ancien/`, vers `/mods/`.
4. Démarrer le serveur.

Les deux jars de retour portent le même nom de fichier que le correctif, ou presque : un seul
jar de Cinematic à la fois dans `/mods`.
