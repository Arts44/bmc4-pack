#!/usr/bin/env python3
# ============================================================
#  construire.py — Construire le zip d'une version du pack à partir de la
#  précédente, par une liste de changements versionnée (v64, 10 octobre 2026)
#
#  python3 releases/construire.py releases/v64/changements.json <zip de base> <zip exporté>
#
#  changements.json :
#    version, nom                       manifest.version et manifest.name
#    retirer      [{projectID, nom, raison}]          entrées du manifest ôtées
#    ajouter      [{projectID, fileID, nom, url}]     entrées ajoutées (CurseForge)
#    overrides_retirer   [chemin sous overrides/]
#    overrides_ajouter   {chemin sous overrides/: fichier du dépôt}
#    overrides_remplacer {chemin sous overrides/: fichier du dépôt}  (déjà présent)
#  Le zip de base n'est jamais modifié. Le zip exporté est ensuite passé à
#  migration/assembler.py, qui ajoute le script de migration (BMC-93).
#  Refuse : une entrée à retirer absente, un projet ajouté déjà présent, un
#  override à retirer ou à remplacer absent, ou à ajouter déjà présent.
# ============================================================
import html, json, os, re, sys, zipfile

def main(chg_chemin, base, sortie):
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chg = json.load(open(chg_chemin, encoding='utf-8'))
    if os.path.abspath(base) == os.path.abspath(sortie):
        raise SystemExit('le zip exporté doit être un nouveau fichier')
    with zipfile.ZipFile(base) as z:
        manifest = json.loads(z.read('manifest.json'))
        modlist = z.read('modlist.html').decode('utf-8-sig')
        noms = set(z.namelist())
        fichiers = manifest['files']
        presents = {f['projectID'] for f in fichiers}
        for r in chg.get('retirer', []):
            if r['projectID'] not in presents:
                raise SystemExit(f"à retirer mais absent du manifest : {r}")
        for a in chg.get('ajouter', []):
            if a['projectID'] in presents:
                raise SystemExit(f"à ajouter mais déjà présent : {a}")
        for p in chg.get('overrides_retirer', []):
            if 'overrides/' + p not in noms:
                raise SystemExit(f"override à retirer absent : {p}")
        for p in chg.get('overrides_ajouter', {}):
            if 'overrides/' + p in noms:
                raise SystemExit(f"override à ajouter déjà présent : {p}")
        remp = {'overrides/' + p: src for p, src in chg.get('overrides_remplacer', {}).items()}
        for p in remp:
            if p not in noms:
                raise SystemExit(f"override à remplacer absent : {p}")
        ret = {r['projectID'] for r in chg.get('retirer', [])}
        manifest['files'] = [f for f in fichiers if f['projectID'] not in ret] + \
            [{'projectID': a['projectID'], 'fileID': a['fileID'], 'required': True, 'isLocked': False} for a in chg.get('ajouter', [])]
        manifest['version'] = chg['version']
        manifest['name'] = chg['nom']
        lignes = modlist.split('\n')
        for r in chg.get('retirer', []):
            avant = len(lignes)
            lignes = [l for l in lignes if not re.search(r'>' + re.escape(html.escape(r['nom'], quote=False)) + r' \(by ', l)]
            if len(lignes) != avant - 1:
                raise SystemExit(f"modlist.html : ligne de « {r['nom']} » introuvable ou multiple")
        fin = lignes.index('</ul>') if '</ul>' in lignes else len(lignes)
        for a in chg.get('ajouter', []):
            lignes.insert(fin, f'<li><a href="{a["url"]}">{html.escape(a["nom"], quote=False)} (by {html.escape(a["auteur"], quote=False)})</a></li>')
            fin += 1
        ot = {'overrides/' + p for p in chg.get('overrides_retirer', [])}
        with zipfile.ZipFile(sortie, 'w', zipfile.ZIP_DEFLATED) as out:
            for info in z.infolist():
                if info.filename in ot:
                    continue
                if info.filename == 'manifest.json':
                    out.writestr(info, json.dumps(manifest, indent=2, ensure_ascii=False))
                elif info.filename == 'modlist.html':
                    out.writestr(info, '﻿' + '\n'.join(lignes))
                elif info.filename in remp:
                    out.writestr(info, open(os.path.join(racine, remp[info.filename]), 'rb').read())
                else:
                    out.writestr(info, z.read(info))
            for p, src in chg.get('overrides_ajouter', {}).items():
                info = zipfile.ZipInfo('overrides/' + p, date_time=(2026, 1, 1, 0, 0, 0))
                info.external_attr = (0o100644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                out.writestr(info, open(os.path.join(racine, src), 'rb').read())
    print(f"{sortie} : {chg['nom']}, {len(manifest['files'])} entrées de manifest "
          f"(−{len(ret)}, +{len(chg.get('ajouter', []))}), overrides −{len(ot)} +{len(chg.get('overrides_ajouter', {}))} ~{len(remp)}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('usage : construire.py <changements.json> <zip de base> <zip exporté>')
    main(*sys.argv[1:])
