#!/bin/bash
# ============================================================
#  migrer-bmc4.command — Reprendre ses réglages et ses waypoints de
#  l'ancienne version du pack (BMC-93, macOS)
#
#  Livré à la racine de chaque nouvelle instance BMC4. Double-clic,
#  AVANT le premier lancement de la nouvelle instance.
#
#  Il trouve, à côté, l'instance BMC4 de la version la plus récente
#  qui précède celle-ci (manifest de minecraftinstance.json), et copie
#  vers la nouvelle :
#    toujours           options.txt, servers.dat, xaero/, local/ftbchunks/,
#                       les packs de ressources ajoutés par le joueur
#                       (ce qui existait déjà ici est renommé
#                       « .avant-migration », jamais supprimé) ;
#    si le joueur       les réglages client que le pack livre aussi
#    les a changés      (shaderpacks/*.txt, config/oculus.properties,
#                       config/xaero/…, config/jei/…, les *-client.*,
#                       la vidéo de Xenon, le son de Sound Physics) :
#                       copiés seulement si le fichier diffère de celui
#                       livré par l'ancienne version, d'après
#                       bmc4-migration/empreintes/<version>.txt.
#  Il ne modifie ni ne supprime rien dans l'ancienne instance.
#  Tout ce qu'il fait est écrit dans migration-bmc4.log, ici.
# ============================================================
set -u

ICI="$(cd "$(dirname "$0")" && pwd)"
JOURNAL="$ICI/migration-bmc4.log"
EMPREINTES="$ICI/bmc4-migration/empreintes"

dire() { printf '%s\n' "$*" | tee -a "$JOURNAL"; }
fin() {
  dire ""
  dire "$1"
  echo
  read -r -p "Appuie sur Entrée pour fermer cette fenêtre. " _
  exit "${2:-0}"
}

# Une valeur du fichier d'instance CurseForge (JSON), par plutil.
valeur() { plutil -extract "$2" raw -o - "$1/minecraftinstance.json" 2>/dev/null; }
numero() { printf '%s' "$1" | sed -n 's/^v\([0-9][0-9]*\)$/\1/p'; }

compter_xaero() {
  [ -d "$1/xaero/minimap" ] || { echo 0; return; }
  find "$1/xaero/minimap" -type f -name 'mw*.txt' -exec grep -h '^waypoint:' {} + 2>/dev/null | wc -l | tr -d ' '
}
compter_ftb() {
  [ -d "$1/local/ftbchunks" ] || { echo 0; return; }
  find "$1/local/ftbchunks" -type f -name 'waypoints.json' -exec grep -o '"name"' {} + 2>/dev/null | wc -l | tr -d ' '
}

# Renomme ce qui existe déjà en « .avant-migration » (ou .avant-migration-2…).
mettre_de_cote() {
  local cible="$1" nom="$1.avant-migration" n=2
  [ -e "$cible" ] || return 0
  while [ -e "$nom" ]; do nom="$1.avant-migration-$n"; n=$((n + 1)); done
  mv "$cible" "$nom" && dire "  gardé de côté : ${nom#$ICI/}"
}

: > "$JOURNAL"
dire "Migration BMC4 — $(date '+%Y-%m-%d %H:%M:%S')"
dire "Nouvelle instance : $ICI"

# ---------- La nouvelle instance ----------
[ -f "$ICI/minecraftinstance.json" ] || fin "❌ Ce script doit être dans le dossier d'une instance CurseForge (minecraftinstance.json introuvable). Rien n'a été copié." 1
NOM=$(valeur "$ICI" manifest.name)
VERSION=$(valeur "$ICI" manifest.version)
N=$(numero "$VERSION")
case "$NOM" in BMC4*) ;; *) fin "❌ Cette instance n'est pas BMC4 (« $NOM »). Rien n'a été copié." 1 ;; esac
[ -n "$N" ] || fin "❌ Version de l'instance illisible (« $VERSION »). Rien n'a été copié." 1
dire "Version : $VERSION"

# ---------- Jamais après un premier lancement ----------
JOUE=$(valeur "$ICI" playedCount); JOUE=${JOUE:-0}
if [ "$JOUE" != "0" ] || [ -f "$ICI/options.txt" ] || [ -d "$ICI/logs" ]; then
  fin "❌ Cette instance a déjà été lancée (lancements : $JOUE). Copier maintenant mélangerait tes réglages avec ceux du premier lancement : rien n'a été copié.
Que faire : dans CurseForge, supprime cette instance, réimporte le zip du pack, puis lance ce script AVANT de cliquer sur Jouer.
Ou suis la procédure manuelle du guide Discord." 1
fi

