#!/usr/bin/env python3
"""Simulation de la première connexion d'un ancien joueur (BMC-89, 6 octobre 2026).

    python3 simuler_connexion.py <dossier du livre> <état du joueur.json> [chapitre ...]

Rejoue sur les fichiers SNBT générés ce que fait ftb-quests-forge-2001.4.22
(javap, voir retroactivite.py pour les classes et méthodes) :

  1. connexion (ServerQuestFile.playerLoggedIn) : un passage sur toutes les
     quêtes, dans l'ordre ; pour chaque quête démarrable non finie, submitTask
     sur les tâches dont checkOnLogin() est vrai ;
  2. ticks (FTBQuestsEventHandler.playerTick) : toutes les N ticks, submitTask
     sur les tâches dont autoSubmitOnPlayerTick() = N > 0, quête démarrable et
     non finie ; on avance jusqu'à ce que plus rien ne change pendant 200 ticks ;
  3. un changement d'inventaire (FTBQuestsInventoryListener.detect) : les
     tâches d'objet non consommées des quêtes démarrables sont revérifiées.

Démarrable (TeamData.canStartTasks, mode « linear ») : dépendances finies —
toutes, ou une seule avec dependency_requirement « one_completed ». Une quête
est finie quand ses tâches non optionnelles le sont ; si toutes sont
optionnelles, quand l'une l'est (QuestObject.isCompletedRaw).

État du joueur (JSON) : {"advancements": [...], "stats": {"minecraft:custom:…": n},
"inventaire": {"mod:objet": n}, "dimension": "…"}. Une tâche structure, biome,
kill, checkmark ou observation ne se valide jamais ici : le joueur se connecte
et ne fait rien.
"""
import json
import os
import re
import sys

TICKS = {'advancement': 5, 'stat': 3, 'dimension': 100, 'structure': 20, 'biome': 20, 'location': 3, 'gamestage': 20}
SANS_LOGIN = {'structure', 'biome', 'checkmark', 'observation'}


# ---------------------------------------------------------------- SNBT
def lire_snbt(texte):
    i = 0
    n = len(texte)

    def blanc():
        nonlocal i
        while i < n and texte[i] in ' \t\r\n,':
            i += 1

    def valeur():
        nonlocal i
        blanc()
        c = texte[i]
        if c == '{':
            i += 1
            d = {}
            while True:
                blanc()
                if texte[i] == '}':
                    i += 1
                    return d
                m = re.compile(r'"((?:[^"\\]|\\.)*)"|([A-Za-z0-9_.+\-]+)').match(texte, i)
                cle = m.group(1) if m.group(1) is not None else m.group(2)
                i = m.end()
                blanc()
                assert texte[i] == ':', texte[i - 20:i + 20]
                i += 1
                d[cle] = valeur()
        if c == '[':
            i += 1
            l = []
            blanc()
            if texte.startswith('I;', i):
                i += 2
            while True:
                blanc()
                if texte[i] == ']':
                    i += 1
                    return l
                l.append(valeur())
        if c == '"':
            m = re.compile(r'"((?:[^"\\]|\\.)*)"').match(texte, i)
            i = m.end()
            return json.loads('"' + m.group(1) + '"')
        m = re.compile(r'[^\s,\]}]+').match(texte, i)
        i = m.end()
        s = m.group(0)
        if s in ('true', 'false'):
            return s == 'true'
        mm = re.fullmatch(r'(-?[0-9.]+(?:[eE]-?[0-9]+)?)([dDfFbBsSlL]?)', s)
        if mm:
            v = float(mm.group(1))
            return int(v) if mm.group(2) in ('b', 'B', 's', 'S', 'l', 'L', '') and '.' not in mm.group(1) else v
        return s

    return valeur()


def charger_livre(dossier, chapitres=None):
    ch = []
    for f in sorted(os.listdir(os.path.join(dossier, 'chapters'))):
        d = lire_snbt(open(os.path.join(dossier, 'chapters', f), encoding='utf-8').read())
        ch.append(d)
    ch.sort(key=lambda d: d.get('order_index', 0))
    quetes = []
    for d in ch:
        for q in d.get('quests', []):
            q['_chapitre'] = d['filename']
            quetes.append(q)
    return quetes


