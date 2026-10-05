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
import re
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
            if k == 'tag_membres':   # les mods ajoutent aux balises vanilla : fusionner, jamais écraser
                tm = ix.setdefault(k, {})
                for t, membres_ in v.items():
                    tm[t] = list(dict.fromkeys(tm.get(t, []) + list(membres_)))
            elif isinstance(v, dict):
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
            'illagerinvasion', 'takesapillage', 'goblintraders', 'quark', 'pet_cemetery',
            'raided', 'whatareyouvotingfor', 'supplementaries']
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


# ------------------------------------------------------------- catalogues d'objets

def _obtenables():
    d = json.load(open(os.path.join(INDEX, 'obtenables.json'), encoding='utf-8'))
    return set(d['recette']) | set(d['butin']) | set(d['monde'])


def membres(ix, tag, vus=None):
    """Membres d'une balise d'objets, sous-balises résolues."""
    vus = vus or set()
    if tag in vus:
        return set()
    vus.add(tag)
    out = set()
    for v in ix['tag_membres'].get(tag, []):
        v = v['id'] if isinstance(v, dict) else v
        out |= membres(ix, v[1:], vus) if v.startswith('#') else {v}
    return out


def chapitre_objets(ix, fichier, titre, icone, icone_fin, intro, objets, verbe='Obtenir', texte=None):
    """objets : identifiants ; seuls les objets obtenables entrent (outils/obtenables.py)."""
    ob = _obtenables()
    entrees, exclues = [], []
    for i in sorted(set(objets)):
        if i not in ix['items']:
            continue
        if i not in ob:
            exclues.append((i, "ne sort d'aucune recette, table de butin ni génération"))
            continue
        mod = i.split(':')[0]
        desc = texte(i) if texte else f"Objet de &b{NOM_MOD_STRUCT.get(mod, MOD_FR.get(mod, mod))}&r."
        entrees.append({'cle': i.replace(':', '_').replace('/', '_'), 'titre': f"{verbe} : {libelle(ix, i, 'objet')}",
                        'tache': f"item {i}", 'icone': i, 'description': desc})
    texte_, n, _ = chapitre_catalogue(fichier, titre, icone, icone_fin, intro, entrees,
                                      "Tout le chapitre réuni. La récompense est symbolique : c'est la collection qui compte.")
    return texte_, n, exclues


MODS_CUISINE = {'farmersdelight': "Farmer's Delight", 'delightful': 'Delightful', 'twilightdelight': "Twilight's Flavor & Delight",
                'crabbersdelight': "Crabber's Delight", 'mynethersdelight': "My Nether's Delight", 'oceansdelight': "Ocean's Delight",
                'endersdelight': "Ender's Delight", 'chefsdelight': "Chef's Delight", 'aetherdelight': 'Aether Delight',
                'quarkdelight': 'Quark Delight'}


def gastronomie(ix, e, n):
    tags = [t for t in ix['tag_membres'] if t in ('c:foods', 'forge:foods') or t.startswith(('c:foods/', 'forge:foods/'))
            or t in ('farmersdelight:meals', 'farmersdelight:drinks', 'farmersdelight:sweets', 'farmersdelight:pies',
                     'farmersdelight:feasts', 'farmersdelight:snacks')]
    objets = set()
    for t in tags:
        objets |= {i for i in membres(ix, t) if i.split(':')[0] in MODS_CUISINE}
    return chapitre_objets(ix, 'gastronomie', '&6Gastronomie', 'farmersdelight:cooking_pot', 'farmersdelight:beef_stew',
                           "Chaque plat, boisson et douceur de Farmer's Delight et de ses extensions présentes dans le pack. Une quête se valide en ayant le plat dans l'inventaire.\n\n"
                           "La liste est celle des balises d'aliments du pack ; seuls les plats qu'une recette ou un butin donne vraiment y sont.",
                           objets, 'Goûter', lambda i: f"Un plat de &b{MODS_CUISINE[i.split(':')[0]]}&r.")


