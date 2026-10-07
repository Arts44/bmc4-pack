#!/bin/sh
# BMC-94 (anti-triche, temps 1 : serveur seul) : prépare tout ce qui part sur
# le serveur, dans quetes/deploiement/bmc94-AAAA-MM-JJ/ (ignoré par git).
# Ne touche à rien sur le serveur. À lancer depuis la racine du dépôt :
#
#     sh quetes/deploiement/preparer-bmc94.sh
#
# Le dossier reproduit les chemins du serveur (voir MISE-EN-PLACE-BMC-94.md) :
#     kubejs/server_scripts/    bmc4_garde.js, bmc4_triche.js
#     kubejs/startup_scripts/   bmc4_teleportations.js (redémarrage requis)
#     mods/                     Xaero's Minimap et World Map (jars du pack v62),
#                               Create Dupe Patch
#     config/xaero/             profils serveur imposés, radar sans joueurs
#     config/                   carryon-common.toml, alexsmobs.toml
#     world/serverconfig/       ftbchunks-world.snbt
# Les jars Xaero viennent de l'instance CurseForge BMC4 v62 de ce Mac : ce sont
# ceux que les clients v62 ont, à l'octet près (SHA-1 relevés le 7 octobre).
set -eu
cd "$(dirname "$0")/../.."
date=$(date +%Y-%m-%d)
D="quetes/deploiement/bmc94-$date"
[ -e "$D" ] && { echo "$D existe déjà : le supprimer ou attendre demain." >&2; exit 1; }

python3 quetes/outils/controle_datapack.py > /dev/null
for f in config/serveur/kubejs/server_scripts/*.js config/serveur/kubejs/startup_scripts/*.js; do
  node --check "$f"
done

INST="$HOME/curseforge/minecraft/Instances/BMC4 v62/mods"
verifier() {  # verifier <jar> <sha1 attendu>
  s=$(shasum -a 1 "$INST/$1" | cut -d' ' -f1)
  [ "$s" = "$2" ] || { echo "SHA-1 inattendu pour $1 : $s" >&2; exit 1; }
}
verifier xaerominimap-forge-1.20.1-26.1.0.jar "$(cat quetes/deploiement/sha1-bmc94/xaerominimap.sha1)"
verifier xaeroworldmap-forge-1.20.1-1.41.0.jar "$(cat quetes/deploiement/sha1-bmc94/xaeroworldmap.sha1)"
# Create Dupe Patch (feu vert d'Arthur, 7 octobre au soir) : CurseForge, projet
# 1447173, fichier 7540240, createdupepatch-1.0.jar (Forge 1.20.1, serveur seul,
# aucun canal réseau ; mixin sur SchematicPrinter.handleCurrentTarget, vérifié
# contre create-1.20.1-6.0.8). Rangé dans quetes/deploiement/jars-bmc94/ (*.jar
# est ignoré par git).
s=$(shasum -a 1 quetes/deploiement/jars-bmc94/createdupepatch-1.0.jar | cut -d' ' -f1)
[ "$s" = "$(cat quetes/deploiement/sha1-bmc94/createdupepatch.sha1)" ] || { echo "SHA-1 inattendu pour createdupepatch-1.0.jar : $s" >&2; exit 1; }

mkdir -p "$D/kubejs/server_scripts" "$D/kubejs/startup_scripts" "$D/mods" \
  "$D/config/xaero/minimap/server_profiles" "$D/config/xaero/world-map/server_profiles" "$D/world/serverconfig"
cp config/serveur/kubejs/server_scripts/bmc4_garde.js config/serveur/kubejs/server_scripts/bmc4_triche.js "$D/kubejs/server_scripts/"
cp config/serveur/kubejs/startup_scripts/bmc4_teleportations.js "$D/kubejs/startup_scripts/"
cp "$INST/xaerominimap-forge-1.20.1-26.1.0.jar" "$INST/xaeroworldmap-forge-1.20.1-1.41.0.jar" "$D/mods/"
cp quetes/deploiement/jars-bmc94/createdupepatch-1.0.jar "$D/mods/"
cp config/serveur/xaero/minimap/server_profiles/default.cfg "$D/config/xaero/minimap/server_profiles/"
cp config/serveur/xaero/minimap/default_radar_categories_server.json "$D/config/xaero/minimap/"
cp config/serveur/xaero/world-map/server_profiles/default.cfg "$D/config/xaero/world-map/server_profiles/"
cp config/serveur/mods-config/carryon-common.toml config/serveur/mods-config/alexsmobs.toml "$D/config/"
cp config/serveur/ftbchunks/ftbchunks-world.snbt "$D/world/serverconfig/"
cp quetes/deploiement/MISE-EN-PLACE-BMC-94.md quetes/deploiement/ESSAIS-BMC-94.md "$D/"
(cd "$D" && find . -type f ! -name .DS_Store ! -name SHA1SUMS | sort | while read -r f; do printf '%s  %s\n' "$(shasum -a 1 "$f" | cut -d' ' -f1)" "$f"; done) > "$D/SHA1SUMS"
echo "Lot prêt : $D ($(find "$D" -type f | wc -l | tr -d ' ') fichiers)"
echo "Dépôt : sh quetes/deploiement/deposer.sh --lot bmc94-$date"
