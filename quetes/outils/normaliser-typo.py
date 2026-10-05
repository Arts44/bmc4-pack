#!/usr/bin/env python3
"""Typographie française dans les données du livre : espace insécable
(U+00A0) avant : ; ! ? et à l'intérieur des « ».

    python3 normaliser-typo.py          # réécrit les TOML de ../donnees
    python3 normaliser-typo.py --essai  # montre ce qui changerait

Règles, les mêmes que controles.py :
  · un « : » collé entre deux caractères d'identifiant (mod:objet, 10:30)
    n'est pas une ponctuation ;
  · « !dragon » (commande du bot) n'est pas une ponctuation ;
  · les lignes de commentaire (#) et les lignes d'identifiants (cle,
    fichier, icone, deps, recompenses…) ne sont pas touchées ;
  · dans une ligne taches = [...], seuls les libellés après « checkmark »
    ou après le nombre d'un « tag » sont concernés — l'exception des
    identifiants suffit à protéger le reste.
"""
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.path.join(ICI, '..', 'donnees')
NBSP = ' '
CLES_INTOUCHEES = re.compile(r'^\s*(cle|fichier|groupe|icone|deps|recompenses|ordre|taille|forme|pos|exigence|optionnel|boss|repetable|delai_s|racine|doublon_voulu|kit_voulu|cache_avant|grille|lignes_cachees|apparition|titre_court)\s*=')


NOMS_PROPRES = ('Aether: Treasure Reforging', 'Dragon Mounts: Legacy', 'CC: Tweaked', 'Snow! Real Magic!')


def normaliser_ligne(l):
    if l.lstrip().startswith('#') or CLES_INTOUCHEES.match(l):
        return l
    garde = {}
    for i, n in enumerate(NOMS_PROPRES):
        if n in l:
            garde[f'\x00{i}\x00'] = n
            l = l.replace(n, f'\x00{i}\x00')
    l = _normaliser(l)
    for k, n in garde.items():
        l = l.replace(k, n)
    return l


def _normaliser(l):
    out = []
    i = 0
    while i < len(l):
        ch = l[i]
        if ch in ':;!?':
            avant = l[i - 1] if i else ''
            apres = l[i + 1] if i + 1 < len(l) else ''
            ident = ch == ':' and re.match(r'[a-z0-9_]', avant or ' ') and re.match(r'[a-z0-9_/.#]', apres or ' ')
            bot = ch == '!' and apres.isalpha()
            if not ident and not bot and avant and avant not in '?!':
                if avant == ' ':
                    out[-1] = NBSP
                elif avant != NBSP and not avant.isspace():
                    out.append(NBSP)
        out.append(ch)
        i += 1
    s = ''.join(out)
    s = re.sub(r'«(?=\S)', '«' + NBSP, s)
    s = re.sub(r'« (?=\S)', '«' + NBSP, s)
    s = re.sub(r'(?<=\S)»', NBSP + '»', s)
    s = re.sub(r'(?<=\S) »', NBSP + '»', s)
    return s


def main(essai):
    change = 0
    for racine, _, fichiers in os.walk(DONNEES):
        for f in sorted(fichiers):
            if not f.endswith('.toml'):
                continue
            p = os.path.join(racine, f)
            src = open(p, encoding='utf-8').read()
            lignes = src.split('\n')
            nouv = [normaliser_ligne(l) for l in lignes]
            n = sum(1 for a, b in zip(lignes, nouv) if a != b)
            if n:
                change += n
                print(f"{os.path.relpath(p, DONNEES)} : {n} ligne(s)")
                if not essai:
                    open(p, 'w', encoding='utf-8').write('\n'.join(nouv))
    print(f"{change} ligne(s) {'à changer' if essai else 'changées'}")


if __name__ == '__main__':
    main('--essai' in sys.argv)
