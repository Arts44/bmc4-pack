#!/usr/bin/env python3
"""Test de bout en bout, hors production (BMC-89, 6 octobre 2026).

    python3 quetes/tests/test_retroactivite.py [dossier de l'ancien livre]

Rejoue la première connexion d'Arts_Vio (ses progrès Twilight réels, lus sur
le serveur) avec outils/simuler_connexion.py, fidèle au jar FTB Quests
2001.4.22. Sur le livre actuel, toute la progression Twilight prouvée par
ses progrès doit se cocher sans rien refaire. Avec le dossier du livre
déployé le 5 octobre (git archive 3411210 quetes/livre), le simulateur doit
reproduire ce qu'Arts_Vio a vu en production : le portail seul.
"""
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, '..', 'outils'))
from simuler_connexion import simuler  # noqa: E402

JOUEUR = json.load(open(os.path.join(ICI, 'arts_vio_twilight.json'), encoding='utf-8'))
ATTENDU = {  # quêtes du chapitre Twilight — progression que ses progrès prouvent
    '49F68B8AEB0F5E46',  # le portail
}


def cochees(dossier, chapitre='monde_twilight_progression'):
    p, _ = simuler(dossier, JOUEUR)
    return {q['id']: q['title'] for q in p.q if q['_chapitre'] == chapitre and p.finie(q)}, p


def main():
    ok = True
    neuf, p = cochees(os.path.join(ICI, '..', 'livre'))
    # Chaque quête dont toutes les tâches sont des progrès acquis doit être cochée.
    for q in p.q:
        if q['_chapitre'] != 'monde_twilight_progression':
            continue
        prouvee = all(t['type'] == 'advancement' and t['advancement'] in JOUEUR['advancements'] for t in q['tasks'])
        if prouvee and q['id'] not in neuf:
            print(f"ÉCHEC : « {q['title']} » est prouvée par ses progrès mais reste ouverte")
            ok = False
        if not prouvee and q['id'] in neuf:
            print(f"ÉCHEC : « {q['title']} » se coche sans preuve")
            ok = False
    print(f"livre actuel : {len(neuf)} quêtes Twilight cochées à la connexion")
    if len(sys.argv) > 1:
        ancien, _ = cochees(sys.argv[1])
        if set(ancien) != ATTENDU:
            print(f"ÉCHEC : sur l'ancien livre, le simulateur coche {sorted(ancien.values())}, la production n'avait coché que le portail")
            ok = False
        else:
            print("ancien livre : le portail seul, comme en production le 5 octobre")
    print('OK' if ok else 'ÉCHEC')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
