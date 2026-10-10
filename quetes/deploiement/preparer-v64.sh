#!/bin/sh
# v64 (BMC-95, BMC-96) : prépare le lot serveur dans
# quetes/deploiement/v64-AAAA-MM-JJ/ (ignoré par git). Ne touche à rien sur
# le serveur. À lancer depuis la racine du dépôt :
#
#     sh quetes/deploiement/preparer-v64.sh
#
# Le dossier :
#     mods/                  les mods v64 qui vont des DEUX côtés (client et
#                            serveur), d'après releases/v64/changements.json
#     mods-si-b-valides/     les mods de #mods (revue du 11 octobre), à ne
#                            mettre en place que s'ils sont validés
#     A-RETIRER.txt          ce qui part du serveur (XaeroPlus, inactif)
#     MISE-EN-PLACE.md, SHA1SUMS
# Les jars viennent de quetes/deploiement/jars-v64/ (*.jar ignoré par git) ;
# leur SHA-1 est contrôlé contre releases/v64/changements*.json. Les mods
# « client » (Do a Barrel Roll, Leawind's Third Person) ne vont pas sur le
# serveur. Les noms de fichiers sont gardés, sauf les espaces, remplacés par
# des tirets (deposer.sh ne les accepte pas ; Forge ignore le nom du jar).
set -eu
cd "$(dirname "$0")/../.."
date=$(date +%Y-%m-%d)
D="quetes/deploiement/v64-$date"
[ -e "$D" ] && { echo "$D existe déjà : le supprimer ou attendre demain." >&2; exit 1; }
mkdir -p "$D/mods" "$D/mods-si-b-valides"
python3 - "$D" <<'PY'
import json, hashlib, shutil, sys
D = sys.argv[1]
a = json.load(open('releases/v64/changements.json', encoding='utf-8'))['ajouter']
tous = json.load(open('releases/v64/changements-avec-b.json', encoding='utf-8'))['ajouter']
ids_a = {m['projectID'] for m in a}
for m in tous:
    if m['cote'] != 'les deux':
        continue
    src = 'quetes/deploiement/jars-v64/' + m['jar']
    s = hashlib.sha1(open(src, 'rb').read()).hexdigest()
    if s != m['sha1']:
        raise SystemExit(f"SHA-1 inattendu pour {m['jar']} : {s} (attendu {m['sha1']})")
    dossier = 'mods' if m['projectID'] in ids_a else 'mods-si-b-valides'
    shutil.copyfile(src, f"{D}/{dossier}/{m['jar'].replace(' ', '-')}")
    print(f"  {dossier}/{m['jar'].replace(' ', '-')}  ({m['nom']}, CurseForge {m['projectID']}/{m['fileID']})")
PY
cat > "$D/A-RETIRER.txt" <<'TXT'
À retirer du serveur pour la v64 (BMC-95 : XaeroPlus quitte le pack).
Aucun de ces fichiers n'est chargé par le serveur (XaeroPlus est un mod client,
rangé hors de /mods) : c'est du rangement. Les déplacer, ne pas les supprimer :

  /mods-clients/XaeroPlus-2.32.0+forge-1.20.1-WM1.41.0-MM26.1.0.jar
  /config/xaeroplus.txt
  /defaultconfigs/xaeroplus.txt

vers /bmc4-depot/sauvegarde-v64/ (mêmes chemins relatifs).
Aucun jar du serveur n'est remplacé par la v64 : les mods ajoutés sont nouveaux.
TXT
cp quetes/deploiement/MISE-EN-PLACE-v64.md "$D/MISE-EN-PLACE.md"
(cd "$D" && find . -type f ! -name .DS_Store ! -name SHA1SUMS | sort | while read -r f; do printf '%s  %s\n' "$(shasum -a 1 "$f" | cut -d' ' -f1)" "$f"; done) > "$D/SHA1SUMS"
echo "Lot prêt : $D ($(find "$D" -type f | wc -l | tr -d ' ') fichiers)"
echo "Dépôt (feu vert d'Arthur seulement) : sh quetes/deploiement/deposer.sh --lot v64-$date"
