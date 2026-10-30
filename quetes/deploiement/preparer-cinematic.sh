#!/bin/sh
# BMC-103 : prépare le lot serveur de Cinematic Interactions dans
# quetes/deploiement/cinematic-AAAA-MM-JJ/ (ignoré par git). Ne touche à rien
# sur le serveur. Depuis la racine du dépôt :
#
#     sh quetes/deploiement/preparer-cinematic.sh <chemin du jar construit>
#
# Le jar vient du fork Arts44/CinematicInteractions, branche bmc4
# (./gradlew ":1.20.1-forge:build"). Son nom d'origine contient des espaces,
# que deposer.sh refuse : il est renommé, Forge ignore le nom du jar.
# Refuse tout jar dont le SHA-1 n'est pas ATTENDU : le lot et le pack client
# doivent porter le même jar.
set -eu
cd "$(dirname "$0")/../.."
ATTENDU=7347340db99202e5a4781c1c2ba832485520e077
SOURCE=${1:?"chemin du jar construit attendu"}
s=$(shasum -a 1 "$SOURCE" | cut -d' ' -f1)
[ "$s" = "$ATTENDU" ] || { echo "SHA-1 inattendu : $s (attendu $ATTENDU)" >&2; exit 1; }
date=$(date +%Y-%m-%d)
D="quetes/deploiement/cinematic-$date"
[ -e "$D" ] && { echo "$D existe déjà : le supprimer ou attendre demain." >&2; exit 1; }
mkdir -p "$D/mods" "$D/licenses"
cp "$SOURCE" "$D/mods/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4.jar"
cp "$(dirname "$SOURCE")/../../../../LICENSE" "$D/licenses/CinematicInteractions-LICENSE.txt"
cp quetes/deploiement/MISE-EN-PLACE-cinematic.md "$D/MISE-EN-PLACE.md"
(cd "$D" && find . -type f ! -name .DS_Store ! -name SHA1SUMS | sort | while read -r f; do printf '%s  %s\n' "$(shasum -a 1 "$f" | cut -d' ' -f1)" "$f"; done) > "$D/SHA1SUMS"
echo "Lot prêt : $D ($(find "$D" -type f | wc -l | tr -d ' ') fichiers)"
echo "Dépôt (feu vert d'Arthur seulement) : sh quetes/deploiement/deposer.sh --lot cinematic-$date"