# ---------- L'ancienne instance : la version précédente la plus récente ----------
PARENT="$(dirname "$ICI")"
ANCIENNE=""; AN=0
for d in "$PARENT"/*/; do
  d="${d%/}"
  [ "$d" = "$ICI" ] && continue
  [ -f "$d/minecraftinstance.json" ] || continue
  case "$(valeur "$d" manifest.name)" in BMC4*) ;; *) continue ;; esac
  v=$(numero "$(valeur "$d" manifest.version)")
  [ -n "$v" ] || continue
  if [ "$v" -lt "$N" ] && [ "$v" -gt "$AN" ]; then ANCIENNE="$d"; AN="$v"; fi
done
[ -n "$ANCIENNE" ] || fin "❌ Aucune instance BMC4 plus ancienne que $VERSION dans $PARENT. Rien n'a été copié." 1
dire "Ancienne instance : $ANCIENNE (v$AN)"

AVANT_X=$(compter_xaero "$ICI"); AVANT_F=$(compter_ftb "$ICI")
dire ""
dire "1. Ce que le pack ne livre pas : toujours repris"
copies=0
for p in options.txt servers.dat xaero local/ftbchunks; do
  if [ -e "$ANCIENNE/$p" ]; then
    mettre_de_cote "$ICI/$p"
    mkdir -p "$(dirname "$ICI/$p")"
    cp -Rp "$ANCIENNE/$p" "$ICI/$p" && { dire "  copié : $p"; copies=$((copies + 1)); }
  else
    dire "  absent de l'ancienne instance : $p"
  fi
done

# Packs de ressources ajoutés par le joueur : ceux que le pack n'a posés ni
# par ses overrides (modpackOverrides) ni par son manifest (installedAddons,
# « fileName ») ; le 7 octobre, les 43 packs de l'instance v61 venaient tous
# de l'un ou de l'autre.
LIVRES=$(plutil -extract modpackOverrides json -o - "$ANCIENNE/minecraftinstance.json" 2>/dev/null)
if [ -d "$ANCIENNE/resourcepacks" ]; then
  for f in "$ANCIENNE/resourcepacks"/*; do
    [ -e "$f" ] || continue
    nom=$(basename "$f")
    case "$LIVRES" in *"\"resourcepacks/$nom\""*|*"\"resourcepacks\/$nom\""*) continue ;; esac
    grep -qF "\"fileName\":\"$nom\"" "$ANCIENNE/minecraftinstance.json" && continue
    mettre_de_cote "$ICI/resourcepacks/$nom"
    mkdir -p "$ICI/resourcepacks"
    cp -Rp "$f" "$ICI/resourcepacks/$nom" && { dire "  copié : resourcepacks/$nom (ajouté par le joueur)"; copies=$((copies + 1)); }
  done
fi

dire ""
dire "2. Ce que le pack livre aussi : repris seulement si tu l'avais changé"
LISTE="$EMPREINTES/v$AN.txt"
changes=0; identiques=0; absents=0
if [ ! -f "$LISTE" ]; then
  dire "  pas d'empreintes pour v$AN : ces réglages ne sont pas repris, la nouvelle version garde les siens."
else
  while read -r h p; do
    case "$p" in
      shaderpacks/*.txt|config/oculus.properties|config/iris*|config/xaero/*|config/xaero*.txt|config/jei/*|*client*) ;;
      config/xenon-options.json|config/xenon++.toml|config/sound_physics_remastered/*) ;;  # vidéo (Xenon) et son (Sound Physics)
      *) continue ;;
    esac
    if [ ! -f "$ANCIENNE/$p" ]; then absents=$((absents + 1)); continue; fi
    a=$(shasum -a 256 "$ANCIENNE/$p" | cut -d' ' -f1)
    if [ "$a" = "$h" ]; then identiques=$((identiques + 1)); continue; fi
    mettre_de_cote "$ICI/$p"
    mkdir -p "$(dirname "$ICI/$p")"
    cp -p "$ANCIENNE/$p" "$ICI/$p" && { dire "  copié (réglé par toi) : $p"; changes=$((changes + 1)); }
  done < "$LISTE"
  dire "  $changes copié(s), $identiques gardé(s) tels que livrés par la nouvelle version, $absents absent(s) de l'ancienne"
fi

APRES_X=$(compter_xaero "$ICI"); APRES_F=$(compter_ftb "$ICI")
LANGUE=$(sed -n 's/^lang://p' "$ICI/options.txt" 2>/dev/null)
TOUCHES=$(grep -c '^key_' "$ICI/options.txt" 2>/dev/null || echo 0)
dire ""
dire "Bilan"
dire "  waypoints Xaero       : $AVANT_X → $APRES_X"
dire "  waypoints FTB Chunks  : $AVANT_F → $APRES_F"
dire "  langue                : ${LANGUE:-non trouvée}"
dire "  touches               : $TOUCHES"
dire "  fichiers repris       : $((copies + changes))"
dire "  ancienne instance     : intacte, rien n'y a été modifié"
fin "✅ Terminé. Lance maintenant la nouvelle instance depuis CurseForge. Le détail est dans migration-bmc4.log."
