"""Contrôles de cohérence du livre (BMC-89, consolidation du 5 octobre 2026).

Importé par generer.py : tout contrôle en erreur arrête la génération,
comme un identifiant inconnu. Lancé seul, il imprime aussi le rapport des
récompenses :

    python3 controles.py            # contrôles + rapport des récompenses

Contrôles par chapitre
  · graphe : pas de quête orpheline (sans dépendance et pas première du
    chapitre, sauf `racine = true`), pas de quête obligatoire qui dépend
    d'une optionnelle (une branche optionnelle ne bloque rien), pas deux
    quêtes à la même position ;
  · texte : espace insécable avant : ; ! ? (hors identifiants et hors
    codes &x), guillemets « » et pas de " droits, pas d'identifiant brut
    (mod:objet) dans une description, pas d'anglais hors citation « »,
    titres sans point final et commençant par une majuscule ou un code.
Contrôles sur tout le livre
  · doublons : deux quêtes de chapitres différents qui demandent la même
    chose (même tâche), sauf entre un Défi ou l'Encyclopédie et un autre
    chapitre, et sauf `doublon_voulu = true` sur l'une des deux.
Rapport
  · total de chaque objet distribué par classe (R0 xp, R1 objet, R2 table,
    S xp des gros nœuds), les 15 objets les plus distribués, et la liste
    des objets de valeur ou de fin de partie trouvés dans les récompenses.
"""
import os
import re
import sys
import tomllib
from collections import Counter, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.path.join(ICI, '..', 'donnees')

NBSP = ' '
GROUPES_LIBRES = {'defis', 'encyclopedie', 'semaine'}   # doublons tolérés avec eux

# Objets qu'une récompense ne doit pas distribuer en quantité (revendables
# au Marché ou de fin de partie). Toute occurrence est listée au rapport.
VALEUR = {
    'minecraft:diamond', 'minecraft:emerald', 'minecraft:netherite_ingot', 'minecraft:netherite_scrap',
    'minecraft:ancient_debris', 'minecraft:enchanted_golden_apple', 'minecraft:totem_of_undying',
    'minecraft:elytra', 'minecraft:shulker_shell', 'minecraft:nether_star', 'minecraft:dragon_egg',
    'minecraft:trident', 'minecraft:heart_of_the_sea', 'minecraft:wither_skeleton_skull',
    'minecraft:diamond_block', 'minecraft:emerald_block', 'minecraft:gold_block', 'minecraft:netherite_block',
}

# « boss », « and », « iron », « dungeons », « use » sont exclus : mots
# français ou noms de mods (Deeper and Darker, Iron's Spells, s'use).
MOTS_ANGLAIS = re.compile(r"\b(the|with|from|your|you|find|kill|obtain|craft|get|make|take|"
                          r"defeat|summon|enter|explore|complete|collect|breed|tame|hunt|slay|reach|"
                          r"chest|chests|bosses|sword|armor|armour|helmet|"
                          r"pickaxe|block|blocks|ore|ores|gold|wood|planks|wool|leather)\b")
# Noms propres anglais dont la ponctuation reste anglaise.
NOMS_PROPRES = ('Aether: Treasure Reforging', 'Aether: Protect Your Moa', 'Dragon Mounts: Legacy', 'CC: Tweaked', 'Snow! Real Magic!')
ID_BRUT = re.compile(r'(?<![\w#!/.])[a-z0-9_]+:[a-z0-9_./-]+')
CODE = re.compile(r'&[0-9a-fk-or]')


def _hors_citations(texte):
    """Le texte sans ce qui est entre « » (titres de progrès cités)."""
    return re.sub(r'«[^»]*»', '', texte)