def disques(ix, e, n):
    return chapitre_objets(ix, 'disques', '&dDisques et musiques', 'minecraft:jukebox', 'minecraft:music_disc_pigstep',
                           "Tous les disques que le pack permet d'obtenir, de tous les mods. Une quête se valide en ayant le disque dans l'inventaire.",
                           membres(ix, 'minecraft:music_discs'), 'Trouver')


def trophees(ix, e, n):
    objets = [i for i in ix['items'] if (i.endswith('_trophy') or i.endswith('_skull') or (i.endswith('_head') and ':' in i))
              and 'wall' not in i and 'piston' not in i and i != 'minecraft:player_head'
              and not re.search(r'_(axe|hoe|pickaxe|shovel|hammer|sword)_head$', i) and i not in ('twilightforest:nagastone_head', 'mysticalagriculture:blank_skull')]
    return chapitre_objets(ix, 'trophees', '&6Trophées et têtes', 'twilightforest:naga_trophy', 'minecraft:dragon_head',
                           "Les trophées des boss, les têtes de créatures et les trophées de décoration. Une quête se valide en ayant l'objet dans l'inventaire.",
                           objets)


def minerais(ix, e, n):
    objets = set()
    for t in ix['tag_membres']:
        if t.startswith(('forge:ingots/', 'forge:gems/')):
            objets |= membres(ix, t)
    return chapitre_objets(ix, 'minerais', '&7Minerais et lingots', 'minecraft:iron_ingot', 'minecraft:diamond',
                           "Chaque lingot et chaque gemme du pack, d'après les balises de lingots et de gemmes. Une quête se valide en ayant l'objet dans l'inventaire.",
                           objets)


def bois(ix, e, n):
    objets = {i for i in membres(ix, 'minecraft:logs') if 'stripped' not in i and re.search(r'(log|stem|stalk)$', i)}
    return chapitre_objets(ix, 'bois', '&2Bois', 'minecraft:oak_log', 'minecraft:oak_sapling',
                           "Chaque bûche et chaque tige d'arbre du pack. Une quête se valide en ayant la bûche dans l'inventaire.",
                           objets, 'Récolter')


ARMES = re.compile(r'_(helmet|chestplate|leggings|boots|sword|axe|bow|crossbow|shield|spear|lance|hammer|scythe|dagger|katana|staff|wand)$')


def armurerie(ix, e, n):
    mods = {'aether', 'deep_aether', 'aether_redux', 'twilightforest', 'blue_skies', 'cataclysm', 'irons_spellbooks',
            'advancednetherite', 'deeperdarker', 'dragonloot', 'mowziesmobs', 'stalwart_dungeons', 'galosphere', 'betterend', 'betternether'}
    # une quête par ensemble d'armure (le casque le représente) et une par arme
    objets = [i for i in ix['items'] if i.split(':')[0] in mods and ARMES.search(i)
              and not re.search(r'_(chestplate|leggings|boots)$', i)]
    return chapitre_objets(ix, 'armurerie', '&cArmurerie', 'minecraft:netherite_chestplate', 'cataclysm:ignitium_helmet',
                           "Chaque armure (son casque la représente) et chaque arme des mods d'aventure du pack : Aether, Twilight Forest, Blue Skies, Cataclysm, Iron's Spells, Advanced Netherite, Deeper and Darker, et les autres. Une quête se valide en ayant l'objet dans l'inventaire.",
                           objets)


def arsenal(ix, e, n):
    objets = [i for i in ix['items'] if i.startswith('securitycraft:')
              and not re.search(r'reinforced|secret_|_mine$|fake|block_pocket_wall|_item$|scanner_field|creative|admin|sentry_disguise', i)]
    objets += [i for i in ix['items'] if i in ('securitycraft:keypad_door_item', 'securitycraft:scanner_door_item', 'securitycraft:mine')]
    return chapitre_objets(ix, 'arsenal', '&cArsenal de défense', 'securitycraft:keypad', 'securitycraft:sentry',
                           "Chaque bloc et chaque outil de SecurityCraft, hors blocs renforcés et variantes déguisées. Une quête se valide en ayant l'objet dans l'inventaire.",
                           objets)


