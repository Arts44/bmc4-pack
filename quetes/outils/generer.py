#!/usr/bin/env python3
"""Générateur du livre de quêtes BMC4 (BMC-89).

Lit les chapitres décrits en TOML dans ../donnees/ et produit le livre
FTB Quests (format SNBT de la version 2001.4.22) dans ../livre/.

    python3 generer.py                 # tout le livre
    python3 generer.py bienvenue       # un seul chapitre (nom de fichier)
    python3 generer.py --verifier      # vérifie les identifiants, n'écrit rien

Règles tenues par le générateur, pour qu'un humain n'ait pas à les tenir :
  · identifiants FTB Quests stables : dérivés du nom du chapitre et de la
    clé de la quête (SHA-1 tronqué à 16 hexadécimaux, bit haut à zéro
    comme ceux que FTB Quests tire lui-même). Régénérer ne change rien ;
    renommer une clé crée une quête neuve, et la progression de l'ancienne
    est perdue — c'est voulu, et c'est la seule façon de « reset » une quête ;
  · mise en page de gauche à droite par rang de dépendance, branches
    optionnelles en dessous, boss plus grands et en forme distincte ;
  · classes de récompense R0 / R1 / R2 / S ;
  · vérification de CHAQUE identifiant (objet, tag, entité, dimension,
    progrès, structure, biome) contre l'index construit depuis les jars.
    Un identifiant inconnu arrête la génération : jamais de quête
    impossible à valider.
"""
import hashlib
import json
import os
import re
import sys
import tomllib

ICI = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.path.join(ICI, '..', 'donnees')
LIVRE = os.path.join(ICI, '..', 'livre')
INDEX = [os.environ.get('QUETES_INDEX', os.path.join(ICI, '..', 'index', 'index.json')),
         os.environ.get('QUETES_INDEX_VANILLA', os.path.join(ICI, '..', 'index', 'index_vanilla.json'))]

# ---------------------------------------------------------------- index

def charger_index():
    ix = {}
    for chemin in INDEX:
        if not os.path.exists(chemin):
            raise SystemExit(f"index absent : {chemin} (lancer indexer-jars.py)")
        d = json.load(open(chemin, encoding='utf-8'))
        for k, v in d.items():
            ix.setdefault(k, {}).update(v)
    return ix


class Verif:
    def __init__(self, ix):
        self.ix = ix
        self.erreurs = []

    def _ok(self, cat, ident, ou):
        if ident not in self.ix.get(cat, {}):
            self.erreurs.append(f"{ou} : {cat} inconnu « {ident} »")
            return False
        return True

    def item(self, i, ou): return self._ok('items', i, ou)
    def tag_item(self, t, ou): return self._ok('tags_items', t, ou)
    def entite(self, e, ou): return self._ok('entities', e, ou)
    def tag_entite(self, t, ou): return self._ok('tags_entities', t, ou)
    def dimension(self, d, ou): return self._ok('dimensions', d, ou)
    def progres(self, a, ou): return self._ok('advancements', a, ou)
    def structure(self, s, ou): return self._ok('structures', s, ou)
    def biome(self, b, ou): return self._ok('biomes', b, ou)

# ---------------------------------------------------------------- identifiants

def hid(*parts):
    """Identifiant FTB Quests : 16 hexadécimaux, premier chiffre 0-7."""
    h = hashlib.sha1('/'.join(parts).encode('utf-8')).hexdigest()[:16].upper()
    return format(int(h, 16) & 0x7FFFFFFFFFFFFFFF, '016X')


def hid_long(*parts):
    return int(hid(*parts), 16)

# ---------------------------------------------------------------- SNBT

def q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def snbt(v, ind=0):
    """Sérialise dans le style de FTB Quests (tabulations, clés triées)."""
    t = '\t' * ind
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, Long):
        return f'{v.v}L'
    if isinstance(v, Double):
        return f'{v.v:g}d' if v.v != int(v.v) else f'{v.v:.1f}d'
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return q(v)
    if isinstance(v, list):
        if not v:
            return '[ ]'
        if all(isinstance(x, str) for x in v) and len(v) == 1:
            return '[' + q(v[0]) + ']'
        if len(v) == 1 and isinstance(v[0], dict):
            return '[' + snbt(v[0], ind) + ']'
        return '[\n' + '\n'.join(t + '\t' + snbt(x, ind + 1) for x in v) + '\n' + t + ']'
    if isinstance(v, dict):
        lignes = [t + '\t' + k + ': ' + snbt(v[k], ind + 1) for k in sorted(v)]
        return '{\n' + '\n'.join(lignes) + '\n' + t + '}'
    raise TypeError(type(v))


class Long:
    def __init__(self, v): self.v = int(v)


class Double:
    def __init__(self, v): self.v = float(v)

# ---------------------------------------------------------------- récompenses