def controler_graphe(quetes, fichier, pos, erreurs, catalogue=False):
    """catalogue : chapitre en grille (Encyclopédie, défis), où les fiches
    sont indépendantes par construction ; seule la dernière quête doit
    dépendre des autres."""
    for i, (c, qd) in enumerate(quetes.items()):
        if i and not qd.get('deps') and not qd.get('racine') and not catalogue:
            erreurs.append(f"{fichier}/{c} : quête orpheline (aucune dépendance ; mettre racine = true si c'est voulu)")
        if not qd.get('optionnel'):
            for d in qd.get('deps', []):
                if quetes[d].get('optionnel') and qd.get('exigence') != 'une':
                    erreurs.append(f"{fichier}/{c} : quête obligatoire bloquée par l'optionnelle « {d} »")
    vus = {}
    for c, p in pos.items():
        if p in vus:
            erreurs.append(f"{fichier}/{c} : même position que « {vus[p]} » ({p[0]}, {p[1]})")
        vus[p] = c


def _controler_texte(texte, ou, erreurs, titre=False):
    if not texte:
        return
    for n in NOMS_PROPRES:
        texte = texte.replace(n, n.replace(':', '').replace('!', ''))
    # espace insécable avant : ; ! ?
    for m in re.finditer(r'(.)([:;!?])', texte):
        avant, signe = m.group(1), m.group(2)
        if avant == NBSP:
            continue
        if signe == ':' and re.match(r'[a-z0-9_]', avant) and re.match(r'[a-z0-9_/.#]', texte[m.end():m.end() + 1] or ' '):
            continue  # identifiant, horaire, « 10:30 » : pas une ponctuation
        if signe == '!' and (texte[m.end():m.end() + 1].isalpha()):
            continue  # « !dragon », « &b!help » : commande du bot, jamais une ponctuation française
        if avant == ' ':
            erreurs.append(f"{ou} : espace simple avant « {signe} » (il faut une insécable) : …{texte[max(0, m.start() - 20):m.end() + 5]}…")
        elif avant not in '?!':
            erreurs.append(f"{ou} : pas d'espace avant « {signe} » : …{texte[max(0, m.start() - 20):m.end() + 5]}…")
    if '"' in re.sub(r'&b[^&]*&r', '', texte):   # un extrait de code &b…&r peut en contenir
        erreurs.append(f"{ou} : guillemet droit \" (utiliser « »)")
    if ('«' in texte) != ('»' in texte):
        erreurs.append(f"{ou} : guillemets « » dépareillés")
    for m in re.finditer(r'«(\S)|(\S)»', texte):
        erreurs.append(f"{ou} : espace insécable manquante à l'intérieur de « » : …{texte[max(0, m.start() - 10):m.end() + 10]}…")
    hors = _hors_citations(texte)
    for m in ID_BRUT.finditer(hors):
        erreurs.append(f"{ou} : identifiant brut « {m.group(0)} » dans le texte")
    anglais = [m.group(0) for m in MOTS_ANGLAIS.finditer(hors.lower())]
    if len(anglais) >= 2:
        erreurs.append(f"{ou} : anglais probable ({', '.join(anglais[:4])})")
    if titre:
        nu = CODE.sub('', texte).strip()
        if nu.endswith('.'):
            erreurs.append(f"{ou} : titre avec un point final « {texte} »")
        if nu and not (nu[0].isupper() or nu[0].isdigit() or nu[0] in 'ŒÉÀÈÇ«!'):
            erreurs.append(f"{ou} : titre sans majuscule « {texte} »")


def controler_textes(quetes, fichier, erreurs):
    for c, qd in quetes.items():
        ou = f"{fichier}/{c}"
        _controler_texte(qd.get('titre', ''), ou + ' (titre)', erreurs, titre=True)
        _controler_texte(qd.get('sous_titre', ''), ou + ' (sous-titre)', erreurs)
        _controler_texte(qd.get('description', ''), ou, erreurs)
        for t in qd.get('taches', []):
            m = t.split(' ')          # pas split() : il couperait aussi sur l'insécable
            if m[0] == 'checkmark':
                _controler_texte(t.split(' ', 1)[1] if len(m) > 1 else '', ou + ' (tâche)', erreurs)
            elif m[0] == 'tag' and len(m) > 3:
                _controler_texte(t.split(' ', 3)[3], ou + ' (tâche)', erreurs)


