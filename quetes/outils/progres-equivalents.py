#!/usr/bin/env python3
"""Progrès équivalents aux tâches non rétroactives (BMC-89, 6 octobre 2026).

    python3 progres-equivalents.py <dossier mods> <jar vanilla 1.20.1>

Parcourt les progrès de tous les jars et retient ceux qui prouvent exactement
une chose, avec un seul critère et aucune autre condition :
  - minecraft:changed_dimension {to}            → « dimension <to> »
  - minecraft:location {structure}              → « structure <id> »
  - minecraft:player_killed_entity {type}       → « kill <entité> »
Écrit index/progres_equivalents.json : { "structure mod:id": [progrès, …] }.
Un progrès acquis se vérifie à la connexion et tous les 5 ticks
(AdvancementTask) ; la tâche d'origine, elle, ne regarde que le présent.
"""
import json, os, re, sys, zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
M = sys.argv[1].rstrip("/") + "/"
jars = [M + j for j in os.listdir(M) if j.endswith(".jar")] + [sys.argv[2]]
eq={}   # (type, cible) -> [advancement]
for j in jars:
    try: z=zipfile.ZipFile(j)
    except Exception: continue
    for n in z.namelist():
        m=re.match(r'data/([^/]+)/advancements/(.+)\.json$',n)
        if not m or '/recipes/' in n: continue
        try: d=json.loads(z.read(n))
        except Exception: continue
        cr=d.get('criteria',{})
        if len(cr)!=1: continue
        (c,),=[cr.values()] if False else [tuple(cr.values())]
        tr=c.get('trigger'); co=c.get('conditions',{}) or {}
        adv=f"{m.group(1)}:{m.group(2)}"
        cle=None
        if tr=='minecraft:changed_dimension' and set(co)=={'to'}:
            cle=('dimension',co['to'])
        elif tr=='minecraft:location':
            p=co.get('player')
            if isinstance(p,list) and len(p)==1 and p[0].get('condition')=='minecraft:entity_properties':
                pr=p[0].get('predicate',{})
                if set(pr)=={'location'} and set(pr['location'])=={'structure'}:
                    cle=('structure',pr['location']['structure'])
            elif isinstance(p,dict) and set(p)=={'location'} and set(p['location'])=={'structure'}:
                cle=('structure',p['location']['structure'])
        elif tr=='minecraft:player_killed_entity' and set(co)=={'entity'}:
            e=co['entity']
            if isinstance(e,list) and len(e)==1 and e[0].get('condition')=='minecraft:entity_properties':
                pr=e[0].get('predicate',{})
                if set(pr)=={'type'}: cle=('kill',pr['type'])
            elif isinstance(e,dict) and set(e)=={'type'}: cle=('kill',e['type'])
        if cle: eq.setdefault(cle,[]).append(adv)
json.dump({f"{a} {b}": sorted(v) for (a, b), v in sorted(eq.items())}, open(os.path.join(ICI, '..', 'index', 'progres_equivalents.json'), 'w'), indent=1, ensure_ascii=False)
print(len(eq))
