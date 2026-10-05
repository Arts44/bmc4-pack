#!/usr/bin/env python3
"""Obtention en chaîne (BMC-89, 5 octobre 2026).

    python3 chaine.py mod:objet [mod:objet ...]   # explique chaque objet

obtenables.py dit si un objet sort d'une recette ; il ne dit pas si les
ingrédients de cette recette s'obtiennent eux-mêmes. Ici, un objet est
obtenable en chaîne s'il sort d'un butin ou de la génération, ou d'une
recette dont chaque ingrédient (objet, ou balise dont un membre au moins)
est lui-même obtenable en chaîne. Point fixe sur tout le pack.

Une recette dont on ne lit aucun ingrédient (type déclaré par le code,
comme Blue Skies) compte comme obtenable : on ne sait pas la lire, on ne
l'accuse pas. Les balises sont complètes (obtenables.py les lit dans le
jeu de base, le jar Forge, les mods et les datapacks) : une balise sans
membre ne fournit rien. Limite connue : ce qui s'obtient autrement que par recette,
butin ou génération (troc, seau, interaction) n'est connu que par la
liste OBTENUS_AUTREMENT de generer.py.
"""
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
FORGE = os.path.expanduser('~/curseforge/minecraft/Install/libraries/net/minecraftforge/forge/'
                           '1.20.1-47.4.20/forge-1.20.1-47.4.20-universal.jar')


def charger():
    o = json.load(open(os.path.join(ICI, '..', 'index', 'obtenables.json'), encoding='utf-8'))
    # Balises complètes (jeu de base, jar Forge, mods, Paxi), lues par obtenables.py
    tm = {k: list(v) for k, v in o.get('tags', {}).items()}
    return o, tm


def membres(tm, t, vus=None):
    vus = vus or set()
    if t in vus:
        return set()
    vus.add(t)
    out = set()
    for v in tm.get(t, []):
        v = v['id'] if isinstance(v, dict) else v
        out |= membres(tm, v[1:], vus) if v.startswith('#') else {v}
    return out


def fermeture(extra=()):
    o, tm = charger()
    ok = set(o['butin']) | set(o['monde']) | set(extra)
    graphe = o['graphe']
    for r in o['recette']:
        if r not in graphe:
            ok.add(r)          # recette lue sans ingrédients lisibles
    cache = {}

    def satisfait(alts):
        for a in alts:
            if a.startswith('#'):
                m = cache.setdefault(a, membres(tm, a[1:]))
                if m & ok:            # balise vide : rien ne la remplit
                    return True
            elif a in ok:
                return True
        return False

    change = True
    while change:
        change = False
        for r, variantes in graphe.items():
            if r in ok:
                continue
            if any(all(satisfait(alts) for alts in v) for v in variantes):
                ok.add(r)
                change = True
    return ok, graphe


if __name__ == '__main__':
    sys.path.insert(0, ICI)
    from generer import Verif
    ok, graphe = fermeture(Verif.OBTENUS_AUTREMENT)
    for i in sys.argv[1:]:
        print(i, 'OBTENABLE' if i in ok else 'NON OBTENABLE en chaîne')
        if i not in ok:
            for v in graphe.get(i, []):
                print('   recette :', ' + '.join('/'.join(a) + ('' if any(x in ok or x.startswith('#') for x in a) else ' ✗') for a in v))
