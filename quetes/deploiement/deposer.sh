#!/bin/sh
# Dépose les deux archives du livre sur le serveur MineStrator, par SFTP.
# À lancer seulement sur le feu vert d'Arthur, depuis la racine du dépôt :
#
#     sh quetes/deploiement/deposer.sh [AAAA-MM-JJ]   # les archives de ce jour (défaut : aujourd'hui)
#     sh quetes/deploiement/deposer.sh --essai        # essai à blanc : un petit fichier texte, déposé, vu, supprimé
#     sh quetes/deploiement/deposer.sh --bmc91 [AAAA-MM-JJ]  # BMC-91 : jars, scripts, configs, datapack
#                                                           # dans /bmc4-depot/bmc91-<date>/ (rien de mis en place)
#     sh quetes/deploiement/deposer.sh --lot <nom>           # un lot préparé, quetes/deploiement/<nom>/,
#                                                           # dans /bmc4-depot/<nom>/ (rien de mis en place)
#
# Ce que fait le script (mode livre), et rien d'autre :
#   - dépose livre-complet-<date>.zip et livre-leger-<date>.zip (produits par
#     preparer.sh) dans /config/ftbquests/ ;
#   - refuse de partir si un fichier du même nom y est déjà : il n'écrase rien ;
#   - ne supprime rien, ne touche pas au dossier quests/ : renommage,
#     extraction et redémarrage restent à faire avec les outils MineStrator ;
#   - compare ensuite la taille en octets de chaque archive sur le serveur et en
#     local, et l'affiche.
# En mode --essai, la seule écriture est un fichier essai-deposer-*.txt de
# quelques octets, supprimé aussitôt après vérification.
#
# Identifiants : jamais dans le dépôt. Ils sont lus dans le trousseau macOS,
# élément « bmc4-minestrator-sftp » : compte = utilisateur SFTP, commentaire =
# hôte:port, mot de passe = mot de passe SFTP. Pour le créer (le mot de passe
# est demandé, il ne passe ni par la ligne de commande ni par l'historique) :
#
#     security add-generic-password -s bmc4-minestrator-sftp -a <utilisateur> -j <hôte>:<port> -w
#
# Le mot de passe est donné à sftp par SSH_ASKPASS : un petit programme qui le
# lit dans le trousseau au moment où ssh le demande ; il ne figure ni dans les
# arguments, ni dans l'environnement, ni dans un fichier.
set -eu
cd "$(dirname "$0")/../.."
SERVICE=bmc4-minestrator-sftp
DEST=/config/ftbquests

attr() {  # attr <nom> : un attribut de l'élément du trousseau
  security find-generic-password -s "$SERVICE" 2>/dev/null | sed -n "s/^ *\"$1\"<blob>=\"\(.*\)\"\$/\1/p"
}
utilisateur=$(attr acct)
cible=$(attr icmt)
if [ -z "$utilisateur" ] || [ -z "$cible" ]; then
  echo "Élément « $SERVICE » absent ou incomplet dans le trousseau (compte, commentaire hôte:port)." >&2
  exit 1
