# v64 — rapport de préparation (10 octobre 2026)

Branche `v64`, partie du tag `v62` (worktree dédié). Rien n'est publié, rien
n'est déposé sur le serveur. Le détail des recherches (sources, javap,
issues) est dans les quatre rapports de lot, non versionnés ; ce qui suit en
reprend les faits.

## Ce qui est prêt

| Livrable | Où |
|---|---|
| Pack v64 (mods A), prêt à publier | `releases/BMC4-v64.zip` (non versionné) ← `releases/construire.py releases/v64/changements.json` puis `migration/assembler.py` |
| Variante « avec B » si la revue valide | `releases/v64/changements-avec-b.json` (même commande) |
| Touches par défaut | `releases/v64/configureddefaults/options.txt` (et `options-avec-b.txt`) |
| Lot serveur | `quetes/deploiement/v64-2026-10-10/` ← `preparer-v64.sh` ; `MISE-EN-PLACE-v64.md` ; dépôt : `deposer.sh --lot v64-<date>` (feu vert seulement) |
| Changelog joueurs | `releases/v64.md` (procédure de secours incluse) |
| Message #informations | `releases/v64/informations-v64.md` |

Le zip v64 : 445 entrées de manifeste (v62 : 440 ; −1 XaeroPlus, +6), le
script de migration et les empreintes v61, v62, v64 dans les overrides.

## BMC-93 — migration

- **Lecture du code, macOS et Windows** : toutes les écritures visent la
  nouvelle instance (`$ICI`) : copies, renommage en `.avant-migration` de ce
  qui existait déjà, journal. L'ancienne instance n'est que lue, et elle ne
  peut pas être la nouvelle (exclue explicitement de la recherche).
- **Trou corrigé** : la vidéo de Xenon (`config/xenon-options.json`,
  `xenon++.toml`) et le son de Sound Physics (`config/sound_physics_remastered/`)
  n'étaient jamais repris ; ils le sont maintenant s'ils diffèrent de ceux de
  l'ancienne version (les deux scripts, même motif).
- **Repris** : `options.txt` en entier (toutes les touches, `lang`, vidéo :
  distance, graphismes, FOV, luminosité ; volumes `soundCategory_*`),
  `xaero/` en entier (minimap avec les waypoints, et world-map),
  `local/ftbchunks/`, `servers.dat`, packs de ressources ajoutés par le joueur.
- **Essai macOS** (copies, v62 → v64) : `options.txt` identique, `xaero/`
  identique (minimap + world-map, 18 waypoints), Xenon et Sound Physics repris,
  **ancienne instance identique octet pour octet** (206 fichiers comparés
  avant/après), seconde exécution refusée sans rien toucher.
- **Windows** : non essayé (BMC-97), lecture du code seulement.
- **Procédure de secours** (5 lignes) : `releases/v64.md` et
  `guides/migration-entre-versions.md`.

## BMC-95 — nettoyage client

- **XaeroPlus** retiré : manifeste, `modlist.html`, `config/xaeroplus.txt`.
  Sur le serveur, il n'est pas chargé (rangé dans `/mods-clients/`) : liste de
  rangement dans le lot (`A-RETIRER.txt`).
- **Conflit sur M** : la carte Xaero World Map, la carte FTB Chunks (qui est
  aussi l'écran des claims) et « couper le micro » de Simple Voice Chat.
  Aucune lettre n'est libre (relevé de l'options.txt du pack).

