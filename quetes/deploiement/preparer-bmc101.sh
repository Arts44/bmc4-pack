#!/bin/sh
# BMC-101 : prépare le lot serveur dans quetes/deploiement/bmc101-AAAA-MM-JJ/
# (ignoré par git). Ne touche à rien sur le serveur. Depuis la racine du dépôt :
#
#     sh quetes/deploiement/preparer-bmc101.sh
#
# Le dossier :
#     kubejs/server_scripts/bmc4_v64_retraits.js   Lentille à distance et Molotov retirés
#     kubejs/startup_scripts/bmc4_v64_sculk.js     cri du Sculk Special plafonné
#     config/kaleidoscope_tavern-common.toml       InfiniteLavaFromTap = false
#     config/kaleidoscope_cookery-common.toml      SatiatedShieldAbsorbEnabled = false
#     MISE-EN-PLACE.md, SHA1SUMS
set -eu
cd "$(dirname "$0")/../.."
date=$(date +%Y-%m-%d)
D="quetes/deploiement/bmc101-$date"
[ -e "$D" ] && { echo "$D existe déjà : le supprimer ou attendre demain." >&2; exit 1; }
mkdir -p "$D/kubejs/server_scripts" "$D/kubejs/startup_scripts" "$D/config"
cp config/serveur/kubejs/server_scripts/bmc4_v64_retraits.js "$D/kubejs/server_scripts/"
cp config/serveur/kubejs/startup_scripts/bmc4_v64_sculk.js "$D/kubejs/startup_scripts/"
cp config/serveur/mods-config/kaleidoscope_tavern-common.toml config/serveur/mods-config/kaleidoscope_cookery-common.toml "$D/config/"
cp quetes/deploiement/MISE-EN-PLACE-bmc101.md "$D/MISE-EN-PLACE.md"
(cd "$D" && find . -type f ! -name .DS_Store ! -name SHA1SUMS | sort | while read -r f; do printf '%s  %s\n' "$(shasum -a 1 "$f" | cut -d' ' -f1)" "$f"; done) > "$D/SHA1SUMS"
echo "Lot prêt : $D ($(find "$D" -type f | wc -l | tr -d ' ') fichiers)"
echo "Dépôt : sh quetes/deploiement/deposer.sh --lot bmc101-$date"
