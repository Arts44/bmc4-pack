#!/usr/bin/env python3
"""Rétroactivité des quêtes (BMC-89, 6 octobre 2026).

Un joueur qui a déjà fait quelque chose doit, à sa première connexion, voir
valider tout ce que le jeu peut prouver, en cascade. Lu dans le jar
ftb-quests-forge-2001.4.22 (javap) :

  - FTBQuestsEventHandler.playerTick → lambda$playerTick$1 : toute tâche dont
    Task.autoSubmitOnPlayerTick() > 0 est soumise tous les N ticks, tant que la
    quête n'est pas finie et que TeamData.canStartTasks(quête) est vrai.
    AdvancementTask : 5 ticks ; StatTask : 3 ; DimensionTask : 100 ;
    StructureTask, BiomeTask : 20 ; LocationTask : 3.
  - ServerQuestFile.playerLoggedIn → lambda$playerLoggedIn$4 : à la connexion,
    un passage sur toutes les quêtes ; pour chaque quête démarrable, submitTask
    sur chaque tâche dont checkOnLogin() est vrai. Task.checkOnLogin() vaut
    !consumesResources() ; StructureTask, BiomeTask, CheckmarkTask et
    ObservationTask le redéfinissent à false.
  - FTBQuestsInventoryListener.detect → lambda$detect$0 : à chaque changement
    d'inventaire, toutes les tâches de getSubmitTasks() (ItemTask non
    consommée : submitItemsOnInventoryChange) des quêtes démarrables sont
    revérifiées sur l'inventaire complet.
  - TeamData.canStartTasks : en mode « linear » (celui du livre), une quête
    ne démarre que si ses dépendances sont finies (areDependenciesComplete ;
    dependency_requirement one_completed : une seule suffit).

Ce que vérifie chaque tâche (canSubmit / submitTask) :
  - AdvancementTask : PlayerAdvancements.getOrStartProgress(...).isDone() —
    un progrès déjà acquis. RÉTROACTIVE (revue tous les 5 ticks).
  - StatTask : ServerStatsCounter.getValue(stat) — le compteur cumulé.
    RÉTROACTIVE (tous les 3 ticks).
  - ItemTask non consommée : l'inventaire actuel. RÉTROACTIVE pour ce que le
    joueur porte : à la connexion, puis à chaque changement d'inventaire.
  - DimensionTask, StructureTask, BiomeTask, LocationTask : la position
    ACTUELLE du joueur (Level.dimension, structure ou biome à sa position). Un
    passage d'autrefois ne compte pas : NON rétroactives.
  - KillTask : l'événement de mise à mort, après démarrage de la quête.
  - CheckmarkTask, ObservationTask : une action du joueur dans l'interface.
  - ItemTask consommée, XPTask : un bouton de remise.

Donc, ici : advancement, stat, et les tâches d'objet non consommées (item,
tag, potion, oeuf_dragon, jetpack) sont rétroactives ; tout le reste ne l'est
pas. Une étape non rétroactive ne doit jamais précéder une étape rétroactive.
"""
import os
import tomllib

ICI = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.path.join(ICI, '..', 'donnees')

# Deux niveaux de preuve (BMC-89, 6 octobre 2026) :
#  - FORTE : advancement, stat — un état acquis pour toujours ;
#  - FAIBLE : objet non consommé — l'inventaire du moment ; un ancien joueur n'a
#    en général plus sur lui les objets du début.
# Une quête qui contient une tâche à preuve forte ne doit dépendre que de
# quêtes prouvables fortement. Une quête d'objet peut dépendre d'une quête
# d'objet (paliers d'outils, d'armure).
TYPES_FORTS = {'advancement', 'stat'}
TYPES_FAIBLES = {'item', 'tag', 'potion', 'oeuf_dragon', 'jetpack'}
TYPES_RETROACTIFS = TYPES_FORTS | TYPES_FAIBLES
RANG = {'fort': 2, 'faible': 1}


def niveau_tache(spec):
    """'fort', 'faible' ou None (non rétroactive)."""
    ty = spec.split(' ')[0]
    if ty in TYPES_FORTS:
        return 'fort'
    if ty in TYPES_FAIBLES and not spec.endswith(' !consommer'):
        return 'faible'
    return None


def tache_retroactive(spec):
    return niveau_tache(spec) is not None


def prouvable_seule(q, niveau='faible'):
    """La quête se termine sur ce que le jeu prouve, à ce niveau au moins :
    toutes ses tâches, ou, quand une seule suffit (taches_une), au moins une."""
    r = [RANG.get(niveau_tache(s), 0) >= RANG[niveau] for s in q.get('taches', [])]
    if not r:
        return False
    return any(r) if q.get('taches_une') else all(r)


def a_tache_retroactive(q):
    return any(tache_retroactive(s) for s in q.get('taches', []))


def niveau_requis(q):
    """Niveau que doivent atteindre les ancêtres : 'fort' si la quête a une
    tâche à preuve forte, 'faible' si elle n'a que des objets, None sinon."""
    n = [niveau_tache(s) for s in q.get('taches', [])]
    if 'fort' in n:
        return 'fort'
    if 'faible' in n:
        return 'faible'
    return None


