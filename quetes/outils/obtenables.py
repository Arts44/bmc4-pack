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


def ingredients(d):
    """Ingrédients obligatoires d'une recette : une liste par emplacement,
    chaque liste donnant les alternatives (objet ou « #balise »)."""
    if not isinstance(d, dict):
        return []
    out = []

    def alt(x):
        if isinstance(x, list):
            r = []
            for y in x:
                r += alt(y)
            return r
        if isinstance(x, dict):
            if isinstance(x.get('item'), str):
                return [x['item']]
            if isinstance(x.get('tag'), str):
                return ['#' + x['tag']]
            if 'ingredient' in x:
                return alt(x['ingredient'])
        if isinstance(x, str):
            return [x] if ID.match(x) else []
        return []

    if isinstance(d.get('key'), dict):
        for v in d['key'].values():
            out.append(alt(v))
    for k in ('ingredients', 'ingredient', 'base', 'addition', 'template', 'input', 'inputs'):
        v = d.get(k)
        if isinstance(v, list) and k in ('ingredients', 'inputs'):
            out += [alt(x) for x in v]
        elif v is not None:
            out.append(alt(v))
    if not out and isinstance(d.get('recipe'), dict):     # forge:conditional et apparentés
        return ingredients(d['recipe'])
    if not out and isinstance(d.get('recipes'), list) and d['recipes']:
        return ingredients(d['recipes'][0].get('recipe', {}))
    return [x for x in out if x]


# Delightful (delightful:enabled) : clés à false dans /config/delightful-common.toml
# du serveur, lu le 5 octobre 2026. Toutes les autres valent true.
DELIGHTFUL_DESACTIVES = {'amethyst_knife', 'copper_knife', 'emerald_knife', 'lapis_lazuli_knife'}


def condition(c, ctx):
    """Une condition de recette Forge est-elle remplie dans ce pack ?
    True, False, ou None quand on ne sait pas la lire (condition propre à un
    mod, balise que l'index ne connaît pas : les balises forge: du jar Forge
    lui-même n'y sont pas). None ne fait jamais écarter une recette."""
    if not isinstance(c, dict):
        return None
    t = c.get('type', '')
    if t == 'forge:mod_loaded':
        return c.get('modid') in ctx['mods']
    if t == 'forge:item_exists':
        return c.get('item') in ctx['objets']
    if t == 'forge:tag_empty':
        m = ctx['tags'].get(c.get('tag'))
        return None if m is None else not m
    if t == 'forge:not':
        v = condition(c.get('value'), ctx)
        return None if v is None else not v
    if t in ('forge:and', 'forge:or'):
        vs = [condition(x, ctx) for x in c.get('values', [])]
        if t == 'forge:and':
            return False if False in vs else (None if None in vs else True)
        return True if True in vs else (None if None in vs else False)
    if t == 'forge:false':
        return False
    if t == 'forge:true':
        return True
    if t == 'delightful:enabled':
        return c.get('value') not in DELIGHTFUL_DESACTIVES
    return None


def passe(conds, ctx):
    return all(condition(c, ctx) is not False for c in conds or [])


def active(d, ctx):
    """La recette telle que le serveur la charge, ou None si ses conditions
    l'écartent (« conditions » Forge, ou forge:conditional : la première
    variante dont les conditions passent)."""
    if not isinstance(d, dict):
        return d
    if not passe(d.get('conditions'), ctx):
        return None
    if d.get('type') == 'forge:conditional' and isinstance(d.get('recipes'), list):
        for v in d['recipes']:
            if isinstance(v, dict) and passe(v.get('conditions'), ctx):
                return v.get('recipe')
        return None
    return d


