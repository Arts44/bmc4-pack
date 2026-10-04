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

ICI = os.path.dirname(os.path.abspath(__file__))
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
    return ix


def t(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def nom_fr(ix, ident):
    return (ix['fr'].get(ident) or ix['entities'].get(ident) or ix['items'].get(ident)
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
    return nom_fr(ix, b)


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
    if note.get('apparition'):
        lignes.append('Apparaît : ' + note['apparition'] + '.')
        voie = True
    butin = [b for b in ix['apparitions']['butin'].get(ent, []) if not b.startswith('#')]
    if butin:
        lignes.append('Butin : ' + ', '.join(dict.fromkeys(nom_fr(ix, b) for b in butin)) + '.')
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


def chapitre_bestiaire(ix, exclusions, notes, mods, hors, fichier, titre, icone, icone_fin, intro):
    lignes = [f'# GÉNÉRÉ par outils/encyclopedie.py — ne pas éditer : notes/{fichier}.toml pour les textes.\n']
    lignes.append(f'[chapitre]\ntitre = "{t(titre)}"\nfichier = "enc_{fichier.replace("-", "_")}"\ngroupe = "encyclopedie"\n'
                  f'icone = "{icone}"\nordre = 0\nlignes_cachees = true\ngrille = 16\n')
    lignes.append(f'[[quete]]\ncle = "intro"\ntitre = "{t(titre)}"\ntaille = 1.5\nicone = "{icone}"\ntaches = ["checkmark Lu"]\n'
                  f'recompenses = ["xp 2"]\ndescription = """\n{t(intro)}\n"""\n')
    exclues, cles, sans_voie = [], [], []
    for ent, oeuf in mobs_avec_oeuf(ix, mods):
        if ent in hors:
            continue
        if ent in exclusions:
            exclues.append((ent, exclusions[ent]))
            continue
        mod = ent.split(':')[0]
        nom = nom_fr(ix, ent)
        cle = ent.replace(':', '_')
        cles.append(cle)
        note = notes.get(ent, {})
        lignes_fiche, voie = fiche(ent, ix, note)
        if not voie:
            sans_voie.append(ent)
        desc = ' '.join([MODELES.get(mod, '')] + lignes_fiche)
        if note.get('description'):
            desc += '\n\n' + note['description']
        titre_q = note.get('titre') or f"Rencontre : {nom}"
        lignes.append(f'[[quete]]\ncle = "{cle}"\ntitre = "{t(titre_q)}"\nsous_titre = "{t(nom)} — {mod}"\noptionnel = true\n'
                      f'icone = "{oeuf}"\ntaches = ["observation entity {ent}"]\nrecompenses = ["xp 1"]\ndescription = """\n{t(desc)}\n"""\n')
    if sans_voie:
        raise SystemExit(f"{fichier} : {len(sans_voie)} créature(s) sans voie d'apparition vérifiée — à documenter "
                         f"(notes, clé apparition) ou à exclure (exclusions.toml) :\n  " + '\n  '.join(sans_voie))
    deps = ', '.join(f'"{c}"' for c in cles)
    lignes.append(f'[[quete]]\ncle = "complet"\ntitre = "&7Tout le chapitre"\ntaille = 1.5\nicone = "{icone_fin}"\nforme = "gear"\n'
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


CHAPITRES = {'bestiaire-overworld': bestiaire_overworld}


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
            f.write(texte)
        print(f"{c} : {n} entrées, {len(exclues)} exclue(s)")
        for e, r in exclues:
            print(f"   exclu {e} — {r}")


if __name__ == '__main__':
    main(sys.argv[1:])
