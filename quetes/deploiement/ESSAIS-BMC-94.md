# BMC-94 — Essais en jeu après le redémarrage

Deux comptes : **A** (op, membre d'une faction F1) et **B** (non op, membre
d'une autre faction F2), plus un mob hostile ou un coéquipier pour « entrer
en combat » (un coup donné ou pris : 15 s). Noter pour chaque ligne :
OK / ÉCHEC, et le message exact reçu.

**Le raid simulé** (console, sans passer par le bot) :
```
team join bmc4_raid_actif A
team join bmc4_raid_actif B
scoreboard players set #fin_h bmc4_raid 23
scoreboard players set #fin_m bmc4_raid 59
```
Puis, à la fin : `team empty bmc4_raid_actif`.
Remarque : la règle des coffres vérifie qu'**un membre** de la faction
propriétaire figure dans `bmc4_raid_actif`. Il faut donc inscrire au moins un
membre de chaque faction, comme le fait le bot.

## 1. Téléportations (décision 2 et 6)

Chaque moyen, trois fois : **hors combat** (doit passer), **en combat**
(refus « …refusé : tu as pris ou donné un coup il y a moins de 15 secondes.
Réessaie dans N s. »), **en raid simulé** (refus « …un raid est en cours pour
ta faction, jusqu'à 23 h 59. »).

| # | Moyen | Hors combat | En combat | En raid |
|---|---|---|---|---|
| 1 | Pierre de waystone (clic droit) | passe | refus | refus |
| 2 | Parchemin de téléportation (warp scroll) | passe | refus | refus |
| 3 | Warp stone | passe | refus | refus |
| 4 | Plaque de téléportation (warp plate) | passe | refus | refus |
| 5 | Sort Téléportation | passe | refus | refus |
| 6 | Sort Pas de sang | passe | refus | refus |
| 7 | Sort Pas de givre | passe | refus | refus |
| 8 | Sort Pas de foudre | passe | refus | refus |
| 9 | Sort Esquive (lancer) | passe | refus | refus |
| 10 | Esquive déjà active, puis un coup reçu | se téléporte | ne se téléporte pas | ne se téléporte pas |
| 11 | Sort Portail | passe | refus | refus |
| 12 | Sort Rappel | passe | refus | refus |
| 13 | Sort Dimension de poche | passe | refus | refus |
| 14 | Fruit de chorus | passe | refus | refus |
| 15 | Portail du Twilight Forest | passe | refus | refus |
| 16 | Portail de l'Aether | passe | refus | refus |
| 17 | **Perle de l'Ender** | passe | **passe** | **passe** |
| 18 | **Portail du Nether** | passe | **passe** | **passe** |
| 19 | **Ascenseur** | passe | **passe** | **passe** |
| 20 | `/home` (contrôle : déjà en place) | passe | refus | refus |
| 21 | `/tp` d'un op sur B en combat | passe (le staff n'est pas bloqué) | passe | passe |

Pour 5 à 13 : essayer aussi depuis un **parchemin** de sort, pas seulement le
livre.

## 2. Coffres (décision 11)

B dans le claim de F1 :

| # | Essai | Hors raid | Raid simulé (A et B inscrits) |
|---|---|---|---|
| 22 | Ouvrir un coffre | refus « Ouvrir ce bloc refusé : il est dans le claim de F1. » | s'ouvre |
| 23 | Ouvrir un four, un baril | refus | s'ouvre |
| 24 | Ouvrir une porte, une trappe, un portillon | s'ouvre | s'ouvre |
| 25 | Bouton, levier, plaque de pression | marche | marche |
| 26 | Établi, cloche, waystone | marche | marche |
| 27 | Casser le coffre | refus (FTB Chunks, comme avant) | refus |
| 28 | Un joueur C d'une **troisième** faction ou indépendant, pendant le raid | refus | **refus** |

Et A dans son propre claim : tout s'ouvre (contrôle).

## 3. Cartes (décisions 1 et 3)

| # | Essai | Attendu |
|---|---|---|
| 29 | A et B proches, minicarte Xaero | aucun point ni nom de joueur ; mobs, animaux, objets visibles |
| 30 | Carte du monde Xaero | aucun joueur |
| 31 | Mode grotte Xaero (minicarte et carte du monde), avec A (op) aussi | refusé / grisé |
| 32 | A (op) passe `ignore_enforcement_if_edit_permission` à true dans ses réglages | sans effet |
| 33 | Minicarte FTB Chunks | absente |
| 34 | Grande carte FTB Chunks (claims) | s'ouvre ; les claims sont là |
| 35 | Grande carte FTB Chunks, joueurs | B ne voit pas A, ni les autres joueurs hors de sa faction (après `settings_for` de l'étape C) |

## 4. Journal des ops et refus des mods (décisions 7 et 8)

| # | Essai | Attendu |
|---|---|---|
| 36 | A tape `/xp query A levels` | ligne dans `#console` en moins d'une minute |
| 37 | B (non op) tape `/prestige` | aucune ligne |
| 38 | `/prestige diagnostic` (A) | « mods du client » OK, « équipe bmc4_raid_actif » OK |
| 39 | Un client d'essai avec Advanced XRay (`xray`) | déconnecté avec le nom du mod et la marche à suivre ; alerte dans `#anti-triche` |

## 5. Duplication (décision 9)

| # | Essai | Attendu |
|---|---|---|
| 40 | Carry On : prendre un allay qui tient un objet | refusé |
| 41 | Table de transmutation d'Alex's Mobs : y poser un objet hors tables de butin | ne devient pas une option |
