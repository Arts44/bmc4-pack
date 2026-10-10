#!/usr/bin/env python3
# ============================================================
#  empreintes.py — Les empreintes des réglages livrés par une version
#  du pack (BMC-93)
#
#  python3 migration/empreintes.py <zip du pack> > migration/empreintes/vNN.txt
#
#  Une ligne par fichier, « <sha256> <chemin> », triée par chemin :
#  lisible sans outil, par le script macOS (shasum) comme par le script
#  Windows (Get-FileHash). Seuls comptent les fichiers que le joueur
#  peut aussi régler : config/…, et les réglages des shaders
#  (shaderpacks/*.txt, à la racine du dossier). Les jars, les shaders
#  eux-mêmes et les packs de ressources livrés n'en font pas partie.
#
#  Le script de migration compare le fichier du joueur à l'empreinte
#  de SA version : identique, le joueur n'y a pas touché, la nouvelle
#  version garde le sien ; différent, c'est un réglage, il est copié.
# ============================================================
import hashlib, sys, zipfile

def garde(chemin):
    if chemin.startswith('config/'):
        return True
    morceaux = chemin.split('/')
    return len(morceaux) == 2 and morceaux[0] == 'shaderpacks' and morceaux[1].endswith('.txt')

def main(zip_chemin):
    lignes = []
    with zipfile.ZipFile(zip_chemin) as z:
        for info in z.infolist():
            if info.is_dir() or not info.filename.startswith('overrides/'):
                continue
            chemin = info.filename[len('overrides/'):]
            if not garde(chemin):
                continue
            if '\n' in chemin or '\r' in chemin:
                raise SystemExit(f'chemin illisible : {chemin!r}')
            lignes.append((chemin, hashlib.sha256(z.read(info)).hexdigest()))
    for chemin, h in sorted(lignes):
        print(f'{h} {chemin}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage : empreintes.py <zip du pack>')
    main(sys.argv[1])
