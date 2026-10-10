# ============================================================
#  migrer-bmc4.ps1 — Reprendre ses réglages et ses waypoints de
#  l'ancienne version du pack (BMC-93, Windows)
#
#  Lancé par migrer-bmc4.bat, à la racine de la nouvelle instance,
#  AVANT son premier lancement. Même règle que migrer-bmc4.command
#  (macOS) : voir ce fichier pour le détail.
#
#  Enregistré en UTF-8 AVEC BOM : sans BOM, Windows PowerShell 5.1 lit
#  le fichier en ANSI et les accents des messages sont abîmés.
# ============================================================
$ErrorActionPreference = 'Stop'

$Ici = Split-Path -Parent $PSScriptRoot
$Journal = Join-Path $Ici 'migration-bmc4.log'
$Empreintes = Join-Path $PSScriptRoot 'empreintes'

function Dire([string]$texte) {
  Write-Host $texte
  Add-Content -LiteralPath $Journal -Value $texte -Encoding UTF8
}
function Fin([string]$texte, [int]$code = 0) {
  Dire ''
  Dire $texte
  Write-Host ''
  Read-Host 'Appuie sur Entrée pour fermer cette fenêtre' | Out-Null
  exit $code
}
function Lire-Instance([string]$dossier) {
  $f = Join-Path $dossier 'minecraftinstance.json'
  if (-not (Test-Path -LiteralPath $f)) { return $null }
  try { return (Get-Content -LiteralPath $f -Raw -Encoding UTF8 | ConvertFrom-Json) } catch { return $null }
}
function Numero([string]$version) {
  if ($version -match '^v(\d+)$') { return [int]$Matches[1] }
  return $null
}
function Compter-Xaero([string]$dossier) {
  $d = Join-Path $dossier 'xaero\minimap'
  if (-not (Test-Path -LiteralPath $d)) { return 0 }
  $n = 0
  Get-ChildItem -LiteralPath $d -Recurse -File -Filter 'mw*.txt' | ForEach-Object {
    $n += @(Select-String -LiteralPath $_.FullName -Pattern '^waypoint:').Count
  }
  return $n
}
function Compter-Ftb([string]$dossier) {
  $d = Join-Path $dossier 'local\ftbchunks'
  if (-not (Test-Path -LiteralPath $d)) { return 0 }
  $n = 0
  Get-ChildItem -LiteralPath $d -Recurse -File -Filter 'waypoints.json' | ForEach-Object {
    $n += ([regex]::Matches((Get-Content -LiteralPath $_.FullName -Raw), '"name"')).Count
  }
  return $n
}
# Renomme ce qui existe déjà en « .avant-migration » (ou .avant-migration-2…).
function Mettre-De-Cote([string]$cible) {
  if (-not (Test-Path -LiteralPath $cible)) { return }
  $nom = "$cible.avant-migration"; $i = 2
  while (Test-Path -LiteralPath $nom) { $nom = "$cible.avant-migration-$i"; $i++ }
  Rename-Item -LiteralPath $cible -NewName (Split-Path -Leaf $nom)
  Dire ('  gardé de côté : ' + $nom.Substring($Ici.Length + 1))
}
function Copier([string]$source, [string]$cible) {
  $parent = Split-Path -Parent $cible
  if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
  Copy-Item -LiteralPath $source -Destination $cible -Recurse -Force
}

