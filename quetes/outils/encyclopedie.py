#!/usr/bin/env python3
"""Génère les chapitres de l'Encyclopédie (cahier §9.2) sous forme de
fichiers TOML dans ../donnees/encyclopedie/, à partir de l'index des jars.

    python3 encyclopedie.py bestiaire-overworld
    python3 encyclopedie.py --tous

Le TOML produit est ensuite lu par generer.py comme n'importe quel
chapitre écrit à la main. Il est REGÉNÉRÉ à chaque passage : les textes
spécifiques se mettent dans notes/<chapitre>.toml (une entrée par
identifiant), jamais dans le TOML généré.

Modèle enrichi (décision 2 du 4 octobre) : chaque entrée dit ce que les
DONNÉES disent, et rien d'autre — catégorie d'apparition (lue dans les
biomes JSON), monde et biomes (biomes JSON, modificateurs Forge, configs
d'apparition d'Alex's Mobs et de Mowzie's Mobs), butin (tables de butin
de l'entité). Une information absente des données est omise.

Voie d'apparition (correction de méthode du 5 octobre) : une créature
sans biome dans les données doit avoir une voie vérifiée sur pièce —
structure, générateur, bloc, objet, rituel, invocation, événement — notée
dans notes/<chapitre>.toml (clé `apparition`, avec la pièce en commentaire)
et imprimée « Apparaît : ... ». Sans voie, le générateur s'arrête et la
nomme : elle va alors dans exclusions.toml, avec la raison mesurée. Une
créature n'est exclue que si AUCUNE voie ne la fait apparaître ; les œufs
d'apparition ne comptent pas.
"""
import json
import os
import sys
import tomllib
import importlib.util as _ilu

ICI = os.path.dirname(os.path.abspath(__file__))
_spec = _ilu.spec_from_file_location('typo', os.path.join(ICI, 'normaliser-typo.py'))
TYPO = _ilu.module_from_spec(_spec); _spec.loader.exec_module(TYPO)
DONNEES = os.path.join(ICI, '..', 'donnees')
NOTES = os.path.join(DONNEES, 'notes')
INDEX = os.path.join(ICI, '..', 'index')


def charger_index():
    ix = {}
    for f in ('index.json', 'index_vanilla.json'):
        d = json.load(open(os.path.join(INDEX, f), encoding='utf-8'))
        for k, v in d.items():
            if isinstance(v, dict):
                ix.setdefault(k, {}).update(v)
    p = os.path.join(INDEX, 'apparitions.json')
    ix['apparitions'] = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'butin': {}, 'biomes_config': {}}
    p = os.path.join(INDEX, 'noms_fr.json')  # outils/noms-fr.py : noms séparés objet / créature / biome
    ix['noms'] = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'entite': {}, 'objet': {}, 'biome': {}}
    p = os.path.join(INDEX, 'voies.json')   # outils/voies.py : biome_modifier, spawn_overrides, NBT
    ix['voies'] = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    return ix


def nom_structure(ix, st):
    """« mod:chemin » d'une structure ou d'un NBT -> un nom lisible."""
    if st in ix['structures']:
        n = ix['fr'].get(st) or ix['structures'].get(st)
        if isinstance(n, str) and n and ':' not in n:
            return n
    mod, chemin = st.split(':', 1)
    base = chemin.split('/')[0].replace('_', ' ')
    return f"{base} ({MOD_FR.get(mod, mod)})"


MOD_FR = {'aether': 'Aether', 'deep_aether': 'Deep Aether', 'aether_redux': 'Aether Redux', 'blue_skies': 'Blue Skies',
          'twilightforest': 'Twilight Forest', 'betternether': 'Better Nether', 'bygonenether': 'Bygone Nether',
          'netherexp': "Jaden's Nether Expansion", 'betterend': 'Better End', 'deeperdarker': 'Deeper and Darker',
          'farmers_structures': "Farmer's Structures", 'soulfulnether': 'Soulful Nether', 'minecraft': 'jeu de base',
          'mes': "Moog's End Structures", 'mns': "Moog's Nether Structures", 'mvs': "Moog's Voyager Structures",
          'philipsruins': "Philip's Ruins", 'adorabuild_structures': 'AdoraBuild', 'repurposed_structures': 'Repurposed Structures',
          'towns_and_towers': 'Towns and Towers', 'dungeons_arise': 'When Dungeons Arise', 'structory': 'Structory',
          'structory_towers': 'Structory Towers', 'explorations': 'Explorations', 'cataclysm': 'Cataclysm',
          'betterdungeons': "YUNG's Better Dungeons", 'bettermineshafts': "YUNG's Better Mineshafts",
          'illagerinvasion': 'Illager Invasion', 'irons_spellbooks': "Iron's Spells", 'stalwart_dungeons': 'Stalwart Dungeons',
          'formationsoverworld': 'Formations', 'formationsnether': 'Formations Nether', 'galosphere': 'Galosphere'}