COULEURS = ('white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black')


def atelier_create(ix, e, n):
    deco = re.compile(r'(cut_|polished_|layered_|_pillar|_slab|_stairs|_wall$|_bricks?$|_tiles?$|small_|^create:(asurine|crimsite|ochrum|veridium|scorchia|scoria|limestone|tuff|andesite|granite|diorite|calcite|dripstone|deepslate)|window|pane|_door$|trapdoor|glass|scaffolding|ladder|bars|seat|toolbox|valve_handle|postbox|table_cloth|_sign$|crate|catwalk|framed|cardboard_block|sheet|nugget|_ingot$|crushed_|raw_|_dust$|powder|dough|cake|sweet|bar_of|honey|chocolate|builders_tea|apple|berries|sandpaper|shard|tube|incomplete|experience|zinc_block|brass_block|andesite_alloy_block|copper_)')
    objets = [i for i in ix['items'] if i.startswith('create:') and not deco.search(i)
              and not any(i.endswith('_' + c) or (':' + c + '_') in i for c in COULEURS)]
    return chapitre_objets(ix, 'atelier-create', '&6Atelier Create', 'create:cogwheel', 'create:mechanical_crafter',
                           "Chaque machine et chaque composant de Create, hors blocs de décoration, couleurs et matériaux. Une quête se valide en ayant l'objet dans l'inventaire.",
                           objets, 'Fabriquer')


def herbier(ix, e, n):
    """Mystical Agriculture : une graine par culture dont le matériau existe
    dans le pack — la règle même du mod (CropHasMaterialCondition) mesurée
    sur les balises du pack : lingot, gemme, poussière ou objet du même nom,
    ou créature du même nom pour les cultures de créatures. Les cultures de
    base (paliers, éléments) sont toujours présentes."""
    base = {'inferium', 'prudentium', 'tertium', 'imperium', 'supremium', 'air', 'earth', 'water', 'fire', 'nature', 'dye',
            'nether', 'end', 'experience', 'mystical_flower', 'dirt', 'stone', 'wood', 'ice', 'coal', 'iron', 'gold', 'copper',
            'diamond', 'emerald', 'lapis_lazuli', 'redstone', 'glowstone', 'nether_quartz', 'netherite', 'amethyst', 'deepslate',
            'basalt', 'coral', 'honey', 'obsidian', 'prismarine', 'slime', 'soulium', 'soul_sand', 'nature', 'marble', 'limestone', 'fish'}
    objets, ecartes = [], []
    for i in ix['items']:
        if not (i.startswith('mysticalagriculture:') and i.endswith('_seeds')):
            continue
        nom = i.split(':')[1][:-6]
        if nom in ('', 'inferium') and nom != 'inferium':
            continue
        materiau = (nom in base or membres(ix, f'forge:ingots/{nom}') or membres(ix, f'forge:gems/{nom}')
                    or membres(ix, f'forge:dusts/{nom}') or f'minecraft:{nom}' in ix['entities'] or f'minecraft:{nom}' in ix['items'])
        if materiau:
            objets.append(i)
        else:
            ecartes.append((i, 'matériau absent du pack (CropHasMaterialCondition)'))
    texte, k, exclues = chapitre_objets(ix, 'herbier', '&aHerbier', 'mysticalagriculture:inferium_seeds', 'mysticalagriculture:supremium_essence',
                                        "Chaque graine de Mystical Agriculture dont le matériau existe dans le pack. Une quête se valide en ayant la graine dans l'inventaire ; les graines se fabriquent à l'autel d'infusion. Les paliers d'essence, d'équipement et d'augments sont au chapitre Mystical Agriculture.",
                                        objets, 'Cultiver', lambda i: "Graine de &aMystical Agriculture&r.")
    return texte, k, exclues + ecartes


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


