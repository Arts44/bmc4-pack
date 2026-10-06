#!/usr/bin/env python3
"""Contrôle statique du datapack bmc4-fixes (BMC-90, 6 octobre 2026).

    python3 controle_datapack.py [dossier du datapack]     # défaut : config/datapack/bmc4-fixes

Né d'un défaut réel : le 5 octobre, le commit 412128c a remplacé dans
tick.mcfunction l'appel à raid_tick par l'appel à coeur_tick au lieu de
l'ajouter ; l'arbitrage des raids n'a plus tourné jusqu'au 6. Le contrôle
vérifie :
  1. chaque « function ns:x » (et « schedule function ») vise une fonction
     ou une balise de fonctions qui existe ;
  2. les balises minecraft:tick et minecraft:load existent, et tick appelle
     les fonctions obligatoires (APPELS_TICK) ;
  3. chaque objectif de score utilisé est créé (« scoreboard objectives
     add ») par une fonction atteinte depuis la balise load ;
  4. aucune fonction n'est orpheline (ni atteinte depuis tick ou load, ni
     appelée par une autre) sans raison écrite : un commentaire
     « # orpheline : <raison> » dans la fonction, ou une entrée dans
     appels-externes.toml à côté du datapack (fonctions lancées par le bot en
     RCON ou à la console) — ce fichier garde le datapack identique, octet
     pour octet, à celui du serveur. Un appel d'une fonction à elle-même
     (« schedule function » de sa propre boucle) ne compte pas : il faut
     encore que quelque chose la démarre.

Un outil autonome peut créer son propre objectif avant de s'en servir. Un
défaut réel de la production, qu'on ne corrige pas sur place, se déclare dans
appels-externes.toml ([[connu]] : debut du message, raison) : il reste
affiché comme « connu » et ne bloque pas.
"""
import json
import os
import re
import sys
import tomllib

ICI = os.path.dirname(os.path.abspath(__file__))
DEFAUT = os.path.join(ICI, '..', '..', 'config', 'datapack', 'bmc4-fixes')

# Ce que tick doit appeler, avec la raison.
APPELS_TICK = {
    'bmc4:raid_tick': "l'arbitrage des raids (cinq minutes en spectateur, perte de cœur)",
    'bmc4:coeur_tick': 'le cœur perdu : soins, vie maximale réappliquée après la mort',
}

RE_APPEL = re.compile(r'(?:^|\s)function\s+(#?[a-z0-9_.\-]+:[a-z0-9_./\-]+)')
RE_AJOUT = re.compile(r'scoreboard\s+objectives\s+add\s+(\S+)')
# Objectifs utilisés : scores={a=…,b=…}, et les formes « players … <cible> <objectif> »,
# « score <cible> <objectif> », « operation <c> <o> <op> <c> <o> ».
RE_SCORES = re.compile(r'scores=\{([^}]*)\}')
RE_PLAYERS = re.compile(r'scoreboard\s+players\s+(set|add|remove|reset|get|enable|operation|display)\s+(.*)')
RE_SCORE = re.compile(r'\bscore\s+(\S+)\s+(\S+)')


def fonctions(dp):
    out = {}
    data = os.path.join(dp, 'data')
    for ns in sorted(os.listdir(data)):
        base = os.path.join(data, ns, 'functions')
        for r, _, fs in os.walk(base):
            for f in fs:
                if f.endswith('.mcfunction'):
                    p = os.path.join(r, f)
                    rel = os.path.relpath(p, base)[:-len('.mcfunction')].replace(os.sep, '/')
                    out[f'{ns}:{rel}'] = open(p, encoding='utf-8').read()
    return out


def balises(dp):
    out = {}
    data = os.path.join(dp, 'data')
    for ns in sorted(os.listdir(data)):
        base = os.path.join(data, ns, 'tags', 'functions')
        for r, _, fs in os.walk(base):
            for f in fs:
                if f.endswith('.json'):
                    rel = os.path.relpath(os.path.join(r, f), base)[:-5].replace(os.sep, '/')
                    vals = json.load(open(os.path.join(r, f), encoding='utf-8')).get('values', [])
                    out[f'#{ns}:{rel}'] = [v if isinstance(v, str) else v.get('id') for v in vals]
    return out


def lignes_actives(texte):
    for l in texte.split('\n'):
        s = l.strip()
        if s and not s.startswith('#'):
            yield s


