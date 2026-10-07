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
     encore que quelque chose la démarre ;
  5. une commande de mod qui prend un joueur (MODS_JOUEUR) n'est pas appelée
     avec un @s ou un @p nu (BMC-91, 6 octobre : « ftbranks add @s » a fait
     rejeter toute la fonction au chargement, « Only players may be affected
     by this command, but the provided selector includes entities » ; ces
     mods lisent le joueur en GameProfileArgument, qui n'exempte pas @s comme
     le fait EntityArgument). Le sélecteur doit porter type=minecraft:player ;
  6. chaque fonction que les scripts KubeJS lancent (« function bmc4:… » dans
     config/serveur/kubejs/server_scripts/*.js, à côté du dépôt) existe, et
     compte comme appelée : /prestige lance devis, confirmer, g_liste…
     (BMC-91, 6 octobre) ;
  7. chaque rang que le datapack ajoute (« ftbranks add … <rang> ») existe dans
     config/serveur/ftbranks/ranks.snbt et ranks-sans-kubejs.snbt, sans clé
     « condition » (ou « default ») : FTB Ranks n'active un rang ajouté à la
     main qu'avec la condition par défaut (RankImpl.java:32-35). Le 6 octobre,
     « condition: "rank_added" » sans champ « rank » rendait les quinze rangs
     inactifs : achetés, mais sans aucune permission ;
  8. les scripts KubeJS n'emploient aucune des formes Java qui n'existent pas
     au runtime sur ce serveur (FORMES_ABSENTES), relevées dans latest.log le
     6 octobre : un mixin de KubeJS renomme la méthode (@RemapForJS), ou la
     propriété n'est pas ce que l'on croit ;
  9. un opérateur n'a que ce que son rang donne (décision d'Arthur, 6 octobre
     au soir) : dans les scripts KubeJS, estOp( ou isOp( n'apparaît que dans
     sa définition (« estOp: ») et dans le bloc de /prestige diagnostic (après
     « ServerEvents.commandRegistry ») ; dans ranks.snbt et
     ranks-sans-kubejs.snbt, bmc4_staff ne porte aucune clé command.* ni
     ftbessentials.*.

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

# Les commandes de mods qui prennent un joueur, et le sélecteur qui y est refusé.
MODS_JOUEUR = ('ftbranks', 'ftbquests', 'ftbteams', 'ftbchunks', 'ftblibrary', 'ftbessentials')
RE_MOD = re.compile(r'(?:^|\brun\s+)(' + '|'.join(MODS_JOUEUR) + r')\b(.*)$')
RE_SELECTEUR = re.compile(r'@[sp](\[[^\]]*\])?')


def selecteurs_nus(ligne):
    """Les @s / @p d'une commande de mod qui ne se limitent pas aux joueurs."""
    m = RE_MOD.search(ligne)
    if not m:
        return []
    return [x.group(0) for x in RE_SELECTEUR.finditer(m.group(2))
            if not re.search(r'type=(minecraft:)?player\b', x.group(1) or '')]


# Formes Java absentes au runtime (KubeJS 2001.6.5, Rhino 2001.2.3, Forge), et la
# forme qui existe : seulement celles que latest.log a prouvées le 6 octobre
# (« Cannot find function getEntity in object DamageSource », « … getUUID … »,
# « Cannot call property dimension … it is "object" »). Source des remplaçantes :
# les mixins de KubeJS (@RemapForJS), lus dans le jar.
FORMES_ABSENTES = {
    r'\.getUUID\(': "getUuid() (EntityMixin.java:79)",
    r'getSource\(\)\.getEntity\(': "getSource().getActual() (DamageSourceMixin.java:24)",
    r'\.dimension\(\)': "getDimensionKey() (LevelMixin.java:32) ; level.dimension est un ResourceLocation",
    # Prouvées absentes par /prestige diagnostic le 6 octobre au soir (voies 1 à 3 de /nickname) :
    r'getProfileCache\(': "usercache.json par JsonIO, ou FTB Teams getKnownPlayerTeams()",
    r'\.profileCache\b': "usercache.json par JsonIO, ou FTB Teams getKnownPlayerTeams()",
    r'm_129927_': "usercache.json par JsonIO, ou FTB Teams getKnownPlayerTeams()",
    # Tout nom SRG brut : Rhino ne les traduit pas sur ce serveur (7 octobre, 16 h 03 :
    # « Cannot find function m_230896_ in object …CommandSourceStack », bmc4_triche.js).
    r'\b[mf]_\d+_\b': "le nom Mojang (getPlayer, hasPermission, connection…), que Rhino traduit",
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
    # 5. sélecteurs nus dans une commande de mod qui prend un joueur
    for f, t in sorted(F.items()):
        for n, l in enumerate(t.split('\n'), 1):
            if l.strip().startswith('#'):
                continue
            for sel in selecteurs_nus(l):
                err.append(f"{f} ligne {n} : « {sel} » dans une commande de mod qui prend un joueur — "
                           "écrire @s[type=minecraft:player] (sinon la fonction entière est rejetée au chargement)")
    # 6. fonctions lancées par KubeJS
    scripts = os.path.normpath(os.path.join(os.path.dirname(dp), '..', 'serveur', 'kubejs', 'server_scripts'))
    par_kubejs = set()
    if os.path.isdir(scripts):
        for nom in sorted(os.listdir(scripts)):
            if not nom.endswith('.js'):
                continue
            texte = open(os.path.join(scripts, nom), encoding='utf-8').read()
            # « function bmc4:rangs/g_manger » en entier, ou « function bmc4:rangs/ ' + nom » en morceaux
            for m in re.finditer(r"function (bmc4:[a-z0-9_/]+)", texte):
                f = m.group(1)
                if f.endswith('/'):
                    for mm in re.finditer(r"lancer\(ctx, '([a-z0-9_]+)'\)", texte):
                        par_kubejs.add(f + mm.group(1))
                else:
                    par_kubejs.add(f)
        for f in sorted(par_kubejs):
            if f not in F:
                err.append(f"KubeJS ({os.path.basename(scripts)}) lance « {f} », qui n'existe pas")
    # 7. rangs ajoutés par le datapack : présents, et sans condition
    ajoutes = set()
    for f, t in F.items():
        for l in lignes_actives(t):
            m = re.search(r'\bftbranks\s+add\s+\S+\s+([a-z0-9_]+)', l)
            if m:
                ajoutes.add(m.group(1))
    dossier_rangs = os.path.normpath(os.path.join(os.path.dirname(dp), '..', 'serveur', 'ftbranks'))
    for fichier in ('ranks.snbt', 'ranks-sans-kubejs.snbt'):
        chemin = os.path.join(dossier_rangs, fichier)
        if not ajoutes:
            break
        if not os.path.exists(chemin):
            err.append(f"le datapack ajoute des rangs FTB Ranks, mais {fichier} est absent")
            continue
        texte = open(chemin, encoding='utf-8').read()
        blocs = dict(re.findall(r'^\t(\w+): \{\n(.*?)^\t\}', texte, re.M | re.S))
        for r in sorted(ajoutes):
            if r not in blocs:
                err.append(f"{fichier} : le rang « {r} », ajouté par le datapack, n'existe pas")
                continue
            c = re.search(r'^\t\tcondition:\s*"?([a-z_]+)', blocs[r], re.M)
            if c and c.group(1) != 'default':
                err.append(f"{fichier} : le rang « {r} » porte « condition: {c.group(1)} » : ajouté par "
                           "ftbranks add, il ne serait jamais actif (retirer la clé)")
    # 8. formes Java absentes au runtime dans les scripts KubeJS
    if os.path.isdir(scripts):
        for nom in sorted(os.listdir(scripts)):
            if not nom.endswith('.js'):
                continue
            for n, l in enumerate(open(os.path.join(scripts, nom), encoding='utf-8').read().split('\n'), 1):
                if l.strip().startswith('//'):
                    continue
                code = l.split('//')[0]
                for motif, forme in FORMES_ABSENTES.items():
                    if re.search(motif, code):
                        err.append(f"{nom} ligne {n} : forme absente au runtime ({motif}) — employer {forme}")
    # 9. aucune exemption d'opérateur hors du diagnostic
    if os.path.isdir(scripts):
        for nom in sorted(os.listdir(scripts)):
            if not nom.endswith('.js'):
                continue
            lignes = open(os.path.join(scripts, nom), encoding='utf-8').read().split('\n')
            diag = next((i for i, l in enumerate(lignes, 1) if 'ServerEvents.commandRegistry' in l
                         and any('diagnostic' in x for x in lignes[i - 1:])), None)
            for n, l in enumerate(lignes, 1):
                code = l.split('//')[0]
                if not re.search(r'\bestOp\(|\.isOp\(', code) or re.search(r'\bestOp\s*:', code):
                    continue
                if diag is not None and n > diag:
                    continue
                err.append(f"{nom} ligne {n} : exemption d'opérateur hors de /prestige diagnostic "
                           "(un opérateur n'a que ce que son rang donne)")
    for fichier in ('ranks.snbt', 'ranks-sans-kubejs.snbt'):
        chemin = os.path.join(dossier_rangs, fichier)
        if not os.path.exists(chemin):
            continue
        bloc = re.search(r'^\tbmc4_staff: \{\n(.*?)^\t\}', open(chemin, encoding='utf-8').read(), re.M | re.S)
        if bloc:
            for cle in re.findall(r'^\t\t"?((?:command|ftbessentials)\.[^":]+)"?\s*:', bloc.group(1), re.M):
                err.append(f"{fichier} : bmc4_staff porte « {cle} » : un opérateur n'a que ce que son rang donne")
    # 4. orphelines
    ext = os.path.join(os.path.dirname(dp), 'appels-externes.toml')
    conf = tomllib.load(open(ext, 'rb')) if os.path.exists(ext) else {}
    externes = conf.get('fonction', {})
    for f, r in externes.items():
        if f not in F:
            err.append(f"appels-externes.toml : « {f} » n'existe pas dans le datapack")
        elif not str(r).strip():
            err.append(f"appels-externes.toml : « {f} » sans raison")
    appelees = depuis_tick | depuis_load | par_kubejs | {a for f, t in F.items() for a in appels(t) if a != f}
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