# ------------------------------------------------------------- collections d'équipement
# BMC-89, 5 octobre 2026 : l'Armurerie complète (une quête par pièce, une
# par ensemble, puis toute l'Armurerie) et les armes et outils par type.
# Garde-fou : chaque objet vient d'un mod chargé (index/mods_charges.json)
# et s'obtient en chaîne (outils/chaine.py : recette dont chaque ingrédient
# s'obtient, butin ou génération ; balises complètes). Le reste est exclu et
# listé. Livraisons jamais consommées (tâches « item » sans consommation).

_OK_CHAINE = None


def obtenables_chaine():
    global _OK_CHAINE
    if _OK_CHAINE is None:
        sys.path.insert(0, ICI)
        from chaine import fermeture
        from generer import Verif
        _OK_CHAINE, _ = fermeture(Verif.OBTENUS_AUTREMENT)
    return _OK_CHAINE


def mods_charges():
    p = os.path.join(INDEX, 'mods_charges.json')
    return set(json.load(open(p, encoding='utf-8'))) if os.path.exists(p) else None


def membres_complets(tag, vus=None):
    """Balise d'objets résolue sur les balises complètes (obtenables.json)."""
    tags = json.load(open(os.path.join(INDEX, 'obtenables.json'), encoding='utf-8')).get('tags', {})
    def m(x, vus):
        if x in vus:
            return set()
        vus.add(x)
        out = set()
        for v in tags.get(x, []):
            out |= m(v[1:], vus) if v.startswith('#') else {v}
        return out
    return m(tag, set())


MOD_AFFICHE = {**MOD_FR, 'minecraft': 'Minecraft', 'advancednetherite': 'Advanced Netherite', 'alexsmobs': "Alex's Mobs",
               'quark': 'Quark', 'create': 'Create', 'mowziesmobs': "Mowzie's Mobs", 'dragonloot': 'DragonLoot',
               'mysticalagriculture': 'Mystical Agriculture', 'lost_aether_content': 'Lost Aether Content',
               'umbral_skies': 'Umbral Skies', 'hazennstuff': "Hazen 'n Stuff", 'justhammers': 'Just Hammers',
               'delightful': 'Delightful', 'farmersdelight': "Farmer's Delight", 'shieldexp': 'Shield Expansion',
               'twilightdelight': "Twilight's Flavor & Delight", 'endersdelight': "Ender's Delight",
               'mynethersdelight': "My Nether's Delight", 'aether_treasure_reforging': 'Aether Treasure Reforging',
               'another_furniture': 'Another Furniture', 'securitycraft': 'SecurityCraft'}
# chapitre du livre où le mod a ses paliers
CHAPITRE_DU_MOD = {'mysticalagriculture': 'Mystical Agriculture', 'aether': "L'Aether", 'deep_aether': "L'Aether",
                   'aether_redux': "L'Aether", 'lost_aether_content': "L'Aether", 'umbral_skies': "L'Aether",
                   'aether_protect_your_moa': "L'Aether", 'twilightforest': 'Twilight Forest', 'irons_spellbooks': "Iron's Spells",
                   'hazennstuff': "Iron's Spells", 'dragonloot': 'Les dragons', 'blue_skies': 'Blue Skies',
                   'cataclysm': 'Cataclysm', 'deeperdarker': 'Deeper and Darker', 'betternether': 'Le Nether',
                   'betterend': "L'End", 'mowziesmobs': "Mowzie's Mobs"}

FENTES = [('helmet', 'casque'), ('chestplate', 'plastron'), ('leggings', 'jambières'), ('boots', 'bottes'), ('gloves', 'gants')]
MOTS_FENTE = re.compile(r"\b(Casque|Plastron|Jambières|Bottes|Gants|Gantelets|Helmet|Chestplate|Leggings|Boots|Gloves|Gauntlets|Mittens|Mask|Visor|Hat|Crown|Hood|Cap|Horns|Tunic|Robe|Masque|Chapeau|Couronne|Capuche|Manteau|Veste|Robes|Robe|Armure|Breastplate|Jacket|Tunique)\b\s*")