def signature_tache(t):
    """Ce qu'une tâche demande, sans sa quantité ni son libellé."""
    m = t.replace(' !consommer', '').split()
    if m[0] in ('item', 'kill', 'dimension', 'advancement', 'structure', 'biome', 'stat'):
        return f"{m[0]} {m[1]}"
    if m[0] == 'tag':
        return f"tag {m[1]}"
    if m[0] == 'potion':
        return f"potion {m[1]} {m[2] if len(m) > 2 else 'normale'}"
    if m[0] == 'observation':
        return f"observation {m[1]} {m[2]}"
    return None


def controler_doublons(chapitres, erreurs):
    """chapitres : liste de (fichier, groupe, quetes)."""
    vu = defaultdict(list)
    for fichier, groupe, quetes in chapitres:
        for c, qd in quetes.items():
            for t in qd.get('taches', []):
                s = signature_tache(t)
                if s:
                    vu[s].append((fichier, groupe, c, bool(qd.get('doublon_voulu'))))
    for s, occ in vu.items():
        fichiers = {o[0] for o in occ}
        if len(fichiers) < 2:
            continue
        stricts = [o for o in occ if o[1] not in GROUPES_LIBRES]
        if len({o[0] for o in stricts}) < 2:
            continue
        if any(o[3] for o in stricts):
            continue
        ou = ', '.join(f"{o[0]}/{o[2]}" for o in stricts)
        erreurs.append(f"doublon : « {s} » demandé par {ou} (mettre doublon_voulu = true sur l'une si c'est voulu)")


def rapport_recompenses(chapitres, tables):
    """Totaux par classe et par objet, les 15 premiers, les objets de valeur."""
    r0 = r2 = s = 0
    objets = Counter()
    par_table = Counter()
    valeur = []
    for fichier, groupe, quetes in chapitres:
        for c, qd in quetes.items():
            gros = bool(qd.get('boss')) or groupe == 'defis' or float(qd.get('taille', 1)) >= 1.5
            for r in qd.get('recompenses', []):
                m = r.split()
                if m[0] == 'xp':
                    if gros:
                        s += int(m[1])
                    else:
                        r0 += int(m[1])
                elif m[0] == 'item':
                    n = int(m[2]) if len(m) > 2 and m[2].isdigit() else 1
                    objets[m[1]] += n
                    if m[1] in VALEUR:
                        valeur.append(f"{fichier}/{c} : {m[1]} ×{n}")
                elif m[0] == 'table':
                    r2 += 1
                    par_table[m[1]] += 1
    lignes = [f"XP distribuée : R0 {r0} niveaux sur les quêtes ordinaires, S {s} niveaux sur les gros nœuds (boss, défis, taille ≥ 1,5)",
              f"Tirages de table R2 : {r2} ({', '.join(f'{k} {v}' for k, v in par_table.most_common())})",
              f"Objets R1 distribués : {sum(objets.values())} unités, {len(objets)} objets distincts",
              "Les 15 objets les plus distribués :"]
    for o, n in objets.most_common(15):
        lignes.append(f"  {n:>5}  {o}")
    lignes.append("Objets de valeur dans les récompenses directes :")
    lignes += [f"  {v}" for v in valeur] or ["  aucun"]
    lignes.append("Objets de valeur dans les tables R2 :")
    for nom, t in tables.items():
        for o in t.get('objets', []):
            if o.split()[0] in VALEUR:
                lignes.append(f"  table {nom} : {o}")
    return '\n'.join(lignes)


def charger_chapitres():
    out = []
    for racine, _, fichiers in os.walk(DONNEES):
        if os.path.basename(racine) == 'notes':
            continue
        for f in sorted(fichiers):
            if f.endswith('.toml') and f not in ('tables.toml', 'groupes.toml', 'livre.toml', 'exclusions.toml', 'retroactivite.toml'):
                d = tomllib.load(open(os.path.join(racine, f), 'rb'))
                ch = d['chapitre']
                out.append((ch['fichier'], ch.get('groupe', ''), {q['cle']: q for q in d.get('quete', [])}))
    return out