def t(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def nom_fr(ix, ident, genre=None):
    """genre : 'entite', 'objet' ou 'biome'. Sans genre, on le devine par le
    registre — une créature d'abord, puisque c'est l'usage le plus fréquent."""
    if genre is None:
        genre = 'entite' if ident in ix['entities'] else 'biome' if ident in ix['biomes'] else 'objet'
    return (ix['noms'][genre].get(ident) or ix['fr'].get(ident) or ix['entities'].get(ident) or ix['items'].get(ident)
            or ix['biomes'].get(ident) or ident.split(':', 1)[-1].replace('_', ' '))


def mobs_avec_oeuf(ix, mods):
    """Une créature = un type d'entité qui a un œuf d'apparition."""
    out = []
    for item in ix['items']:
        mod, nom = item.split(':', 1)
        if mod not in mods:
            continue
        if nom.endswith('_spawn_egg'):
            ent = f'{mod}:{nom[:-10]}'
        elif nom.startswith('spawn_egg_'):
            ent = f'{mod}:{nom[10:]}'
        else:
            continue
        if ent in ix['entities']:
            out.append((ent, item))
    return sorted(set(out))


# ------------------------------------------------------------- mondes et biomes

VANILLA_NETHER = {'minecraft:nether_wastes', 'minecraft:soul_sand_valley', 'minecraft:crimson_forest',
                  'minecraft:warped_forest', 'minecraft:basalt_deltas'}
VANILLA_END = {'minecraft:the_end', 'minecraft:end_highlands', 'minecraft:end_midlands', 'minecraft:small_end_islands',
               'minecraft:end_barrens'}
BOP_NETHER = {'biomesoplenty:crystalline_chasm', 'biomesoplenty:erupting_inferno', 'biomesoplenty:undergrowth',
              'biomesoplenty:visceral_heap', 'biomesoplenty:withered_abyss'}
MONDE_PAR_MOD = {
    'twilightforest': 'Twilight Forest', 'aether': 'Aether', 'deep_aether': 'Aether', 'aether_redux': 'Aether',
    'lost_aether_content': 'Aether', 'betternether': 'Nether', 'bygonenether': 'Nether', 'netherexp': 'Nether',
    'soulfulnether': 'Nether', 'betterend': 'End', 'deeperdarker': 'Otherside', 'galosphere': 'Overworld',
    'yungscavebiomes': 'Overworld', 'biomesoplenty': 'Overworld', 'minecraft': 'Overworld', 'terralith': 'Overworld',
    'blue_skies': 'Blue Skies',
}
DIM_FR = {'twilightforest:twilight_forest': 'Twilight Forest', 'aether:the_aether': 'Aether', 'blue_skies:everbright': 'Everbright',
          'blue_skies:everdawn': 'Everdawn', 'deeperdarker:otherside': 'Otherside', 'minecraft:the_nether': 'Nether',
          'minecraft:the_end': 'End', 'minecraft:overworld': 'Overworld'}
TAG_MONDE = {'minecraft:is_overworld': 'Overworld', 'minecraft:is_nether': 'Nether', 'minecraft:is_end': 'End',
             'forge:is_overworld': 'Overworld', 'forge:is_nether': 'Nether', 'forge:is_end': 'End'}
TAG_FR = {
    'minecraft:is_forest': 'forêts', 'minecraft:is_jungle': 'jungles', 'minecraft:is_savanna': 'savanes',
    'minecraft:is_taiga': 'taïgas', 'minecraft:is_mountain': 'montagnes', 'minecraft:is_ocean': 'océans',
    'minecraft:is_river': 'rivières', 'minecraft:is_beach': 'plages', 'minecraft:is_badlands': 'badlands',
    'minecraft:is_hill': 'collines', 'minecraft:is_deep_ocean': 'océans profonds',
    'forge:is_snowy': 'biomes enneigés', 'forge:is_cold': 'biomes froids', 'forge:is_hot': 'biomes chauds',
    'forge:is_dry': 'biomes secs', 'forge:is_wet': 'biomes humides', 'forge:is_sandy': 'biomes sableux',
    'forge:is_peak': 'pics', 'forge:is_plains': 'plaines', 'forge:is_swamp': 'marais', 'forge:is_desert': 'déserts',
    'forge:is_mushroom': 'champs de champignons', 'forge:is_spooky': 'forêts sombres', 'forge:is_dense': 'forêts denses',
    'forge:is_sparse': 'biomes clairsemés', 'forge:is_cave': 'grottes', 'forge:is_underground': 'souterrains',
    'forge:is_lush': 'biomes luxuriants', 'forge:is_coniferous': 'forêts de conifères', 'forge:is_water': "plans d'eau",
    'forge:is_mountain': 'montagnes', 'forge:is_slope': 'pentes', 'forge:is_plateau': 'plateaux',
    'minecraft:is_overworld': "tout l'Overworld", 'minecraft:is_nether': 'tout le Nether', 'minecraft:is_end': "tout l'End",
    'mowziesmobs:is_magical': 'biomes magiques', 'forge:is_void': 'le Vide',
}


def monde_de_biome(b, ix):
    if b.startswith('#'):
        return TAG_MONDE.get(b[1:])
    d = ix.get('biome_dim', {}).get(b)
    if d:
        return DIM_FR.get(d, d)
    if b in VANILLA_NETHER or b in BOP_NETHER:
        return 'Nether'
    if b in VANILLA_END:
        return 'End'
    return MONDE_PAR_MOD.get(b.split(':')[0])


def connu(c, ix):
    """Un biome nommé dans une config n'est retenu que s'il existe dans le pack."""
    return c.startswith('#') or c in ix['biomes']


def biome_fr(b, ix):
    if b.startswith('#'):
        return TAG_FR.get(b[1:], b[1:].split(':')[-1].replace('is_', '').replace('_', ' '))
    return libelle(ix, b, 'biome')


def regles_fr(regles, ix):
    """Config d'apparition (Alex's / Mowzie's) -> texte lisible."""
    morceaux = []
    for groupe in regles:
        pos = [c for c in groupe if c and not c.startswith('!')]
        neg = [c[1:] for c in groupe if c.startswith('!') and connu(c[1:], ix)]
        if any(not connu(c, ix) for c in pos):
            continue  # cite un biome absent du pack (Terralith…) : la règle est sans effet ici
        txt = ' et '.join(biome_fr(c, ix) for c in pos) if pos else 'partout'
        if neg:
            txt += ' (sauf ' + ', '.join(biome_fr(c, ix) for c in neg) + ')'
        morceaux.append(txt)
    morceaux = list(dict.fromkeys(morceaux))
    suite = " ; et d'autres" if len(morceaux) > 4 else ''
    return ' ; '.join(morceaux[:4]) + suite


CAT_FR = {'monster': 'monstre', 'creature': 'animal', 'ambient': "créature d'ambiance", 'water_creature': 'créature aquatique',
          'water_ambient': 'poisson', 'underground_water_creature': 'créature des eaux souterraines', 'axolotls': 'axolotl',
          'misc': 'divers', 'aether_surface_monster': "monstre de surface de l'Aether", 'aether_darkness_monster': "monstre de l'ombre de l'Aether",
          'aether_sky_monster': "monstre du ciel de l'Aether", 'aether_aerwhale': 'aérobaleine'}


def fiche(ent, ix, note=None):
    """Ce que les données disent de la créature. Rien d'inventé.
    Renvoie (lignes, a_une_voie)."""
    note = note or {}
    lignes = []
    voie = False
    sp = ix.get('spawns', {}).get(ent)
    cfg = ix['apparitions']['biomes_config'].get(ent)
    cats = sp['cat'] if sp else []
    if cats:
        lignes.append('Catégorie : ' + ', '.join(CAT_FR.get(c, c) for c in cats) + '.')
    mondes, biomes = [], []
    if sp:
        for b in sp['biomes']:
            m = monde_de_biome(b, ix)
            if m and m not in mondes:
                mondes.append(m)
            biomes.append(biome_fr(b, ix))
    if cfg:
        for groupe in cfg:
            for c in groupe:
                m = TAG_MONDE.get(c.lstrip('!').lstrip('#'))
                if m and not c.startswith('!') and m not in mondes:
                    mondes.append(m)
    if mondes:
        lignes.append('Monde : ' + ', '.join(mondes) + '.')
    if biomes:
        vus = list(dict.fromkeys(biomes))
        suite = " et d'autres" if len(vus) > 6 else ''
        lignes.append('Biomes : ' + ', '.join(vus[:6]) + suite + '.')
        voie = True
    elif cfg and regles_fr(cfg, ix):
        lignes.append('Apparition (config du serveur) : ' + regles_fr(cfg, ix) + '.')
        voie = True
    elif cfg is not None:
        lignes.append("Apparition naturelle : aucune (config du serveur).")
    vo = ix.get('voies', {}).get(ent, {})
    if not biomes and vo.get('biomes'):
        bm = [biome_fr(x, ix) for x in vo['biomes'] if connu(x.lstrip('#') if not x.startswith('#') else x, ix)]
        if bm:
            lignes.append('Biomes : ' + ', '.join(list(dict.fromkeys(bm))[:6]) + '.')
            voie = True
    # Structures : seulement pour une créature sans biome ni config, et
    # nommées par le mod qui les pose (un chemin de fichier NBT ne dit rien
    # au joueur). Les pièces de compatibilité (« integration », « compat »)
    # ne comptent pas : elles ne se génèrent que si l'autre mod est là.
    if not voie and not note.get('apparition'):
        mods_st = [MOD_FR.get(x.split(':')[0], x.split(':')[0]) for x in vo.get('structures_spawn', []) + vo.get('nbt', [])
                   if not any(k in x for k in ('integration', 'compat', 'farmers_structures:'))]
        mods_st = list(dict.fromkeys(mods_st))
        if mods_st:
            lignes.append('Apparaît : dans des structures de ' + ', '.join(mods_st[:4]) + ('' if len(mods_st) <= 4 else ' et d\'autres') + '.')
            voie = True
    if note.get('apparition'):
        lignes.append('Apparaît : ' + note['apparition'] + '.')
        voie = True
    # Butin : seulement les objets qui ont un nom français dans le pack (le
    # reste serait de l'anglais brut dans une fiche française).
    butin = [b for b in ix['apparitions']['butin'].get(ent, []) if not b.startswith('#') and ix['noms']['objet'].get(b)]
    if butin:
        lignes.append('Butin : ' + ', '.join(dict.fromkeys(nom_fr(ix, b, 'objet') for b in butin)) + '.')
    return lignes, voie


MODELES = {
    'minecraft': "Créature du jeu de base.",
    'alexsmobs': "Créature d'&bAlex's Mobs&r.",
    'friendsandfoes': "Créature de &bFriends & Foes&r, les candidats des votes de créature Minecraft.",
    'mowziesmobs': "Créature de &bMowzie's Mobs&r.",
    'guardvillagers': "Créature de &bGuard Villagers&r.",
    'conjurer_illager': "Créature de &bThe Conjurer&r.",
    'illagerinvasion': "Illageois d'&bIllager Invasion&r.",
    'takesapillage': "Illageois de &bTakes a Pillage&r.",
    'goblintraders': "Marchand de &bGoblin Traders&r.",
    'quark': "Créature de &bQuark&r.",
    'pet_cemetery': "Créature de &bPet Cemetery&r.",
    'betternether': "Créature de &bBetter Nether&r.",
    'bygonenether': "Créature de &bBygone Nether&r.",
    'netherexp': "Créature de &bJaden's Nether Expansion&r.",
    'soulfulnether': "Créature de &bSoulful Nether&r.",
    'betterend': "Créature de &bBetter End&r.",
    'aether': "Créature de l'&bAether&r.",
    'deep_aether': "Créature de &bDeep Aether&r.",
    'aether_redux': "Créature d'&bAether Redux&r.",
    'lost_aether_content': "Créature de &bLost Aether Content&r.",
    'twilightforest': "Créature de la &aTwilight Forest&r.",
    'blue_skies': "Créature de &bBlue Skies&r.",
    'deeperdarker': "Créature de &3Deeper and Darker&r.",
}

# Créatures vanilla qui ne vivent pas dans l'Overworld (Bestiaire Nether/End).
VANILLA_HORS_OVERWORLD = {
    'minecraft:blaze', 'minecraft:ghast', 'minecraft:hoglin', 'minecraft:magma_cube', 'minecraft:piglin',
    'minecraft:piglin_brute', 'minecraft:strider', 'minecraft:wither_skeleton', 'minecraft:zoglin',
    'minecraft:zombified_piglin', 'minecraft:endermite', 'minecraft:shulker', 'minecraft:ender_dragon',
    'minecraft:wither', 'minecraft:happy_ghast',
    # Alex's Mobs : configs d'apparition minecraft:is_nether / is_end (config/alexsmobs/*_spawns.json)
    'alexsmobs:bone_serpent', 'alexsmobs:crimson_mosquito', 'alexsmobs:warped_toad', 'alexsmobs:warped_mosco',
    'alexsmobs:straddler', 'alexsmobs:stradpole', 'alexsmobs:soul_vulture', 'alexsmobs:mimicube',
    'alexsmobs:laviathan', 'alexsmobs:cosmaw', 'alexsmobs:enderiophage', 'alexsmobs:endergrade',
    'alexsmobs:cosmic_cod', 'alexsmobs:void_worm',
    # Friends & Foes : la citadelle (has_structure/citadel = #minecraft:is_nether)
    'friendsandfoes:wildfire',
    # Goblin Traders : le gobelin des veines a son compteur dans world/DIM-1 (Nether)
    'goblintraders:vein_goblin_trader',
    # Quark, quark-common.toml du serveur : foxhound (nether_wastes, basalt_deltas, soul_sand_valley), wraith (soul_sand_valley)
    'quark:foxhound', 'quark:wraith',
}


def chapitre_bestiaire(ix, exclusions, notes, mods, hors, fichier, titre, icone, icone_fin, intro, seulement=None):
    lignes = [f'# GÉNÉRÉ par outils/encyclopedie.py — ne pas éditer : notes/{fichier}.toml pour les textes.\n']
    lignes.append(f'[chapitre]\ntitre = "{t(titre)}"\nfichier = "enc_{fichier.replace("-", "_")}"\ngroupe = "encyclopedie"\n'
                  f'icone = "{icone}"\nordre = 0\nlignes_cachees = true\ngrille = 16\n')
    lignes.append(f'[[quete]]\ncle = "intro"\ntitre = "{t(titre)}"\ntaille = 1.5\nicone = "{icone}"\ntaches = ["checkmark Lu"]\n'
                  f'recompenses = ["xp 2"]\ndescription = """\n{t(intro)}\n"""\n')
    exclues, cles, sans_voie = [], [], []
    for ent, oeuf in mobs_avec_oeuf(ix, mods):
        if ent in hors or (seulement is not None and not seulement(ent)):
            continue
        if ent in exclusions:
            exclues.append((ent, exclusions[ent]))
            continue
        mod = ent.split(':')[0]
        nom = libelle(ix, ent, 'entite')
        cle = ent.replace(':', '_')
        note = notes.get(ent, {})
        if not note.get('defi'):
            cles.append(cle)  # un défi ne compte pas dans « Tout le chapitre »
        lignes_fiche, voie = fiche(ent, ix, note)
        if not voie:
            sans_voie.append(ent)
        desc = ' '.join([MODELES.get(mod, '')] + lignes_fiche)
        if note.get('description'):
            desc += '\n\n' + note['description']
        titre_q = note.get('titre') or f"Rencontre : {nom}"
        forme = 'forme = "octagon"\ntaille = 1.3\n' if note.get('defi') else ''
        lignes.append(f'[[quete]]\ncle = "{cle}"\ntitre = "{t(titre_q)}"\nsous_titre = "{t(nom)} — {mod}"\noptionnel = true\n{forme}'
                      f'icone = "{oeuf}"\ntaches = ["observation entity {ent}"]\nrecompenses = ["xp 1"]\ndescription = """\n{t(desc)}\n"""\n')
    if sans_voie:
        raise SystemExit(f"{fichier} : {len(sans_voie)} créature(s) sans voie d'apparition vérifiée — à documenter "
                         f"(notes, clé apparition) ou à exclure (exclusions.toml) :\n  " + '\n  '.join(sans_voie))
    deps = ', '.join(f'"{c}"' for c in cles)
    # optionnel comme les fiches : l'Encyclopédie entière reste hors du
    # pourcentage du livre, et aucune quête obligatoire n'attend une optionnelle.
    lignes.append(f'[[quete]]\ncle = "complet"\ntitre = "&7Tout le chapitre"\noptionnel = true\ntaille = 1.5\nicone = "{icone_fin}"\nforme = "gear"\n'
                  f'taches = ["checkmark Chapitre complet"]\nrecompenses = ["xp 20"]\ndeps = [{deps}]\ndescription = """\n'
                  f"Toutes les créatures de ce chapitre rencontrées. La récompense est symbolique : c'est la quête qui compte.\n\"\"\"\n")
    return '\n'.join(lignes), len(cles), exclues


def bestiaire_overworld(ix, exclusions, notes):
    mods = ['minecraft', 'alexsmobs', 'friendsandfoes', 'mowziesmobs', 'guardvillagers', 'conjurer_illager',
            'illagerinvasion', 'takesapillage', 'goblintraders', 'quark', 'pet_cemetery']
    intro = ("Chaque créature de l'Overworld, du jeu de base et des mods de faune. Une quête se valide en &lregardant&r la créature : il suffit de l'avoir devant soi.\n\n"
             "Chaque fiche dit ce que les données du pack disent : la catégorie d'apparition, le monde, les biomes, le butin — et, quand la créature ne vient pas d'un biome, la voie qui la fait apparaître. Rien de plus.\n\n"
             "Ce chapitre est facultatif, un catalogue à remplir au fil des rencontres. La dernière quête récompense le bestiaire complet.")
    return chapitre_bestiaire(ix, exclusions, notes, mods, VANILLA_HORS_OVERWORLD, 'bestiaire-overworld',
                              '&7Bestiaire — Overworld', 'minecraft:zombie_head', 'minecraft:creeper_head', intro)


# ------------------------------------------------------------- catalogues

def libelle(ix, ident, genre='objet'):
    """Nom affichable : le nom français du pack, sinon le nom du mod entre
    guillemets (un nom propre cité, jamais une traduction inventée)."""
    fr = ix['noms'][genre].get(ident)
    if fr:
        return fr
    brut = ix['items'].get(ident) or ix['biomes'].get(ident) or ix['entities'].get(ident)
    if not isinstance(brut, str) or not brut or ':' in brut:
        brut = ident.split(':', 1)[1].split('/')[-1].replace('_', ' ').strip().capitalize()
    return f"«{chr(160)}{brut}{chr(160)}»"


def chapitre_catalogue(fichier, titre, icone, icone_fin, intro, entrees, fin="Tout le chapitre rempli."):
    """entrees : [{cle, titre, sous_titre, tache, icone?, description}]."""
    lignes = [f'# GÉNÉRÉ par outils/encyclopedie.py — ne pas éditer.\n']
    lignes.append(f'[chapitre]\ntitre = "{t(titre)}"\nfichier = "enc_{fichier.replace("-", "_")}"\ngroupe = "encyclopedie"\n'
                  f'icone = "{icone}"\nordre = 0\nlignes_cachees = true\ngrille = 16\n')
    lignes.append(f'[[quete]]\ncle = "intro"\ntitre = "{t(titre)}"\ntaille = 1.5\nicone = "{icone}"\ntaches = ["checkmark Lu"]\n'
                  f'recompenses = ["xp 2"]\ndescription = """\n{t(intro)}\n"""\n')
    cles = []
    for e in entrees:
        cles.append(e['cle'])
        ic = f'icone = "{e["icone"]}"\n' if e.get('icone') else ''
        st = f'sous_titre = "{t(e["sous_titre"])}"\n' if e.get('sous_titre') else ''
        lignes.append(f'[[quete]]\ncle = "{e["cle"]}"\ntitre = "{t(e["titre"])}"\n{st}optionnel = true\n{ic}'
                      f'taches = ["{t(e["tache"])}"]\nrecompenses = ["xp 1"]\ndescription = """\n{t(e["description"])}\n"""\n')
    deps = ', '.join(f'"{c}"' for c in cles)
    lignes.append(f'[[quete]]\ncle = "complet"\ntitre = "&7Tout le chapitre"\noptionnel = true\ntaille = 1.5\nicone = "{icone_fin}"\nforme = "gear"\n'
                  f'taches = ["checkmark Chapitre complet"]\nrecompenses = ["xp 20"]\ndeps = [{deps}]\ndescription = """\n{t(fin)}\n"""\n')
    return '\n'.join(lignes), len(cles), []


def _generation():
    return json.load(open(os.path.join(INDEX, 'generation.json'), encoding='utf-8'))


DIM_TEXTE = {'minecraft:overworld': "l'Overworld", 'minecraft:the_nether': 'le Nether', 'minecraft:the_end': "l'End",
             'aether:the_aether': "l'Aether", 'twilightforest:twilight_forest': 'la Twilight Forest',
             'blue_skies:everbright': "l'Everbright", 'blue_skies:everdawn': "l'Everdawn", 'deeperdarker:otherside': "l'Otherside"}
MOD_BIOMES = {'minecraft': 'du jeu de base', 'biomesoplenty': "de Biomes O' Plenty", 'galosphere': 'de Galosphere',
              'yungscavebiomes': "de YUNG's Cave Biomes", 'climaterivers': 'de Climate Rivers', 'quark': 'de Quark',
              'betternether': 'de Better Nether', 'netherexp': "de Jaden's Nether Expansion", 'soulfulnether': 'de Soulful Nether',
              'gardens_of_the_dead': 'de Gardens of the Dead', 'betterend': 'de Better End', 'aether': "de l'Aether",
              'deep_aether': 'de Deep Aether', 'aether_redux': "d'Aether Redux", 'twilightforest': 'de la Twilight Forest',
              'blue_skies': 'de Blue Skies', 'deeperdarker': 'de Deeper and Darker'}


def chapitre_biomes(ix, fichier, titre, icone, icone_fin, dims, intro):
    gen = _generation()['biomes']
    habitants = {}
    for ent, sp in ix.get('spawns', {}).items():
        for b in sp['biomes']:
            if ix['noms']['entite'].get(ent):
                habitants.setdefault(b, []).append(ix['noms']['entite'][ent])
    entrees = []
    for b in sorted(gen, key=lambda x: (x.split(':')[0] != 'minecraft', x)):
        if gen[b] not in dims:
            continue
        mod = b.split(':')[0]
        desc = f"Biome {MOD_BIOMES.get(mod, 'de ' + mod)}, dans {DIM_TEXTE.get(gen[b], gen[b])}."
        h = list(dict.fromkeys(habitants.get(b, [])))
        if h:
            desc += ' On y croise : ' + ', '.join(h[:6]) + (" et d'autres" if len(h) > 6 else '') + ' (données du pack).'
        entrees.append({'cle': b.replace(':', '_').replace('/', '_'), 'titre': f"Découvrir : {libelle(ix, b, 'biome')}",
                        'tache': f"biome {b}", 'description': desc})
    return chapitre_catalogue(fichier, titre, icone, icone_fin, intro, entrees,
                              "Tous les biomes de ce chapitre visités. La récompense est symbolique : c'est la carte qui compte.")


def biomes_overworld(ix, exclusions, notes):
    return chapitre_biomes(ix, 'biomes-overworld', '&2Biomes — Overworld', 'minecraft:grass_block', 'minecraft:filled_map',
                           {'minecraft:overworld'},
                           "Chaque biome de l'Overworld que le serveur génère : le jeu de base, Biomes O' Plenty, les grottes de YUNG's et de Galosphere, les rivières de Climate Rivers, le Glimmering Weald de Quark. Une quête se valide en &lentrant&r dans le biome.\n\n"
                           "Seuls les biomes que les configs du serveur laissent générer sont là (outils/generation.py).")


def biomes_nether_end(ix, exclusions, notes):
    return chapitre_biomes(ix, 'biomes-nether-end', '&4Biomes — Nether et End', 'minecraft:netherrack', 'minecraft:end_stone',
                           {'minecraft:the_nether', 'minecraft:the_end'},
                           "Chaque biome du Nether et de l'End que le serveur génère : le jeu de base, Biomes O' Plenty, Better Nether, Gardens of the Dead, Jaden's Nether Expansion, Soulful Nether, Better End. Une quête se valide en &lentrant&r dans le biome.")


def biomes_dimensions(ix, exclusions, notes):
    return chapitre_biomes(ix, 'biomes-dimensions', '&bBiomes — dimensions', 'aether:aether_grass_block', 'minecraft:compass',
                           {'aether:the_aether', 'twilightforest:twilight_forest', 'blue_skies:everbright', 'blue_skies:everdawn', 'deeperdarker:otherside'},
                           "Chaque biome de l'Aether, de la Twilight Forest, de l'Everbright, de l'Everdawn et de l'Otherside que le serveur génère. Une quête se valide en &lentrant&r dans le biome.")


NOM_MOD_STRUCT = {**MOD_FR, 'bettermineshafts': "YUNG's Better Mineshafts", 'betterwitchhuts': "YUNG's Better Witch Huts",
                  'betterfortresses': "YUNG's Better Nether Fortresses", 'betterjungletemples': "YUNG's Better Jungle Temples",
                  'betteroceanmonuments': "YUNG's Better Ocean Monuments", 'betterstrongholds': "YUNG's Better Strongholds",
                  'mmv': "Moog's Missing Villages", 'hearths': 'Hearths', 'friendsandfoes': 'Friends & Foes', 'mowziesmobs': "Mowzie's Mobs",
                  'takesapillage': 'Takes a Pillage', 'aether_villages': 'Aether Villages', 'conjurer_illager': 'The Conjurer',
                  'endersdelight': "Ender's Delight", 'joshie': 'Blossom Blade', 'twigs': 'Twigs', 'villagesandpillages': 'Villages & Pillages',
                  'lost_aether_content': 'Lost Aether Content', 'deep_aether': 'Deep Aether'}


def chapitre_structures(ix, fichier, titre, icone, icone_fin, mods, intro):
    gen = _generation()['structures']
    entrees, exclues = [], []
    for st in sorted(gen):
        mod = st.split(':')[0]
        if mod not in mods:
            continue
        e = gen[st]
        if not e['generee']:
            exclues.append((st, e['raison']))
            continue
        bs = [libelle(ix, b, 'biome') for b in e.get('biomes', [])]
        desc = f"Structure de &b{NOM_MOD_STRUCT.get(mod, mod)}&r."
        if bs:
            vus = list(dict.fromkeys(bs))
            desc += ' Se génère dans : ' + ', '.join(vus[:5]) + (" et d'autres" if len(vus) > 5 else '') + ' (données du serveur).'
        nom = st.split(':', 1)[1].split('/')[-1].replace('_', ' ').strip().capitalize()
        entrees.append({'cle': st.replace(':', '_').replace('/', '_'), 'titre': f"Visiter : «{chr(160)}{nom}{chr(160)}»",
                        'sous_titre': NOM_MOD_STRUCT.get(mod, mod), 'tache': f"structure {st}", 'description': desc})
    texte, n, _ = chapitre_catalogue(fichier, titre, icone, icone_fin, intro, entrees,
                                     "Toutes les structures de ce chapitre visitées. La récompense est symbolique.")
    return texte, n, exclues


INTRO_STRUCT = ("Une quête par structure que le serveur génère vraiment : placée par la génération du monde, dans au moins un biome qui existe ici (outils/generation.py, datapacks du serveur compris). "
                "Elle se valide en &lentrant&r dans la structure. Les noms sont ceux du mod, entre guillemets.")


def structures_vanilla(ix, e, n):
    return chapitre_structures(ix, 'structures-vanilla', '&6Structures — jeu de base et YUNG', 'minecraft:mossy_cobblestone', 'minecraft:filled_map',
                               {'minecraft', 'bettermineshafts', 'betterwitchhuts', 'betterfortresses', 'betterjungletemples', 'betteroceanmonuments',
                                'betterstrongholds', 'betterdungeons', 'twigs', 'villagesandpillages', 'hearths', 'mmv', 'takesapillage', 'friendsandfoes',
                                'conjurer_illager', 'illagerinvasion', 'joshie', 'galosphere', 'mowziesmobs'}, INTRO_STRUCT)


def structures_repurposed(ix, e, n):
    return chapitre_structures(ix, 'structures-repurposed', '&6Structures — Repurposed Structures', 'minecraft:cracked_stone_bricks', 'minecraft:filled_map',
                               {'repurposed_structures'}, INTRO_STRUCT)


def structures_moogs(ix, e, n):
    return chapitre_structures(ix, 'structures-moogs', "&6Structures — Moog's", 'minecraft:oak_log', 'minecraft:filled_map',
                               {'mvs', 'mns', 'mes'}, INTRO_STRUCT)


def structures_villages(ix, e, n):
    return chapitre_structures(ix, 'structures-donjons-villages', '&6Structures — donjons, villes et tours', 'minecraft:bell', 'minecraft:filled_map',
                               {'dungeons_arise', 'towns_and_towers', 'structory', 'structory_towers'}, INTRO_STRUCT)


def structures_ruines(ix, e, n):
    return chapitre_structures(ix, 'structures-ruines', '&6Structures — ruines et petites choses', 'minecraft:chiseled_stone_bricks', 'minecraft:filled_map',
                               {'adorabuild_structures', 'formationsoverworld', 'formationsnether', 'philipsruins', 'explorations', 'farmers_structures'}, INTRO_STRUCT)


def structures_mondes(ix, e, n):
    return chapitre_structures(ix, 'structures-mondes', '&6Structures — autres mondes', 'minecraft:ender_eye', 'minecraft:filled_map',
                               {'aether', 'aether_villages', 'deep_aether', 'lost_aether_content', 'twilightforest', 'blue_skies', 'deeperdarker',
                                'cataclysm', 'irons_spellbooks', 'betternether', 'betterend', 'netherexp', 'bygonenether', 'endersdelight'}, INTRO_STRUCT)


MODS_NETHER_END = ['betternether', 'bygonenether', 'netherexp', 'soulfulnether', 'betterend']
MODS_DIMENSIONS = ['aether', 'deep_aether', 'aether_redux', 'lost_aether_content', 'twilightforest', 'blue_skies', 'deeperdarker']


def bestiaire_nether_end(ix, exclusions, notes):
    mods = ['minecraft', 'alexsmobs', 'friendsandfoes', 'goblintraders', 'quark'] + MODS_NETHER_END
    intro = ("Les créatures du Nether et de l'End : le jeu de base, Better Nether, Bygone Nether, Soulful Nether, Jaden's Nether Expansion, Better End, et celles des mods de faune qui y vivent. Une quête se valide en &lregardant&r la créature.\n\n"
             "Chaque fiche dit ce que les données du pack disent : biomes, structure ou voie qui la fait apparaître, butin. Les boss sont comptés au défi &cChasseur de boss&r, pas ici.")
    return chapitre_bestiaire(ix, exclusions, notes, mods, BOSS, 'bestiaire-nether-end', '&7Bestiaire — Nether et End',
                              'minecraft:wither_skeleton_skull', 'minecraft:dragon_head', intro,
                              seulement=lambda e: e.split(':')[0] in MODS_NETHER_END or e in VANILLA_HORS_OVERWORLD)


def bestiaire_dimensions(ix, exclusions, notes):
    intro = ("Les créatures de l'Aether (avec Deep Aether, Aether Redux et Lost Aether Content), de la Twilight Forest, de l'Everbright et de l'Everdawn, et de l'Otherside. Une quête se valide en &lregardant&r la créature.\n\n"
             "Chaque fiche dit ce que les données du pack disent. Les boss sont comptés au défi &cChasseur de boss&r, pas ici.")
    return chapitre_bestiaire(ix, exclusions, notes, MODS_DIMENSIONS, BOSS, 'bestiaire-dimensions', '&7Bestiaire — dimensions',
                              'aether:aechor_petal', 'twilightforest:naga_trophy', intro)


# Les boss ont leur hexagone au défi Chasseur de boss (même liste que le
# bot) : pas de doublon dans les bestiaires des autres mondes.
BOSS = {'minecraft:ender_dragon', 'minecraft:wither', 'twilightforest:naga', 'twilightforest:lich', 'twilightforest:minoshroom',
        'twilightforest:hydra', 'twilightforest:knight_phantom', 'twilightforest:ur_ghast', 'twilightforest:alpha_yeti',
        'twilightforest:snow_queen', 'aether:slider', 'aether:valkyrie_queen', 'aether:sun_spirit',
        'lost_aether_content:aerwhale_king', 'deep_aether:eots_controller', 'blue_skies:summoner', 'blue_skies:alchemist',
        'blue_skies:arachnarch', 'blue_skies:starlit_crusher', 'deeperdarker:stalker', 'alexsmobs:void_worm'}

CHAPITRES = {'bestiaire-overworld': bestiaire_overworld, 'bestiaire-nether-end': bestiaire_nether_end,
             'bestiaire-dimensions': bestiaire_dimensions,
             'biomes-overworld': biomes_overworld, 'biomes-nether-end': biomes_nether_end,
             'biomes-dimensions': biomes_dimensions,
             'structures-vanilla': structures_vanilla, 'structures-repurposed': structures_repurposed,
             'structures-moogs': structures_moogs, 'structures-donjons-villages': structures_villages,
             'structures-ruines': structures_ruines, 'structures-mondes': structures_mondes}


def main(argv):
    ix = charger_index()
    exclusions = tomllib.load(open(os.path.join(DONNEES, 'exclusions.toml'), 'rb')).get('exclusion', {})
    cibles = list(CHAPITRES) if '--tous' in argv else [a for a in argv if not a.startswith('--')]
    for c in cibles:
        notes_p = os.path.join(NOTES, c + '.toml')
        notes = tomllib.load(open(notes_p, 'rb')).get('note', {}) if os.path.exists(notes_p) else {}
        texte, n, exclues = CHAPITRES[c](ix, exclusions, notes)
        os.makedirs(os.path.join(DONNEES, 'encyclopedie'), exist_ok=True)
        with open(os.path.join(DONNEES, 'encyclopedie', c + '.toml'), 'w', encoding='utf-8') as f:
            # même typographie que les chapitres écrits à la main (normaliser-typo.py)
            f.write('\n'.join(TYPO.normaliser_ligne(l) for l in texte.split('\n')))
        print(f"{c} : {n} entrées, {len(exclues)} exclue(s)")
        for e, r in exclues:
            print(f"   exclu {e} — {r}")


if __name__ == '__main__':
    main(sys.argv[1:])
