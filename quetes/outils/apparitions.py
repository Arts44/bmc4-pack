#!/usr/bin/env python3
"""Ce que les données disent des créatures (BMC-89, décision 2) :
  · butin : data/<mod>/loot_tables/entities/<nom>.json dans les jars ;
  · biomes d'Alex's Mobs : config/alexsmobs/<nom>_spawns.json et
    config/alexsmobs/<nom>.json (farseer, murmur, skreecher, underminer)
    de l'instance — identiques à ceux du serveur, relus le 5 octobre 2026 ;
    leafcutter_anthill_spawns.json vaut pour la fourmi (la fourmilière) ;
  · biomes de Mowzie's Mobs : biome_tags ET biome_whitelist de
    mowziesmobs-common.toml du serveur (5 octobre 2026), recopiés ici,
    rattachés à l'entité que SpawnHandler.SPAWN_CONFIGS leur associe ;
  · biomes de Friends & Foes : balises has_<créature> du jar
    (data/friendsandfoes/tags/worldgen/biome/), toutes activées dans
    friendsandfoes.json du serveur (enable*Spawn = true) ;
  · biomes de Quark : mobs.*.spawn_config de quark-common.toml du serveur ;
  · Vanilla Backport : apparitions ajoutées par le code (classes
    ChaosCubedFeatureManager, ArmoredPawsFeatureManager, SpringToLife),
    balises du jar, options toutes à true dans vanillabackport-common.toml
    du serveur.
Produit quetes/index/apparitions.json : {'butin': {...}, 'biomes_config':
{entité: [[condition, ...], ...]}} — une condition est un biome, « #balise »,
ou l'un des deux précédé de « ! » (négation) ; une règle = toutes ses
conditions à la fois ; plusieurs règles = l'une ou l'autre."""
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

jars = sorted(glob.glob(os.path.join(mods, '*.jar'))) + [vanilla]
for jar in jars:
    try: z = zipfile.ZipFile(jar)
    except Exception: continue
    for n in z.namelist():
        m = re.match(r'^data/([a-z0-9_.-]+)/loot_tables/entities/([a-z0-9_./-]+)\.json$', n)
        if m:
            try: t = json.loads(z.read(n).decode('utf-8', 'replace'))
            except Exception: continue
            out['butin'][f'{m.group(1)}:{m.group(2)}'] = items_de(t)

# ---- Alex's Mobs : <nom>_spawns.json et <nom>.json (même format)
def regles_alex(d):
    regles = []
    for groupe in d.get('biomes', []):
        regles.append([('!' if c.get('negate') else '') + ('#' if c.get('type') == 'BIOME_TAG' else '') + c.get('value', '') for c in groupe])
    return regles
for f in glob.glob(os.path.join(cfg, 'alexsmobs', '*.json')):
    base = os.path.basename(f)[:-5]
    nom = base[:-len('_spawns')] if base.endswith('_spawns') else base
    if nom == 'leafcutter_anthill':
        nom = 'leafcutter_ant'
    try: d = json.load(open(f))
    except Exception: continue
    if 'biomes' not in d:
        continue
    out['biomes_config'][f'alexsmobs:{nom}'] = regles_alex(d)