def contexte():
    ctx = {'mods': {'minecraft', 'forge'}, 'objets': set(), 'tags': {}}
    for f in ('index_vanilla.json', 'index.json'):
        try:
            ix = json.load(open(os.path.join(ICI, '..', 'index', f), encoding='utf-8'))
        except OSError:
            continue
        ctx['mods'] |= set(ix.get('mods', {}))
        ctx['objets'] |= set(ix.get('items', {}))
        # l'index ne garde que le premier modId d'un jar : les espaces de noms
        # des objets complètent la liste des mods chargés
        ctx['mods'] |= {i.split(':')[0] for i in ix.get('items', {})}
        for k, v in ix.get('tag_membres', {}).items():
            ctx['tags'][k] = list(ctx['tags'].get(k, [])) + list(v)
    return ctx


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
            if n.startswith('data/') and n.endswith('.json') and ('/recipes/' in n or '/loot_tables/' in n or '/loot_modifiers/' in n or '/worldgen/configured_feature/' in n):
                if n.endswith('/global_loot_modifiers.json'):
                    n = f'{n}@{z.filename}'   # chaque jar a le sien : on les cumule
                fichiers[n] = (z, n.split('@')[0])   # le dernier (datapack) l'emporte
    rec, but, monde = set(), set(), set()
    ctx = contexte()
    ecartees = 0
    actifs, modifs = set(), {}   # loot modifiers déclarés / leur contenu
    graphe = {}   # résultat -> [[ingrédient obligatoire, sous forme de liste d'alternatives], ...]
    for n, (z, nom) in fichiers.items():
        try:
            d = json_tolerant(z.read(nom))
        except Exception:
            continue
        if '/recipes/' in n and '/advancements/' not in n:
            if isinstance(d, dict) and d.get('type') in (None, '') and not d:
                continue
            d = active(d, ctx)
            if d is None:
                ecartees += 1
                continue
            ici = set()
            resultats(d, ici)
            if isinstance(d, dict) and isinstance(d.get('result'), dict) and isinstance(d['result'].get('item'), str):
                ici.add(d['result']['item'])
            rec |= ici
            for r in ici:
                graphe.setdefault(r, []).append(ingredients(d))
            # Blue Skies : {"type": "blue_skies:bluebright_sword"} — un type de
            # recette au nom de l'objet, le contenu de la recette est dans le code.
            if isinstance(d, dict) and set(d) == {'type'} and isinstance(d['type'], str):
                rec.add(d['type'])
        elif '/loot_tables/' in n:
            butin(d, but)
        elif '/loot_modifiers/' in n:
            if '/global_loot_modifiers.json' in n:
                for e in (d.get('entries', []) if isinstance(d, dict) else []):
                    actifs.add(e)
            else:
                p = n.split('/')
                modifs[f"{p[1]}:{'/'.join(p[3:])[:-5]}"] = d
        elif '/worldgen/configured_feature/' in n:
            for m in re.findall(r'"([a-z0-9_]+:[a-z0-9_/]+)"', json.dumps(d)):
                monde.add(m)
    # Loot modifiers (Forge) : seuls ceux qu'un global_loot_modifiers.json
    # déclare sont chargés. Leurs objets ajoutés (« item », « name »…) comptent
    # comme butin ; ceux qui suppriment (« remove ») ou remplacent n'en ajoutent
    # pas moins leur objet de remplacement, lu de la même façon.
    for k in actifs:
        d = modifs.get(k)
        if isinstance(d, dict) and passe(d.get('conditions'), ctx):
            for cle in ('item', 'result', 'addition', 'replacement', 'added_item'):
                v = d.get(cle)
                if isinstance(v, str) and ID.match(v):
                    but.add(v)
                elif isinstance(v, dict):
                    tous(v, but)
            butin(d, but)
    out = {'recette': sorted(rec), 'butin': sorted(but), 'monde': sorted(monde), 'graphe': graphe}
    json.dump(out, open(os.path.join(ICI, '..', 'index', 'obtenables.json'), 'w', encoding='utf-8'), indent=0)
    print({k: len(v) for k, v in out.items()}, 'recettes écartées par leurs conditions :', ecartees)


if __name__ == '__main__':
    main(*sys.argv[1:4])
