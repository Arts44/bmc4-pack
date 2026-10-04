#!/usr/bin/env python3
"""Génère les chapitres de l'Encyclopédie (cahier §9.2) sous forme de
fichiers TOML dans ../donnees/encyclopedie/, à partir de l'index des jars.

    python3 encyclopedie.py bestiaire-overworld
    python3 encyclopedie.py --tous

Le TOML produit est ensuite lu par generer.py comme n'importe quel
chapitre écrit à la main. Il est REGÉNÉRÉ à chaque passage : les textes
spécifiques se mettent dans notes/<chapitre>.toml (une entrée par
identifiant), jamais dans le TOML généré.

Garde-fou : ce qui n'apparaît pas sur le serveur est dans
exclusions.toml, avec la raison, et ne devient pas une quête.
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
            ix.setdefault(k, {}).update(v)
    return ix


def t(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def nom_fr(ix, ident):
    return ix['fr'].get(ident) or ix['entities'].get(ident) or ix['items'].get(ident) or ident.split(':', 1)[1]


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


# Créatures vanilla qui ne vivent pas dans l'Overworld (Bestiaire Nether/End).
VANILLA_HORS_OVERWORLD = {
    'minecraft:blaze', 'minecraft:ghast', 'minecraft:hoglin', 'minecraft:magma_cube', 'minecraft:piglin',
    'minecraft:piglin_brute', 'minecraft:strider', 'minecraft:wither_skeleton', 'minecraft:zoglin',
    'minecraft:zombified_piglin', 'minecraft:endermite', 'minecraft:shulker', 'minecraft:ender_dragon',
    'minecraft:wither', 'minecraft:happy_ghast',
    # Alex's Mobs : créatures du Nether et de l'End, pour le Bestiaire Nether et End.
    'alexsmobs:bone_serpent', 'alexsmobs:crimson_mosquito', 'alexsmobs:warped_toad', 'alexsmobs:warped_mosco',
    'alexsmobs:straddler', 'alexsmobs:stradpole', 'alexsmobs:soul_vulture', 'alexsmobs:mimicube',
    'alexsmobs:laviathan', 'alexsmobs:cosmaw', 'alexsmobs:enderiophage', 'alexsmobs:endergrade',
    'alexsmobs:cosmic_cod', 'alexsmobs:void_worm',
}

MODELES = {
    'minecraft': "Créature du jeu de base.",
    'alexsmobs': "Créature d'&bAlex's Mobs&r, l'un des mods de faune du pack.",
    'friendsandfoes': "Créature de &bFriends & Foes&r, les candidats des votes de créature Minecraft.",
    'mowziesmobs': "Créature de &bMowzie's Mobs&r : des monstres rares et dangereux, souvent gardiens d'un lieu.",
    'guardvillagers': "Créature de &bGuard Villagers&r : les villages se défendent.",
    'conjurer_illager': "Créature de &bThe Conjurer&r.",
    'illagerinvasion': "Illageois d'&bIllager Invasion&r : les raids et les avant-postes ont de nouveaux visages.",
    'takesapillage': "Illageois de &bTakes a Pillage&r.",
    'goblintraders': "Marchand de &bGoblin Traders&r : il vend des objets rares contre de l'émeraude et plus.",
    'quark': "Créature de &bQuark&r.",
    'villagersplus': "Villageois de &bVillagersPlus&r.",
}


def bestiaire_overworld(ix, exclusions, notes):
    mods = ['minecraft', 'alexsmobs', 'friendsandfoes', 'mowziesmobs', 'guardvillagers', 'conjurer_illager',
            'illagerinvasion', 'takesapillage', 'goblintraders', 'quark']
    lignes = []
    lignes.append('# GÉNÉRÉ par outils/encyclopedie.py — ne pas éditer : notes/bestiaire-overworld.toml pour les textes.\n')
    lignes.append('[chapitre]\ntitre = "&7Bestiaire — Overworld"\nfichier = "enc_bestiaire_overworld"\ngroupe = "encyclopedie"\nicone = "minecraft:zombie_head"\nordre = 0\nlignes_cachees = true\n')
    lignes.append('[[quete]]\ncle = "intro"\ntitre = "&7Bestiaire — Overworld"\ntaille = 1.5\nicone = "minecraft:zombie_head"\ntaches = ["checkmark Lu"]\nrecompenses = ["xp 2"]\ndescription = """\nChaque créature de l\'Overworld, du jeu de base et des mods de faune. Une quête se valide en &lregardant&r la créature : il suffit de l\'avoir devant soi.\n\nCe chapitre est facultatif, un catalogue à remplir au fil des rencontres. La dernière quête récompense le bestiaire complet.\n"""\n')
    exclues = []
    cles = []
    for ent, oeuf in mobs_avec_oeuf(ix, mods):
        if ent in VANILLA_HORS_OVERWORLD:
            continue
        if ent in exclusions:
            exclues.append((ent, exclusions[ent]))
            continue
        mod = ent.split(':')[0]
        nom = nom_fr(ix, ent)
        cle = ent.replace(':', '_')
        cles.append(cle)
        note = notes.get(ent, {})
        desc = note.get('description') or MODELES.get(mod, '')
        titre = note.get('titre') or f"Rencontrer {nom}"
        lignes.append(f'[[quete]]\ncle = "{cle}"\ntitre = "{t(titre)}"\nsous_titre = "{t(nom)} — {mod}"\noptionnel = true\nicone = "{oeuf}"\ntaches = ["observation entity {ent}"]\nrecompenses = ["xp 1"]\ndescription = """\n{t(desc)}\n"""\n')
    deps = ', '.join(f'"{c}"' for c in cles)
    lignes.append(f'[[quete]]\ncle = "complet"\ntitre = "&7Tout le bestiaire de l\'Overworld"\ntaille = 1.5\nicone = "minecraft:creeper_head"\nforme = "gear"\ntaches = ["checkmark Bestiaire complet"]\nrecompenses = ["xp 20"]\ndeps = [{deps}]\ndescription = """\nToutes les créatures de l\'Overworld rencontrées. La récompense est symbolique : c\'est la quête qui compte.\n"""\n')
    return '\n'.join(lignes), len(cles), exclues


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