# Mods sans contenu jouable (bibliothèques, rendu, performance, compat) ou
# dont le contenu est volontairement hors du livre. Chacun avec sa raison.
# Mods à contenu sans quête, raison mesurée (5 octobre 2026). Tout mod
# absent de cette liste et qu'aucune tâche ne cite sort au rapport.
COUVERTURE_IGNORES = {
    # bibliothèques et outils : objets de débogage ou d'interface
    'baguettelib': "bibliothèque (objets internes)",
    'blueprint': "bibliothèque d'Abnormals (créatures et biome de test)",
    'citadel': "bibliothèque d'Alex's Mobs (débogueur, objets d'icône)",
    'geckolib': "bibliothèque d'animation (créatures et objets de test)",
    'gtbcs_spell_lib': "bibliothèque de sorts (objets internes)",
    'irons_lib': "bibliothèque d'Iron's Spells (objets internes)",
    'patchouli': "bibliothèque des livres de guide",
    'structure_gel': "outils de construction de structures (gels, créatif)",
    'terrablender': "bibliothèque de biomes (biome technique)",
    'underlay': "bibliothèque (objet interne)",
    'ftblibrary': "bibliothèque FTB (objet interne)",
    'ftbfiltersystem': "filtre FTB pour d'autres mods, pas une progression",
    'itemfilters': "filtres d'objets FTB pour d'autres mods, pas une progression",
    'immersive_portals': "moteur de portails (objets et créatures techniques)",
    'diagonalwallfix': "correctif de murs (variantes de blocs sans objet propre)",
    'fastpaintings': "optimisation des tableaux (objet technique)",
    # contenu réel, mais rien de vérifiable qui vaille une quête
    'storagedrawersextra': "tiroirs dans les bois d'autres mods : mêmes mécaniques que Storage Drawers, déjà au chapitre Stockage",
    'extra_compat': "seaux en skyroot pour les poissons d'autres mods : variantes sans mécanique propre",
    'snowrealmagic': "neige posée sur les clôtures, dalles et murs : états de blocs, aucun objet obtenable",
    'glow_up': "modèle d'ornement lumineux inobtenable ; pâte et torche lumineuses sans mécanique lisible",
    'irons_patreon_lib': "bibliothèque d'Iron's Spells (objets internes)",
    'abridged': "structure de pont qui ne se génère pas sur ce serveur (outils/generation.py)",
    'ivp': "petits villages qui ne se génèrent pas sur ce serveur (outils/generation.py)",
}


def rapport_couverture(chapitres, ix, ignores=None):
    """Mods qui ajoutent du contenu (objets, créatures, biomes, structures)
    et qu'aucune tâche, icône ou récompense du livre ne cite."""
    ignores = COUVERTURE_IGNORES if ignores is None else ignores
    contenu = {}
    charges = ix.get('_mods') or set(ix.get('mods', {}))   # mods chargés (index/mods_charges.json)
    for cat in ('items', 'entities', 'biomes', 'structures'):
        for i in ix.get(cat, {}):
            ns = i.split(':')[0]
            if '.' in ns or ':' not in i or ns not in charges:
                continue   # clés de langue ou objets d'un mod absent
            contenu.setdefault(i.split(':')[0], {}).setdefault(cat, 0)
            contenu[i.split(':')[0]][cat] += 1
    cites = {}
    for fichier, groupe, quetes in chapitres:
        for c, qd in quetes.items():
            textes = list(qd.get('taches', [])) + list(qd.get('recompenses', [])) + [qd.get('icone', '')]
            for t in textes:
                for m in re.findall(r'#?([a-z0-9_.-]+):[a-z0-9_./-]+', t):
                    cites.setdefault(m, 0)
                    cites[m] += 1
    manque = {m: n for m, n in contenu.items() if m not in cites and m not in ignores and m != 'minecraft'}
    return manque, cites


if __name__ == '__main__':
    chapitres = charger_chapitres()
    tables = tomllib.load(open(os.path.join(DONNEES, 'tables.toml'), 'rb'))['table']
    erreurs = []
    for fichier, groupe, quetes in chapitres:
        controler_textes(quetes, fichier, erreurs)
    controler_doublons(chapitres, erreurs)
    print('\n'.join(erreurs))
    print(f"{len(erreurs)} remarque(s)\n")
    print(rapport_recompenses(chapitres, tables))
    sys.exit(1 if erreurs else 0)