def fente(i):
    for s, _ in FENTES:
        if i.endswith('_' + s):
            return s
    return None


def nom_ensemble(ix, pieces):
    """« Ensemble en zanite », « Ensemble « Seraph » » : le nom d'une pièce,
    le mot de la pièce retiré."""
    ref = next((p for p in pieces if fente(p) == 'chestplate'), pieces[0])
    n = libelle(ix, ref, 'objet')
    guill = n.startswith('«')
    coeur = n.strip('«»  ')
    coeur = MOTS_FENTE.sub('', coeur).strip()
    coeur = re.sub(r"^(en|de|d'|du|des)\s+", lambda m: m.group(0), coeur)
    if not guill and (coeur[:3] in ('en ', 'de ', 'du ') or coeur[:2] == "d'" or coeur[:1].islower()):
        return f"Ensemble {coeur}"
    return f"Ensemble «\u00a0{coeur}\u00a0»"


def chapitre_collection(fichier, titre, icone, icone_fin, intro, entrees, titre_fin, fin, extra_fin=''):
    """entrees : [{cle, titre, taches[], icone, description, deps?, forme?}]."""
    lignes = ['# GÉNÉRÉ par outils/encyclopedie.py — ne pas éditer.\n']
    lignes.append(f'[chapitre]\ntitre = "{t(titre)}"\nfichier = "enc_{fichier.replace("-", "_")}"\ngroupe = "encyclopedie"\n'
                  f'icone = "{icone}"\nordre = 0\nlignes_cachees = true\ngrille = 16\n')
    lignes.append(f'[[quete]]\ncle = "intro"\ntitre = "{t(titre)}"\ntaille = 1.5\nicone = "{icone}"\ntaches = ["checkmark Lu"]\n'
                  f'recompenses = ["xp 2"]\ndescription = """\n{t(intro)}\n"""\n')
    cles = []
    for e in entrees:
        cles.append(e['cle'])
        x = ''
        if e.get('deps'):
            x += 'deps = [' + ', '.join(f'"{d}"' for d in e['deps']) + ']\n'
        if e.get('forme'):
            x += f'forme = "{e["forme"]}"\n'
        if e.get('icone'):
            x += f'icone = "{e["icone"]}"\n'
        tt = ', '.join(f'"{t(k)}"' for k in e['taches'])
        # une collection est exhaustive : les outils du kit de départ en font partie
        x += 'kit_voulu = true\n'
        tit = e['titre'][0].upper() + e['titre'][1:] if e['titre'] and e['titre'][0].isalpha() else e['titre']
        lignes.append(f'[[quete]]\ncle = "{e["cle"]}"\ntitre = "{t(tit)}"\noptionnel = true\n{x}'
                      f'taches = [{tt}]\nrecompenses = ["xp {e.get("xp", 1)}"]\ndescription = """\n{t(e["description"])}\n"""\n')
    deps = ', '.join(f'"{c}"' for c in cles)
    lignes.append(f'[[quete]]\ncle = "complet"\ntitre = "{t(titre_fin)}"\noptionnel = true\ntaille = 1.5\nicone = "{icone_fin}"\nforme = "gear"\n'
                  f'taches = ["checkmark Collection complète"]\nrecompenses = ["xp 20"]\ndeps = [{deps}]\ndescription = """\n{t(fin)}\n"""\n')
    if extra_fin:
        lignes.append(extra_fin)
    return '\n'.join(lignes), len(cles), []


def candidats(ix, filtre):
    """Objets de l'index et du jeu de base retenus par filtre(id), répartis
    entre obtenables et exclus (mod absent, ou inobtenable en chaîne)."""
    ok = obtenables_chaine()
    mods = mods_charges()
    pris, exclus = [], []
    for i in sorted(set(ix['items'])):
        if not filtre(i):
            continue
        if mods is not None and i.split(':')[0] not in mods:
            continue   # mod absent : rien à exclure, l'objet n'existe pas en jeu
        if i in ok:
            pris.append(i)
        else:
            exclus.append((i, "ne s'obtient pas en chaîne (recette dont un ingrédient manque, ni butin ni génération)"))
    return pris, exclus


