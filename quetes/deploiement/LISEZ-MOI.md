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

   Sortie attendue : deux lignes, `livre-complet-…zip : 76 chapitres` et `livre-leger-…zip : 54 chapitres`. Le script s'arrête si un contrôle du générateur échoue.
3. Décider des questions 1 et 2 en fin de fichier (HelXo1, bot de connexions).

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
- **Un opérateur entre malgré la liste blanche.** HelXo1 est op niveau 4 : voir la question 1. Si la réponse est de le retirer le temps du test : `deop HelXo1`.

Bot de connexions : sans la retouche de la question 2, chaque joueur refusé produit un message dans #connexions toutes les 15 minutes tant qu'il réessaie, avec un conseil faux (« la liste blanche est normalement désactivée ici »).

## 3. Déploiement

1. Renommer `/config/ftbquests/quests` en `/config/ftbquests/quests-ancien` (outil `move_files`). Le mod ne lira plus l'ancien livre ; rien n'est supprimé.
2. Déposer l'archive choisie dans `/config/ftbquests/` et l'extraire (`extract_archive`) : elle crée `/config/ftbquests/quests/`. Commencer par **le livre complet** (question 3).
3. Vérifier la présence de `quests/data.snbt`, `quests/chapter_groups.snbt`, `quests/chapters/` (76 fichiers en complet, 54 en léger) et `quests/reward_tables/` (5 fichiers).
4. **Redémarrer** le serveur (`power_action restart`). Pas de `/ftbquests reload` : le jar lui-même l'annonce comme « non recommandé sur un serveur en service » (message `commands.ftbquests.command.feedback.reloaded.disclaimer`).

### Lignes du journal à surveiller au démarrage

Chaînes relevées dans le jar FTB Quests ; aucune ne doit apparaître :

- `Unknown task type!` ou `Unknown reward type!` — un champ du livre mal lu ;
- `Invalid quest object id` ou `Unknown quest object id` — une dépendance cassée ;
- `MissingItem` — un objet du livre absent du serveur ;
- toute ligne `ERROR` ou `Exception` mentionnant `ftbquests`, `snbt` ou un nom de chapitre.

Et, côté joueur, à la première ouverture du livre : le temps d'ouverture, et la fluidité en faisant défiler le groupe Encyclopédie (22 chapitres, 2 343 quêtes).

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

### Les six essais

| # | Chapitre → quête | Ce qu'on fait | Résultat attendu |
|---|---|---|---|
| 1 | **Bienvenue sur BMC4** → « Bienvenue sur BMC4 » | cliquer la case « Lu ! », sans être op | la case se coche, la quête se termine, « 2 niveaux » se réclame |
| 2 | **Bienvenue sur BMC4** → « Le kit de départ », « Du bois », « Un premier abri », puis « Poser son claim » | sac élimé, 16 bûches et lit en poche ; cocher « Claim posé » | les trois premières se valident seules ; la dernière donne **un** tirage de la table « Débutant » (pain, torches, charbon, fer, cuir, bœuf cuit, flèches ou pousses) |
| 3 | **Alchimie** → « L'alambic », « Fabriquer l'alambic », « La potion étrange » | alambic, 4 poudres de blaze, 3 potions étranges en poche | « La potion étrange » se valide avec les 3 potions étranges ; la fiole d'eau seule ne compte pas |
| 4 | **Explorateur** → « Voir le monde », puis « Dix kilomètres à pied » | ouvrir la quête | la barre montre la distance marchée **depuis le début du serveur** (statistique « Distance parcourue à pied », en cm) ; au-delà de 10 km, la quête se termine aussitôt — c'est voulu, la statistique est cumulée |
| 5 | **Villages et commerce** → « Le village, version BMC4 », puis « Trouver un village » | entrer dans un village | la quête se valide à l'entrée. La balise `#minecraft:village` compte 38 structures : villages du jeu de base, de Towns and Towers, de Blue Skies et de Repurposed Structures |
| 6 | **Contrats de la semaine** → « Le tableau des contrats », puis « Livrer du blé » | 64 blés en poche ; cliquer la tâche pour livrer | les 64 blés **disparaissent**, la quête se termine ; on réclame 3 niveaux et un tirage « Contrat » ; ensuite la quête affiche un délai d'environ 7 jours avant de revenir (`repeat_cooldown: 604800` secondes, compté depuis la réclamation) |

