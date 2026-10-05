#!/usr/bin/env python3
"""Ce qu'un joueur peut obtenir (BMC-89, garde-fou des catalogues de l'Encyclopédie).

    python3 obtenables.py <dossier mods> <jar vanilla> <dossier datapacks paxi>

Lu dans les jars puis les datapacks Paxi (même ordre que le serveur) :
  · recettes : tout objet cité comme résultat (« result », « output »,
    « results »…), quel que soit le type de recette ;
  · tables de butin : tout objet d'une entrée « minecraft:item » (coffres,
    créatures, blocs, pêche, archéologie, troc…) ;
  · génération : tout bloc cité par un configured_feature (arbres,
    minerais, végétation).
Une recette ou une table vidée par un datapack (même chemin) compte comme
retirée. Produit ../index/obtenables.json :
  {"recette": [...], "butin": [...], "monde": [...]}
Limite connue : les recettes créées par le code au lancement (graines de
Mystical Agriculture, par exemple) n'apparaissent pas ; le chapitre qui
en dépend le traite à part.
"""
import glob
import json
import os
import re
import sys
import zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from generation import json_tolerant, sources  # noqa: E402

ID = re.compile(r'^[a-z0-9_.-]+:[a-z0-9_./-]+$')


def resultats(d, out):
    """Objets produits par une recette, quelle que soit sa forme."""
    if isinstance(d, dict):
        for k, v in d.items():
            if k in ('result', 'output', 'results', 'outputs', 'mainOutput', 'secondaryOutputs', 'byproducts'):
                tous(v, out)
            elif isinstance(v, (dict, list)) and k not in ('ingredients', 'ingredient', 'key', 'input', 'inputs', 'base', 'addition', 'template', 'container', 'tool'):
                resultats(v, out)
    elif isinstance(d, list):
        for x in d:
            resultats(x, out)


def tous(v, out):
    if isinstance(v, str) and ID.match(v):
        out.add(v)
    elif isinstance(v, dict):
        for k in ('item', 'id', 'name'):
            if isinstance(v.get(k), str) and ID.match(v[k]):
                out.add(v[k])
        for x in v.values():
            if isinstance(x, (dict, list)):
                tous(x, out)
    elif isinstance(v, list):
        for x in v:
            tous(x, out)


def butin(d, out):
    if isinstance(d, dict):
        if d.get('type') in ('minecraft:item', 'item') and isinstance(d.get('name'), str):
            out.add(d['name'])
        for v in d.values():
            butin(v, out)
    elif isinstance(d, list):
        for x in d:
            butin(x, out)


def main(mods, vanilla, paxi):
    fichiers = {}
    for z in sources(mods, vanilla, paxi):
        for n in z.namelist():
            if n.startswith('data/') and n.endswith('.json') and ('/recipes/' in n or '/loot_tables/' in n or '/worldgen/configured_feature/' in n):
                fichiers[n] = (z, n)   # le dernier (datapack) l'emporte
    rec, but, monde = set(), set(), set()
    for n, (z, nom) in fichiers.items():
        try:
            d = json_tolerant(z.read(nom))
        except Exception:
            continue
        if '/recipes/' in n:
            if isinstance(d, dict) and d.get('type') in (None, '') and not d:
                continue
            resultats(d, rec)
        elif '/loot_tables/' in n:
            butin(d, but)
        else:
            for m in re.findall(r'"([a-z0-9_]+:[a-z0-9_/]+)"', json.dumps(d)):
                monde.add(m)
    out = {'recette': sorted(rec), 'butin': sorted(but), 'monde': sorted(monde)}
    json.dump(out, open(os.path.join(ICI, '..', 'index', 'obtenables.json'), 'w', encoding='utf-8'), indent=0)
    print({k: len(v) for k, v in out.items()})


if __name__ == '__main__':
    main(*sys.argv[1:4])
