#!/usr/bin/env python3
"""Ce que le serveur génère vraiment (BMC-89, garde-fou de l'Encyclopédie).

    python3 generation.py <dossier mods> <jar vanilla> <dossier datapacks paxi>

Reconstitue les données de génération comme le serveur les charge : les
jars d'abord, puis les datapacks Paxi par-dessus (même chemin = le
datapack l'emporte ; une balise avec "replace": true remplace, sinon elle
s'ajoute). Les 34 datapacks Paxi du pack local ont été comparés à ceux du
serveur le 5 octobre 2026 (mêmes noms, mêmes tailles).

Biomes générés (mesurés sur les configs du serveur, 5 octobre 2026) :
  · Overworld : biomes vanilla de surface et de grottes, Biomes O' Plenty
    (biome_toggles.json : tous à true), Galosphere, YUNG's Cave Biomes,
    Climate Rivers, le Glimmering Weald de Quark (« Glimmering Weald » =
    true, région TerraBlender), Vanilla Backport (pale garden, sulfur caves) ;
  · Nether : vanilla, Biomes O' Plenty (nether), Better Nether (bclib
    biomes.json : rien d'exclu), Gardens of the Dead, Jaden's Nether
    Expansion, Soulful Nether ;
  · End : vanilla et Better End (bclib : rien d'exclu) ;
  · dimensions : la liste du biome_source de leur JSON de dimension
    (Twilight Forest, Otherside), la balise blue_skies:everbright /
    everdawn, et pour l'Aether les régions AeroBlender de Deep Aether
    (DARegion, DARareRegion) et d'Aether Redux (ReduxRegion), qui
    reprennent les quatre biomes de base malgré « Aether Region Weight » = 0.
Une structure est générée si un structure_set la place ET si sa liste de
biomes, balises résolues, touche au moins un biome généré.

Produit ../index/generation.json : {"biomes": {biome: monde}, "structures":
{structure: {"generee": bool, "raison": str, "biomes": [...]}}}
"""
import glob
import json
import os
import re
import sys
import zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
TECHNIQUES = {'minecraft:the_void', 'minecraft:custom'}


def json_tolerant(octets):
    """Comme le lecteur de Minecraft (Gson tolérant) : commentaires // et
    /* */ acceptés hors des chaînes, virgules finales tolérées."""
    t = octets.decode('utf-8', 'replace')
    out, i, n, chaine = [], 0, len(t), False
    while i < n:
        c = t[i]
        if chaine:
            out.append(c)
            if c == '\\' and i + 1 < n:
                out.append(t[i + 1]); i += 2; continue
            if c == '"':
                chaine = False
            i += 1; continue
        if c == '"':
            chaine = True; out.append(c); i += 1; continue
        if t.startswith('//', i):
            j = t.find('\n', i); i = n if j < 0 else j; continue
        if t.startswith('/*', i):
            j = t.find('*/', i + 2); i = n if j < 0 else j + 2; continue
        out.append(c); i += 1
    return json.loads(re.sub(r',(\s*[}\]])', r'\1', ''.join(out)))


def ns(x):
    """« beach » vaut « minecraft:beach » ; « #foo » vaut « #minecraft:foo »."""
    if x.startswith('#'):
        return '#' + ns(x[1:])
    return x if ':' in x else 'minecraft:' + x


def sources(mods, vanilla, paxi):
    """Fichiers data/ dans l'ordre de chargement : vanilla, mods, Paxi."""
    zs = [zipfile.ZipFile(vanilla)]
    for j in sorted(glob.glob(os.path.join(mods, '*.jar'))):
        try:
            zs.append(zipfile.ZipFile(j))
        except zipfile.BadZipFile:
            pass
    for d in sorted(glob.glob(os.path.join(paxi, '*.zip'))):
        zs.append(zipfile.ZipFile(d))
    return zs


def charger(zs):
    fichiers = {}    # chemin -> contenu (le dernier gagne)
    tags = {}        # tag de biome -> liste (fusion / replace)
    for z in zs:
        for n in z.namelist():
            if not n.startswith('data/') or not n.endswith('.json'):
                continue
            m = re.match(r'data/([^/]+)/tags/worldgen/biome/(.+)\.json$', n)
            try:
                d = json_tolerant(z.read(n))
            except Exception:
                continue
            if m:
                cle = f"{m.group(1)}:{m.group(2)}"
                vals = [ns(v['id'] if isinstance(v, dict) else v) for v in d.get('values', [])]
                if d.get('replace') or cle not in tags:
                    tags[cle] = list(vals)
                else:
                    tags[cle] += vals
            elif '/worldgen/structure/' in n or '/worldgen/structure_set/' in n or '/dimension/' in n:
                fichiers[n] = d
    return fichiers, tags


