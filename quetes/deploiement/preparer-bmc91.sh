#!/bin/sh
# BMC-91 (rangs de prestige) : prépare tout ce qui part sur le serveur pendant
# la maintenance, dans quetes/deploiement/bmc91-AAAA-MM-JJ/ (ignoré par git).
# Ne touche à rien sur le serveur. À lancer depuis la racine du dépôt :
#
#     sh quetes/deploiement/preparer-bmc91.sh
#
# Le dossier reproduit les chemins du serveur, pour que chaque déplacement
# soit mécanique (voir BMC-91.md) :
#     mods/                      les quatre jars, vérifiés par SHA-1
#     kubejs/server_scripts/     les trois scripts serveur
#     world/serverconfig/        ftbessentials.snbt, ftbranks/ranks.snbt
#     retour-arriere/            ranks-sans-kubejs.snbt
#     bmc4-fixes.zip             le datapack (un dossier bmc4-fixes/ dedans)
# Le livre se prépare à part, avec preparer.sh (mêmes archives que BMC-89).
#
# Les jars viennent des dépôts Maven des auteurs (mêmes fichiers que
# CurseForge). Les empreintes ci-dessous ont été relevées le 6 octobre 2026 sur
# les fichiers .sha1 publiés à côté de chaque jar ; celle de FTB Ranks est
# aussi celle du jar de l'instance Creative locale. Un jar qui ne correspond
# pas arrête tout.
set -eu
cd "$(dirname "$0")/../.."
date=$(date +%Y-%m-%d)
D="quetes/deploiement/bmc91-$date"
[ -e "$D" ] && { echo "$D existe déjà : le supprimer ou attendre demain." >&2; exit 1; }

# Les contrôles d'abord : rien ne part si le dépôt n'est pas cohérent.
python3 config/rangs/generer.py --verifier
python3 quetes/outils/controle_datapack.py > /dev/null
python3 quetes/outils/generer.py --verifier > /dev/null

mkdir -p "$D/mods" "$D/kubejs/server_scripts" "$D/world/serverconfig/ftbranks" "$D/retour-arriere"

# nom|url|sha1|taille
while IFS='|' read -r nom url sha taille; do
  [ -n "$nom" ] || continue
  curl -fsSL -o "$D/mods/$nom" "$url"
  vu=$(shasum -a 1 "$D/mods/$nom" | cut -d' ' -f1)
  t=$(stat -f %z "$D/mods/$nom")
  if [ "$vu" != "$sha" ] || [ "$t" != "$taille" ]; then
    echo "$nom : empreinte ou taille inattendue ($vu, $t o) — arrêt" >&2
    exit 1
  fi
  echo "mods/$nom : $t o, SHA-1 vérifié"
done <<'LISTE'
ftb-ranks-forge-2001.1.7.jar|https://maven.ftb.dev/releases/dev/ftb/mods/ftb-ranks-forge/2001.1.7/ftb-ranks-forge-2001.1.7.jar|1ef101b4c5991cc239d9b56a95500e3b404228f7|87362
ftb-essentials-forge-2001.2.4.jar|https://maven.ftb.dev/releases/dev/ftb/mods/ftb-essentials-forge/2001.2.4/ftb-essentials-forge-2001.2.4.jar|4f898578e3cc321397dbc59a0c44e2927000bd32|157732
kubejs-forge-2001.6.5-build.26.jar|https://maven.latvian.dev/releases/dev/latvian/mods/kubejs-forge/2001.6.5-build.26/kubejs-forge-2001.6.5-build.26.jar|6986aef8f4a918b8df0e2ed9dc82244c5ac740da|1658792
rhino-forge-2001.2.3-build.10.jar|https://maven.latvian.dev/releases/dev/latvian/mods/rhino-forge/2001.2.3-build.10/rhino-forge-2001.2.3-build.10.jar|54db3943a391723bc0c2b84a46038eb2d66ebb25|1798243
LISTE

cp config/serveur/kubejs/server_scripts/*.js "$D/kubejs/server_scripts/"
cp config/serveur/ftbessentials.snbt "$D/world/serverconfig/"
cp config/serveur/ftbranks/ranks.snbt "$D/world/serverconfig/ftbranks/"
cp config/serveur/ftbranks/ranks-sans-kubejs.snbt "$D/retour-arriere/"

tmp=$(mktemp -d)
cp -R config/datapack/bmc4-fixes "$tmp/bmc4-fixes"
find "$tmp" -name .DS_Store -delete
(cd "$tmp" && zip -qr bmc4-fixes.zip bmc4-fixes)
mv "$tmp/bmc4-fixes.zip" "$D/"
rm -rf "$tmp"
n=$(find config/datapack/bmc4-fixes -name '*.mcfunction' | wc -l | tr -d ' ')
echo "bmc4-fixes.zip : $n fonctions"
echo "Prêt : $D"