ARMURE_TAGS = ('minecraft:trimmable_armor', 'forge:armors/helmets', 'forge:armors/chestplates', 'forge:armors/leggings',
               'forge:armors/boots', 'forge:armors')
GROUPES_ARMURE = [
    ('armurerie', '&cArmurerie — base et aventure', None),
    ('armurerie-dimensions', '&cArmurerie — dimensions', {'aether', 'deep_aether', 'aether_redux', 'lost_aether_content', 'umbral_skies',
                                                        'twilightforest', 'blue_skies', 'betterend', 'betternether'}),
    ('armurerie-magie', '&cArmurerie — magie', {'irons_spellbooks', 'hazennstuff'}),
]


def _armures(ix):
    tagues = set()
    for tg in ARMURE_TAGS:
        tagues |= membres_complets(tg)
    def est(i):
        return (fente(i) is not None or i in tagues) and 'horse' not in i and 'moa_armor' not in i and 'wolf' not in i
    return candidats(ix, est)


def chapitre_armurerie(ix, fichier):
    pieces, exclus = _armures(ix)
    autres = set().union(*[g[2] for g in GROUPES_ARMURE if g[2]])
    titre = next(g[1] for g in GROUPES_ARMURE if g[0] == fichier)
    mods_g = next(g[2] for g in GROUPES_ARMURE if g[0] == fichier)
    garde = [p for p in pieces if (p.split(':')[0] in mods_g if mods_g else p.split(':')[0] not in autres)]
    ordre_f = {s: k for k, (s, _) in enumerate(FENTES)}
    ensembles = {}
    for p in garde:
        f = fente(p)
        cle = p[:-(len(f) + 1)] if f else p
        ensembles.setdefault(cle, []).append(p)
    entrees = []
    for cle_e in sorted(ensembles, key=lambda c: (c.split(':')[0], c)):
        ps = sorted(ensembles[cle_e], key=lambda p: ordre_f.get(fente(p), 9))
        mod = cle_e.split(':')[0]
        chap = CHAPITRE_DU_MOD.get(mod)
        renvoi = f" Ses paliers sont au chapitre &7{chap}&r." if chap else ''
        nom_e = nom_ensemble(ix, ps) if len(ps) > 1 else None
        for p in ps:
            desc = f"Pièce d'armure de &b{MOD_AFFICHE.get(mod, mod)}&r." + (f" Elle fait partie de l'{nom_e[0].lower() + nom_e[1:]}." if nom_e else '') + renvoi + " À garder : la livraison n'est pas consommée."
            entrees.append({'cle': p.replace(':', '_'), 'titre': libelle(ix, p, 'objet'), 'taches': [f'item {p}'], 'icone': p, 'description': desc})
        if nom_e:
            entrees.append({'cle': 'ensemble_' + cle_e.replace(':', '_'), 'titre': nom_e, 'taches': [f'item {p}' for p in ps],
                            'icone': ps[min(1, len(ps) - 1)], 'deps': [p.replace(':', '_') for p in ps], 'forme': 'hexagon', 'xp': 5,
                            'description': f"Toutes les pièces de l'{nom_e[0].lower() + nom_e[1:]} ({len(ps)}), ensemble dans l'inventaire."})
    extra = ''
    if fichier == 'armurerie':
        ext = ', '.join(f'"enc_{g[0].replace("-", "_")}/complet"' for g in GROUPES_ARMURE if g[0] != 'armurerie')
        extra = ('[[quete]]\ncle = "toute_armurerie"\ntitre = "&c&lToute l\'Armurerie"\noptionnel = true\ntaille = 2.0\nforme = "gear"\n'
                 'icone = "minecraft:netherite_chestplate"\ndeps = ["complet"]\n'
                 f'deps_externes = [{ext}]\ntaches = ["checkmark Toute l\'Armurerie"]\nrecompenses = ["xp 50"]\n'
                 'description = """\nLes trois chapitres de l\'Armurerie complets : chaque pièce d\'armure du pack que ce serveur permet d\'obtenir.\n"""\n')
    intro = (f"Chaque pièce d'armure {'des mods de base et d' + chr(39) + 'aventure' if fichier == 'armurerie' else ('des dimensions' if 'dimensions' in fichier else 'des mods de magie')}, "
             "une quête par pièce, et une quête par ensemble complet. Une quête se valide en ayant la pièce dans l'inventaire ; rien n'est consommé.\n\n"
             "Seules les pièces qu'une recette, un butin ou la génération donnent vraiment sur ce serveur sont là. Les paliers de chaque mod, eux, sont dans son chapitre.")
    texte, n, _ = chapitre_collection(fichier, titre, 'minecraft:iron_chestplate', 'minecraft:netherite_chestplate', intro, entrees,
                                      '&7Tout le chapitre', "Toutes les pièces et tous les ensembles de ce chapitre.", extra)
    return texte, n, [e for e in exclus if (e[0].split(':')[0] in mods_g if mods_g else e[0].split(':')[0] not in autres)]


