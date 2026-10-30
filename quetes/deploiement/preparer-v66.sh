#!/bin/sh
# v66 : prépare le lot serveur dans quetes/deploiement/v66-AAAA-MM-JJ/ (ignoré par
# git). Ne touche à rien sur le serveur. Depuis la racine du dépôt :
#
#     sh quetes/deploiement/preparer-v66.sh
#
# Les jars viennent de quetes/deploiement/jars-v66/ ; chaque SHA-1 est contrôlé,
# le lot et le pack client doivent porter les mêmes jars.
set -eu
cd "$(dirname "$0")/../.."
J=quetes/deploiement/jars-v66
date=$(date +%Y-%m-%d)
D="quetes/deploiement/v66-$date"
[ -e "$D" ] && { echo "$D existe déjà : le supprimer ou attendre demain." >&2; exit 1; }
mkdir -p "$D/mods" "$D/licenses"
while read -r sha jar; do
  s=$(shasum -a 1 "$J/$jar" | cut -d' ' -f1)
  [ "$s" = "$sha" ] || { echo "SHA-1 inattendu pour $jar : $s" >&2; rm -rf "$D"; exit 1; }
  cp "$J/$jar" "$D/mods/"
done <<'L'
7347340db99202e5a4781c1c2ba832485520e077 Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4.jar
ffb68135b88bdbb25224378c76daf922c3f4c322 refurbished_furniture-forge-1.20.1-1.0.20.jar
L
cp releases/v66/overrides/licenses/CinematicInteractions-LICENSE.txt "$D/licenses/"
cp quetes/deploiement/MISE-EN-PLACE-v66.md "$D/MISE-EN-PLACE.md"
(cd "$D" && find . -type f ! -name .DS_Store ! -name SHA1SUMS | sort | while read -r f; do printf '%s  %s\n' "$(shasum -a 1 "$f" | cut -d' ' -f1)" "$f"; done) > "$D/SHA1SUMS"
echo "Lot prêt : $D ($(find "$D" -type f | wc -l | tr -d ' ') fichiers)"
echo "Dépôt (feu vert d'Arthur seulement) : sh quetes/deploiement/deposer.sh --lot v66-$date"
