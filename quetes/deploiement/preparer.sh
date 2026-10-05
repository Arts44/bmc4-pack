#!/bin/sh
# Prépare les deux variantes du livre, prêtes à déposer sur le serveur.
# Ne touche à rien sur le serveur. À lancer depuis la racine du dépôt :
#
#     sh quetes/deploiement/preparer.sh
#
# Produit, dans quetes/deploiement/ (fichiers ignorés par git) :
#     livre-complet-AAAA-MM-JJ.zip   le livre entier, Encyclopédie comprise
#     livre-leger-AAAA-MM-JJ.zip     le même sans l'Encyclopédie
# Chaque archive contient un seul dossier « quests/ », à extraire dans
# /config/ftbquests/ sur le serveur.
set -eu
cd "$(dirname "$0")/../.."
python3 quetes/outils/generer.py --verifier
python3 quetes/outils/generer.py > /dev/null
date=$(date +%Y-%m-%d)
tmp=$(mktemp -d)
for v in complet leger; do
  src=quetes/livre; [ "$v" = leger ] && src=quetes/livre-leger
  rm -rf "$tmp/quests"; cp -R "$src" "$tmp/quests"
  find "$tmp/quests" -name .DS_Store -delete
  (cd "$tmp" && zip -qr "livre-$v-$date.zip" quests)
  mv "$tmp/livre-$v-$date.zip" quetes/deploiement/
  n=$(ls "$src/chapters" | wc -l | tr -d ' ')
  echo "quetes/deploiement/livre-$v-$date.zip : $n chapitres"
done
rm -rf "$tmp"
