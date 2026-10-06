#!/usr/bin/env python3
"""Sorts d'Iron's Spells réellement obtenables en parchemin (BMC-89, 6 octobre 2026).

    python3 sorts-irons.py <jar irons_spellbooks> [<jar d'extension> ...]

Écrit index/sorts_irons.json. Lu dans le jar (javap), pas supposé :
  - un sort = une classe qui construit un DefaultConfig et pose son
    identifiant par ResourceLocation.fromNamespaceAndPath(<espace>, <id>) ;
  - DefaultConfig.setDeprecated(true) met enabled à false : sort désactivé ;
  - setAllowCrafting(false) : pas de parchemin à la Scroll Forge ;
  - butin : RandomizeSpellFunction → SpellFilter.isSpellAllowed = isEnabled()
    et allowLooting() ; allowLooting() vaut SchoolType.allowLooting, sauf
    redéfinition dans la classe du sort (« return false ») ; l'école eldritch
    est construite (requiresLearning = true, allowLooting = false) :
    fabricable seulement une fois le sort appris (canBeCraftedBy) ;
  - une table de butin qui nomme un sort (spell_filter.spells) ne filtre que
    par isEnabled() (référence AbstractSpell::isEnabled) : ce sort s'y
    obtient même sans allowLooting.
Le serveur ne surcharge aucun sort (/config/irons_spellbooks_spell_config ne
contient qu'un exemple) : la config par défaut du code fait foi.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile

ICI = os.path.dirname(os.path.abspath(__file__))


def classes_de_sorts(base):
    for r, _, fs in os.walk(base):
        for f in fs:
            if f.endswith('Spell.class') and '$' not in f:
                yield os.path.relpath(os.path.join(r, f), base)[:-6].replace(os.sep, '.')


def lire_sorts(jar):
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(jar) as z:
        z.extractall(tmp, [n for n in z.namelist() if n.endswith('.class')])
    ecoles_sans_butin = set()
    reg = [c for c in classes_de_sorts(tmp)]
    sr = subprocess.run(['javap', '-c', '-p', '-classpath', tmp, 'io.redspace.ironsspellbooks.api.registry.SchoolRegistry'],
                        capture_output=True, text=True).stdout
    # Les noms des écoles sont déclarés d'abord, les constructeurs ensuite, dans
    # le même ordre. Le constructeur à deux booléens reçoit (requiresLearning,
    # allowLooting) ; l'autre vaut (false, true).
    statique = sr[sr.index('static {}'):] if 'static {}' in sr else ''   # extension sans registre d'écoles
    noms = re.findall(r'// String ([a-z_]+)\n', statique)
    noms = [n for n in noms if n not in ('irons_spellbooks', 'schools')]
    ctors = re.findall(r'(?:iconst_(\d)\n\s+\d+: iconst_(\d)\n\s+\d+: )?invokespecial\s+#\d+\s+// Method io/redspace/ironsspellbooks/api/spells/SchoolType\."<init>"', statique)
    for nom, (apprend, butin) in zip(noms, ctors):
        if butin == '0':
            ecoles_sans_butin.add(nom.upper())
    sorts = {}
    for c in reg:
        out = subprocess.run(['javap', '-c', '-p', '-classpath', tmp, c], capture_output=True, text=True).stdout
        if 'DefaultConfig' not in out:
            continue
        ids = re.findall(r'String ([a-z0-9_]+)\n\s+\d+: ldc\s+#\d+\s+// String ([a-z0-9_]+)\n\s+\d+: invokestatic\s+#\d+\s+'
                         r'// Method net/minecraft/resources/ResourceLocation\.fromNamespaceAndPath', out)
        if not ids:
            continue
        sid = f'{ids[0][0]}:{ids[0][1]}'
        ecole = (re.findall(r'SchoolRegistry\.([A-Z_]+)_RESOURCE', out) or ['?'])[0]
        redef = re.search(r'public boolean allowLooting\(\);\n\s+Code:\n\s+0: iconst_(\d)', out)
        sorts[sid] = {
            'ecole': ecole.lower(),
            'active': not re.search(r'iconst_1\n\s+\d+: invokevirtual\s+#\d+\s+// Method [\w/]+DefaultConfig\.setDeprecated', out),
            'forge': not re.search(r'iconst_0\n\s+\d+: invokevirtual\s+#\d+\s+// Method [\w/]+DefaultConfig\.setAllowCrafting', out),
            'butin': (redef.group(1) == '1') if redef else ecole not in ecoles_sans_butin,
            'appris': ecole in ecoles_sans_butin,
            'max_niveau': int(m.group(1)) if (m := re.search(r'iconst_(\d)\n\s+\d+: invokevirtual\s+#\d+\s+// Method [\w/]+DefaultConfig\.setMaxLevel', out)) else None,
        }
    # Tables de butin qui nomment un sort.
    with zipfile.ZipFile(jar) as z:
        for n in z.namelist():
            if '/loot_tables/' in n and n.endswith('.json'):
                for s in re.findall(r'"spells"\s*:\s*\[([^\]]*)\]', z.read(n).decode('utf-8', 'ignore')):
                    for sid in re.findall(r'"([a-z0-9_]+:[a-z0-9_]+)"', s):
                        if sid in sorts:
                            sorts[sid].setdefault('tables', []).append(n.split('/loot_tables/')[1][:-5])
        noms = {}
        for lang in ('en_us', 'fr_fr'):
            for n in z.namelist():
                if n.endswith(f'lang/{lang}.json'):
                    d = json.loads(z.read(n).decode('utf-8', 'ignore'))
                    for k, v in d.items():
                        m = re.fullmatch(r'spell\.([a-z0-9_]+)\.([a-z0-9_]+)', k)
                        if m:
                            noms.setdefault(f'{m.group(1)}:{m.group(2)}', {})[lang] = v
    for sid, s in sorts.items():
        s['nom'] = noms.get(sid, {}).get('fr_fr') or noms.get(sid, {}).get('en_us') or sid
        s['obtenable'] = s['active'] and sid.split(':')[1] != 'none' and (s['butin'] or s['forge'] or bool(s.get('tables')))
    return sorts


if __name__ == '__main__':
    tous = {}
    for j in sys.argv[1:]:
        tous.update(lire_sorts(j))
    json.dump(tous, open(os.path.join(ICI, '..', 'index', 'sorts_irons.json'), 'w'), indent=1, ensure_ascii=False, sort_keys=True)
    ob = [k for k, v in tous.items() if v['obtenable']]
    print(f"{len(tous)} sorts lus, {len(ob)} obtenables")
    for k, v in sorted(tous.items()):
        if not v['obtenable'] or not v['butin'] or v.get('tables'):
            print(f"  {k:40} actif={v['active']} butin={v['butin']} forge={v['forge']} appris={v['appris']} tables={v.get('tables')}")
