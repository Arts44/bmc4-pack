#!/usr/bin/env python3
"""Noms français séparés par genre (BMC-89, consolidation du 5 octobre 2026).

    python3 noms-fr.py <dossier mods> <dossier assets Minecraft> <index d'assets>

L'index des jars range dans une même table « fr » les noms d'objets, de
créatures et de biomes : quand un objet et une créature partagent un
identifiant (minecraft:chicken), le nom de l'objet (« Poulet cru »)
écrasait celui de la créature (« Poulet »). Cet outil relit les
fr_fr.json — celui du jeu de base (assets, index 5 de la 1.20.1) et ceux
des jars — et produit ../index/noms_fr.json :
  {"entite": {...}, "objet": {...}, "biome": {...}}
"""
import glob
import json
import os
import re
import sys
import zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
MOTIF = re.compile(r'^(item|block|entity|biome)\.([a-z0-9_.-]+)\.([a-z0-9_./-]+)$')
GENRE = {'item': 'objet', 'block': 'objet', 'entity': 'entite', 'biome': 'biome'}


def ajoute(out, d):
    for k, v in d.items():
        m = MOTIF.match(k)
        if m and isinstance(v, str):
            genre = GENRE[m.group(1)]
            ident = f'{m.group(2)}:{m.group(3)}'
            if genre == 'objet' and m.group(1) == 'block' and ident in out['objet']:
                continue   # le nom d'objet (item.) prime sur celui du bloc
            out[genre][ident] = v


def main(mods, assets, index_assets):
    out = {'entite': {}, 'objet': {}, 'biome': {}}
    idx = json.load(open(index_assets))
    h = idx['objects']['minecraft/lang/fr_fr.json']['hash']
    ajoute(out, json.load(open(os.path.join(assets, 'objects', h[:2], h), encoding='utf-8')))
    for j in sorted(glob.glob(os.path.join(mods, '*.jar'))):
        try:
            z = zipfile.ZipFile(j)
        except zipfile.BadZipFile:
            continue
        for n in z.namelist():
            if n.startswith('assets/') and n.endswith('/lang/fr_fr.json'):
                try:
                    ajoute(out, json.loads(z.read(n).decode('utf-8', 'replace')))
                except Exception:
                    pass
    json.dump(out, open(os.path.join(ICI, '..', 'index', 'noms_fr.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0, sort_keys=True)
    print({k: len(v) for k, v in out.items()})


if __name__ == '__main__':
    main(*sys.argv[1:4])