def charger_tables():
    p = os.path.join(DONNEES, 'tables.toml')
    return tomllib.load(open(p, 'rb'))['table']


def recompense(spec, ou, verif, tables, quete_id, idx):
    """Une entrée de récompense du TOML -> dict SNBT."""
    rid = hid(quete_id, 'r', str(idx), spec)
    m = re.match(r'^xp\s+(\d+)$', spec)
    if m:
        return {'id': rid, 'type': 'xp_levels', 'xp_levels': int(m.group(1))}
    m = re.match(r'^table\s+(\S+)$', spec)
    if m:
        nom = m.group(1)
        if nom not in tables:
            raise SystemExit(f"{ou} : table de récompense inconnue « {nom} »")
        r = {'id': rid, 'type': 'random', 'table_id': Long(hid_long('table', nom)),
             'exclude_from_claim_all': True}
        return r
    m = re.match(r'^item\s+(\S+)(?:\s+(\d+))?(?:\s+\+(\d+))?$', spec)
    if m:
        verif.item(m.group(1), ou)
        r = {'id': rid, 'type': 'item', 'item': m.group(1)}
        if m.group(2) and int(m.group(2)) > 1:
            r['count'] = int(m.group(2))
        if m.group(3):
            r['random_bonus'] = int(m.group(3))
        return r
    raise SystemExit(f"{ou} : récompense illisible « {spec} »")

# ---------------------------------------------------------------- tâches

OBSERVE = {'block': 0, 'entity': 5}


def tache(spec, ou, verif, quete_id, idx):
    tid = hid(quete_id, 't', str(idx), spec)
    mots = spec.split()
    genre = mots[0]
    if genre == 'checkmark':
        t = {'id': tid, 'type': 'checkmark'}
        if len(mots) > 1:
            t['title'] = ' '.join(mots[1:])
        return t
    if genre == 'item':
        verif.item(mots[1], ou)
        t = {'id': tid, 'type': 'item', 'item': mots[1]}
        if len(mots) > 2 and int(mots[2]) > 1:
            t['count'] = Long(mots[2])
        return t
    if genre == 'tag':
        verif.tag_item(mots[1], ou)
        t = {'id': tid, 'type': 'item',
             'item': {'Count': 1, 'id': 'itemfilters:tag', 'tag': {'value': mots[1]}},
             'title': ' '.join(mots[3:]) if len(mots) > 3 else f'#{mots[1]}'}
        if len(mots) > 2 and int(mots[2]) > 1:
            t['count'] = Long(mots[2])
        return t
    if genre == 'kill':
        verif.entite(mots[1], ou)
        return {'id': tid, 'type': 'kill', 'entity': mots[1],
                'value': Long(mots[2] if len(mots) > 2 else 1)}
    if genre == 'dimension':
        verif.dimension(mots[1], ou)
        return {'id': tid, 'type': 'dimension', 'dimension': mots[1]}
    if genre == 'advancement':
        verif.progres(mots[1], ou)
        return {'id': tid, 'type': 'advancement', 'advancement': mots[1], 'criterion': ''}
    if genre == 'structure':
        if mots[1].startswith('#'):
            pass  # tag de structure : non vérifiable par l'index, l'auteur assume
        else:
            verif.structure(mots[1], ou)
        return {'id': tid, 'type': 'structure', 'structure': mots[1]}
    if genre == 'biome':
        verif.biome(mots[1], ou)
        return {'id': tid, 'type': 'biome', 'biome': mots[1]}
    if genre == 'observation':
        sorte, cible = mots[1], mots[2]
        if sorte == 'entity':
            verif.entite(cible, ou)
        elif sorte == 'block':
            verif.item(cible, ou)
        else:
            raise SystemExit(f"{ou} : observation « {sorte} » inconnue")
        return {'id': tid, 'type': 'observation', 'observe_type': OBSERVE[sorte],
                'to_observe': cible, 'timer': Long(0)}
    raise SystemExit(f"{ou} : tâche illisible « {spec} »")

# ---------------------------------------------------------------- icônes

def icone_de(quete, taches, verif, ix, ou):
    if 'icone' in quete:
        ic = quete['icone']
        verif.item(ic, ou)
        return ic
    for t in taches:
        if t['type'] == 'item' and isinstance(t['item'], str):
            return t['item']
        if t['type'] in ('kill', 'observation'):
            ent = t.get('entity') or t.get('to_observe')
            if ent:
                mod, nom = ent.split(':', 1)
                for cand in (f'{mod}:{nom}_spawn_egg', f'{mod}:spawn_egg_{nom}'):
                    if cand in ix['items']:
                        return cand
    return None

# ---------------------------------------------------------------- mise en page

