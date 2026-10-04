#!/usr/bin/env python3
"""Ce que les données disent des créatures (BMC-89, décision 2) :
  · butin : data/<mod>/loot_tables/entities/<nom>.json dans les jars ;
  · biomes d'Alex's Mobs : config/alexsmobs/<nom>_spawns.json de l'instance
    (format BIOME_TAG / REGISTRY_NAME, avec négation) ;
  · biomes de Mowzie's Mobs : biome_tags lus dans mowziesmobs-common.toml
    du serveur le 5 octobre 2026, recopiés ici.
Produit quetes/index/apparitions.json."""
import glob, json, os, sys, zipfile, re
ICI = os.path.dirname(os.path.abspath(__file__))
mods = sys.argv[1]; vanilla = sys.argv[2]; cfg = sys.argv[3]
out = {'butin': {}, 'biomes_config': {}}

def items_de(table):
    found = []
    def walk(o):
        if isinstance(o, dict):
            if o.get('type') in ('minecraft:item', 'item') and 'name' in o: found.append(o['name'])
            if o.get('type') == 'minecraft:loot_table' and 'name' in o: found.append('#' + o['name'])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(table); return list(dict.fromkeys(found))

for jar in sorted(glob.glob(os.path.join(mods, '*.jar')) + [vanilla]):
    try: z = zipfile.ZipFile(jar)
    except Exception: continue
    for n in z.namelist():
        m = re.match(r'^data/([a-z0-9_.-]+)/loot_tables/entities/([a-z0-9_./-]+)\.json$', n)
        if m:
            try: t = json.loads(z.read(n).decode('utf-8', 'replace'))
            except Exception: continue
            out['butin'][f'{m.group(1)}:{m.group(2)}'] = items_de(t)
for f in glob.glob(os.path.join(cfg, 'alexsmobs', '*_spawns.json')):
    nom = os.path.basename(f)[:-len('_spawns.json')]
    try: d = json.load(open(f))
    except Exception: continue
    regles = []
    for groupe in d.get('biomes', []):
        regles.append([('!' if c.get('negate') else '') + ('#' if c.get('type') == 'BIOME_TAG' else '') + c.get('value', '') for c in groupe])
    out['biomes_config'][f'alexsmobs:{nom}'] = regles
# Mowzie's Mobs, mowziesmobs-common.toml du serveur, 5 octobre 2026
MOWZIE = {'frostmaw': ["forge:is_snowy,!minecraft:is_ocean,!minecraft:is_river,!minecraft:is_beach,!minecraft:is_forest,!minecraft:is_taiga"],
          'umvuthi': ["minecraft:is_savanna"], 'wroughtnaut': ["!minecraft:is_ocean"], 'sculptor': ["forge:is_peak"],
          'grottol': ["!forge:is_mushroom"], 'lantern': ["minecraft:is_forest,mowziesmobs:is_magical,!forge:is_snowy"],
          'umvuthana': ["minecraft:is_savanna"], 'naga': [], 'foliaath': ["minecraft:is_jungle"], 'bluff': [], 'elokosa': ["minecraft:is_jungle"]}
for k, v in MOWZIE.items():
    out['biomes_config'][f'mowziesmobs:{k}'] = [[('!#' + x[1:]) if x.startswith('!') else ('#' + x) for x in e.split(',')] for e in v]
json.dump(out, open(os.path.join(ICI, '..', 'index', 'apparitions.json'), 'w'), ensure_ascii=False)
print('butin', len(out['butin']), 'biomes_config', len(out['biomes_config']))
