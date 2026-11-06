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
