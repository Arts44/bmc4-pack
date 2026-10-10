#!/usr/bin/env python3
# ============================================================
#  assembler.py — Ajouter la migration à un zip du pack (BMC-93)
#
#  python3 migration/assembler.py <zip exporté> <zip de la release>
#
#  1. calcule les empreintes du zip exporté et les écrit dans
#     migration/empreintes/<version du manifest>.txt (à commiter) ;
#  2. écrit le zip de la release : le zip exporté, plus, dans overrides/,
#       migrer-bmc4.command        (droit d'exécution gardé)
#       migrer-bmc4.bat
#       bmc4-migration/migrer-bmc4.ps1
#       bmc4-migration/empreintes/vNN.txt   (toutes les versions connues)
#       bmc4-migration/LISEZ-MOI.txt
#  Le zip exporté n'est jamais modifié. Refuse un zip qui contient déjà
#  la migration, ou dont la version n'a pas la forme vNN.
# ============================================================
import io, json, os, re, sys, zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import empreintes  # noqa: E402

def main(entree, sortie):
    if os.path.abspath(entree) == os.path.abspath(sortie):
        raise SystemExit('le zip de la release doit être un nouveau fichier')
    with zipfile.ZipFile(entree) as z:
        version = json.loads(z.read('manifest.json'))['version']
        if not re.fullmatch(r'v\d+', version):
            raise SystemExit(f'version du manifest illisible : {version!r}')
        if any(n.startswith('overrides/bmc4-migration/') for n in z.namelist()):
            raise SystemExit('ce zip contient déjà la migration')

    tampon = io.StringIO()
    sys_stdout, sys.stdout = sys.stdout, tampon
    try:
        empreintes.main(entree)
    finally:
        sys.stdout = sys_stdout
    chemin = os.path.join(ICI, 'empreintes', f'{version}.txt')
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(tampon.getvalue())
    print(f'empreintes : {chemin} ({tampon.getvalue().count(chr(10))} fichiers)')

    ajouts = [
        ('overrides/migrer-bmc4.command', os.path.join(ICI, 'migrer-bmc4.command'), 0o755),
        ('overrides/migrer-bmc4.bat', os.path.join(ICI, 'migrer-bmc4.bat'), 0o644),
        ('overrides/bmc4-migration/migrer-bmc4.ps1', os.path.join(ICI, 'bmc4-migration', 'migrer-bmc4.ps1'), 0o644),
        ('overrides/bmc4-migration/LISEZ-MOI.txt', os.path.join(ICI, 'bmc4-migration', 'LISEZ-MOI.txt'), 0o644),
    ]
    for nom in sorted(os.listdir(os.path.join(ICI, 'empreintes'))):
        if re.fullmatch(r'v\d+\.txt', nom):
            ajouts.append((f'overrides/bmc4-migration/empreintes/{nom}', os.path.join(ICI, 'empreintes', nom), 0o644))

    with zipfile.ZipFile(entree) as z, zipfile.ZipFile(sortie, 'w', zipfile.ZIP_DEFLATED) as out:
        for info in z.infolist():
            out.writestr(info, z.read(info))
        for nom, source, mode in ajouts:
            info = zipfile.ZipInfo(nom, date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = (0o100000 | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(source, 'rb') as f:
                out.writestr(info, f.read())
    print(f'release : {sortie} (+{len(ajouts)} fichiers de migration)')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage : assembler.py <zip exporté> <zip de la release>')
    main(sys.argv[1], sys.argv[2])