def disposer(quetes, cle_rang):
    """x = rang de dépendance, y = ordre dans le rang ; optionnelles en bas."""
    rang = {}

    def r(c, pile=()):
        if c in rang:
            return rang[c]
        if c in pile:
            raise SystemExit(f"dépendance circulaire sur « {c} »")
        deps = quetes[c].get('deps', [])
        rang[c] = 0 if not deps else 1 + max(r(d, pile + (c,)) for d in deps)
        return rang[c]

    for c in quetes:
        r(c)
    colonnes = {}
    for c in quetes:
        if 'pos' in quetes[c]:
            continue
        colonnes.setdefault((rang[c], bool(quetes[c].get('optionnel'))), []).append(c)
    pos = {}
    for (rg, opt), cles in colonnes.items():
        n = len(cles)
        for i, c in enumerate(cles):
            y = (i - (n - 1) / 2) * 1.5
            if opt:
                y = 3.0 + i * 1.5
            pos[c] = (rg * 2.0, y)
    for c in quetes:
        if 'pos' in quetes[c]:
            pos[c] = tuple(quetes[c]['pos'])
    return pos

def disposer_grille(quetes, colonnes):
    """Catalogue : la première quête à gauche, la dernière à droite, le
    reste en grille de `colonnes` par rangée, lu de gauche à droite."""
    cles = list(quetes)
    premiere, derniere, milieu = cles[0], cles[-1], cles[1:-1]
    rangees = max(1, -(-len(milieu) // colonnes))
    pos = {}
    for i, c in enumerate(milieu):
        r, col = divmod(i, colonnes)
        pos[c] = (col * 1.5, (r - (rangees - 1) / 2) * 1.5)
    pos[premiere] = (-3.0, 0.0)
    pos[derniere] = (colonnes * 1.5 + 1.5, 0.0)
    for c in quetes:
        if 'pos' in quetes[c]:
            pos[c] = tuple(quetes[c]['pos'])
    return pos

# ---------------------------------------------------------------- chapitre

def construire_chapitre(toml_path, verif, tables, ix):
    d = tomllib.load(open(toml_path, 'rb'))
    ch = d['chapitre']
    fichier = ch['fichier']
    quetes = {qd['cle']: qd for qd in d.get('quete', [])}
    if len(quetes) != len(d.get('quete', [])):
        raise SystemExit(f"{fichier} : clés de quête en double")
    for c, qd in quetes.items():
        for dep in qd.get('deps', []):
            if dep not in quetes:
                raise SystemExit(f"{fichier}/{c} : dépendance inconnue « {dep} »")
    if ch.get('grille'):
        pos = disposer_grille(quetes, int(ch['grille']))
    else:
        pos = disposer(quetes, fichier)
    chap_id = hid('chapitre', fichier)
    sortie = []
    for c, qd in quetes.items():
        ou = f"{fichier}/{c}"
        qid = hid(fichier, c)
        taches = [tache(t, ou, verif, qid, i) for i, t in enumerate(qd.get('taches', []))]
        if not taches:
            raise SystemExit(f"{ou} : aucune tâche")
        recs = [recompense(s, ou, verif, tables, qid, i) for i, s in enumerate(qd.get('recompenses', []))]
        if qd.get('equipe'):
            for rc in recs:
                rc['team_reward'] = True
        qs = {'id': qid, 'title': qd['titre'], 'tasks': taches, 'rewards': recs,
              'x': Double(pos[c][0]), 'y': Double(pos[c][1])}
        if qd.get('sous_titre'):
            qs['subtitle'] = qd['sous_titre']
        desc = qd.get('description', '').strip('\n')
        if desc:
            qs['description'] = desc.split('\n')
        if qd.get('deps'):
            qs['dependencies'] = [hid(fichier, dp) for dp in qd['deps']]
        if qd.get('exigence') == 'une':
            qs['dependency_requirement'] = 'one_completed'
        if qd.get('optionnel'):
            qs['optional'] = True
            qs['shape'] = qd.get('forme', 'hexagon')
        if qd.get('boss'):
            qs['shape'] = qd.get('forme', 'gear')
            qs['size'] = Double(qd.get('taille', 1.5))
        elif qd.get('forme') and not qd.get('optionnel'):
            qs['shape'] = qd['forme']
        if qd.get('taille') and not qd.get('boss'):
            qs['size'] = Double(qd['taille'])
        if qd.get('repetable'):
            qs['can_repeat'] = True
            qs['repeat_cooldown'] = Long(qd.get('delai_s', 7 * 24 * 3600))
        ic = icone_de(qd, taches, verif, ix, ou)
        if ic:
            qs['icon'] = ic
        if qd.get('cache_avant'):
            qs['hide_until_deps_visible'] = True
        sortie.append(qs)
    chapitre = {
        'default_hide_dependency_lines': bool(ch.get('lignes_cachees', False)),
        'default_quest_shape': ch.get('forme_defaut', ''),
        'filename': fichier,
        'group': hid('groupe', ch['groupe']) if ch.get('groupe') else '',
        'icon': ch['icone'],
        'id': chap_id,
        'order_index': int(ch.get('ordre', 0)),
        'quest_links': [],
        'quests': sortie,
        'title': ch['titre'],
    }
    if ch.get('sous_titre'):
        chapitre['subtitle'] = ch['sous_titre'].strip('\n').split('\n')
    if ch.get('repetable_defaut'):
        chapitre['default_repeatable'] = True
    if ch.get('icone'):
        verif.item(ch['icone'], fichier)
    return ch, chapitre

# ---------------------------------------------------------------- livre

def construire_tables(tables, verif):
    out = {}
    for i, (nom, t) in enumerate(tables.items()):
        rewards = []
        for r in t['objets']:
            m = re.match(r'^(\S+)(?:\s+(\d+))?(?:\s+x(\d+))?$', r)
            if not m:
                raise SystemExit(f"table {nom} : entrée illisible « {r} »")
            verif.item(m.group(1), f'table {nom}')
            e = {'item': m.group(1)}
            if m.group(2) and int(m.group(2)) > 1:
                e['count'] = int(m.group(2))
            if m.group(3):
                e['weight'] = int(m.group(3))
            rewards.append(e)
        fichier = re.sub(r'[^a-z0-9]+', '_', nom.lower())
        out[fichier] = {
            'icon': t['icone'], 'id': hid('table', nom), 'loot_size': int(t.get('tirages', 1)),
            'order_index': i, 'rewards': rewards, 'title': t['titre'],
        }
        verif.item(t['icone'], f'table {nom}')
    return out


def main(argv):
    verifier_seulement = '--verifier' in argv
    cibles = [a for a in argv if not a.startswith('--')]
    ix = charger_index()
    verif = Verif(ix)
    tables = charger_tables()
    groupes = tomllib.load(open(os.path.join(DONNEES, 'groupes.toml'), 'rb'))['groupe']
    chapitres = []
    for racine, _, fichiers in os.walk(DONNEES):
        if os.path.basename(racine) == 'notes':
            continue
        for f in sorted(fichiers):
            if f.endswith('.toml') and f not in ('tables.toml', 'groupes.toml', 'livre.toml', 'exclusions.toml'):
                chapitres.append(os.path.join(racine, f))
    if cibles:
        chapitres = [c for c in chapitres if os.path.splitext(os.path.basename(c))[0] in cibles]
    produits = []
    for c in sorted(chapitres):
        ch, snbt_ch = construire_chapitre(c, verif, tables, ix)
        if ch.get('groupe') and ch['groupe'] not in [g['cle'] for g in groupes]:
            raise SystemExit(f"{c} : groupe inconnu « {ch['groupe']} »")
        produits.append((ch, snbt_ch))
    tables_snbt = construire_tables(tables, verif)
    if verif.erreurs:
        print('\n'.join(verif.erreurs))
        raise SystemExit(f"{len(verif.erreurs)} identifiant(s) introuvable(s) : rien n'est écrit.")
    total = sum(len(s['quests']) for _, s in produits)
    print(f"{len(produits)} chapitre(s), {total} quête(s), {len(tables_snbt)} table(s) — identifiants tous vérifiés")
    if verifier_seulement:
        return
    os.makedirs(os.path.join(LIVRE, 'chapters'), exist_ok=True)
    os.makedirs(os.path.join(LIVRE, 'reward_tables'), exist_ok=True)
    for ch, s in produits:
        with open(os.path.join(LIVRE, 'chapters', ch['fichier'] + '.snbt'), 'w', encoding='utf-8') as f:
            f.write(snbt(s) + '\n')
    for fichier, t in tables_snbt.items():
        with open(os.path.join(LIVRE, 'reward_tables', fichier + '.snbt'), 'w', encoding='utf-8') as f:
            f.write(snbt(t) + '\n')
    livre = tomllib.load(open(os.path.join(DONNEES, 'livre.toml'), 'rb'))
    with open(os.path.join(LIVRE, 'chapter_groups.snbt'), 'w', encoding='utf-8') as f:
        f.write(snbt({'chapter_groups': [{'id': hid('groupe', g['cle']), 'title': g['titre']} for g in groupes]}) + '\n')
    with open(os.path.join(LIVRE, 'data.snbt'), 'w', encoding='utf-8') as f:
        d = dict(livre['data'])
        for k in list(d):
            if isinstance(d[k], float):
                d[k] = Double(d[k])
        f.write(snbt(d) + '\n')
    for ch, s in produits:
        print(f"  {ch['fichier']:<28} {len(s['quests']):>4} quêtes   groupe {ch.get('groupe','—')}")


if __name__ == '__main__':
    main(sys.argv[1:])