TYPES_ARMES = [
    ('epees', '&cÉpées', 'Toutes les épées', r'_(sword|katana|rapier|cutlass|blade|saber|sabre|greatsword|longsword|claymore|flamberge)$', ('minecraft:swords',), 'minecraft:iron_sword', 'minecraft:netherite_sword', 'Épée'),
    ('pioches', '&7Pioches', 'Toutes les pioches', r'_pickaxe$', ('minecraft:pickaxes',), 'minecraft:iron_pickaxe', 'minecraft:netherite_pickaxe', 'Pioche'),
    ('haches', '&7Haches', 'Toutes les haches', r'(?<!pick)_axe$', ('minecraft:axes',), 'minecraft:iron_axe', 'minecraft:netherite_axe', 'Hache'),
    ('pelles', '&7Pelles', 'Toutes les pelles', r'_shovel$', ('minecraft:shovels',), 'minecraft:iron_shovel', 'minecraft:netherite_shovel', 'Pelle'),
    ('houes', '&7Houes', 'Toutes les houes', r'_hoe$', ('minecraft:hoes',), 'minecraft:iron_hoe', 'minecraft:netherite_hoe', 'Houe'),
    ('armes-distance', '&cArmes à distance', 'Toutes les armes à distance', r'_(bow|crossbow|trident|longbow|shortbow|blowgun|dart_shooter|slingshot)$', ('forge:tools/bows', 'forge:tools/crossbows', 'forge:tools/tridents'), 'minecraft:bow', 'minecraft:crossbow', 'Arme à distance'),
    ('boucliers', '&7Boucliers', 'Tous les boucliers', r'_(shield|targe)$', ('forge:tools/shields',), 'minecraft:shield', 'minecraft:shield', 'Bouclier'),
    ('armes-autres', '&cAutres armes et outils', 'Toutes les autres armes', r'_(hammer|spear|lance|scythe|sickle|dagger|mace|halberd|glaive|staff|knife|cleaver|battleaxe|warhammer|whip)$', ('forge:tools/knives',), 'minecraft:mace' , 'minecraft:netherite_sword', 'Arme'),
]


def _armes_par_type(ix):
    pris_tous, res, exclus_tous = set(), {}, {}
    for f, _, _, rx, tags, *_ in TYPES_ARMES:
        tagues = set()
        for tg in tags:
            tagues |= membres_complets(tg)
        p, e = candidats(ix, lambda i, rx=rx, tagues=tagues: (re.search(rx, i) is not None or i in tagues) and 'horse' not in i)
        res[f] = [i for i in p if i not in pris_tous]
        exclus_tous[f] = [x for x in e if x[0] not in pris_tous]
        pris_tous |= set(res[f])
    return res, exclus_tous