def resoudre(entree, tags, vus=None):
    vus = vus or set()
    if isinstance(entree, list):
        out = set()
        for e in entree:
            out |= resoudre(e, tags, vus)
        return out
    if isinstance(entree, dict):
        return {'?' + json.dumps(entree, sort_keys=True)[:80]}
    entree = ns(entree)
    if entree.startswith('#'):
        t = entree[1:]
        if t in vus:
            return set()
        vus.add(t)
        return resoudre(tags.get(t, []), tags, vus)
    return {entree}


def biomes_generes(index, fichiers, tags):
    tous = set(index['biomes'])
    gen = {}
    for b in tous:
        if b in TECHNIQUES:
            continue
        mod = b.split(':')[0]
        if mod in ('terrablender', 'blueprint'):
            continue
        gen[b] = None
    # dimensions à source listée
    for n, d in fichiers.items():
        m = re.match(r'data/([^/]+)/dimension/(.+)\.json$', n)
        if m and m.group(1) in ('twilightforest', 'deeperdarker'):
            for b in re.findall(r'"([a-z0-9_]+:[a-z0-9_/]+)"', json.dumps(d)):
                if b in gen:
                    gen[b] = f"{m.group(1)}:{m.group(2)}"
    for b in resoudre('#blue_skies:everbright', tags):
        if b in gen:
            gen[b] = 'blue_skies:everbright'
    for b in resoudre('#blue_skies:everdawn', tags):
        if b in gen:
            gen[b] = 'blue_skies:everdawn'
    for b in list(gen):
        if gen[b]:
            continue
        mod = b.split(':')[0]
        if mod in ('aether', 'deep_aether', 'aether_redux', 'lost_aether_content'):
            gen[b] = 'aether:the_aether'
        elif mod in ('betterend',):
            gen[b] = 'minecraft:the_end'
        elif mod in ('betternether', 'netherexp', 'soulfulnether', 'gardens_of_the_dead', 'bygonenether'):
            gen[b] = 'minecraft:the_nether'
        elif b in resoudre('#minecraft:is_nether', tags):
            gen[b] = 'minecraft:the_nether'
        elif b in resoudre('#minecraft:is_end', tags) or b in ('minecraft:the_end', 'minecraft:end_highlands', 'minecraft:end_midlands', 'minecraft:small_end_islands', 'minecraft:end_barrens'):
            gen[b] = 'minecraft:the_end'
        elif mod in ('twilightforest', 'blue_skies', 'deeperdarker'):
            gen[b] = None   # absent de la source de sa dimension : pas généré
        else:
            gen[b] = 'minecraft:overworld'
    return {b: d for b, d in gen.items() if d}


def main(mods, vanilla, paxi):
    index = {}
    for f in ('index.json', 'index_vanilla.json'):
        d = json.load(open(os.path.join(ICI, '..', 'index', f), encoding='utf-8'))
        for k in ('biomes', 'structures'):
            index.setdefault(k, {}).update(d[k])
    fichiers, tags = charger(sources(mods, vanilla, paxi))
    gen = biomes_generes(index, fichiers, tags)
    placees = {}
    for n, d in fichiers.items():
        m = re.match(r'data/([^/]+)/worldgen/structure_set/(.+)\.json$', n)
        if m:
            for s in d.get('structures', []):
                placees.setdefault(ns(s['structure'] if isinstance(s, dict) else s), []).append(f"{m.group(1)}:{m.group(2)}")
    structures = {}
    for st in index['structures']:
        mod, chemin = st.split(':', 1)
        d = fichiers.get(f"data/{mod}/worldgen/structure/{chemin}.json")
        if st not in placees:
            structures[st] = {'generee': False, 'raison': 'aucun structure_set ne la place'}
            continue
        if d is None:
            structures[st] = {'generee': True, 'raison': 'placée (JSON de structure non lu, biomes non vérifiés)', 'biomes': []}
            continue
        bs = resoudre(d.get('biomes', []), tags)
        if any(b.startswith('?') for b in bs):
            structures[st] = {'generee': True, 'raison': 'placée ; biomes décrits par un objet non lu : ' + next(b for b in bs if b.startswith('?'))[1:], 'biomes': []}
            continue
        ok = sorted(b for b in bs if b in gen)
        if not ok:
            structures[st] = {'generee': False, 'raison': 'aucun biome généré dans sa liste (balise vide ou biomes absents)'}
        else:
            structures[st] = {'generee': True, 'raison': '', 'biomes': ok}
    out = {'biomes': gen, 'structures': structures}
    json.dump(out, open(os.path.join(ICI, '..', 'index', 'generation.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0, sort_keys=True)
    n = sum(1 for v in structures.values() if v['generee'])
    print(f"{len(gen)} biomes générés ; {n} structures générées sur {len(structures)}")


if __name__ == '__main__':
    main(*sys.argv[1:4])