# ---- Mowzie's Mobs, mowziesmobs-common.toml du serveur, 5 octobre 2026.
# (biome_tags, biome_whitelist) ; clé = entité réellement concernée
# (SpawnHandler.SPAWN_CONFIGS : umvuthana → umvuthana_raptor, Elokosa →
# elokosa_howler). Les quatre boss sont des structures ; leur biome_config
# borne le placement de la structure (commentaire du fichier, ligne 702).
MOWZIE = {
    'mowziesmobs:frostmaw': (["forge:is_snowy,!minecraft:is_ocean,!minecraft:is_river,!minecraft:is_beach,!minecraft:is_forest,!minecraft:is_taiga"], []),
    'mowziesmobs:umvuthi': (["minecraft:is_savanna"], []),
    'mowziesmobs:ferrous_wroughtnaut': (["!minecraft:is_ocean"], []),
    'mowziesmobs:sculptor': (["forge:is_peak"], []),
    'mowziesmobs:grottol': (["!forge:is_mushroom"], []),
    'mowziesmobs:lantern': (["minecraft:is_forest,mowziesmobs:is_magical,!forge:is_snowy"], []),
    'mowziesmobs:umvuthana_raptor': (["minecraft:is_savanna"], []),
    'mowziesmobs:naga': ([], ["minecraft:stony_shore"]),
    'mowziesmobs:foliaath': (["minecraft:is_jungle"], []),
    'mowziesmobs:bluff': ([], []),
    'mowziesmobs:elokosa_howler': (["minecraft:is_jungle"], []),
}
for k, (tags, blancs) in MOWZIE.items():
    regles = [[('!#' + x[1:]) if x.startswith('!') else ('#' + x) for x in e.split(',')] for e in tags]
    regles += [[b] for b in blancs]
    out['biomes_config'][k] = regles

# ---- Friends & Foes : balises has_<créature> du jar (résolution d'un niveau
# de balise interne), toutes les apparitions activées sur le serveur.
def valeurs_tag(z, chemin):
    try: d = json.loads(z.read(chemin))
    except Exception: return []
    vals = []
    for v in d.get('values', []):
        ident = v['id'] if isinstance(v, dict) else v
        if ident.startswith('#friendsandfoes:'):
            vals += valeurs_tag(z, 'data/friendsandfoes/tags/worldgen/biome/' + ident.split(':', 1)[1] + '.json')
        else:
            vals.append(ident)
    return vals
for jar in jars:
    if 'friendsandfoes' not in os.path.basename(jar): continue
    z = zipfile.ZipFile(jar)
    FF = {'friendsandfoes:crab': ['has_crab'], 'friendsandfoes:glare': ['has_glare'], 'friendsandfoes:rascal': ['has_rascal'],
          'friendsandfoes:moobloom': ['has_moobloom/any'],
          'friendsandfoes:mauler': ['has_desert_mauler', 'has_badlands_mauler', 'has_savanna_mauler']}
    for ent, tags in FF.items():
        regles = []
        for t in tags:
            for v in valeurs_tag(z, f'data/friendsandfoes/tags/worldgen/biome/{t}.json'):
                if v.startswith('#c:'):
                    continue  # balises Fabric « c: », facultatives, sans effet ici
                regles.append([v])
        out['biomes_config'][ent] = regles

# ---- Quark, quark-common.toml du serveur ([mobs], 5 octobre 2026)
out['biomes_config']['quark:crab'] = [['#minecraft:is_beach']]
out['biomes_config']['quark:shiba'] = [['#minecraft:is_mountain']]
out['biomes_config']['quark:toretoise'] = [['!#forge:is_void', '!#minecraft:is_nether', '!#minecraft:is_end']]
out['biomes_config']['quark:stoneling'] = [['!#forge:is_void', '!#minecraft:is_nether', '!#minecraft:is_end']]
out['biomes_config']['quark:foxhound'] = [['minecraft:nether_wastes'], ['minecraft:basalt_deltas'], ['minecraft:soul_sand_valley']]
out['biomes_config']['quark:wraith'] = [['minecraft:soul_sand_valley']]

# ---- Vanilla Backport (code + balises du jar, config serveur à true)
out['biomes_config']['minecraft:sulfur_cube'] = [['minecraft:sulfur_caves']]           # ChaosCubedFeatureManager, has_sulfur_cubes
out['biomes_config']['minecraft:armadillo'] = [['#minecraft:is_savanna'], ['#minecraft:is_badlands']]  # ArmoredPawsFeatureManager, spawns_armadillos*
out['biomes_config']['minecraft:camel'] = [['#forge:is_desert']]                       # SpringToLife, spawns_camels, camel_spawns

json.dump(out, open(os.path.join(ICI, '..', 'index', 'apparitions.json'), 'w'), ensure_ascii=False)
print('butin', len(out['butin']), 'biomes_config', len(out['biomes_config']))