fi
hote=${cible%:*}
port=${cible##*:}

aide=$(mktemp -t bmc4-askpass)
trap 'rm -f "$aide" "${lot:-}" "${essai:-}"' EXIT
printf '#!/bin/sh\nexec /usr/bin/security find-generic-password -s %s -w\n' "$SERVICE" > "$aide"
chmod 700 "$aide"

lancer() {  # lancer <fichier de commandes> : une session sftp, sortie sur stdout
  SSH_ASKPASS="$aide" SSH_ASKPASS_REQUIRE=force DISPLAY=:0 \
    sftp -q -P "$port" -o PreferredAuthentications=password,keyboard-interactive \
         -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 \
         "$utilisateur@$hote" < "$1" 2>&1
}
taille_distante() {  # taille_distante <sortie de ls -l> <nom>
  # Seules les lignes de « ls -l » comptent : sftp réimprime aussi chaque
  # commande (« sftp> put … <nom> »), dont le dernier champ est le même nom.
  awk -v n="$2" 'NF >= 9 && $1 ~ /^[-dl]/ && $NF == n { print $5 }' "$1" | head -1
}

lot=$(mktemp -t bmc4-sftp)
liste=$(mktemp -t bmc4-ls)

if [ "${1:-}" = "--essai" ]; then
  nom="essai-deposer-$(date +%Y%m%d-%H%M%S).txt"
  essai=$(mktemp -t bmc4-essai)
  echo "Essai à blanc de deposer.sh (BMC-89) — ce fichier est supprimé aussitôt." > "$essai"
  printf 'cd %s\nput %s %s\nls -l\n' "$DEST" "$essai" "$nom" > "$lot"
  lancer "$lot" > "$liste"
  vu=$(taille_distante "$liste" "$nom")
  local_t=$(stat -f %z "$essai")
  printf 'cd %s\nrm %s\nls -l\n' "$DEST" "$nom" > "$lot"
  lancer "$lot" > "$liste.apres"
  encore=$(taille_distante "$liste.apres" "$nom")
  rm -f "$liste" "$liste.apres"
  echo "essai : $nom déposé dans $DEST — serveur ${vu:-absent} o, local $local_t o"
  if [ "${vu:-}" = "$local_t" ] && [ -z "$encore" ]; then
    echo "essai : présent puis supprimé — OK"
  else
    echo "essai : ÉCHEC (taille ${vu:-absente}, encore présent : ${encore:-non})" >&2
    exit 1
  fi
  exit 0
fi

if [ "${1:-}" = "--bmc91" ] || [ "${1:-}" = "--lot" ]; then
  # --bmc91 [date] : le dossier de preparer-bmc91.sh, bmc91-<date>.
  # --lot <nom>    : n'importe quel dossier quetes/deploiement/<nom>/ préparé
  #                  par un preparer-*.sh (BMC-94 : bmc94-<date>).
  # Déposé tel quel dans /bmc4-depot/<nom>/. Rien n'est mis en place ici : les
  # déplacements vers /mods, /kubejs, /world/... se font ensuite avec les
  # outils MineStrator (voir le MISE-EN-PLACE du lot). Refuse si le dossier
  # existe déjà.
  if [ "$1" = "--lot" ]; then
    nomlot=${2:?"--lot attend le nom d’un dossier de quetes/deploiement/"}
    case "$nomlot" in */*|.*) echo "Nom de lot invalide : $nomlot" >&2; exit 1 ;; esac
  else
    nomlot="bmc91-${2:-$(date +%Y-%m-%d)}"
  fi
  src="quetes/deploiement/$nomlot"
  [ -d "$src" ] || { echo "Dossier absent : $src (lancer d'abord le preparer-*.sh du lot)" >&2; exit 1; }
  cible="/bmc4-depot/$nomlot"
  # « cd » puis « ls -l » : les noms sortent nus, comme dans le mode livre.
  printf -- '-mkdir /bmc4-depot\ncd /bmc4-depot\nls -l\n' > "$lot"
  lancer "$lot" > "$liste"
  if [ -n "$(taille_distante "$liste" "$nomlot")" ]; then
    echo "$cible existe déjà : rien n'est déposé." >&2
    exit 1
  fi
  {
    printf 'mkdir %s\n' "$cible"
    (cd "$src" && find . -mindepth 1 -type d | sed 's|^\./||' | sort) | while read -r d; do printf 'mkdir %s/%s\n' "$cible" "$d"; done
    (cd "$src" && find . -type f ! -name .DS_Store | sed 's|^\./||' | sort) | while read -r f; do printf 'put %s/%s %s/%s\n' "$src" "$f" "$cible" "$f"; done
  } > "$lot"
  lancer "$lot" > /dev/null
  ok=1
  for f in $(cd "$src" && find . -type f ! -name .DS_Store | sed 's|^\./||' | sort); do
    printf 'cd %s/%s\nls -l\n' "$cible" "$(dirname "$f")" > "$lot"
    lancer "$lot" > "$liste"
    s=$(taille_distante "$liste" "$(basename "$f")")
    l=$(stat -f %z "$src/$f")
    if [ "${s:-}" = "$l" ]; then etat=identique; else etat=DIFFÉRENT; ok=0; fi
    printf '%-58s serveur %10s o   local %10s o   %s\n' "$f" "${s:-absent}" "$l" "$etat"
  done
  rm -f "$liste"
  [ "$ok" = 1 ] && echo "Dépôt vérifié dans $cible. Suite : la mise en place du lot (MISE-EN-PLACE.md ou BMC-91.md)." || { echo "Dépôt incomplet." >&2; exit 1; }
  exit 0
fi

date=${1:-$(date +%Y-%m-%d)}
fichiers=""
for v in complet leger; do
  f="quetes/deploiement/livre-$v-$date.zip"
  [ -f "$f" ] || { echo "Archive absente : $f (lancer d'abord preparer.sh)" >&2; exit 1; }
  fichiers="$fichiers $f"
done

# 1. Rien n'est écrasé : le dossier ne doit pas déjà contenir ces noms.
printf 'cd %s\nls -l\n' "$DEST" > "$lot"
lancer "$lot" > "$liste"
for f in $fichiers; do
  if [ -n "$(taille_distante "$liste" "$(basename "$f")")" ]; then
    echo "$(basename "$f") existe déjà dans $DEST : rien n'est déposé." >&2
    exit 1
  fi
done

# 2. Dépôt, puis liste du dossier.
{ printf 'cd %s\n' "$DEST"; for f in $fichiers; do printf 'put %s\n' "$f"; done; printf 'ls -l\n'; } > "$lot"
lancer "$lot" > "$liste"

# 3. Tailles en octets, serveur contre local.
ok=1
for f in $fichiers; do
  n=$(basename "$f")
  s=$(taille_distante "$liste" "$n")
  l=$(stat -f %z "$f")
  if [ "${s:-}" = "$l" ]; then etat=identique; else etat=DIFFÉRENT; ok=0; fi
  printf '%-34s serveur %12s o   local %12s o   %s\n' "$n" "${s:-absent}" "$l" "$etat"
done
rm -f "$liste"
[ "$ok" = 1 ] && echo "Dépôt vérifié. Reste à faire côté MineStrator : renommage, extraction, redémarrage." || { echo "Dépôt incomplet." >&2; exit 1; }
