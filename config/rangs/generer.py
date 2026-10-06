#!/usr/bin/env python3
"""Rangs de prestige BMC4 (BMC-91, 6 octobre 2026) : tout tirer de rangs.toml.

    python3 config/rangs/generer.py              # écrit les fichiers
    python3 config/rangs/generer.py --verifier   # compare, n'écrit rien

Produit, à partir de config/rangs/rangs.toml :
  - les fonctions du datapack qui dépendent de l'échelle, dans
    config/datapack/bmc4-fixes/data/bmc4/functions/rangs/ (préfixe « g_ ») ;
  - config/serveur/ftbranks/ranks.snbt, et sa variante de retour arrière
    ranks-sans-kubejs.snbt (téléportations fermées à tous les joueurs) ;
  - config/serveur/kubejs/server_scripts/bmc4_00_table.js (global.BMC4) ;
  - config/rangs/rangs.json, que le bot (discord-factions/rangs.json) recopie ;
  - le chapitre du livre quetes/donnees/factions/rangs.toml.

Les fonctions écrites à la main (achat, paiement, auras, /feed, connexion)
sont à côté, dans rangs/, sans préfixe : elles appellent les g_*.

Ce qui est vérifié ici et nulle part ailleurs : un rang par numéro, des coûts
croissants, des couleurs nommées que Minecraft connaît, une aura par numéro,
une commande donnée à un rang qui existe.
"""
import json
import os
import re
import sys
import tomllib

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.normpath(os.path.join(ICI, '..', '..'))
FONCTIONS = os.path.join(DEPOT, 'config', 'datapack', 'bmc4-fixes', 'data', 'bmc4', 'functions', 'rangs')
SERVEUR = os.path.join(DEPOT, 'config', 'serveur')
CHAPITRE = os.path.join(DEPOT, 'quetes', 'donnees', 'factions', 'rangs.toml')

# Les noms français des objets (index du livre) et la typographie du livre :
# le chapitre sort déjà normalisé, sinon normaliser-typo.py le réécrirait et
# la vérification verrait une différence à chaque passage.
sys.path.insert(0, os.path.join(DEPOT, 'quetes', 'outils'))
import encyclopedie  # noqa: E402
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location('normaliser_typo', os.path.join(DEPOT, 'quetes', 'outils', 'normaliser-typo.py'))
normaliser_typo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(normaliser_typo)
_IX = None


def nom_objet(ident):
    global _IX
    if _IX is None:
        _IX = encyclopedie.charger_index()
    if ident not in _IX['items']:
        raise SystemExit(f"rangs.toml : objet inconnu « {ident} » (absent de quetes/index)")
    return encyclopedie.nom_fr(_IX, ident, 'objet')


def kit_lisible(kit):
    return ', '.join(f"{k.split()[1]} × {nom_objet(k.split()[0])}" for k in kit)

ENTETE_MC = "# Généré par config/rangs/generer.py depuis config/rangs/rangs.toml : ne pas\n# modifier à la main.\n"

COULEURS_NOMMEES = {
    'black': '0', 'dark_blue': '1', 'dark_green': '2', 'dark_aqua': '3', 'dark_red': '4',
    'dark_purple': '5', 'gold': '6', 'gray': '7', 'dark_gray': '8', 'blue': '9', 'green': 'a',
    'aqua': 'b', 'red': 'c', 'light_purple': 'd', 'yellow': 'e', 'white': 'f',
}