Si un essai échoue : noter le chapitre, la quête, ce qui s'est passé, et passer au retour arrière (§ 5) ou à la variante légère.

### Le livre rame ?

Si l'ouverture ou le défilement est lent avec le livre complet : refaire le § 3 avec `livre-leger-…zip` (54 chapitres, 1 010 quêtes, sans l'Encyclopédie). Rien n'est à réécrire : les deux variantes sortent de la même commande, les quêtes communes ont les mêmes identifiants, et la progression faite pendant le test est conservée.

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

- Si HelXo1 a été retiré des opérateurs : `op HelXo1`.
- Si Arts_Vio n'a pas récupéré son op : `op Arts_Vio`.
- Vérifier : `whitelist.json` vaut `[]`, `white-list=false`, `ops.json` contient HelXo1 et Arts_Vio au niveau 4. C'est l'état noté dans `etat-avant-fermeture.md`.
- Poster le texte de `annonce-reouverture.md` dans #annonces (Arthur, pas le bot).

## 7. La progression des joueurs

- Le remplacement efface la progression sur l'ancien livre : c'est accepté.
- **Aucun recouvrement d'identifiants** : les 471 identifiants de l'ancien livre ne figurent ni parmi les 10 498 du livre complet ni parmi les 3 446 du léger, et le nouveau livre n'a aucun doublon interne. Les fichiers `/world/ftbquests/<équipe>.snbt` ne gardent que des identifiants ; ceux de l'ancien livre n'existent plus et ne font rien. Une ancienne quête ne peut donc pas apparaître comme « déjà faite » dans le nouveau livre.
- Ce qui se validera tout seul pour un joueur ancien : les quêtes d'objets qu'il a déjà en poche, les progrès déjà obtenus, les statistiques de distance. C'est l'annonce qui le dit.
- Les fichiers d'équipe ne sont pas à toucher.

---

## Questions pour Arthur

**1. HelXo1 pendant la fermeture.**
Situation : HelXo1 est opérateur niveau 4, et un opérateur entre même quand la liste blanche est active. La fermeture « Arts_Vio seul » n'est donc pas étanche.
Options : (a) le retirer des opérateurs le temps du test (`deop HelXo1`, puis `op HelXo1` à la réouverture) ; (b) le prévenir et lui demander de ne pas se connecter ; (c) ne rien faire.
Conséquences : (a) ferme vraiment le serveur, au prix d'un retrait de droits temporaire qu'il faut lui expliquer ; (b) repose sur sa parole ; (c) laisse une porte ouverte pendant un déploiement.
Recommandation : (a), en le prévenant avant.

**2. Le bot de connexions.**
Situation : pendant la fermeture, chaque refus de la liste blanche produit un message dans #connexions, répété toutes les 15 minutes par joueur, avec un conseil devenu faux.
Options : (a) fusionner la branche locale `bmc89-fermeture-whitelist` du dépôt `discord-factions` avant la fermeture (un message par joueur et par fermeture, titre « Serveur fermé pour maintenance », renvoi à #annonces) ; (b) laisser le bot tel quel ; (c) couper le module de connexions le temps du test.
Conséquences : (a) se déploie sur Railway au push sur `main` (audit 0 grave, vérificateur 94/94) ; (b) quelques messages trompeurs pendant le test ; (c) on perd aussi les vraies alertes de connexion.
Recommandation : (a). La retouche est inoffensive hors fermeture : elle ne change que le cas « pas sur la liste blanche ».

**3. Quelle variante déployer d'abord.**
Situation : le livre complet fait 3 353 quêtes, dont 2 343 dans l'Encyclopédie ; personne ne sait s'il s'ouvre sans ramer. Le léger en fait 1 010.
Options : (a) complet d'abord, léger si ça rame ; (b) léger d'abord, complet si ça tient.
Conséquences : (a) mesure directement le cas le plus lourd ; (b) donne un premier livre sûr, mais ne dit rien du complet.
Recommandation : (a). Le passage à la variante légère prend un redémarrage et ne perd rien.