def appels(texte):
    return [m.group(1) for l in lignes_actives(texte) for m in RE_APPEL.finditer(l)]


def objectifs_utilises(texte):
    out = set()
    for l in lignes_actives(texte):
        for m in RE_SCORES.finditer(l):
            for paire in m.group(1).split(','):
                if '=' in paire:
                    out.add(paire.split('=')[0].strip())
        m = RE_PLAYERS.search(l)
        if m:
            verbe, reste = m.group(1), m.group(2).split()
            if verbe == 'operation' and len(reste) >= 5:
                out.update({reste[1], reste[4]})
            elif verbe in ('set', 'add', 'remove', 'get', 'enable') and len(reste) >= 2:
                out.add(reste[1])
            elif verbe == 'reset' and len(reste) >= 2:
                out.add(reste[1])
        for m in RE_SCORE.finditer(l):
            if not l[:m.start()].rstrip().endswith('players'):
                out.add(m.group(2))
    return {o for o in out if re.fullmatch(r'[A-Za-z0-9_.\-+]+', o)}


def atteintes(depart, F, B):
    vus, pile = set(), list(depart)
    while pile:
        x = pile.pop()
        if x in vus:
            continue
        vus.add(x)
        if x.startswith('#'):
            pile.extend(B.get(x, []))
        elif x in F:
            pile.extend(appels(F[x]))
    return vus


def controler(dp=DEFAUT):
    dp = os.path.abspath(dp)
    F, B = fonctions(dp), balises(dp)
    err = []
    # 1. appels vers des fonctions ou balises existantes
    for f, t in sorted(F.items()):
        for a in appels(t):
            if a not in F and a not in B:
                err.append(f"{f} : appelle « {a} », qui n'existe pas")
    # 2. tick et load
    for b in ('#minecraft:tick', '#minecraft:load'):
        if b not in B:
            err.append(f"balise {b} absente : rien n'est lancé")
    depuis_tick = atteintes(['#minecraft:tick'], F, B)
    for f, raison in APPELS_TICK.items():
        if f not in depuis_tick:
            err.append(f"tick n'atteint pas {f} ({raison})")
    # 3. objectifs créés par une fonction atteinte depuis load
    depuis_load = atteintes(['#minecraft:load'], F, B)
    crees = {m.group(1) for f in depuis_load if f in F for l in lignes_actives(F[f]) for m in RE_AJOUT.finditer(l)}
    for f, t in sorted(F.items()):
        propres = {m.group(1) for l in lignes_actives(t) for m in RE_AJOUT.finditer(l)}
        for o in sorted(objectifs_utilises(t) - crees - propres):
            err.append(f"{f} : objectif « {o} » utilisé, jamais créé depuis load")
    # 4. orphelines
    ext = os.path.join(os.path.dirname(dp), 'appels-externes.toml')
    conf = tomllib.load(open(ext, 'rb')) if os.path.exists(ext) else {}
    externes = conf.get('fonction', {})
    for f, r in externes.items():
        if f not in F:
            err.append(f"appels-externes.toml : « {f} » n'existe pas dans le datapack")
        elif not str(r).strip():
            err.append(f"appels-externes.toml : « {f} » sans raison")
    appelees = depuis_tick | depuis_load | {a for f, t in F.items() for a in appels(t) if a != f}
    for f, t in sorted(F.items()):
        if f in appelees or f in externes or re.search(r'(?m)^#\s*orpheline\s*:\s*\S', t):
            continue
        err.append(f"{f} : orpheline (ni tick, ni load, ni appel) — écrire « # orpheline : raison » "
                   "ou l'inscrire dans appels-externes.toml")
    connus = conf.get('connu', [])
    graves, avoues = [], []
    for e in err:
        c = next((k for k in connus if e.startswith(k['debut'])), None)
        (avoues if c else graves).append(e if not c else f"{e}  [connu : {c['raison']}]")
    for k in connus:
        if not any(e.startswith(k['debut']) for e in err):
            graves.append(f"appels-externes.toml : défaut connu « {k['debut']} » introuvable — corrigé ? retirer l'entrée")
    return graves, avoues


if __name__ == '__main__':
    graves, avoues = controler(sys.argv[1] if len(sys.argv) > 1 else DEFAUT)
    for e in avoues:
        print('connu   ' + e)
    for e in graves:
        print('DÉFAUT  ' + e)
    print(f"datapack : {len(graves)} défaut(s), {len(avoues)} connu(s)")
    sys.exit(1 if graves else 0)