ROMAINS = [(10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]


def romain(n):
    s = ''
    for v, r in ROMAINS:
        while n >= v:
            s, n = s + r, n - v
    return s


def milliers(n):
    """2000 → « 2 000 » (espace insécable fine, comme le livre)."""
    return f"{n:,}".replace(',', ' ')


def charger():
    d = tomllib.load(open(os.path.join(ICI, 'rangs.toml'), 'rb'))
    inf = d['infini']
    rangs = []
    cumul = 0
    for i, r in enumerate(d['rang'], 1):
        cumul += r['cout']
        rangs.append(dict(r, numero=i, cumul=cumul, gras=r.get('gras', False),
                          id=f"rang_{i}", equipe=f"bmc4_r{i}",
                          affiche=f"{r['symbole']} {r['nom']}"))
    base = len(rangs)
    for k in range(1, inf['paliers'] + 1):
        cout = inf['cout_depart'] + inf['hausse'] * (k - 1)
        cumul += cout
        rangs.append(dict(nom=f"{inf['nom']} {romain(k)}", article="de l'", symbole=inf['symbole'],
                          couleur=inf['couleur'], nom_couleur=inf['nom_couleur'], gras=inf['gras'],
                          cout=cout, banniere=inf['banniere'], kit=inf['kit'], avantages=[],
                          numero=base + k, cumul=cumul, palier=k, id=None, equipe=f"bmc4_i{k}",
                          affiche=f"{inf['symbole']} {inf['nom']} {romain(k)}"))
    return d, rangs, base


def controler(d, rangs, base):
    err = []
    for r in rangs:
        if r['nom_couleur'] not in COULEURS_NOMMEES:
            err.append(f"{r['nom']} : couleur nommée inconnue « {r['nom_couleur']} »")
        if not re.fullmatch(r'#[0-9A-Fa-f]{6}', r['couleur']):
            err.append(f"{r['nom']} : couleur « {r['couleur']} » pas en #RRGGBB")
        if len(r['equipe']) > 16:
            err.append(f"{r['nom']} : nom d'équipe trop long")
    for a, b in zip(rangs, rangs[1:]):
        if b['numero'] <= base and b['cout'] < a['cout']:
            err.append(f"{b['nom']} coûte moins que {a['nom']}")
    for cmd, n in d['commandes'].items():
        if not 0 <= n <= base:
            err.append(f"commande /{cmd} : rang {n} inexistant")
    for n in d['homes']:
        if not 1 <= int(n) <= base:
            err.append(f"homes : rang {n} inexistant")
    for i, a in enumerate(d['aura'], 1):
        if not 1 <= a['rang'] <= base:
            err.append(f"aura {i} : rang {a['rang']} inexistant")
    if len(d['aura']) >= 10:
        err.append("10 auras ou plus : le numéro 10 sert à couper l'aura")
    return err


# ----------------------------------------------------------------------
#  Textes JSON de Minecraft
# ----------------------------------------------------------------------
def j(*parts):
    return json.dumps(["", *parts], ensure_ascii=False)


def t(texte, **style):
    return dict(text=texte, **style)


def rang_txt(r):
    return t(r['affiche'], color=r['couleur'], bold=r['gras'])


def bouton(texte, commande, survol, couleur="aqua"):
    """Un bouton cliquable qui lance une commande (clickEvent run_command)."""
    return dict(text=texte, color=couleur, bold=True,
                clickEvent=dict(action="run_command", value=commande),
                hoverEvent=dict(action="show_text", contents=survol))


def score(obj):
    return {"score": {"name": "@s", "objective": obj}}


B_ACHETER = bouton("[Acheter]", "/prestige acheter", "Voir le prix et ce qu'apporte le rang suivant, puis confirmer", "green")
B_ECHELLE = bouton("[Voir l'échelle]", "/prestige liste", "Les quinze rangs, puis l'Infini")
B_ETAT = bouton("[Où j'en suis]", "/prestige", "Ton rang, le suivant, ce qu'il te manque")


def ligne_si(n, commande):
    return f"execute if score @s bmc4_cible matches {n} run {commande}"


# ----------------------------------------------------------------------
#  Datapack
# ----------------------------------------------------------------------
def datapack(d, rangs, base):
    f = {}
    dernier = rangs[-1]

    # Objectifs, équipes : appelé depuis load. Les équipes de rang n'ont aucun
    # effet de jeu (tir allié permis, invisibles alliés non révélés).
    lignes = [ENTETE_MC, "# Objectifs et équipes des rangs, créés au chargement (sans effet s'ils existent).\n"]
    for o, crit in [('bmc4_rang', 'trigger'), ('bmc4_aura', 'trigger'), ('bmc4_manger', 'trigger'),
                    ('bmc4_rangs', 'dummy'), ('bmc4_aura_choix', 'dummy'), ('bmc4_manger_t', 'dummy'),
                    ('bmc4_niveaux', 'dummy'), ('bmc4_cible', 'dummy'), ('bmc4_calc', 'dummy'),
                    ('bmc4_devis', 'dummy'), ('bmc4_devis_t', 'dummy'),
                    ('bmc4_depart', 'minecraft.custom:minecraft.leave_game')]:
        lignes.append(f"scoreboard objectives add {o} {crit}")
    lignes.append("")
    for r in rangs:
        e = r['equipe']
        lignes += [
            f"team add {e}",
            f"team modify {e} prefix {json.dumps(t(r['affiche'] + ' ', color=r['couleur'], bold=r['gras']), ensure_ascii=False)}",
            f"team modify {e} color {r['nom_couleur']}",
            f"team modify {e} friendlyFire true",
            f"team modify {e} seeFriendlyInvisibles false",
        ]
    f['g_init'] = '\n'.join(lignes) + '\n'

    # Coût du rang visé (bmc4_cible) dans #cout bmc4_calc.
    lignes = [ENTETE_MC, "# Coût en niveaux du rang visé (@s bmc4_cible) → #cout bmc4_calc.\n",
              "scoreboard players set #cout bmc4_calc -1"]
    for r in rangs:
        lignes.append(ligne_si(r['numero'], f"scoreboard players set #cout bmc4_calc {r['cout']}"))
    f['g_cout'] = '\n'.join(lignes) + '\n'

    # Message : il manque des niveaux. bmc4_calc de @s = ce qui manque.
    lignes = [ENTETE_MC, "# Achat refusé faute de niveaux : ce qui manque, le prix, ce qu'il a, rien de retiré.\n"]
    for r in rangs:
        lignes.append(ligne_si(r['numero'], "tellraw @s " + j(
            t("Rang ", color="red"), rang_txt(r), t(" : il te manque ", color="red"),
            dict(score('bmc4_calc'), color="white", bold=True), t(" niveaux (", color="red"),
            t(f"{milliers(r['cout'])} requis", color="white"), t(", tu en as ", color="red"),
            dict(score('bmc4_niveaux'), color="white"), t("). ", color="red"),
            t("Rien n'a été retiré. Retape /prestige acheter quand tu les auras.", color="gray"))))
    f['g_manque'] = '\n'.join(lignes) + '\n'

    # Message : rang obtenu (bmc4_cible vient d'être payé).
    lignes = [ENTETE_MC, "# Achat réussi : le rang, le prix payé, ce qui reste, les avantages.\n"]
    for r in rangs:
        av = ' · '.join(r['avantages']) if r['avantages'] else "préfixe du palier, annonce dans #faits-d-armes"
        lignes.append(ligne_si(r['numero'], "tellraw @s " + j(
            t("Rang ", color="green"), rang_txt(r), t(" obtenu : ", color="green"),
            t(f"{milliers(r['cout'])} niveaux retirés", color="white"), t(", il t'en reste ", color="green"),
            dict(score('bmc4_niveaux'), color="white"), t(".\n", color="green"),
            t("Avantages : ", color="gray"), t(av, color="white"),
            t("\nTon kit est dans ton inventaire (au sol s'il est plein).", color="gray"))))
    f['g_obtenu'] = '\n'.join(lignes) + '\n'

    # Rangs FTB Ranks (permissions) : ré-ajoute tous ceux qui sont acquis.
    lignes = [ENTETE_MC, "# Les rangs FTB Ranks acquis (permissions des commandes). Ré-ajouter un rang\n"
                          "# déjà présent ne change rien : appelée à l'achat et à chaque connexion.\n"
                          "# Le sélecteur porte type=minecraft:player : l'argument joueur de FTB Ranks\n"
                          "# refuse un @s nu au chargement (« Only players may be affected »).\n"]
    for r in rangs[:base]:
        lignes.append(f"execute if score @s bmc4_rangs matches {r['numero']}.. run ftbranks add @s[type=minecraft:player] {r['id']}")
    f['g_ftbranks'] = '\n'.join(lignes) + '\n'

    # Équipe du rang le plus haut (préfixe et couleur au-dessus de la tête et dans Tab).
    lignes = [ENTETE_MC, "# Met @s dans l'équipe de son rang le plus haut. Hors raid seulement (voir tick).\n"]
    for r in rangs:
        lignes.append(f"execute if score @s bmc4_rangs matches {r['numero']} run team join {r['equipe']} @s")
    lignes.append(f"execute if score @s bmc4_rangs matches {dernier['numero'] + 1}.. run team join {dernier['equipe']} @s")
    f['g_equipe'] = '\n'.join(lignes) + '\n'

    # Kit du rang qui vient d'être acquis : donné une fois, à l'achat.
    lignes = [ENTETE_MC, "# Kit du rang acquis (@s bmc4_cible), donné une seule fois : à l'achat.\n"]
    for r in rangs:
        nom = json.dumps(t(f"Étendard {r['article']}{'' if r['article'].endswith(chr(39)) else ' '}{r['nom']}",
                           color=r['couleur'], bold=r['gras'], italic=False), ensure_ascii=False)
        lore = json.dumps(t("Rang de prestige BMC4", color="gray", italic=False), ensure_ascii=False)
        nbt = "{display:{Name:'" + nom.replace("'", "\\'") + "',Lore:['" + lore + "']}}"
        lignes.append(ligne_si(r['numero'], f"give @s {r['banniere']}{nbt} 1"))
        for k in r['kit']:
            ident, n = k.split()
            lignes.append(ligne_si(r['numero'], f"give @s {ident} {n}"))
    f['g_kit'] = '\n'.join(lignes) + '\n'

    # Annonce Discord : rang 12 et plus, et chaque palier de l'Infini.
    seuil = next(r['numero'] for r in rangs if r['nom'] == 'Éternel')
    f['g_annonce'] = ENTETE_MC + (
        f"# À l'achat d'un rang {seuil} ou plus, une ligne pour le bot (#faits-d-armes) :\n"
        "# il lit storage bmc4:rangs annonces par RCON, puis retire ce qu'il a lu.\n\n"
        f"execute if score @s bmc4_rangs matches {seuil}.. run data modify storage bmc4:rangs annonces append value {{Rang:0}}\n"
        f"execute if score @s bmc4_rangs matches {seuil}.. run data modify storage bmc4:rangs annonces[-1].UUID set from entity @s UUID\n"
        f"execute if score @s bmc4_rangs matches {seuil}.. store result storage bmc4:rangs annonces[-1].Rang int 1 run scoreboard players get @s bmc4_rangs\n")

    # État : rang actuel, prochain rang, prix, ce qui manque.
    lignes = [ENTETE_MC, "# /prestige : où j'en suis. @s bmc4_cible = rang suivant,\n"
                          "# bmc4_niveaux = niveaux actuels, bmc4_calc = ce qui manque (0 si assez).\n",
              "execute if score @s bmc4_rangs matches 0 run tellraw @s " + j(t("Tu n'as pas encore de rang de prestige.", color="gray"))]
    for r in rangs:
        lignes.append(f"execute if score @s bmc4_rangs matches {r['numero']} run tellraw @s " + j(
            t("Ton rang : ", color="gray"), rang_txt(r), t(f" ({r['numero']}/{base}{' + Infini' if r['numero'] > base else ''}).", color="gray")))
    for r in rangs:
        n = r['numero']
        lignes.append(f"execute if score @s bmc4_cible matches {n} if score @s bmc4_calc matches 1.. run tellraw @s " + j(
            t("Prochain : ", color="gray"), rang_txt(r), t(f", {milliers(r['cout'])} niveaux ; tu en as ", color="gray"),
            dict(score('bmc4_niveaux'), color="white"), t(", il t'en manque ", color="gray"),
            dict(score('bmc4_calc'), color="white"), t(". ", color="gray"), B_ECHELLE))
        lignes.append(f"execute if score @s bmc4_cible matches {n} if score @s bmc4_calc matches ..0 run tellraw @s " + j(
            t("Prochain : ", color="gray"), rang_txt(r), t(f", {milliers(r['cout'])} niveaux ; tu en as ", color="gray"),
            dict(score('bmc4_niveaux'), color="white"), t(". ", color="gray"), B_ACHETER, t(" "), B_ECHELLE))
    f['g_etat'] = '\n'.join(lignes) + '\n'

    # /prestige acheter : le devis (assez de niveaux). bmc4_calc = ce qui restera.
    lignes = [ENTETE_MC, "# /prestige acheter, niveaux suffisants : le rang visé (@s bmc4_cible), son prix,\n"
                          "# ce qu'il apporte, ce qui restera (@s bmc4_calc), et le bouton de confirmation.\n"]
    for r in rangs:
        apport = (' · '.join(r['avantages']) if r['avantages']
                  else f"le palier {r['nom']} dans ton préfixe, une annonce dans #faits-d-armes et à ta connexion")
        lignes.append(ligne_si(r['numero'], "tellraw @s " + j(
            t("Rang ", color="gold"), rang_txt(r), t(f" : {milliers(r['cout'])} niveaux.\n", color="gold"),
            t("Il apporte : ", color="gray"), t(apport.rstrip('.') + '.', color="white"),
            t("\nAprès l'achat, il te restera ", color="gray"), dict(score('bmc4_calc'), color="white"),
            t(" niveaux. ", color="gray"),
            bouton("[Confirmer l'achat]", "/prestige confirmer", "Retire les niveaux et donne le rang", "green"),
            t(" (valable 30 secondes)", color="gray"))))
    f['g_devis'] = '\n'.join(lignes) + '\n'

    # /prestige liste : l'échelle, avec ✔ pour les rangs acquis et ◀ pour le rang actuel.
    inf = d['infini']
    lignes = [ENTETE_MC, "# /prestige liste : l'échelle complète, la marque du joueur, ses boutons.\n",
              "execute unless score @s bmc4_rangs matches 0.. run scoreboard players set @s bmc4_rangs 0",
              "tellraw @s " + j(t("Les rangs de prestige", color="gold", bold=True), t(" (prix en niveaux, retirés à l'achat)", color="gray"))]
    for r in rangs[:base]:
        n = r['numero']
        corps = [rang_txt(r), t(f" — {milliers(r['cout'])}", color="white")]
        lignes.append(f"execute if score @s bmc4_rangs matches {n + 1}.. run tellraw @s " + j(t("✔ ", color="green"), *corps))
        lignes.append(f"execute if score @s bmc4_rangs matches {n} run tellraw @s " + j(t("✔ ", color="green"), *corps, t("  ◀ ton rang", color="yellow", bold=True)))
        lignes.append(f"execute if score @s bmc4_rangs matches ..{n - 1} run tellraw @s " + j(t("· ", color="dark_gray"), *corps))
    infini = [t(f"{inf['symbole']} {inf['nom']} I, II, III…", color=inf['couleur'], bold=inf['gras']),
              t(f" — {milliers(inf['cout_depart'])}, puis {milliers(inf['hausse'])} de plus à chaque palier (jusqu'à {romain(inf['paliers'])})", color="white")]
    lignes.append(f"execute if score @s bmc4_rangs matches {base + 1}.. run tellraw @s " + j(t("✔ ", color="green"), *infini))
    lignes.append(f"execute if score @s bmc4_rangs matches ..{base} run tellraw @s " + j(t("· ", color="dark_gray"), *infini))
    for r in rangs[base:]:
        lignes.append(f"execute if score @s bmc4_rangs matches {r['numero']} run tellraw @s " + j(
            t("  ◀ ton palier : ", color="yellow", bold=True), rang_txt(r)))
    lignes.append("tellraw @s " + j(B_ETAT, t(" "), B_ACHETER))
    f['g_liste'] = '\n'.join(lignes) + '\n'

    # Auras : affichage (toutes les 10 ticks) et choix.
    lignes = [ENTETE_MC, "# Les auras, toutes les 10 ticks. Rien pour un spectateur ni un invisible.\n"]
    for i, a in enumerate(d['aura'], 1):
        lignes.append(f"execute as @a[scores={{bmc4_aura_choix={i}}},gamemode=!spectator] "
                      f"unless entity @s[nbt={{ActiveEffects:[{{Id:14}}]}}] at @s run particle {a['particule']}")
    f['g_aura'] = '\n'.join(lignes) + '\n'

    rangs_par_num = {r['numero']: r for r in rangs}
    lignes = [ENTETE_MC, "# /prestige aura <n> (ou /trigger bmc4_aura set <n>) : choisir (1 à " + str(len(d['aura'])) + "), 10 pour couper.\n",
              "execute if score @s bmc4_aura matches 10 run scoreboard players set @s bmc4_aura_choix 0",
              "execute if score @s bmc4_aura matches 10 run tellraw @s " + j(t("Aura coupée. ", color="gray"), t("La remettre : /prestige aura <numéro>", color="aqua"))]
    for i, a in enumerate(d['aura'], 1):
        r = rangs_par_num[a['rang']]
        lignes += [
            f"execute if score @s bmc4_aura matches {i} if score @s bmc4_rangs matches {a['rang']}.. run scoreboard players set @s bmc4_aura_choix {i}",
            f"execute if score @s bmc4_aura matches {i} if score @s bmc4_rangs matches {a['rang']}.. run tellraw @s " + j(
                t("Aura choisie : ", color="green"), t(a['nom'], color="white"), t(". Couper : /prestige aura couper", color="gray")),
            f"execute if score @s bmc4_aura matches {i} unless score @s bmc4_rangs matches {a['rang']}.. run tellraw @s " + j(
                t("Aura refusée : ", color="red"), t(f"« {a['nom']} » s'obtient au rang ", color="red"), rang_txt(r),
                t(". ", color="red"), t("Voir ce qu'il te manque : ", color="gray"), B_ETAT),
        ]
    lignes.append(f"execute unless score @s bmc4_aura matches 1..{len(d['aura'])} unless score @s bmc4_aura matches 10 run tellraw @s " + j(
        t("Aura inconnue. ", color="red"), t(f"Les numéros vont de 1 à {len(d['aura'])} (voir le chapitre Rangs du livre) ; /prestige aura couper la coupe.", color="gray")))
    f['g_aura_choix'] = '\n'.join(lignes) + '\n'

    # /feed : réservé à un rang (voir manger.mcfunction pour le délai).
    rf = rangs_par_num[d['commandes']['feed']]
    f['g_manger'] = ENTETE_MC + (
        f"\n# /feed (KubeJS le renvoie ici) ou /trigger bmc4_manger : rang {rf['numero']} et plus.\n"
        f"execute unless score @s bmc4_rangs matches {rf['numero']}.. run tellraw @s " + j(
            t("/feed refusé : ", color="red"), t("il s'obtient au rang ", color="red"), rang_txt(rf), t(". ", color="red"),
            t("Voir ce qu'il te manque : ", color="gray"), B_ETAT) + "\n"
        f"execute if score @s bmc4_rangs matches {rf['numero']}.. run function bmc4:rangs/manger\n"
        "scoreboard players set @s bmc4_manger 0\n")

    # Message : dernier palier préparé.
    f['g_plafond'] = ENTETE_MC + "\n# Le dernier palier préparé est atteint.\n" + "tellraw @s " + j(
        t("Achat refusé : ", color="red"), t("tu as atteint ", color="red"), rang_txt(dernier),
        t(", le dernier palier préparé. ", color="red"),
        t("Préviens le staff : les suivants seront ajoutés. Rien n'a été retiré. ", color="gray"), B_ECHELLE) + "\n"
    return f


# ----------------------------------------------------------------------
#  FTB Ranks
# ----------------------------------------------------------------------
TELEPORTS = ['home', 'sethome', 'delhome', 'listhomes', 'back', 'tpa', 'tpahere', 'tpaccept', 'tpdeny']


def snbt_ranks(d, rangs, base, sans_kubejs=False):
    cmds = {c: n for c, n in d['commandes'].items() if c != 'feed'}   # /feed passe par le datapack
    homes = {int(k): v for k, v in d['homes'].items()}

    def ouvert(c, n):
        return not (sans_kubejs and c in TELEPORTS)

    out = ["# Généré par config/rangs/generer.py depuis config/rangs/rangs.toml.",
           "# Va dans <monde>/serverconfig/ftbranks/ranks.snbt." + (
               " VARIANTE DE RETOUR ARRIÈRE : sans KubeJS, les blocages\n# (combat, raid, claim) ne sont plus garantis, donc /home, /back et /tpa sont fermés à tous." if sans_kubejs else ""),
           "{"]
    # Les joueurs : tout ce qui est réservé à un rang est fermé.
    lignes = ['\t\tname: "Joueur"', '\t\tpower: 1', '\t\tcondition: "always_active"']
    for c, n in sorted(cmds.items()):
        if n > 0 or (sans_kubejs and c in TELEPORTS):
            lignes.append(f'\t\t"command.{c}": false')
    lignes.append('\t\t"ftbessentials.home.max": 0')
    out += ["\tbmc4_joueur: {", *lignes, "\t}"]
    for r in rangs[:base]:
        # Pas de clé « condition » : FTB Ranks pose alors la condition par défaut,
        # « actif si ajouté » (RankImpl.java:32-35, DefaultCondition.java:27-30).
        # « rank_added » voulait dire autre chose : actif si un AUTRE rang, nommé
        # dans le champ « rank », est ajouté (RankAddedCondition.java:12-27) ;
        # sans ce champ, jamais actif — le défaut vu en jeu le 6 octobre.
        lignes = [f'\t\tname: "{r["affiche"]}"', f'\t\tpower: {10 * r["numero"]}']
        for c, n in sorted(cmds.items()):
            if n == r['numero'] and n > 0 and ouvert(c, n):
                lignes.append(f'\t\t"command.{c}": true')
        if r['numero'] in homes and not sans_kubejs:
            lignes.append(f'\t\t"ftbessentials.home.max": {homes[r["numero"]]}')
        out += [f"\t{r['id']}: {{", *lignes, "\t}"]
    # Le staff (op) garde tout, y compris /feed d'Essentials.
    lignes = ['\t\tname: "Staff"', '\t\tpower: 1000', '\t\tcondition: "op"']
    for c in sorted(d['commandes']):
        lignes.append(f'\t\t"command.{c}": true')
    lignes.append('\t\t"ftbessentials.home.max": 10')
    out += ["\tbmc4_staff: {", *lignes, "\t}", "}"]
    return '\n'.join(out) + '\n'


# ----------------------------------------------------------------------
#  KubeJS, bot, livre
# ----------------------------------------------------------------------
def table(d, rangs, base):
    return {
        'base': base,
        'rangs': [{'numero': r['numero'], 'nom': r['nom'], 'affiche': r['affiche'], 'couleur': r['couleur'],
                   'gras': r['gras'], 'cout': r['cout']} for r in rangs],
        'commandes': d['commandes'],
        'homes': {int(k): v for k, v in d['homes'].items()},
        'delais': d['delais'],
    }


def kubejs(d, rangs, base):
    return ("// Généré par config/rangs/generer.py depuis config/rangs/rangs.toml : ne pas\n"
            "// modifier à la main. Lu par bmc4_garde.js (les autres scripts serveur\n"
            "// partagent l'objet global).\n\n"
            "global.BMC4 = " + json.dumps(table(d, rangs, base), ensure_ascii=False, indent=1) + "\n")


def bot(d, rangs, base):
    tb = table(d, rangs, base)
    tb['seuil_annonce'] = next(r['numero'] for r in rangs if r['nom'] == 'Éternel')
    tb['seuil_salon'] = next(r['numero'] for r in rangs if r['nom'] == 'Primordial')
    tb['seuil_resurrection'] = next(r['numero'] for r in rangs if r['nom'] == 'Draconique')
    return json.dumps(tb, ensure_ascii=False, indent=1) + '\n'


def code_couleur(r):
    return '&' + COULEURS_NOMMEES[r['nom_couleur']] + ('&l' if r['gras'] else '')


def chapitre(d, rangs, base):
    inf = d['infini']
    q = ['# Chapitre « Rangs » — généré par config/rangs/generer.py depuis config/rangs/rangs.toml',
         '# (BMC-91). Catalogue : on achète en jeu avec /prestige, pas dans le',
         '# livre (la progression du livre est partagée par faction, un rang ne l\'est pas).',
         '', '[chapitre]', 'titre = "&dLes rangs de prestige"', 'fichier = "factions_rangs"',
         'groupe = "factions"', 'icone = "minecraft:experience_bottle"', 'ordre = 5', '',
         '[[quete]]', 'cle = "intro"', 'titre = "&dDépenser ses niveaux"',
         'sous_titre = "Quinze rangs, puis l\'Infini. Confort et prestige, jamais de force."',
         'taille = 1.5', 'icone = "minecraft:experience_bottle"', 'taches = ["checkmark Lu"]',
         'recompenses = ["xp 1"]', 'description = """',
         "Les niveaux d'XP qui ne servent plus s'échangent contre un &lrang de prestige&r. Chaque rang &lretire&r des niveaux, s'affiche devant ton pseudo (chat, liste Tab, au-dessus de la tête) et donne des avantages de &lconfort et de prestige&r : jamais de force au combat, jamais de claims en plus.",
         '',
         "&bOù j'en suis :&r &e/prestige&r. Le rang actuel, le suivant, son prix et ce qu'il te manque.",
         "&bAcheter le rang suivant :&r &e/prestige acheter&r montre le prix et ce qu'apporte le rang, puis un bouton &e[Confirmer l'achat]&r, valable 30 secondes. Les niveaux sont vérifiés puis retirés d'un seul coup ; s'il en manque, rien n'est retiré et le message dit combien.",
         "&bL'échelle :&r &e/prestige liste&r.",
         '',
         "Les rangs s'achètent dans l'ordre. Chacun donne son &lkit une seule fois&r, à l'achat. Le rang est personnel : il ne se partage pas avec la faction, même si ce livre, lui, l'est.",
         '',
         "&7Pendant un raid, l'équipe du raid remplace l'affichage du rang. /home, /back et /tpa sont bloqués en combat (15 s après un coup pris ou donné), pendant un raid de ta faction, et dans le claim d'une autre faction.",
         '"""', '']
    prec = 'intro'
    for r in rangs[:base]:
        av = '\n'.join(f"· {a}" for a in r['avantages'])
        kit = kit_lisible(r['kit'])
        nom_objet(r['banniere'])
        extra = ''
        if r['nom'] == 'Diamant':
            extra = '\n\n&bAuras :&r ' + ' · '.join(f"{i} {a['nom']}" for i, a in enumerate(d['aura'], 1) if a['rang'] <= 5) + \
                    ". Choisir : &e/prestige aura <numéro>&r ; couper : &e/prestige aura couper&r."
        if r['nom'] == 'Divin':
            n = next(i for i, a in enumerate(d['aura'], 1) if a['rang'] == 14)
            extra = f"\n\n&bAura exclusive :&r &e/prestige aura {n}&r."
        if r['nom'] == 'Nétherite':
            extra = "\n\n&e/feed&r te rassasie, une fois toutes les 30 minutes."
        if r['nom'] == 'Draconique':
            extra = ("\n\nSur Discord, &e!resurrection <nom>&r ramène un de tes dragons morts : même race, même nom, adulte, "
                     "apprivoisé et lié à toi, à tes pieds (tu dois être connecté). Une fois par semaine, remise à zéro le lundi à 0 h. "
                     "&lSans équipement&r : selle, armure et coffre sont tombés au sol à sa mort.")
        q += ['[[quete]]', f'cle = "rang_{r["numero"]}"',
              f'titre = "{code_couleur(r)}{r["nom"]} {r["symbole"]}"',
              f'sous_titre = "{milliers(r["cout"])} niveaux (cumul {milliers(r["cumul"])})"',
              f'deps = ["{prec}"]', f'icone = "{r["banniere"]}"', 'taches = ["checkmark Lu"]',
              'recompenses = ["xp 1"]', 'description = """',
              f"Rang {r['numero']} sur {base}. Prix : &l{milliers(r['cout'])} niveaux&r, retirés à l'achat (cumul depuis le début : {milliers(r['cumul'])}).",
              '', av, '', f"&7Kit, une seule fois :&r l'étendard {r['article']}{'' if r['article'].endswith(chr(39)) else ' '}{r['nom']}, {kit}.{extra}",
              '"""', '']
        prec = f"rang_{r['numero']}"
    exemples = ', '.join(f"{romain(k)} : {milliers(inf['cout_depart'] + inf['hausse'] * (k - 1))}" for k in (1, 2, 3, 4))
    q += ['[[quete]]', 'cle = "infini"', f'titre = "&d&l{inf["nom"]} {inf["symbole"]}"',
          f'sous_titre = "{milliers(inf["cout_depart"])} niveaux, puis {milliers(inf["hausse"])} de plus à chaque palier"',
          f'deps = ["{prec}"]', 'taille = 1.5', 'forme = "diamond"', f'icone = "{inf["banniere"]}"',
          'taches = ["checkmark Lu"]', 'recompenses = ["xp 1"]', 'description = """',
          f"Après l'Absolu, les paliers de l'Infini : {exemples}… jusqu'au palier {romain(inf['paliers'])}. Le palier s'affiche dans le préfixe (&d∞ Infini IV&r), chaque palier est annoncé dans &9#faits-d-armes&r et à ta connexion.",
          '', "Même commande : &e/prestige acheter&r.", '',
          f"&7Kit à chaque palier :&r un étendard de l'Infini, {kit_lisible(inf['kit'])}.",
          '"""', '']
    return ''.join(normaliser_typo.normaliser_ligne(l) for l in ('\n'.join(q) + '\n').splitlines(keepends=True))


# ----------------------------------------------------------------------
def sorties():
    d, rangs, base = charger()
    err = controler(d, rangs, base)
    if err:
        raise SystemExit('rangs.toml :\n  ' + '\n  '.join(err))
    out = {}
    for nom, texte in datapack(d, rangs, base).items():
        out[os.path.join(FONCTIONS, nom + '.mcfunction')] = texte
    out[os.path.join(SERVEUR, 'ftbranks', 'ranks.snbt')] = snbt_ranks(d, rangs, base)
    out[os.path.join(SERVEUR, 'ftbranks', 'ranks-sans-kubejs.snbt')] = snbt_ranks(d, rangs, base, sans_kubejs=True)
    out[os.path.join(SERVEUR, 'kubejs', 'server_scripts', 'bmc4_00_table.js')] = kubejs(d, rangs, base)
    out[os.path.join(ICI, 'rangs.json')] = bot(d, rangs, base)
    out[CHAPITRE] = chapitre(d, rangs, base)
    return out


def main(argv):
    out = sorties()
    verifier = '--verifier' in argv
    differents = []
    for chemin, texte in out.items():
        actuel = open(chemin, encoding='utf-8').read() if os.path.exists(chemin) else None
        if actuel == texte:
            continue
        differents.append(os.path.relpath(chemin, DEPOT))
        if not verifier:
            os.makedirs(os.path.dirname(chemin), exist_ok=True)
            open(chemin, 'w', encoding='utf-8').write(texte)
    # Les fichiers g_* qui ne sont plus produits
    for f in sorted(os.listdir(FONCTIONS)) if os.path.isdir(FONCTIONS) else []:
        p = os.path.join(FONCTIONS, f)
        if f.startswith('g_') and p not in out:
            differents.append(os.path.relpath(p, DEPOT) + ' (orphelin)')
            if not verifier:
                os.remove(p)
    bot_copie = os.path.join(DEPOT, '..', 'discord-factions', 'rangs.json')
    if os.path.exists(bot_copie) and open(bot_copie, encoding='utf-8').read() != out[os.path.join(ICI, 'rangs.json')]:
        print("attention : discord-factions/rangs.json diffère de config/rangs/rangs.json (le recopier)")
    if verifier:
        if differents:
            print("rangs : fichiers à régénérer (python3 config/rangs/generer.py) :\n  " + '\n  '.join(differents))
            return 1
        print(f"rangs : {len(out)} fichiers à jour")
        return 0
    print(f"rangs : {len(differents)} fichier(s) écrit(s) sur {len(out)}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
