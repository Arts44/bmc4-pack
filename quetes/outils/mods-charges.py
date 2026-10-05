#!/usr/bin/env python3
"""Mods réellement chargés (BMC-89, 5 octobre 2026).

    python3 mods-charges.py <dossier mods>   → ../index/mods_charges.json

L'index (indexer-jars.py) ne garde que le premier modId de chaque jar, et
contient des objets de mods absents (fichiers de compatibilité embarqués par
d'autres mods : umbral_skies, alexscaves…). Ici, chaque [[mods]] de chaque
META-INF/mods.toml compte, et l'id des mods Fabric chargés par Connector : c'est la liste des espaces de noms enregistrés.
"""
import glob
import json
import os
import re
import sys
import zipfile

ICI = os.path.dirname(os.path.abspath(__file__))


def ids(z):
    """modId des blocs [[mods]] (pas ceux des [[dependencies.*]]), ou id
    d'un fabric.mod.json (mods Fabric chargés par Sinytra Connector)."""
    out = set()
    if 'META-INF/mods.toml' in z.namelist():
        t = z.read('META-INF/mods.toml').decode('utf-8', 'replace')
        for bloc in re.split(r'^\s*\[\[', t, flags=re.M)[1:]:
            if bloc.startswith('mods]]'):
                out |= set(re.findall(r'modId\s*=\s*"([^"]+)"', bloc))
    elif 'fabric.mod.json' in z.namelist():
        try:
            out.add(json.loads(z.read('fabric.mod.json'), strict=False)['id'])
        except (ValueError, KeyError):
            pass
    return out


def main(dossier):
    mods = {'minecraft', 'forge'}
    for j in sorted(glob.glob(os.path.join(dossier, '*.jar'))):
        try:
            z = zipfile.ZipFile(j)
        except zipfile.BadZipFile:
            continue
        mi = ids(z)
        mods |= mi
        # Espaces de noms que le jar fait vivre : sa langue (assets/<ns>/lang)
        # ou sa génération (data/<ns>/worldgen, structures). Moog's
        # (moogs_structures → mvs, mns, mes, mmv), Towns and Towers
        # (t_and_t → towns_and_towers), Blossom (joshie). Les données de
        # compatibilité qu'un jar embarque pour un mod absent (recettes,
        # balises) n'en font pas partie.
        for n in z.namelist():
            m = re.match(r'(?:assets/([^/]+)/lang/|data/([^/]+)/(?:worldgen|structures?)/)', n)
            if m:
                mods.add(m.group(1) or m.group(2))
        # jar-in-jar : les mods embarqués (META-INF/jarjar) se chargent aussi
        for n in z.namelist():
            if n.startswith('META-INF/jarjar/') and n.endswith('.jar'):
                try:
                    mods |= ids(zipfile.ZipFile(z.open(n)))
                except Exception:
                    pass
    json.dump(sorted(mods), open(os.path.join(ICI, '..', 'index', 'mods_charges.json'), 'w'), indent=0)
    print(len(mods), 'mods chargés')


if __name__ == '__main__':
    main(sys.argv[1])
