# v67 — suivi (pas encore construite)

## À embarquer

- **Cinematic Interactions, correctif BMC-108.** Le prochain zip doit porter dans
  `overrides/mods/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4.jar` le jar du fork
  `Arts44/CinematicInteractions`, branche `bmc4`, commit `e3938ef`, SHA-1
  `e1cb79d2f2e8e136223526cd452eb1d472d93a6f`, à la place de `7347340db99202e5a4781c1c2ba832485520e077`
  (v66). Copie locale : `quetes/deploiement/jars-v66/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4-bmc108.jar`
  (ignorée par git) ; à reconstruire depuis le fork si elle a disparu (`./gradlew ":1.20.1-forge:build"`).
  - Changement serveur seul, canal `12` inchangé : un client v66 reste compatible avec le serveur corrigé.
  - Penser à `preparer-v66.sh` / au prochain lot (`ATTENDU`) et à la liste Crash Assistant.

## État du 13 novembre (zip construit en local, ni tag ni release)

- Branche `v67` = `bmc107-garde-recharge` (`f277099`) = `bmc103-cinematic` (`8a62f26`) + la garde des coffres (BMC-107).
- Zip `releases/BMC4-v67.zip` (ignoré par git), construit par `releases/construire.py releases/v67/changements.json` sur la v66 sans migration, puis `migration/assembler.py`.
- Changements par rapport au zip v66 (`0a72c73f…`) : le jar Cinematic Interactions (`7347340d…` → `e1cb79d2…`, commit `e3938ef` du fork), la liste Crash Assistant (les deux empreintes de ce jar seulement), `manifest.json` (nom et version) et `overrides/bmc4-migration/empreintes/v67.txt`. Aucun mod ajouté, retiré ni changé : 453 entrées de manifeste, comme la v66.
- Côté serveur, hors zip : `bmc4_garde.js` et `startup_scripts/bmc4_coffres_recharge.js` (voir `quetes/deploiement/MISE-EN-PLACE-bmc107.md`, redémarrage nécessaire).
- `bmc4_garde.js` de la v67 = la version EN SERVICE (celle de `origin/bmc94-serveur`) plus le correctif BMC-107. Elle contient tout ce que contient celle de `main` (la refonte BMC-91, 690 lignes) : aucune ligne de `main` ne manque, 138 lignes de plus (coffres des autres factions, `global.bmc4GardeTeleport`), puis les 108 du correctif.