def chapitre_armes(ix, fichier):
    res, exclus = _armes_par_type(ix)
    spec = next(s for s in TYPES_ARMES if s[0] == fichier)
    _, titre, titre_fin, _, _, icone, icone_fin, genre = spec
    if icone not in ix['items']:
        icone = 'minecraft:iron_sword'
    entrees = []
    for i in sorted(res[fichier], key=lambda i: (i.split(':')[0] != 'minecraft', i.split(':')[0], i)):
        mod = i.split(':')[0]
        chap = CHAPITRE_DU_MOD.get(mod)
        desc = f"{genre} de &b{MOD_AFFICHE.get(mod, mod)}&r." + (f" Ses paliers sont au chapitre &7{chap}&r." if chap else '') + " À garder : la livraison n'est pas consommée."
        entrees.append({'cle': i.replace(':', '_'), 'titre': libelle(ix, i, 'objet'), 'taches': [f'item {i}'], 'icone': i, 'description': desc})
    extra = ''
    if fichier == TYPES_ARMES[-1][0]:
        ext = ', '.join(f'"enc_{s[0].replace("-", "_")}/complet"' for s in TYPES_ARMES[:-1])
        extra = ('[[quete]]\ncle = "tout_arsenal"\ntitre = "&c&lTout l\'arsenal"\noptionnel = true\ntaille = 2.0\nforme = "gear"\n'
                 'icone = "minecraft:netherite_sword"\ndeps = ["complet"]\n'
                 f'deps_externes = [{ext}]\ntaches = ["checkmark Tout l\'arsenal"]\nrecompenses = ["xp 50"]\n'
                 'description = """\nÉpées, pioches, haches, pelles, houes, armes à distance, boucliers et le reste : chaque arme et chaque outil du pack que ce serveur permet d\'obtenir.\n"""\n')
    intro = (f"{titre_fin.replace('Toutes les ', 'Chaque ').replace('Tous les ', 'Chaque ').rstrip('s')} du pack, mod par mod, une quête par objet. "
             "Une quête se valide en ayant l'objet dans l'inventaire ; rien n'est consommé. Seuls les objets qu'une recette, un butin ou la génération donnent vraiment sur ce serveur sont là.")
    texte, n, _ = chapitre_collection(fichier, titre, icone, icone_fin if icone_fin in ix['items'] else icone, intro, entrees,
                                      f'&7{titre_fin}', f"{titre_fin} de ce chapitre réunies.", extra)
    return texte, n, exclus[fichier]


CHAPITRES = {'bestiaire-overworld': bestiaire_overworld, 'bestiaire-nether-end': bestiaire_nether_end,
             'bestiaire-dimensions': bestiaire_dimensions,
             'biomes-overworld': biomes_overworld, 'biomes-nether-end': biomes_nether_end,
             'biomes-dimensions': biomes_dimensions,
             'structures-vanilla': structures_vanilla, 'structures-repurposed': structures_repurposed,
             'structures-moogs': structures_moogs, 'structures-donjons-villages': structures_villages,
             'structures-ruines': structures_ruines, 'structures-mondes': structures_mondes,
             'gastronomie': gastronomie, 'disques': disques, 'trophees': trophees, 'minerais': minerais, 'bois': bois,
             'armurerie': lambda ix, e, n: chapitre_armurerie(ix, 'armurerie'),
             'armurerie-dimensions': lambda ix, e, n: chapitre_armurerie(ix, 'armurerie-dimensions'),
             'armurerie-magie': lambda ix, e, n: chapitre_armurerie(ix, 'armurerie-magie'),
             **{s[0]: (lambda f: (lambda ix, e, n: chapitre_armes(ix, f)))(s[0]) for s in TYPES_ARMES},
             'arsenal': arsenal, 'atelier-create': atelier_create, 'herbier': herbier}


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