| Action | Avant | v64 (nouvelle installation) |
|---|---|---|
| Carte Xaero (`gui.xaero_open_map`) | M | **M** |
| Carte FTB Chunks / claims (`key.ftbchunks.map`) | M | **`'`** (`key.keyboard.apostrophe`) |
| Couper le micro (`key.mute_microphone`) | M | **`` ` ``** (`key.keyboard.grave.accent`) |
| Do a Barrel Roll, activer (`key.do_a_barrel_roll.toggle_enabled`) | I (conflit) | **F7** |
| Leawind, régler la caméra (`key.leawind_third_person.adjust_position`) | Z (conflit) | **F8** |
| Immersive Eating (`key.food.animation`), si B validé | U (conflit ×4) | **F9** |
| Placebo, ailes et traînées Patreon | pavé 8 / 9 | inchangées (libres) |

  Les noms sont ceux de GLFW, par position sur un clavier QWERTY : sur AZERTY,
  le menu Commandes affiche d'autres étiquettes (non vérifié en jeu).
- **Comment** : `configureddefaults/options.txt` (ConfiguredDefaults, déjà dans
  le pack) n'est copié que si l'instance n'a pas encore d'`options.txt`. Le
  mod copie dans le constructeur de son fournisseur de langage FML, donc avant
  la lecture des options (javap) — **non vu en jeu**. Un joueur qui migre
  garde ses touches, conflit compris.
- **#informations** : seule la ligne « version actuelle : v62 » → v64
  (`releases/v64/informations-v64.md`).

## BMC-96 — les mods

Distribution tierce CurseForge : **non établie pour aucun** (le champ n'est
lisible qu'avec l'API officielle et une clé ; l'API de projet du site répond
403). Les couples projet/fichier ont été vérifiés par l'API publique cfwidget.

| Mod | Forge 1.20.1 | Fichier (CurseForge projet / fichier) | Côté | Dépendances | Conflits, risques | Verdict |
|---|---|---|---|---|---|---|
| **Just Outdoor Stuffs** (Hyenify, 5,5 M, seul projet de ce nom) | oui | `JustOutdoorStuffs-1.20.1-forge-v1.0.2.jar` 896219 / 4693390 | les deux (50 blocs, une entité d'assise) | aucune | issue #2 ouverte : l'entité d'assise rend une texture nulle (confirmé dans le jar), qui fait planter d'autres mods ; ETF/EMF sont dans le pack, aucun crash rapporté avec eux. Pas de touche. | **Intégré** — essai d'assise avant publication |
| **Steve Goes Fishing** (Dragonblob, 6,5 K, seul projet de ce nom) | **non** (un seul fichier, Fabric 1.21.1) | — | — | — | — | **Non intégré** |
| **FastFurnace** (Shadows_of_Fire) | oui | `FastFurnace-1.20.1-8.0.2.jar` 299540 / 5181098 | les deux (effet serveur ; Placebo a un canal réseau) | **Placebo 8.6.3** (283644 / 6274231), ajouté | Polymorph : compatible (module dédié). Radium modifie aussi le four, à d'autres endroits (non essayé). Ne va pas plus vite : moins de calcul serveur. | **Intégré** |
| **Connectible Chains [FORGE]** (Mysticpasta1, 8,8 M) | oui | `Connectible Chains-forge-1.20.1-1.1.1.jar` 418514 / 6142294 | les deux (2 entités, canal réseau) | aucune | deux dupes corrigés côté Fabric 1.21.1 (#78, #86) après le dernier port Forge : **non vérifiés sur le port Forge** ; avec Sodium Dynamic Lights (dans le pack), les chaînes ne cassent pas quand on retire la clôture (rapport Fabric). Pas de touche. | **Intégré** — essai de dupe obligatoire avant publication |
| **Studious Key Bind** | ? | aucun projet de ce nom ; seul candidat « Studious Keybinds » (StudiousGoose, 4,6 K) 1731572 / 9107028, `studious-keybinds-forge-1.20.1-1.0.10-beta.1.jar` | client | — | projet de 3 jours, bêta, licence « Unspecified » ; éditeur visuel de touches, aucune touche propre | **Non intégré** — à confirmer |
| **Do a Barrel Roll** (enjarai) | oui | `do_a_barrel_roll-forge-3.5.6+1.20.1.jar` 663658 / 5326142 | **client** (le canal réseau accepte un serveur sans le mod : prédicats toujours vrais, javap) | aucune (MixinExtras embarqué ; YACL facultatif absent : réglages par fichier) | caméra : ne change que le roulis, en vol d'élytre ; **ni vue à travers les blocs, ni caméra libre**. Accélération infinie bloquée tant que le serveur ne l'autorise pas — sans le mod sur le serveur, elle est refusée. Issue ouverte : **le roulis ne marche pas avec l'élytre dans Elytra Slot**. Touche I en conflit → F7. | **Intégré** |
| **Voxy** | **non** (Fabric seul, aucune 1.20.1 ; un fork Forge existe mais l'auteur interdit les versions non officielles en modpack) | — | — | — | — | **Non intégré**, alternatives ci-dessous |
| **Leawind's Third Person** (Leawind, 9,4 M) | oui (2.2.0 stable ; 3.0.3 bêta écartée, elle exige Perspective API) | `leawind_third_person-v2.2.0-mc1.20-1.20.1-forge.jar` 930880 / 5961735 | client | Architectury ≤ 9.2.14 (le pack a 9.2.14 : à ne pas monter) | caméra arrêtée par les blocs, aucune option pour la désactiver (sauf spectateur) ; **pas de freecam** ; distance ≈ 3 blocs, jusqu'à ≈ 12, plus grande sur une grosse monture (dragon). **Aide à la visée active par défaut** (cône de 30° en visée à l'arc/arbalète). Z en conflit avec Crawl on Demand → F8. | **Intégré** — aide à la visée : décision |
| **Maps 3D** (Postvein) | oui | `maps3d-forge-1.20.1-1.0.0.jar` 1691687 / 8860560 | les deux | — | **affiche tous les joueurs à portée sur la carte, sans filtre ni option** ; capture de terrain à distance (OP par défaut) | **Refus proposé** (préparé, non intégré) |
| **Kaleidoscope Tavern** (TartaricAcid) | oui | `kaleidoscopetavern-1.2.0-forge+mc1.20.1.jar` 1475175 / 8350841 | les deux | aucune | effets de boisson : allonge +3 ; minage 3×3 sans l'événement de cassage que surveille FTB Chunks (**contournement des claims probable**) ; téléportation à la surface | **Sous conditions** (préparé) |
| **Kaleidoscope Cookery** (YSBB) | oui | `kaleidoscopecookery-1.6.0-forge+mc1.20.1.jar` 1309203 / 9019240 | les deux | aucune | compatibilité intégrée Farmer's Delight et Create ; doublons de contenu avec Farmer's Delight | **Acceptable** (préparé) |
| **Kaleidoscope Immersive Eating** (MemoryToame) | oui | `kaleidoscope_immersiveEating-forge1.20.1-1.5.0.jar` 1659858 / 9068150 | les deux | GeckoLib (présent, 4.8.3), Cookery | modId `food` ; touche U en conflit ×4 → F9 | **Acceptable avec Cookery** (préparé) |
| **Create: Steam 'n' Rails** (IThundxr, 65 M) | oui (« C6 », pas « -beta C0.5 ») | `Steam_Rails-1.7.3+forge-mc1.20.1.jar` 688231 / 8745475 | les deux | Create ≥ 6.0.7 (pack : 6.0.8) | 192 mixins, aucun sur `SchematicPrinter` (classe de Create Dupe Patch) ; seul dupe connu (#359) en 1.19, fermé en 2023. « Conductor spy » : voir par les yeux d'un conducteur à distance, **à essayer** (point caméra). Alt gauche partagé avec Create, voulu. | **Acceptable** (préparé) |

**Alternatives à Voxy** (Forge 1.20.1) :
- **Distant Horizons 3.3.3** (508933 / 9004753, LGPL) : client, ou les deux.
  - Compatibilité : Oculus ≥ 1.8.0 déclaré, ce qui est la version du pack ; rien d'officiel pour Xenon ; une issue ouverte avec Immersive Portals sur exactement notre combinaison (en DH 2.3.2).
  - Coûts sourcés : 6 à 8 Go de RAM conseillés, 4 à 8 cœurs, ≥ 500 Ko/s par joueur si installé sur le serveur, ~11 Go de LOD rapportés côté serveur, TPS en baisse pendant la génération.
  - En factions, côté serveur, il rend les constructions visibles de très loin.
- **Farsight** : déjà dans le pack (vrais chunks gardés côté client, pas de LOD).

## Anti-triche (BMC-94)

- **Listes** : aucun modId v64 n'est dans `BMC4_MODS_REFUSES` (cheatutils, atianxray, xray) ni dans `BMC4_MODS_ALERTE` (zergatulfreecam, autoclickermod). Comparaison mécanique sur les `mods.toml` de tous les jars : connectiblechains, do_a_barrel_roll, fastfurnace, placebo, justoutdoorstuffs, leawind_third_person, kaleidoscope_tavern, kaleidoscope_cookery, food, railways, maps3d, studiouskeybinds.
- **Caméras** : Leawind et Do a Barrel Roll ne voient pas à travers les blocs et ne décollent pas la caméra du joueur (code lu, pas essayé en jeu). Steam 'n' Rails (B) a un « conductor spy » à vérifier.
- **Cartes** : Maps 3D montre les autres joueurs, d'où le refus proposé. Xaero reste soumis au profil serveur imposé par BMC-94 (radar sans joueurs).

## Non essayé en jeu (à faire avant la publication)

1. Un client v64 neuf se connecte au serveur v64 ; les touches de ConfiguredDefaults apparaissent dans Commandes.
2. S'asseoir sur un meuble de Just Outdoor Stuffs (texture nulle, issue #2).
3. Connectible Chains : chaîne entre deux clôtures, casser une clôture, recharger — aucune chaîne ni objet dupliqué ; avec Sodium Dynamic Lights actif.
4. Do a Barrel Roll avec l'élytre dans l'emplacement Elytra Slot.
5. Leawind en vol de dragon et près d'un mur (la caméra s'arrête).
6. Migration sous Windows (BMC-97).

## Décisions qui te reviennent

1. **Steve Goes Fishing** : pas de Forge 1.20.1. Abandonner, ou un autre mod de pêche ?
2. **Voxy** : rien en Forge. Rien, Distant Horizons (coûts ci-dessus, serveur ou non), ou on garde Farsight ?
3. **Studious Key Bind** : est-ce « Studious Keybinds » de StudiousGoose (bêta, licence non précisée) ?
4. **Leawind** : garder l'aide à la visée active par défaut, ou livrer une configuration qui la coupe ? (aucune configuration livrée aujourd'hui).
5. **Do a Barrel Roll** : l'intégrer malgré l'issue Elytra Slot ?
6. **Connectible Chains** : la publication attend l'essai de dupe (point 3 ci-dessus) ?
7. **Revue de #mods** : Maps 3D (refus proposé), Kaleidoscope Tavern (trois effets, dont un contournement de claims probable), Cookery + Immersive Eating, Steam 'n' Rails (conductor spy).
8. **Touches** : la répartition ci-dessus ; les joueurs qui migrent gardent leur conflit sur M.
9. **#informations** : « ~380 mods » à garder ou à mettre à jour.
10. **Distribution** : non établie pour les 10 nouveaux mods. L'import par l'app CurseForge télécharge tout ; vérifier par un import réel avant publication.
11. **Crash Assistant** : `config/crash_assistant/modlist.json` des overrides est périmé depuis avant la v62 (364 entrées, XaeroPlus 2.31.5). On le laisse ?
12. **Ordre de sortie** : serveur et release dans la même maintenance (JOS, Connectible Chains et Placebo rendent v62 et v64 incompatibles).

## Décisions d'Arthur (10 octobre, soir) et ce qui en découle

1. **Steve Goes Fishing** : abandonné pour la v64.
2. **Voxy** : rien ; Farsight reste.
3. **Studious Keybinds** (StudiousGoose, CurseForge 1731572/9107028, client) : intégré.
   - Aucune touche par défaut : le jar n'enregistre aucun `KeyMapping`. Il ajoute un bouton « Keyboard » à l'écran Contrôles (`ControlsScreenMixin`, son seul mixin) ; la liste vanilla « Assignation des touches… » reste.
   - Il modifie les touches par les méthodes vanilla (`setKeyModifierAndCode`, `setToDefault`) et les enregistre dans `options.txt` par `Options.save` : même format, donc ni le script de migration ni ConfiguredDefaults ne sont touchés. Sa seule écriture propre est `config/studiouskeybinds.properties` (disposition 60/75/100 %), hors du filtre du script de migration.
   - modId `studiouskeybinds` : absent de `BMC4_MODS_REFUSES` et `BMC4_MODS_ALERTE`.
   - `clientSideOnly=true`, `displayTest="IGNORE_ALL_VERSION"` : pas sur le serveur.
   - Bêta, licence « Unspecified » : l'étape 21 de `MAINTENANCE-v64.md` le retire si l'import CurseForge le refuse ou le passe en manuel.
4. **Leawind** : configuration par défaut du mod, aide à la visée comprise. Aucune configuration livrée.
5. **Do a Barrel Roll** : intégré ; essai avec Elytra Slot pendant la maintenance.
6. **Connectible Chains** : intégré ; le serveur n'ouvre qu'après l'essai de dupe (`MAINTENANCE-v64.md`, essai 2 : issues #78 et #86 rejouées).
7. **#mods**
   - Maps 3D refusé : message prêt dans `releases/v64/mods-refus-maps3d.md`. Sa configuration (grille, hauteur, placement) n'a aucune option sur les joueurs.
   - Kaleidoscope Tavern : **aucune option de configuration** ne coupe les effets (sa `GeneralConfig` ne règle que la cuve, le robinet de lave et la pose des bouteilles). Les effets sont des données de datapack, donc le datapack serveur `config/datapack/bmc4-taverne/` les remplace : Emerald (Long Reach), Brass Heart et Depth Charge (Ardent Heat), Godfather (Zenith) donnent « Slightly Tipsy » 30 s. Les cocktails ne font que fusionner les effets de leurs ingrédients, ils n'en héritent donc plus. Non essayé en jeu.
   - Le reste attend la revue de 20 h 30.
8. **Touches** : validées. Le changelog dit aux joueurs qui migrent où remettre FTB Chunks / Open Map sur ù et Chat vocal / Couper le microphone sur ². Le menu s'appelle **Options → Contrôles… → Assignation des touches…** en français (lang vanilla `fr_fr`), pas « Commandes ». FTB Chunks n'a pas de traduction française : ses libellés restent en anglais.
9. **#informations** : « ~380 mods » gardé.
10. **Crash Assistant** : `config/crash_assistant/modlist.json` regénéré pour la v64 par `releases/liste-crash-assistant.py` (une version sans B, une avec B), et remplacé dans le zip par `overrides_remplacer` (nouveau dans `construire.py`). Le script de migration ne recopie pas ce fichier.
11. **Ordre** : serveur et release dans la même maintenance (`quetes/deploiement/MAINTENANCE-v64.md`). Branche v64 poussée, aucune release créée.
