#!/usr/bin/env python3
"""Aperçu lisible de tous les chapitres (quetes/apercu.md), pour la relecture."""
import tomllib, glob, os, re
ICI = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(ICI, '..', 'donnees')
out = ['# Aperçu des chapitres générés\n', 'Relecture humaine : titre, tâches, récompense, par chapitre. Produit depuis quetes/donnees/ par outils/apercu.py.\n']
for f in sorted(glob.glob(os.path.join(D, '**', '*.toml'), recursive=True)):
    if os.path.basename(f) in ('tables.toml', 'groupes.toml', 'livre.toml', 'exclusions.toml', 'retroactivite.toml') or '/notes/' in f or '/paliers/' in f: continue
    dd = tomllib.load(open(f, 'rb')); ch = dd['chapitre']
    out.append(f"\n## {re.sub('&.', '', ch['titre'])}  (`{ch['fichier']}`, {len(dd['quete'])} quêtes)\n")
    for q in dd['quete']:
        flags = ' *(optionnelle)*' if q.get('optionnel') else ''
        out.append(f"- **{re.sub('&.', '', q['titre'])}**{flags} — tâches : {', '.join(q['taches'])} — récompense : {', '.join(q['recompenses'])}" + (f" — après : {', '.join(q['deps'])}" if q.get('deps') and len(dd['quete']) < 60 else ''))
        if q.get('description'): out.append('  > ' + re.sub('&.', '', q['description'].strip()).replace('\n\n', '\n  > ').replace('\n', '\n  > '))
nch = sum(1 for l in out if l.startswith('\n## '))
nq = sum(int(m) for m in re.findall(r', (\d+) quêtes\)', '\n'.join(out)))
out.insert(2, f"Livre complet : {nch} chapitres, {format(nq, ',').replace(',', chr(0x202f))} quêtes.\n")
open(os.path.join(ICI, '..', 'apercu.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('apercu.md écrit')