def charger_quetes(chapitres):
    """{ 'fichier/cle': (quête, fichier) } pour tous les chapitres donnés."""
    Q = {}
    for c in chapitres:
        d = tomllib.load(open(c, 'rb'))
        fic = d['chapitre']['fichier']
        for q in d.get('quete', []):
            Q[f"{fic}/{q['cle']}"] = (q, fic)
    return Q


def deps_completes(q, fic):
    return [f"{fic}/{d}" for d in q.get('deps', [])] + list(q.get('deps_externes', []))


def bloquees(Q, exceptions=frozenset()):
    """Quêtes à tâche rétroactive qu'aucun chemin de quêtes prouvables au
    niveau requis ne permet de démarrer. Renvoie {clé: (niveau requis,
    première quête fautive)}."""
    memo = {}

    def demarrable(k, niveau, pile):
        q, fic = Q[k]
        ds = [d for d in deps_completes(q, fic) if d in Q]
        if not ds:
            return True, None
        res = [(prouvable(d, niveau, pile + (k,)), d) for d in ds if d not in pile]
        if q.get('exigence') == 'une':
            ok = any(r for r, _ in res)
        else:
            ok = all(r for r, _ in res) and len(res) == len(ds)
        fautive = next((d for r, d in res if not r), None)
        return ok, fautive

    def prouvable(k, niveau, pile):
        if (k, niveau) in memo:
            return memo[(k, niveau)]
        q, _ = Q[k]
        ok = prouvable_seule(q, niveau) and demarrable(k, niveau, pile)[0]
        memo[(k, niveau)] = ok
        return ok

    out = {}
    for k, (q, _) in Q.items():
        n = niveau_requis(q)
        if k in exceptions or n is None:
            continue
        ok, fautive = demarrable(k, n, ())
        if not ok:
            out[k] = (n, fautive)
    return out


def charger_exceptions():
    p = os.path.join(DONNEES, 'retroactivite.toml')
    if not os.path.exists(p):
        return {}
    d = tomllib.load(open(p, 'rb'))
    return {e['quete']: e['raison'] for e in d.get('exception', [])}


def controler(chapitres, verif):
    """Contrôle du générateur : aucune quête dont une tâche est rétroactive
    n'attend une étape que le jeu ne peut pas prouver, sauf exception listée
    (donnees/retroactivite.toml, une par une, avec sa raison)."""
    Q = charger_quetes(chapitres)
    exc = charger_exceptions()
    for k, r in exc.items():
        if k not in Q:
            verif.erreurs.append(f"retroactivite.toml : exception pour une quête inconnue « {k} »")
        elif not r.strip():
            verif.erreurs.append(f"retroactivite.toml : exception « {k} » sans raison")
    for k, (n, f) in sorted(bloquees(Q, frozenset(exc)).items()):
        if n == 'fort':
            verif.erreurs.append(f"{k} : une tâche à preuve forte (progrès, statistique) attend « {f} »,"
                                 " qui n'est pas prouvé pour toujours (objet en poche, visite, case, kill)"
                                 " — en faire une branche latérale, ou une exception motivée")
        else:
            verif.erreurs.append(f"{k} : une tâche d'objet attend « {f} », que le jeu ne peut pas prouver"
                                 " — en faire une branche latérale, ou une exception motivée")
    controler_progres(Q, verif)
    return Q


# ---------------------------------------------------------------- progrès équivalents
# index/progres_equivalents.json (outils/progres-equivalents.py) : progrès à
# critère unique qui prouvent exactement une entrée de dimension, une visite de
# structure ou une mise à mort. Quand plusieurs conviennent, celui du jeu de
# base ou du mod propriétaire de la dimension.
PREFERE = {'dimension minecraft:the_nether': 'minecraft:story/enter_the_nether',
           'dimension minecraft:the_end': 'minecraft:story/enter_the_end',
           'dimension aether:the_aether': 'aether:enter_aether'}
_EQ = None


def equivalents():
    global _EQ
    if _EQ is None:
        p = os.path.join(ICI, '..', 'index', 'progres_equivalents.json')
        _EQ = __import__('json').load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    return _EQ


def progres_equivalent(spec):
    """Le progrès qui prouve la même chose que la tâche, ou None. Une tâche à
    compte (« kill x 5 ») n'en a pas : le progrès ne compte qu'une fois."""
    w = spec.split(' ')
    if w[0] not in ('dimension', 'structure', 'kill') or len(w) < 2:
        return None
    if len(w) > 2 and w[2].isdigit() and int(w[2]) > 1:
        return None
    k = f"{w[0]} {w[1]}"
    eq = equivalents().get(k)
    return (PREFERE.get(k) or sorted(eq)[0]) if eq else None


def doit_rester(cle, q, fichier):
    """Relances et répétables : un nouveau combat, ou à refaire chaque semaine.
    Le progrès, déjà acquis, les validerait sans rien refaire."""
    return 'relance' in cle or q.get('repetable') or fichier.startswith('semaine')


def controler_progres(Q, verif):
    for k, (q, fic) in sorted(Q.items()):
        cle = k.split('/', 1)[1]
        if doit_rester(cle, q, fic):
            continue
        for s in q.get('taches', []):
            a = progres_equivalent(s)
            if a:
                verif.erreurs.append(f"{k} : « {s} » a un progrès équivalent, rétroactif : advancement {a}")