# ---------------------------------------------------------------- jeu
class Partie:
    def __init__(self, quetes, joueur):
        self.q = quetes
        self.par_id = {q['id']: q for q in quetes}
        self.adv = set(joueur.get('advancements', []))
        self.stats = joueur.get('stats', {})
        self.inv = joueur.get('inventaire', {})
        self.dim = joueur.get('dimension', 'minecraft:overworld')
        self.taches_faites = set()
        self.quetes_faites = {}
        self.journal = []

    def finie(self, q):
        return q['id'] in self.quetes_faites

    def demarrable(self, q):
        deps = [d for d in q.get('dependencies', []) if d in self.par_id]
        if not deps:
            return True
        ok = [self.finie(self.par_id[d]) for d in deps]
        return any(ok) if q.get('dependency_requirement') in ('one_completed', 'one_started') else all(ok)

    def preuve(self, t):
        ty = t['type']
        if ty == 'advancement':
            return t['advancement'] in self.adv
        if ty == 'stat':
            return self.stats.get(t['stat'], 0) >= int(t.get('value', 1))
        if ty == 'item':
            if t.get('consume_items'):
                return False
            it = t['item']['id'] if isinstance(t['item'], dict) else t['item']
            return self.inv.get(it, 0) >= int(t.get('count', 1))
        if ty == 'dimension':
            return t['dimension'] == self.dim
        return False

    def soumettre(self, q, t, tick):
        if t['id'] in self.taches_faites or not self.preuve(t):
            return False
        self.taches_faites.add(t['id'])
        ts = q['tasks']
        oblig = [x for x in ts if not x.get('optional_task')]
        if oblig:
            fini = all(x['id'] in self.taches_faites for x in oblig)
        else:
            fini = any(x['id'] in self.taches_faites for x in ts)
        if fini and self.demarrable(q):
            self.quetes_faites[q['id']] = tick
            self.journal.append((tick, q['_chapitre'], q['title']))
        return True

    def connexion(self):
        for q in self.q:
            if self.finie(q) or not self.demarrable(q):
                continue
            for t in q['tasks']:
                if t['type'] in SANS_LOGIN or (t['type'] == 'item' and t.get('consume_items')):
                    continue
                self.soumettre(q, t, 0)

    def ticks(self, maxi=20000):
        calme = 0
        tick = 0
        while calme < 200 and tick < maxi:
            tick += 1
            change = False
            for q in self.q:
                if self.finie(q) or not self.demarrable(q):
                    continue
                for t in q['tasks']:
                    n = TICKS.get(t['type'], 0)
                    if n and tick % n == 0 and self.soumettre(q, t, tick):
                        change = True
            calme = 0 if change else calme + 1
        return tick

    def changement_inventaire(self, tick):
        for q in self.q:
            if self.finie(q) or not self.demarrable(q):
                continue
            for t in q['tasks']:
                if t['type'] == 'item' and not t.get('consume_items'):
                    self.soumettre(q, t, tick)


def simuler(dossier, joueur, inventaire_bouge=True):
    p = Partie(charger_livre(dossier), joueur)
    p.connexion()
    fin = p.ticks()
    if inventaire_bouge:
        # Le joueur ramasse un objet : un changement d'inventaire, puis les ticks
        # reprennent (la cascade continue derrière les objets).
        for _ in range(50):
            avant = len(p.quetes_faites)
            p.changement_inventaire(fin)
            fin = p.ticks() + fin
            if len(p.quetes_faites) == avant:
                break
    return p, fin


if __name__ == '__main__':
    dossier, etat = sys.argv[1], sys.argv[2]
    filtres = set(sys.argv[3:])
    p, fin = simuler(dossier, json.load(open(etat, encoding='utf-8')))
    total = {}
    for q in p.q:
        total.setdefault(q['_chapitre'], [0, 0])[0] += 1
    for q in p.q:
        if p.finie(q):
            total[q['_chapitre']][1] += 1
    for ch, (n, f) in sorted(total.items()):
        if (not filtres or ch in filtres) and f:
            print(f"{ch:34} {f:4} / {n} validées")
    if filtres:
        for tick, ch, titre in sorted(p.journal):
            if ch in filtres:
                print(f"   tick {tick:5}  {re.sub('&.', '', titre)}")
