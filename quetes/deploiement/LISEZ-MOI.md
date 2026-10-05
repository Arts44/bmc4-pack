# Déployer le nouveau livre de quêtes — et revenir en arrière

BMC-89. Préparé le 5 octobre 2026. **Rien de ce qui suit n'a été exécuté.**
Arthur donne le feu vert ; le serveur est fermé aux autres joueurs pendant
toute l'opération.

Serveur MineStrator 486488. Le livre est lu par FTB Quests 2001.4.22 dans
`/config/ftbquests/quests/`. Les commandes « console » se tapent dans la
console MineStrator (ou par l'outil `send_console_command`), sans « / ».

Contenu de ce dossier :

| Fichier | Rôle |
|---|---|
| `LISEZ-MOI.md` | cette marche à suivre |
| `preparer.sh` | fabrique les deux archives du livre, datées |
| `etat-avant-fermeture.md` | liste blanche, opérateurs, livre et progression relevés avant |
| `sauvegarde-ancien-livre-2026-10-05/` | copie exacte du livre actuel du serveur |
| `annonce-reouverture.md` | texte proposé pour #annonces, à poster par Arthur |

---

## 0. La veille

1. Relire `etat-avant-fermeture.md` contre le serveur (liste blanche, `ops.json`). Si une valeur a changé, corriger le fichier : c'est elle qu'on rendra.
2. Fabriquer les archives :

   ```bash
   sh quetes/deploiement/preparer.sh
   ```

   Sortie attendue : deux lignes, `livre-complet-…zip : 89 chapitres` et `livre-leger-…zip : 54 chapitres`. Le script s'arrête si un contrôle du générateur échoue.
   Vérifier aussi que le dépôt par SFTP répond, sans rien laisser sur le serveur : `sh quetes/deploiement/deposer.sh --essai` (un petit fichier texte est déposé dans `/config/ftbquests/`, vu, puis supprimé ; sortie attendue « présent puis supprimé — OK »).
3. Bot de connexions : la retouche « serveur fermé pour maintenance » est en production depuis le 5 octobre (commit `fe1b79c`). Rien à faire.

## 1. Sauvegarde (avant toute modification)

1. **Snapshot MineStrator** : `create_snapshot`, nom `avant-livre-bmc89`. Attendre qu'il soit terminé.
2. **Archive du livre actuel sur le serveur**, hors du dossier lu par le mod : compresser `/config/ftbquests/quests` en `/config/ftbquests/ancien-livre-AAAA-MM-JJ.zip` (outil `compress_files`, ou gestionnaire de fichiers du panel).
3. La copie du dépôt (`sauvegarde-ancien-livre-2026-10-05/`) est la seconde sauvegarde. Elle est identique au serveur au 5 octobre ; si le livre du serveur a changé depuis, l'archive de l'étape 2 fait foi.

## 2. Fermeture : le serveur pour Arts_Vio seul

Console, dans cet ordre :

```
whitelist add Arts_Vio
whitelist on
kick @a[name=!Arts_Vio] Le serveur ferme un moment pour une maintenance. Réouverture annoncée dans #annonces.
```

- `whitelist on` enregistre `white-list=true` dans `server.properties` : la fermeture tient au redémarrage.
- `enforce-whitelist` reste à `false` : personne n'est éjecté automatiquement, d'où le `kick`.
- Un op (HelXo1) peut entrer malgré la whitelist ; si quelqu'un d'autre qu'Arts_Vio apparaît dans `list`, c'est lui.

Bot de connexions : chaque joueur refusé produit **un** message dans #connexions, « Serveur fermé pour maintenance », puis plus rien pendant six heures.

## 3. Déploiement

1. Renommer `/config/ftbquests/quests` en `/config/ftbquests/quests-ancien` (outil `move_files`). Le mod ne lira plus l'ancien livre ; rien n'est supprimé.
2. Déposer **les deux** archives dans `/config/ftbquests/` (la légère servira peut-être à la bascule), sur le feu vert d'Arthur :

   ```bash
   sh quetes/deploiement/deposer.sh
   ```

   Le script dépose les archives du jour par SFTP (identifiants lus dans le trousseau macOS, élément `bmc4-minestrator-sftp`, jamais dans le dépôt), refuse d'écraser un fichier du même nom, ne supprime rien et ne touche pas à `quests/`. Il affiche ensuite, pour chaque archive, la taille en octets sur le serveur et en local : les deux doivent être « identique ». Pour des archives d'un autre jour : `sh quetes/deploiement/deposer.sh AAAA-MM-JJ`.
   Puis extraire `livre-complet-…zip` (`extract_archive`) : elle crée `/config/ftbquests/quests/`. On commence par le livre complet, 4 688 quêtes.
3. Vérifier la présence de `quests/data.snbt`, `quests/chapter_groups.snbt`, `quests/chapters/` (89 fichiers en complet, 54 en léger) et `quests/reward_tables/` (5 fichiers).
4. **Redémarrer** le serveur (`power_action restart`). Pas de `/ftbquests reload` : le jar lui-même l'annonce comme « non recommandé sur un serveur en service » (message `commands.ftbquests.command.feedback.reloaded.disclaimer`).

### Lignes du journal à surveiller au démarrage

Chaînes relevées dans le jar FTB Quests ; aucune ne doit apparaître :

- `Unknown task type!` ou `Unknown reward type!` — un champ du livre mal lu ;
- `Invalid quest object id` ou `Unknown quest object id` — une dépendance cassée ;
- `MissingItem` — un objet du livre absent du serveur ;
- toute ligne `ERROR` ou `Exception` mentionnant `ftbquests`, `snbt` ou un nom de chapitre.

Et, côté joueur, à la première ouverture du livre : le temps d'ouverture, et la fluidité en faisant défiler le groupe Encyclopédie (35 chapitres, 3 147 quêtes).

## 4. Le test d'Arthur

### Préparer les objets (encore op)

```
give Arts_Vio inmis:frayed_backpack
give Arts_Vio minecraft:oak_log 16
give Arts_Vio minecraft:red_bed
give Arts_Vio minecraft:brewing_stand
give Arts_Vio minecraft:blaze_powder 4
give Arts_Vio minecraft:potion{Potion:"minecraft:awkward"} 3
give Arts_Vio minecraft:potion{Potion:"minecraft:water"} 1
give Arts_Vio minecraft:wheat 64
```

### Se retirer l'op le temps du test

Console : `deop Arts_Vio`. Après le test : `op Arts_Vio` (rend le niveau 4, celui d'avant, `op-permission-level=4`).

### Les huit essais

| # | Chapitre → quête | Ce qu'on fait | Résultat attendu |
|---|---|---|---|
| 1 | **Bienvenue sur BMC4** → « Bienvenue sur BMC4 » | cliquer la case « Lu ! », sans être op | la case se coche, la quête se termine, « 2 niveaux » se réclame |
| 2 | **Bienvenue sur BMC4** → « Le kit de départ », « Du bois », « Un premier abri », puis « Poser son claim » | sac élimé, 16 bûches et lit en poche ; cocher « Claim posé » | les trois premières se valident seules ; la dernière donne **un** tirage de la table « Débutant » (pain, torches, charbon, fer, cuir, bœuf cuit, flèches ou pousses) |
| 3 | **Alchimie** → « L'alambic », « Fabriquer l'alambic », « La potion étrange » | alambic, 4 poudres de blaze, 3 potions étranges en poche | « La potion étrange » se valide avec les 3 potions étranges ; la fiole d'eau seule ne compte pas |
| 4 | **Explorateur** → « Voir le monde », puis « Dix kilomètres à pied » | ouvrir la quête | la barre montre la distance marchée **depuis le début du serveur** (statistique « Distance parcourue à pied », en cm) ; au-delà de 10 km, la quête se termine aussitôt — c'est voulu, la statistique est cumulée |
| 5 | **Villages et commerce** → « Le village, version BMC4 », puis « Trouver un village » | entrer dans un village | la quête se valide à l'entrée. La balise `#minecraft:village` compte 38 structures : villages du jeu de base, de Towns and Towers, de Blue Skies et de Repurposed Structures |
| 6 | **Contrats de la semaine** → « Le tableau des contrats », puis « Livrer du blé » | 64 blés en poche ; cliquer la tâche pour livrer | les 64 blés **disparaissent**, la quête se termine ; on réclame 3 niveaux et un tirage « Contrat » ; ensuite la quête affiche un délai d'environ 7 jours avant de revenir (`repeat_cooldown: 604800` secondes, compté depuis la réclamation) |
| 7 | **Twilight Forest — la progression**, avec le compte d'un ancien joueur qui a fini la Twilight (Arts_Vio) | se connecter, ouvrir le chapitre, ne rien faire | dans les secondes qui suivent la connexion, sans rien refaire : le portail, les sept boss (Naga, Liche, Hydre, Chevaliers fantômes, Ur-Ghast, Yéti alpha, Reine des neiges), le stroganoff, le piédestal, le piège à Ghast, les trolls, les géants, la lampe et le Plateau final sont cochés — 16 quêtes sur 40. Restent ouvertes, et c'est voulu : les huit visites de structures, les relances, le Minoshroom (aucun progrès de victoire dans le jar), la case finale ; les trophées se cochent dès qu'ils sont en poche. Simulation : `python3 quetes/outils/simuler_connexion.py quetes/livre quetes/tests/arts_vio_twilight.json monde_twilight_progression` |
| 8 | **L'Aether** et **Les dragons**, avec le compte d'un ancien joueur qui a vaincu la Reine des Valkyries, sans glowstone ni œuf en poche | se connecter ; dans les Dragons, regarder son dragon | « Entrer dans l'Aether », « Vaincre le Slider » et « Vaincre la Reine des Valkyries » se cochent sans rien en poche ; dans les Dragons, « Un œuf de dragon » puis « Faire éclore » se cochent en regardant le dragon, et le reste du chapitre s'ouvre. Simulation : `python3 quetes/tests/test_retroactivite.py` |

Si un essai échoue : noter le chapitre, la quête, ce qui s'est passé, et passer au retour arrière (§ 5) ou à la variante légère.

### Critère de bascule vers le livre léger

Avant d'ouvrir le livre, noter les FPS affichés par F3, immobile au Marché. On bascule si **une seule** de ces trois conditions est vraie :

1. **Ouverture lente** : plus de **5 secondes** entre le clic sur le bouton du livre et l'affichage des chapitres, chronométrées, à la deuxième ouverture (la première peut charger des textures).
2. **FPS en chute** : en faisant défiler les chapitres de l'Encyclopédie (Structures — Moog's, 200 quêtes, est le plus lourd), les FPS tombent **sous la moitié** de la valeur notée avant, ou le jeu se fige plus d'une seconde.
3. **Journal** : au démarrage, une seule des lignes de la liste ci-dessus, ou toute ligne `WARN` ou `ERROR` de FTB Quests.

Sinon, on garde le livre complet.

### La bascule, en trois opérations

Serveur toujours fermé, l'archive légère déjà déposée à l'étape 2 :

```
move_files      /config/ftbquests/quests  →  /config/ftbquests/quests-complet
extract_archive /config/ftbquests/livre-leger-AAAA-MM-JJ.zip  dans  /config/ftbquests/
power_action    restart
```

Le livre léger fait 54 chapitres et 1 541 quêtes, sans l'Encyclopédie. Rien n'est à réécrire : les quêtes communes ont les mêmes identifiants, et la progression faite pendant le test est conservée.

### Lecture du NBT pour le Grimoire et les Dragons

Lecture seule, après les huit essais et **après** `op Arts_Vio` (la commande `data` demande l'op). Elle sert à générer plus tard les chapitres Grimoire et Dragons ; ils ne partiront qu'au déploiement suivant.

1. Prendre en main un vrai **parchemin de sort** d'Iron's Spells, puis taper en console :

   ```
   data get entity Arts_Vio SelectedItem
   ```

2. Si la ligne est coupée par la console MineStrator, lire un sous-chemin à la fois :

   ```
   data get entity Arts_Vio SelectedItem.id
   data get entity Arts_Vio SelectedItem.tag
   data get entity Arts_Vio SelectedItem.tag.ISB_Spells
   data get entity Arts_Vio SelectedItem.tag.ISB_Spells.data
   data get entity Arts_Vio SelectedItem.tag.ISB_Spells.data[0]
   data get entity Arts_Vio SelectedItem.tag.ISB_Spells.data[0].id
   data get entity Arts_Vio SelectedItem.tag.ISB_Spells.data[0].level
   ```

   Si `tag.ISB_Spells` n'existe pas, la sortie de `SelectedItem.tag` donne les vrais noms : descendre champ par champ de la même façon.
3. Recommencer avec **un second parchemin du même sort, à un autre niveau**. C'est la comparaison des deux qui dira si une quête peut ignorer le niveau (la comparaison NBT « faible » de FTB Quests) ou s'il faut une quête par niveau.
4. Prendre en main un vrai **œuf de dragon** de Dragon Mounts :

   ```
   data get entity Arts_Vio SelectedItem
   data get entity Arts_Vio SelectedItem.id
   data get entity Arts_Vio SelectedItem.tag
   data get entity Arts_Vio SelectedItem.tag.BlockEntityTag
   ```

   Même méthode si la ligne est coupée.
5. Copier les sorties telles quelles (une capture d'écran de la console suffit) dans BMC-89.

## 5. Retour arrière

1. Renommer `/config/ftbquests/quests` en `/config/ftbquests/quests-nouveau`.
2. Renommer `/config/ftbquests/quests-ancien` en `/config/ftbquests/quests`.
3. Redémarrer, vérifier le journal (§ 3), ouvrir le livre : il doit s'appeler « Better Minecraft [FORGE] 1.20.1 ».
4. Si quelque chose ne va pas : restaurer le snapshot `avant-livre-bmc89` (il ramène aussi la progression des joueurs à l'instant de la sauvegarde).
5. Réouvrir (§ 6).

## 6. Réouverture

Console :

```
whitelist off
whitelist remove Arts_Vio
```

- Si Arts_Vio n'a pas récupéré son op : `op Arts_Vio`.
- Vérifier : `whitelist.json` vaut `[]`, `white-list=false`, `ops.json` contient HelXo1 et Arts_Vio au niveau 4. C'est l'état noté dans `etat-avant-fermeture.md`.
- Poster le texte de `annonce-reouverture.md` dans #annonces (Arthur, pas le bot).

## 7. La progression des joueurs

- Le remplacement efface la progression sur l'ancien livre : c'est accepté.
- **Aucun recouvrement d'identifiants** : les 471 identifiants de l'ancien livre ne figurent ni parmi les 15 462 du livre complet ni parmi les 5 732 du léger, et le nouveau livre n'a aucun doublon interne. Les fichiers `/world/ftbquests/<équipe>.snbt` ne gardent que des identifiants ; ceux de l'ancien livre n'existent plus et ne font rien. Une ancienne quête ne peut donc pas apparaître comme « déjà faite » dans le nouveau livre.
- **Ce qui se valide tout seul pour un joueur ancien**, lu dans le jar FTB Quests 2001.4.22 (détail et classes dans `quetes/outils/retroactivite.py`) :
  - les tâches **progrès** (`advancement`) : un progrès déjà obtenu suffit. Vérifiées à la connexion, puis toutes les 5 ticks tant que la quête est ouverte ;
  - les tâches **statistique** (`stat`) : le compteur est cumulé depuis le début du serveur. Vérifiées à la connexion, puis toutes les 3 ticks ;
  - les tâches **objet non consommé** : seulement ce que le joueur **a sur lui** — à la connexion, puis à chaque changement d'inventaire. Un objet rangé dans un coffre ne compte pas tant qu'il n'est pas repris.
- **Ce qui ne se valide jamais tout seul** : visiter une structure ou un biome, être dans une dimension (seule la position *actuelle* compte), tuer une créature (seulement après l'ouverture de la quête), cocher une case, observer, remettre des objets consommés.
- **La cascade** : une quête ne démarre que quand ses dépendances sont finies (mode « linear »). Deux niveaux de preuve (6 octobre) : **forte** — progrès et statistiques, acquis pour toujours ; **faible** — objet en poche, qui dépend de l'inventaire du moment. Une quête à preuve forte ne dépend que de quêtes prouvées fortement ; une quête d'objet peut suivre une quête d'objet (paliers d'outils, d'armure). Les objets en poche, les cases « Lu », les visites, les kills de défi et les relances sont donc des branches latérales, et le contrôle `retroactivite` du générateur fait échouer `--verifier` sinon. Quand le mod donne un progrès équivalent (entrée de dimension, découverte de structure, boss tué), c'est lui qui est demandé. À la connexion, toute la colonne vertébrale des progrès et statistiques se coche d'un coup ; les quêtes d'objets se cochent pour ce que le joueur a sur lui, et à chaque changement d'inventaire.
- **Dragons** : la première quête accepte un œuf **ou** la vue d'un dragon. Un joueur qui a déjà fait éclore ses œufs regarde son dragon, et le chapitre s'ouvre.
- Ce qui s'est passé le 5 octobre (Arts_Vio) : seul le portail de la Twilight s'est validé, parce que « La cour de la Naga » (visite) précédait « Vaincre la Naga ». Le simulateur reproduit exactement ce résultat sur l'ancien livre (3411210).
- Les fichiers d'équipe ne sont pas à toucher.

---

## Décisions d'Arthur (5 octobre)

1. HelXo1 garde son op pendant la maintenance ; rien n'est fait pour lui.
2. La retouche du bot de connexions est en production (`fe1b79c`).
3. Le livre complet est déployé en premier ; la bascule suit le critère ci-dessus.
4. Le NBT des parchemins et des œufs est lu pendant la maintenance ; Grimoire et Dragons sont générés après, pour le déploiement suivant.