Set-Content -LiteralPath $Journal -Value '' -Encoding UTF8
Dire ('Migration BMC4 — ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
Dire "Nouvelle instance : $Ici"

try {
  # ---------- La nouvelle instance ----------
  $moi = Lire-Instance $Ici
  if ($null -eq $moi) { Fin "❌ Ce script doit être dans le dossier d'une instance CurseForge (minecraftinstance.json introuvable). Rien n'a été copié." 1 }
  $nomPack = [string]$moi.manifest.name
  $version = [string]$moi.manifest.version
  $n = Numero $version
  if (-not $nomPack.StartsWith('BMC4')) { Fin "❌ Cette instance n'est pas BMC4 (« $nomPack »). Rien n'a été copié." 1 }
  if ($null -eq $n) { Fin "❌ Version de l'instance illisible (« $version »). Rien n'a été copié." 1 }
  Dire "Version : $version"

  # ---------- Jamais après un premier lancement ----------
  $joue = [int]$moi.playedCount
  if ($joue -ne 0 -or (Test-Path -LiteralPath (Join-Path $Ici 'options.txt')) -or (Test-Path -LiteralPath (Join-Path $Ici 'logs'))) {
    Fin ("❌ Cette instance a déjà été lancée (lancements : $joue). Copier maintenant mélangerait tes réglages avec ceux du premier lancement : rien n'a été copié.`n" +
      "Que faire : dans CurseForge, supprime cette instance, réimporte le zip du pack, puis lance ce script AVANT de cliquer sur Jouer.`n" +
      'Ou suis la procédure manuelle du guide Discord.') 1
  }

  # ---------- L'ancienne instance : la version précédente la plus récente ----------
  $parent = Split-Path -Parent $Ici
  $ancienne = $null; $an = 0; $ancienneInfo = $null
  Get-ChildItem -LiteralPath $parent -Directory | ForEach-Object {
    if ($_.FullName -eq $Ici) { return }
    $info = Lire-Instance $_.FullName
    if ($null -eq $info -or -not ([string]$info.manifest.name).StartsWith('BMC4')) { return }
    $v = Numero ([string]$info.manifest.version)
    if ($null -ne $v -and $v -lt $n -and $v -gt $an) { $script:ancienne = $_.FullName; $script:an = $v; $script:ancienneInfo = $info }
  }
  if ($null -eq $ancienne) { Fin "❌ Aucune instance BMC4 plus ancienne que $version dans $parent. Rien n'a été copié." 1 }
  Dire "Ancienne instance : $ancienne (v$an)"

  $avantX = Compter-Xaero $Ici; $avantF = Compter-Ftb $Ici
  Dire ''
  Dire '1. Ce que le pack ne livre pas : toujours repris'
  $copies = 0
  foreach ($p in @('options.txt', 'servers.dat', 'xaero', 'local\ftbchunks')) {
    $src = Join-Path $ancienne $p; $dst = Join-Path $Ici $p
    if (Test-Path -LiteralPath $src) {
      Mettre-De-Cote $dst
      Copier $src $dst
      Dire ('  copié : ' + ($p -replace '\\', '/')); $copies++
    } else {
      Dire ('  absent de l''ancienne instance : ' + ($p -replace '\\', '/'))
    }
  }

  # Packs de ressources ajoutés par le joueur : ni dans les overrides
  # (modpackOverrides), ni dans le manifest (installedAddons, fileName).
  $livres = @{}
  foreach ($o in @($ancienneInfo.modpackOverrides)) { if ($o) { $livres[([string]$o).ToLower()] = $true } }
  foreach ($a in @($ancienneInfo.installedAddons)) {
    if ($a.installedFile -and $a.installedFile.fileName) { $livres[('resourcepacks/' + [string]$a.installedFile.fileName).ToLower()] = $true }
  }
  $rp = Join-Path $ancienne 'resourcepacks'
  if (Test-Path -LiteralPath $rp) {
    Get-ChildItem -LiteralPath $rp | ForEach-Object {
      if ($livres.ContainsKey(('resourcepacks/' + $_.Name).ToLower())) { return }
      $dst = Join-Path (Join-Path $Ici 'resourcepacks') $_.Name
      Mettre-De-Cote $dst
      Copier $_.FullName $dst
      Dire ('  copié : resourcepacks/' + $_.Name + ' (ajouté par le joueur)'); $script:copies++
    }
  }

  Dire ''
  Dire '2. Ce que le pack livre aussi : repris seulement si tu l''avais changé'
  $liste = Join-Path $Empreintes "v$an.txt"
  $changes = 0; $identiques = 0; $absents = 0
  $concerne = '^(shaderpacks/.*\.txt|config/oculus\.properties|config/iris.*|config/xaero/.*|config/xaero[^/]*\.txt|config/jei/.*|.*client.*|config/xenon-options\.json|config/xenon\+\+\.toml|config/sound_physics_remastered/.*)$'
  if (-not (Test-Path -LiteralPath $liste)) {
    Dire "  pas d'empreintes pour v$an : ces réglages ne sont pas repris, la nouvelle version garde les siens."
  } else {
    foreach ($ligne in (Get-Content -LiteralPath $liste -Encoding UTF8)) {
      $i = $ligne.IndexOf(' ')
      if ($i -lt 1) { continue }
      $h = $ligne.Substring(0, $i); $p = $ligne.Substring($i + 1)
      if ($p -notmatch $concerne) { continue }
      $src = Join-Path $ancienne ($p -replace '/', '\')
      if (-not (Test-Path -LiteralPath $src -PathType Leaf)) { $absents++; continue }
      $a = (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash.ToLower()
      if ($a -eq $h) { $identiques++; continue }
      $dst = Join-Path $Ici ($p -replace '/', '\')
      Mettre-De-Cote $dst
      Copier $src $dst
      Dire "  copié (réglé par toi) : $p"; $changes++
    }
    Dire "  $changes copié(s), $identiques gardé(s) tels que livrés par la nouvelle version, $absents absent(s) de l'ancienne"
  }

  $apresX = Compter-Xaero $Ici; $apresF = Compter-Ftb $Ici
  $options = Join-Path $Ici 'options.txt'
  $langue = 'non trouvée'; $touches = 0
  if (Test-Path -LiteralPath $options) {
    $lignes = Get-Content -LiteralPath $options -Encoding UTF8
    $l = $lignes | Where-Object { $_ -like 'lang:*' } | Select-Object -First 1
    if ($l) { $langue = $l.Substring(5) }
    $touches = @($lignes | Where-Object { $_ -like 'key_*' }).Count
  }
  Dire ''
  Dire 'Bilan'
  Dire "  waypoints Xaero       : $avantX → $apresX"
  Dire "  waypoints FTB Chunks  : $avantF → $apresF"
  Dire "  langue                : $langue"
  Dire "  touches               : $touches"
  Dire ('  fichiers repris       : ' + ($copies + $changes))
  Dire '  ancienne instance     : intacte, rien n''y a été modifié'
  Fin '✅ Terminé. Lance maintenant la nouvelle instance depuis CurseForge. Le détail est dans migration-bmc4.log.'
} catch {
  Fin ("❌ Erreur inattendue : " + $_.Exception.Message + "`nRien n'a été supprimé. Envoie migration-bmc4.log au staff.") 2
}
