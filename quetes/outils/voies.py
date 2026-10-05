#!/usr/bin/env python3
"""Voies d'apparition lues dans les jars (BMC-89, Encyclopédie, 5 octobre 2026).

    python3 voies.py <dossier mods> <jar vanilla>

Trois sources, toutes des données du pack, rien de deviné :
  · biome_modifier Forge (data/*/forge/biome_modifier/*.json, type
    forge:add_spawns) : l'entité apparaît dans ces biomes ou balises ;
  · spawn_overrides des structures (data/*/worldgen/structure/*.json) :
    l'entité apparaît dans l'emprise de la structure ;
  · structures NBT (data/*/structures/**/*.nbt) : générateur de monstres
    (SpawnData / SpawnPotentials) ou entité posée dans la structure.
Produit ../index/voies.json :
  {entité: {"biomes": [...], "structures_spawn": [...], "nbt": [fichier, ...]}}
Les fichiers NBT sont donnés par leur chemin dans le jar
(<mod>:<chemin sans extension>), pour que la fiche cite sa pièce.
"""
import glob
import gzip
import io
import json
import os
import struct
import sys
import zipfile

ICI = os.path.dirname(os.path.abspath(__file__))


def lire_nbt(data):
    pos = [0]

    def rd(f):
        s = struct.calcsize(f)
        v = struct.unpack('>' + f, data[pos[0]:pos[0] + s])
        pos[0] += s
        return v[0]

    def rstr():
        n = rd('H')
        s = data[pos[0]:pos[0] + n].decode('utf-8', 'replace')
        pos[0] += n
        return s

    def charge(t):
        if t == 1: return rd('b')
        if t == 2: return rd('h')
        if t == 3: return rd('i')
        if t == 4: return rd('q')
        if t == 5: return rd('f')
        if t == 6: return rd('d')
        if t == 7:
            n = rd('i'); pos[0] += n; return None
        if t == 8: return rstr()
        if t == 9:
            et = rd('b'); n = rd('i'); return [charge(et) for _ in range(n)]
        if t == 10:
            d = {}
            while True:
                tt = rd('b')
                if tt == 0:
                    return d
                nom = rstr(); d[nom] = charge(tt)
        if t == 11:
            n = rd('i'); pos[0] += 4 * n; return None
        if t == 12:
            n = rd('i'); pos[0] += 8 * n; return None
        raise ValueError(t)

    t = rd('b'); rstr()
    return charge(t)


def entites_nbt(racine):
    """Entités d'un NBT de structure : générateurs et entités posées."""
    trouve = set()

    def marche(o, dans_entite=False):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'id' and isinstance(v, str) and ':' in v and dans_entite:
                    trouve.add(v)
                marche(v, dans_entite or k in ('SpawnData', 'SpawnPotentials', 'entity', 'nbt', 'entities', 'Passengers'))
        elif isinstance(o, list):
            for x in o:
                marche(x, dans_entite)

    if isinstance(racine, dict):
        marche(racine.get('entities'), True)
        for b in racine.get('blocks') or []:
            if isinstance(b, dict) and isinstance(b.get('nbt'), dict):
                marche(b['nbt'], False)
    return trouve


def main(mods, vanilla):
    voies = {}

    def ajoute(ent, cle, val):
        e = voies.setdefault(ent, {'biomes': [], 'structures_spawn': [], 'nbt': []})
        if val not in e[cle]:
            e[cle].append(val)

    jars = sorted(glob.glob(os.path.join(mods, '*.jar'))) + [vanilla]
    for jar in jars:
        try:
            z = zipfile.ZipFile(jar)
        except zipfile.BadZipFile:
            continue
        for n in z.namelist():
            if not n.startswith('data/'):
                continue
            parts = n.split('/')
            mod = parts[1]
            try:
                if '/forge/biome_modifier/' in n and n.endswith('.json'):
                    d = json.loads(z.read(n))
                    if d.get('type') in ('forge:add_spawns',):
                        bs = d.get('biomes')
                        bs = [bs] if isinstance(bs, str) else (bs or [])
                        sp = d.get('spawners')
                        sp = [sp] if isinstance(sp, dict) else (sp or [])
                        for s in sp:
                            for b in bs:
                                ajoute(s['type'], 'biomes', b)
                elif '/worldgen/structure/' in n and n.endswith('.json'):
                    d = json.loads(z.read(n))
                    st = f"{mod}:{'/'.join(parts[4:])[:-5]}"
                    for cat in (d.get('spawn_overrides') or {}).values():
                        for s in cat.get('spawns', []):
                            ajoute(s['type'], 'structures_spawn', st)
                elif '/structures/' in n and n.endswith('.nbt'):
                    raw = z.read(n)
                    try:
                        raw = gzip.decompress(raw)
                    except OSError:
                        pass
                    for ent in entites_nbt(lire_nbt(raw)):
                        ajoute(ent, 'nbt', f"{mod}:{'/'.join(parts[3:])[:-4]}")
            except Exception:
                continue
    sortie = os.path.join(ICI, '..', 'index', 'voies.json')
    json.dump(voies, open(sortie, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    print(f"{len(voies)} entités avec au moins une voie -> {sortie}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
