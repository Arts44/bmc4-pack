#!/usr/bin/env python3
"""Test de bout en bout, hors production (BMC-89, 6 octobre 2026).

    python3 quetes/tests/test_retroactivite.py [--3411210 <livre>] [--b0655e8 <livre>]

Rejoue des premières connexions avec outils/simuler_connexion.py, fidèle au
jar FTB Quests 2001.4.22, sur le livre actuel (quetes/livre) :

  1. Arts_Vio (ses progrès Twilight réels, lus sur le serveur) : toute quête
     Twilight prouvée par ses progrès se coche, et rien d'autre.
  2. Un joueur qui a enter_aether, bronze_dungeon et silver_dungeon, rien en
     poche : la Reine des Valkyries se coche.
  3. Un joueur sans œuf qui regarde son dragon : « Un œuf de dragon » et
     « Faire éclore » se cochent, le chapitre s'ouvre.

Avec les anciens livres (git archive <commit> quetes/livre), le simulateur
doit retrouver les défauts : sur 3411210 (déployé le 5 octobre), la Twilight
d'Arts_Vio s'arrête au portail, comme en production ; sur b0655e8, la Reine
des Valkyries reste ouverte (l'Aether attendait la glowstone en poche).
"""
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, '..', 'outils'))
from simuler_connexion import simuler  # noqa: E402

LIVRE = os.path.join(ICI, '..', 'livre')


def joueur(nom):
    return json.load(open(os.path.join(ICI, nom + '.json'), encoding='utf-8'))


def cochees(dossier, j, chapitre):
    p, _ = simuler(dossier, j)
    return {q['title'] for q in p.q if q['_chapitre'] == chapitre and p.finie(q)}, p


def main(argv):
    anciens = dict(zip(argv[::2], argv[1::2]))
    ok = True

    def verifier(cond, msg):
        nonlocal ok
        print(('  ok    ' if cond else '  ÉCHEC ') + msg)
        ok = ok and cond

    # 1. Arts_Vio, Twilight
    arts = joueur('arts_vio_twilight')
    faites, p = cochees(LIVRE, arts, 'monde_twilight_progression')
    print(f"Arts_Vio — Twilight : {len(faites)} quêtes cochées à la connexion")
    for q in p.q:
        if q['_chapitre'] != 'monde_twilight_progression':
            continue
        prouvee = all(t['type'] == 'advancement' and t['advancement'] in arts['advancements'] for t in q['tasks'])
        if prouvee != (q['title'] in faites):
            verifier(False, f"« {q['title']} » : prouvée={prouvee}, cochée={q['title'] in faites}")
    verifier('&2Le Plateau final' in faites or any('Plateau final' in t for t in faites), "le Plateau final est coché")

    # 2. Aether sans objet
    aether = joueur('aether_sans_objet')
    faites, _ = cochees(LIVRE, aether, 'monde_aether')
    print(f"Aether sans objet : {sorted(faites)}")
    verifier(any('Reine des Valkyries' in t for t in faites), "la Reine des Valkyries est cochée")

    # 3. Dragon sans œuf
    dragon = joueur('dragon_sans_oeuf')
    faites, _ = cochees(LIVRE, dragon, 'monde_dragons')
    print(f"Dragon sans œuf : {sorted(faites)}")
    verifier(any('éclore' in t for t in faites), "« Faire éclore » est cochée, le chapitre s'ouvre")

    # Anciens livres : le simulateur retrouve les défauts constatés
    if '--3411210' in anciens:
        faites, _ = cochees(anciens['--3411210'], arts, 'monde_twilight_progression')
        verifier(len(faites) == 1 and any('portail' in t for t in faites),
                 f"3411210 : Twilight d'Arts_Vio arrêtée au portail, comme en production ({len(faites)} cochée)")
    if '--b0655e8' in anciens:
        faites, _ = cochees(anciens['--b0655e8'], aether, 'monde_aether')
        verifier(not any('Reine des Valkyries' in t for t in faites),
                 "b0655e8 : la Reine des Valkyries reste ouverte sans glowstone en poche")
        faites, _ = cochees(anciens['--b0655e8'], dragon, 'monde_dragons')
        verifier(not any('éclore' in t for t in faites), "b0655e8 : sans œuf, le chapitre des Dragons reste fermé")
    print('OK' if ok else 'ÉCHEC')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main(sys.argv[1:])
