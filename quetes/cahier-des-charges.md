# Quêtes BMC4 — cahier des charges

Version 1 · 4 octobre 2026 · tâche BMC-89

Ce document décrit **toutes** les quêtes à écrire. Il remplace entièrement les 14 chapitres hérités de Better MC (environ 150 quêtes en anglais, écrites pour la 1.19.2, qui ignorent la trentaine de mods ajoutés depuis et tout ce qui fait BMC4).

Objectif chiffré : **environ 75 chapitres et 1 500 à 2 000 quêtes**, en français. Les sections 3 à 7 décrivent le parcours principal (≈600 quêtes, écrites une à une) ; la section 9 ajoute trois groupes générés à partir des données du pack (≈1 000 à 1 400 quêtes), qui font du livre une encyclopédie du serveur sans noyer le parcours.

Version 2 · 4 octobre 2026, 23 h 15 : Arthur veut « encore plus ». Ajout de la section 9 et approfondissement des chapitres de mods (section 9.4).

---

## 1. Règles générales

### Langue et ton

- Tout en **français** : titres, sous-titres, descriptions. Les noms d'objets restent ceux du jeu (on ne traduit pas « Mechanical Press » dans un titre si le jeu l'affiche en anglais ; on écrit « la Presse mécanique (Mechanical Press) » dans la description quand c'est utile).
- **Le titre dit l'action** : « Fabriquer une presse mécanique », pas « Presse ! ».
- **La description explique pourquoi** : à quoi sert la chose, où la trouver, le piège à éviter. Deux à quatre phrases. C'est elle qui fait de la quête un guide.
- Chaque chapitre s'ouvre sur une **quête d'introduction** sans tâche lourde (case à cocher ou objet de base) dont la description présente le mod ou la dimension en quelques lignes, et renvoie au salon de guide Discord correspondant quand il existe (`#create`, `#twilight-forest`, etc.).

### Les tâches

- **Objet** (`item`) pour fabriquer ou obtenir. C'est le cas général.
- **Tuer** (`kill`, et Quest Kill Task pour les entités par tag) pour les boss et les créatures notables.
- **Dimension** (`dimension`) pour la première entrée dans un monde.
- **Progrès** (`advancement`) quand un mod fournit déjà un progrès fiable — en particulier la **progression de Twilight Forest** (`twilightforest:progress_*`), qui est la seule mesure correcte des boss vaincus.
- **Structure** (`structure`) pour « trouver » un lieu, quand l'identifiant de structure existe.
- **Case à cocher** (`checkmark`) pour ce que le jeu ne mesure pas : régler le vocal, lier son compte Discord, déclarer un trophée. Ces quêtes sont honnêtes par nature ; leur récompense est donc toujours symbolique.
- **Observation** (`observation`) pour regarder un bloc ou une entité rare, quand c'est plus juste que de demander l'objet.

### Les récompenses — la règle d'équilibre

BMC4 est un serveur factions. Une quête qui donne des ressources donne de l'avance, et la faction la plus active en quêtes deviendrait la plus riche. D'où quatre classes, et une règle par arc :

| Classe | Contenu | Où |
|---|---|---|
| **R0** | XP seulement (2 à 10 niveaux) | partout, par défaut |
| **R1** | de quoi essayer : la poignée d'objets nécessaire à l'étape suivante (16 andésite alliage, 4 graines d'inferium, un livre de sorts de cuivre…) | ouverture des chapitres de mods, arc Premiers pas |
| **R2** | ressource réelle, plafonnée (quelques lingots, une table de butin « modeste ») | arc Premiers pas, jalons majeurs du monde |
| **S** | symbolique : bannière, tête, objet décoratif unique, trophée cosmétique, XP | boss, factions, collections |

Règles dures :
1. **Rien de revendable en quantité au Marché Flottant** : pas de stacks de diamants, de nétherite, d'essences de Mystical Agriculture au-delà de l'amorçage.
2. **Aucun objet qui saute une étape** : la récompense d'une quête ne fournit jamais l'objet que la quête suivante demande de fabriquer.
3. **Les boss donnent du symbolique** : le butin du boss suffit, la quête ne double pas.
4. **Les quêtes de l'arc Factions ne donnent que du S**.
5. Utiliser les **tables de récompense** de FTB Quests (`reward_tables/`) pour R2 : quatre tables, « Débutant », « Explorateur », « Artisan », « Aventurier », au contenu modéré et sans objet de fin de partie.

⚠️ **Progression par équipe.** FTB Quests suit la progression **par équipe FTB Teams** — et les factions sont des équipes FTB. Une faction de quatre complète donc ses quêtes ensemble. **Décidé le 4 octobre : une récompense par joueur**, pas de `team_reward`, R2 comprises. Chaque membre réclame la sienne. Conséquence assumée : une faction nombreuse touche plus qu'un indépendant seul, d'où l'importance des règles d'équilibre ci-dessous — rien de revendable en quantité, rien de fin de partie dans les tables.

### Mise en page

- Un chapitre se lit **de gauche à droite**, les dépendances tracées. Pas de quête orpheline au milieu de nulle part.
- Les quêtes facultatives (collections, défis) sont **sur une branche à part**, en forme distincte (`optional: true`, forme hexagone).
- Les quêtes de boss en forme **gear** ou **diamond**, plus grandes (`size: 1.5`).
- Icônes : l'objet de la tâche, ou l'œuf / la tête du boss.

---

## 2. Organisation

Cinq groupes de chapitres, dans cet ordre dans le livre :

```
1. Bienvenue            1 chapitre
2. Les bases du jeu     8 chapitres     (section 9.1)
3. Le monde            13 chapitres
4. Les mods            22 chapitres     (approfondis, section 9.4)
5. Les factions         4 chapitres     (+ 9.5)
6. Chaque semaine       2 chapitres     (section 9.3)
7. Défis                3 chapitres
8. Encyclopédie        ~22 chapitres    (section 9.2, générés)
```

L'**Encyclopédie** est placée en dernier et marquée comme facultative dans sa description : c'est un catalogue à remplir au fil du jeu, pas un chemin à suivre. Le parcours guidé reste lisible.

---

## 3. Bienvenue

### 3.1 Premiers pas au Marché Flottant (~22 quêtes)

Le spawn est au Marché Flottant (0 / 64 / 0) depuis le 4 octobre : tout commence là.

1. **Bienvenue sur BMC4** — case à cocher. Présente le serveur en factions, le Marché, le Discord. R0.
2. **Activer la waystone du Marché** — tâche : utiliser/obtenir la waystone (observation de la waystone centrale). Explique qu'une waystone activée reste accessible à vie et qu'on peut revenir ici gratuitement. R1.
3. **Lire le règlement** — case à cocher, renvoie à `#règles` et aux deux zones neutres. R0.
4. **Lier son compte Discord** — case à cocher, explique `/discord link` et ce qu'il débloque. S.
5. **Régler le vocal de proximité** — case à cocher. Touche V, choix du micro, 48 blocs / 24 en chuchotant. S.
6. **Le kit de départ** — tâche : avoir le sac `inmis:frayed_backpack`. Explique les paliers de sacs. R0.
7. **Choisir son camp** — case à cocher. Apex, Farmer's, indépendant, ou créer une faction (`#diplomatie`). R0.
8. **Bois, pierre, fer** — trois quêtes classiques (bûches, pierre taillée, lingot de fer). R1 chacune.
9. **Un premier abri** — lit. R0.
10. **Poser son claim** — case à cocher, touche M, FTB Chunks, 40 chunks par équipe, ce qu'un claim protège et ce qu'il ne protège pas (explosions). R2 « Débutant ».
11. **Une waystone à soi** — fabriquer une waystone. R0.
12. **Ne plus se perdre** — fabriquer une boussole, ouvrir la carte Xaero (case à cocher). R0.
13. **Nature's Compass** — fabriquer la boussole de biomes. R0.
14. **La première nuit** — tuer 5 zombies. R0.
15. **Diamants** — obtenir un diamant. R2 « Débutant ».
16. **Un sac plus grand** — sac `plated_backpack`. R0.
17. **Les tombes** — case à cocher expliquant You're in Grave Danger : où retrouver ses affaires après une mort. R0.
18. **Les coffres par joueur** — ouvrir un coffre Lootr. Explique que les coffres classiques de structure sont par joueur, que ceux de certains mods restent partagés. R0.
19. **Commercer** — case à cocher, renvoie au forum `#commerce` et aux barils des pavillons. S.
20. **Le livre des quêtes** — case à cocher qui présente les quatre autres groupes et l'ordre conseillé. R0.

---

## 4. Le monde

### 4.1 Overworld — exploration (~30 quêtes)
Trouver et piller : village, avant-poste de pillards, manoir des bois, temple du désert, temple de la jungle (YUNG's), monument océanique (YUNG's), mine abandonnée (YUNG's), donjon (YUNG's Better Dungeons), cabane de sorcière (YUNG's), ruines (Philips Ruins), tour d'Illusioniste, structures de Towns and Towers, Repurposed Structures (au moins trois variantes notables), Moog's (villages manquants, structures voyageur), Formations, Structory. Une quête par grande famille, tâche « structure » quand l'ID existe, sinon objet propre à la structure. R0, R2 « Explorateur » sur trois jalons.

Créatures : Conjurer (The Conjurer), Illager Invasion (Invoker = boss → arc 4.12), raid de village défendu (progrès `hero_of_the_village`). Biomes O' Plenty : visiter cinq biomes notables (tâche biome). Serene Seasons : passer une saison complète (case à cocher + description du calendrier des cultures).

### 4.2 Overworld — cavernes (~12 quêtes)
YUNG's Cave Biomes, Galosphere (cristaux, lumière, Spectre, lanterne d'allurite), géodes, ancienne cité (Dungeons and Taverns Ancient City Overhaul), Warden (S). Le **Deeper and Darker** se rattache ici : portail vers l'Otherside → chapitre 4.9.

### 4.3 Le Nether (~25 quêtes)
Entrer (dimension). Forteresse (YUNG's Better Nether Fortresses + compat Cataclysm), bastion, Better Nether (biomes, bois), Bygone Nether, Soulful Nether, Jaden's Nether Expansion, Nether's Delight (arc cuisine). Blaze, Wither squelette, tête de Wither ×3. **Invoquer et tuer le Wither** (S, gros nœud) — description : à faire loin de toute base, le claim ne protège pas des explosions. Débris antiques, lingot de nétherite (R0 : la nétherite ne se donne pas). Netherite Tweaks / Advanced Netherite → chapitre 5.17.

### 4.4 L'End (~22 quêtes)
Œil de l'Ender, forteresse (YUNG's Better Strongholds), portail, **Ender Dragon** (S, et rappel : le dragon donne la Poussière cognizante si `dragonDropsCognizant`), île de l'End (YUNG's Better End Island), villes de l'End, élytres (Elytra Slot), Better End (une quête par biome majeur : cinq), BetterEnd Crashed Ships, Moog's End Structures, coquilles de shulker → sac Shulker. Void Totem (objet de survie). R0 / S.

### 4.5 L'Aether (~35 quêtes)
Portail en glowstone, dimension. Aether de base : Moa (œuf, Protect Your Moa), holystone, zanite, gravitite, ambrosium, **Pierre de Soin** (lien direct avec la règle mediumcore des raids : elle rend un cœur — à expliquer). Donjons : **Slider** (bronze), **Reine des Valkyries** (argent), **Esprit du Soleil** (or) — S. Deep Aether (biomes, Stormwing, bois), Aether Redux (biomes, équipements), Aether: Lost Content (**Aerwhale King** S), Aether Villages, Treasure Reforging. Umbral Skies si présent dans la même dimension.

### 4.6 Twilight Forest — la progression (~30 quêtes)
Le cœur du chapitre est la **chaîne des boss**, chacune mesurée par l'avancement de progression du mod (`twilightforest:progress_*`), pas par un kill seul :

```
Naga → Liche → Minoshroom (labyrinthe) / Hydre
     → Chevaliers fantômes (bastion des Gobelins) → Ur-Ghast (tour sombre)
     → Yéti Alpha → Reine des Neiges → Château final
```

Pour chaque boss : une quête « trouver » (structure), une quête « vaincre » (progrès, S, forme gear), une quête « trophée » (obtenir le trophée du boss, S).

Descriptions à soigner, elles contiennent ce que les joueurs ont appris à leurs dépens :
- **Liche** : une seule est réelle, les autres sont des clones d'ombre invulnérables ; casser les six boucliers d'abord, chaque coup en retire un, une boule de neige suffit.
- **Labyrinthe** : la salle du Minoshroom est à l'étage **inférieur**.
- **Bastion des Gobelins** : poser un trophée de boss sur le piédestal à l'entrée pour dissoudre les boucliers ; il faut avoir vaincu la Liche.
- **Zones verrouillées** : la progression est appliquée sur le serveur, un biome dont le boss précédent n'est pas tombé inflige des malus.
- **Mac** : désactiver les shaders (crash près des portails).

### 4.7 Twilight Forest — exploration (~20 quêtes)
Collines creuses (petite, moyenne, géante — **pas de boss**, c'est du butin), clairière des quêtes (Quest Ram), tour des champignons, labyrinthe de haies, grotte des Trolls, Forêt enchantée, Forêt sombre, Marais du feu, objets marquants (bâton de la Liche, épée de feu, Fiery Ingot, Knightmetal, Ironwood, Steeleaf, arbres magiques : Transformation, Temps, Minage, Tri), Twilight's Flavor & Delight (lien cuisine). R0, R2 « Explorateur » sur un jalon.

### 4.8 Blue Skies (~30 quêtes)
Les deux mondes, **un chapitre chacun** (Everbright, Everdawn) comme aujourd'hui, mais réécrits :
- Portail (Zeal Lighter), Gatekeeper, Journal bleu.
- Outils et armures de chaque bois/minerai.
- **Donjons aveuglants** : l'Invocateur (Everbright), l'Alchimiste (Everdawn) ; puis le **Starlit Crusher** (donjon de la nature) et l'**Arachnarch** (donjon du poison). S chacun.
- **Artéfacts** : expliquer la relance d'un boss à difficulté supérieure en utilisant son artéfact sur la keystone, et les échanges du Gatekeeper pour les clés.

### 4.9 Deeper and Darker (~15 quêtes)
Ancienne cité, portail de l'Otherside, dimension, Echo, sculk transmitter, Soul Elytra, **Stalker** (S), Warden, compat Cataclysm (`deeper_and_darker_to_cataclysm`).

### 4.10 Cataclysm (~25 quêtes)
Un nœud par boss, chacun avec « trouver la structure » puis « vaincre » (S) puis l'équipement débloqué :
**Ender Guardian**, **Netherite Monstrosity**, **Ignis**, **The Harbinger**, **The Leviathan**, **Ancient Remnant**, **Maledictus**, **Scylla** si présent en 3.31. Armures **Ignitium** et **Cursium** (rappel : leurs recettes ont été réparées le 24 septembre).

### 4.11 Mowzie's Mobs (~10 quêtes)
Ferrous Wroughtnaut, Frostmaw, Umvuthi et ses Barakoa, Naga de Mowzie (à ne pas confondre avec celle de Twilight — le dire), Foliaath, Grottol. S pour les boss.

### 4.12 Donjons et autres boss (~25 quêtes)
When Dungeons Arise (une quête par structure majeure : six à huit), Stalwart Dungeons (**Awful Ghast**, **Nether Keeper**, **Shelterer** — S), Illager Invasion (**Invoker** — S, sorcier, Illusioner), Iron's Spells (**Dead King**, **Tyros** → aussi en 5.6), Alex's Mobs (**Void Worm** — S, rappel : plusieurs entités, la quête se mesure par l'objet qu'il lâche), Bountiful (prendre trois primes au tableau de primes), Dungeons and Taverns.

### 4.13 Les dragons (~15 quêtes)
Dragon Mounts: Legacy. Obtenir un œuf, **le faire éclore via le salon `#dragons`** (les œufs n'éclosent pas sur serveur dédié : l'échange œuf contre dragon passe par le bot — case à cocher), apprivoiser, selle, monter, une quête par race notable (feu, eau, Aether, fantôme, End, Nether…), croisement hybride (25 % de réussite sur BMC4 — le dire), DragonLoot (ce qu'il ajoute), hangar (lien BMC-19 côté Apex, mais quête neutre).

---

## 5. Les mods

Chaque chapitre : introduction (R1, de quoi démarrer), chaîne principale (R0), jalons (R2 plafonné), fin de chapitre (S).

### 5.1 Create — les bases (~25)
Alliage d'andésite, arbre, engrenage, grand engrenage, roue hydraulique, moulin à vent, manivelle, boîte de vitesses, courroie, **Presse mécanique**, **Mélangeur**, **Meule**, **Roues de broyage**, ventilateur encastré (lavage, fumage, hantise : trois quêtes), bassin, dépôt, entonnoir et tunnel en andésite, **Ponder** (expliquer la touche W de Ponder).

### 5.2 Create — fabrication avancée (~25)
Laiton, mécanisme de précision (**assemblage séquencé**), Deployer, scie et foreuse mécaniques, bras mécanique, Blaze Burner (et le nourrir), Super-chauffe, moteur à vapeur, régulateur de vitesse, mesureurs (stress, vitesse), contraptions (piston mécanique, roulement, portique), Schematicannon et Schematic Table.

### 5.3 Create — logistique et trains (~20)
Create 6 : Packager, Frogport, chaîne de convoyeur, Stock Link, Stock Ticker, Factory Gauge — une quête par élément, la description dit à quoi il sert concrètement. Trains : voie, station, signal, horaire, assembler un train. (Si Steam 'n' Rails passe au vote, un chapitre 5.3 bis s'ajoute.)

### 5.4 Mystical Agriculture (~30)
Essence de prospérité, Inferium, graines d'essence, **les six paliers** (Inferium → Prudentium → Tertium → Imperium → Supremium → **Supremium éveillé**), infusion, cultures de ressources (une quête par famille : bois, pierre, fer, or, diamant, nétherite), Growth Accelerator, Harvester, outils et armures par palier, **Autel d'éveil** et **Poussière cognizante** (Wither ou Dragon avec une arme Mystical Enlightenment). Cucumber en bibliothèque, rien à expliquer.

### 5.5 Pylons (~6)
Les pylônes, en particulier le **Harvester Pylon** : description complète (houe obligatoire, 1 durabilité par récolte, impossible à automatiser, d'où la houe en Supremium éveillé). Lien avec 5.4.

### 5.6 Iron's Spells 'n Spellbooks (~35)
Essence arcanique, table d'inscription, livres de sorts (cuivre → … → légendaire), parchemins, **une quête par école** (feu, glace, foudre, sacré, ender, sang, évocation, nature, éclipse si présente), orbes d'amélioration, enclume arcanique, chaudron d'alchimiste, armures de mage par école, **Dead King** et **Tyros** (S), Hazen 'n Stuff (armures « Pure », +150 mana) en fin de chapitre.

### 5.7 Énergie : Powah (~25)
Câbles, Energizing Orb et Rod, **les sept paliers** (Starter → Basic → Hardened → Blazing → Niotic → Spirited → Nitro), générateurs (solaire, thermo, Furnator, Magmator, **réacteur**), Energy Cell, Ender Cell, Player Transmitter, chargeur.

### 5.8 Stockage (~30)
Trois sous-arbres, et la description d'ouverture rappelle de **n'en choisir qu'un par base** :
- **Storage Drawers** : tiroir, tiroir de compactage, contrôleur, améliorations (stockage, void), Extras.
- **Simple Storage Network** : maître, câble, table de requête, câble d'import.
- **Refined Storage** : contrôleur, lecteur de disques, disques 1k → 64k, grille, grille de fabrication, grille de patrons, crafter, importeur/exportateur, grille sans fil.

### 5.9 Tuyaux et transport : Pipez (~8)
Tuyau d'objets, de fluides, d'énergie, universel, améliorations, filtres (FTB Filter System, Item Filters).

### 5.10 CC: Tweaked (~10)
Ordinateur, ordinateur avancé, moniteur, modem, **tortue**, tortue minière. Description d'ouverture : écrire ses propres règles (alarme, porte à code, affichage de stock).

### 5.11 SecurityCraft (~25)
Le chapitre qui intéresse le plus un serveur factions. Keypad, **blocs renforcés** et Universal Block Reinforcer, porte à clavier, Laser Block, caméra et moniteur, Inventory Scanner, Retinal Scanner, mines, Sentry, Block Change Detector, Codebreaker. Description : un claim protège l'intérieur, SecurityCraft protège ce qui est **hors claim** (le donjon du trophée).

### 5.12 Iron Jetpacks (~10)
Composants, les paliers de jetpack (bois → … → émeraude/créatif selon ce qui est disponible), moteur, améliorations.

### 5.13 Cuisine (~40)
Farmer's Delight (planche à découper, marmite, poêle, couteau, **plats mijotés** — rappel : chacun rend un cœur perdu en raid), puis une branche par extension : Chef's Delight, Ender's Delight, My Nether's Delight, Ocean's Delight, Crabber's Delight, Twilight's Flavor & Delight, Delightful, Autochef's Delight. Brasserie et Kaleidoscope si les votes passent (chapitre à compléter). Hearth & Home, Hearths (cheminées).

### 5.14 Magie : enchantement (~12)
Enchanting Infuser (avancé), Easy Anvils, Easy Disenchanting, Easy Magic, XP Tome, Treasure Reforging (Aether), livres rares. Rappel règle : **Soulbound est retiré** (BMC-82) — ne pas en faire une quête.

### 5.15 Construction et décoration (~35)
Chipped (établis), Dawn of Time, Handcrafted, Another Furniture, **Paladin's Furniture** (cuisine fonctionnelle), Decorative Blocks, Supplementaries (+ Squared, Amendments), Quark (blocs), Twigs, Stoneworks, Universal Sawmill, Vertical Slabs, Every Compat (le dire : c'est lui qui décline les blocs dans tous les bois), Immersive Lanterns, Diagonal Fences/Walls, Gallery (tableaux), Elevator Mod (ascenseur). R0, une collection optionnelle par mod.

### 5.16 Faune (~20)
Alex's Mobs (une sélection de créatures et d'objets utiles), Friends & Foes, Guard Villagers (golem et gardes), RevampedWolf, Incubation, Just Enough Breeding (le signaler pour l'élevage), Pet Cemetery.

### 5.17 Équipement de fin de partie (~12)
Advanced Netherite (paliers fer, or, émeraude, diamant sur nétherite), Netherite Tweaks, Shield Expansion, Charm of Undying, Just Hammers, Vein Mining (le signaler), Blossom Blade.

### 5.18 Villages et commerce (~12)
Villages & Pillages, VillagersPlus, Smarter Farmers, Trading Post, Goblin Traders, Bartering Station, Just Enough Professions. Une quête par métier clé (bibliothécaire, forgeron d'armes…).

### 5.19 Déplacement (~10)
Waystones (pierre de retour, parchemin de téléportation), Grand Teleport, élytres, bateaux (Boatload), Carry On (transporter un coffre — le dire, et ce qui est interdit), Nature's Compass.

### 5.20 Saisons et monde vivant (~6)
Serene Seasons (calendrier, cultures de saison, thermomètre), Snow! Real Magic!, Climate Rivers. R0.

### 5.21 Confort (~8)
Sacs Inmis (tous les paliers), Comforts (sac de couchage), Mouse Tweaks, Jade, EMI/JEI (case à cocher : la touche U et R), Ping Wheel (case à cocher : marquer un point pour sa faction), Xaero (points de passage).

### 5.22 Nouveautés du pack (chapitre vivant)
Chapitre court qui reçoit les quêtes des mods ajoutés après le vote du dimanche (Kaleidoscope, Maps 3D, etc.), pour ne pas bousculer les autres chapitres.

---

## 6. Les factions

Uniquement des récompenses **S**. La plupart des tâches sont des **cases à cocher**, parce que ces actions vivent dans le bot Discord et pas dans le jeu. Prévoir pour plus tard : le bot pourrait cocher lui-même via `/ftbquests change_progress` quand l'événement a lieu (à noter, pas à faire maintenant).

### 6.1 Bâtir sa faction (~15)
Rejoindre une faction (ou en créer une via `#diplomatie`), poser sa base (claim), étendre le claim, sécuriser ses waystones (une waystone activée reste ouverte à vie à qui l'a visitée), le salon `#stratégie` de sa faction, `!help faction`, `!tache`, `!lieu`.

### 6.2 Le trophée et les raids (~15)
Lire les règles de raid, **déclarer son trophée** (`!trophee poser`, contraintes : hors claim, à moins de 50 blocs du bord du claim, atteignable sans rien casser, aucun lit ni ancre à 50 blocs), bâtir le donjon du trophée (SecurityCraft, pièges), déclarer un raid 24 h à l'avance, participer à un raid, **mourir en raid coûte un cœur** (mediumcore pendant l'heure de raid, plancher 3 cœurs, plats mijotés et Pierre de Soin pour récupérer), gagner un raid.

### 6.3 Diplomatie et commerce (~10)
Proposer une alliance, signer un traité, négocier à la Table des négociations, ouvrir une offre dans `#commerce`, conclure un échange au Marché Flottant, respecter la zone neutre (description : 50 blocs autour du Marché, aucune protection technique, la trêve ne tient que sur la règle).

---

## 7. Défis

Tout est **optionnel**, forme hexagone, récompenses **S** uniquement.

### 7.1 Chasseur de boss (~1 quête par boss du serveur)
Un tableau de chasse : chaque boss listé dans les chapitres ci-dessus, en optionnel, avec une quête finale « Tous les boss » (S, gros nœud). Reprend la liste de `boss.js` du bot pour rester cohérent avec `#faits-d-armes`.

### 7.2 Explorateur (~15)
Visiter chaque dimension, X biomes, Y structures, parcourir N km (statistique), toutes les collines creuses.

### 7.3 Collectionneur (~15)
Toutes les essences de Mystical Agriculture, tous les trophées Twilight, toutes les races de dragons, tous les disques, toutes les armures de boss.

---

## 9. Version étendue

### 9.1 Les bases du jeu (8 chapitres, ≈150 quêtes, écrites à la main)

Le vanilla que Better MC ne couvrait pas, réécrit comme un guide. R0 partout, R1 sur l'ouverture de chaque chapitre.

1. **Agriculture et élevage** (~25) : chaque culture vanilla, composteur, poudre d'os, chaque animal élevable (Just Enough Breeding en appui), ruches et miel, et les cultures des saisons (Serene Seasons : ce qui pousse quand).
2. **Pêche et océan** (~15) : canne, trésors de pêche, Ocean's Delight, Crabber's Delight, tortues, axolotls, conduit.
3. **Archéologie** (~12) : pinceau, sable suspect, chaque motif de poterie, renifleur et ses graines.
4. **Redstone** (~20) : de la torche au comparateur, observateur, piston collant, trappe automatique, ferme automatique simple, puis Alternate Current (le signaler : la redstone est plus rapide sur ce serveur).
5. **Alchimie** (~30) : alambic, **chaque potion vanilla** dans ses variantes (normale, prolongée, renforcée, jetable, persistante), flèches à effet.
6. **Enchantement et forge** (~20) : table, bibliothèques, enclume, meule, table de forgeron, **chaque modèle d'ornement d'armure** (trims) — rappel BMC-60 : seuls les matériaux présents dans le pack s'affichent.
7. **Musique et décor** (~15) : chaque disque, juke-box, têtes de créatures, bannières et leurs motifs.
8. **Cartographie** (~10) : carte, table de cartographie, cartes au trésor, marqueurs, Xaero (points de passage partagés), Maps 3D si le vote passe.

### 9.2 L'Encyclopédie (≈22 chapitres, ≈1 000 quêtes, générés)

C'est ici que vient le volume, et il ne s'écrit pas à la main : le générateur **parcourt les registres et les tags des jars** et crée une quête par entrée, avec une description courte tirée d'un modèle par catégorie (« Rencontrer le Grizzly — Alex's Mobs. Neutre, attaque si on s'approche de ses petits. »). Les descriptions spécifiques ne sont écrites à la main que pour les entrées notables.

Toutes ces quêtes sont **facultatives**, en hexagone, récompense **R0 ou S** — jamais de ressource : 1 000 quêtes à ressources, ce serait une imprimerie à diamants.

| Chapitre | Contenu | Tâche | Volume indicatif |
|---|---|---|---|
| Bestiaire — Overworld | chaque créature vanilla + Alex's Mobs + Friends & Foes + Mowzie's + Guard Villagers | observation de l'entité | ~150 |
| Bestiaire — Nether et End | créatures de Better Nether, Bygone, Soulful, Jaden's, Better End | observation | ~50 |
| Bestiaire — dimensions | Aether (+ Deep Aether, Redux, Lost Content), Twilight Forest, Blue Skies, Otherside | observation | ~120 |
| Biomes — Overworld | chaque biome vanilla + Biomes O' Plenty + YUNG's Cave Biomes | biome | ~110 |
| Biomes — Nether et End | Better Nether, Bygone, Better End | biome | ~45 |
| Biomes — dimensions | Aether, Twilight Forest, Everbright, Everdawn, Otherside | biome | ~45 |
| Structures | chaque structure présente dans les registres (YUNG's, Dungeons Arise, Towns and Towers, Repurposed Structures, Moog's, Structory, Formations, Philips Ruins, Stalwart, Explorations+, Farmer's Structures, Dungeons and Taverns, AdoraBuild…) | structure | ~200 |
| Gastronomie | chaque plat de Farmer's Delight et des huit extensions | objet | ~200 |
| Grimoire | chaque sort d'Iron's Spells, via son parchemin | objet | ~100 |
| Herbier | chaque essence de Mystical Agriculture (graine et récolte) | objet | ~90 |
| Armurerie | chaque armure et arme notable des mods (Aether, Twilight, Blue Skies, Cataclysm, Iron's Spells, Advanced Netherite, Deeper and Darker) | objet | ~80 |
| Arsenal de défense | chaque bloc de SecurityCraft | objet | ~60 |
| Atelier Create | chaque machine et composant de Create | objet | ~80 |
| Trophées | chaque trophée de boss et chaque tête | objet | ~30 |
| Disques et musiques | tous les disques de tous les mods | objet | ~25 |
| Dragons | chaque race de Dragon Mounts | observation | ~15 |
| Minerais | chaque minerai et lingot de tous les mods | objet | ~60 |
| Bois | chaque essence d'arbre de tous les mods (Every Compat) | objet (bûche) | ~60 |

Chaque chapitre se termine par une quête « Tout le chapitre » (S, gros nœud), et le groupe par une quête « L'Encyclopédie complète » — la récompense la plus rare du serveur, purement cosmétique.

**Garde-fou de génération** : une entité, un biome ou une structure qui n'apparaît pas réellement sur le serveur (désactivé par config, dimension non chargée, structure retirée par Sparse Structures ou Structure Essentials) ne doit pas devenir une quête impossible. Croiser avec les configs du serveur et avec `#structures` / `#génération-du-monde`, et lister les exclusions dans le compte-rendu.

### 9.3 Chaque semaine (2 chapitres, quêtes répétables)

FTB Quests sait rendre une quête **répétable** avec un délai. Deux chapitres qui font revenir les joueurs :

- **Contrats de la semaine** (~20 quêtes répétables, délai 7 jours) : livrer 64 blé, tuer 30 squelettes, miner 500 blocs, pêcher 20 poissons, cuisiner 10 plats mijotés, visiter le Marché… Récompense **R0 + une table « Contrat »** très modeste (de la nourriture, des torches, de la poudre d'os, jamais de minerai rare). Le délai se cale sur le dimanche 20 h du classement si la version le permet.
- **Défis de faction** (~10 quêtes répétables, délai 7 jours, **progression d'équipe**) : effort collectif mesurable en jeu (miner 5 000 blocs en équipe, tuer 3 boss différents dans la semaine). Récompense **S** seulement — une bannière de la semaine, de l'XP.

### 9.4 Approfondir les chapitres de mods

Chaque chapitre de la section 5 passe de « la chaîne principale » à **tout ce que le mod apporte d'utile**, en gardant la chaîne principale au centre et en mettant le reste en branches latérales :

- **Create** : 3 → **5 chapitres** (bases, fabrication, contraptions et machines mobiles, logistique Create 6, trains), ~120 quêtes.
- **Mystical Agriculture** : chaque palier devient une rangée complète (graine, outils, armure, infusion), ~60 quêtes.
- **Iron's Spells** : une **sous-branche par école** avec ses sorts phares, son armure, son orbe, ~70 quêtes.
- **Powah** : chaque appareil à chaque palier, ~45 quêtes.
- **Stockage** : chaque élément des trois systèmes, ~50 quêtes.
- **SecurityCraft** : par usage (portes, détection, pièges, caméras, renforcement), ~45 quêtes.
- **Cuisine** : une **branche par extension**, chacune avec ses ustensiles et ses plats signature, ~80 quêtes (la liste exhaustive des plats va dans l'Encyclopédie).
- **Construction** : une branche par mod de déco, ~70 quêtes.

### 9.5 Factions — un quatrième chapitre

**Histoire du serveur** (~15, cases à cocher, S) : un chapitre de récit qui raconte BMC4 — l'ouverture, la création d'Apex et des Farmer's, le Marché Flottant, la première règle de raid, la mise en place du mediumcore — et qui fait visiter les lieux qui en témoignent. Il grandit avec le serveur : à compléter après chaque événement marquant (premier raid gagné, nouvelle faction, battle royale du 5 janvier).

---

## 10. Ce qu'il ne faut pas faire

- **Ne jamais inventer un identifiant.** Chaque objet, entité, structure, dimension et progrès cité dans une quête doit être **vérifié dans les jars du pack** (registres, fichiers de langue, données) avant d'être écrit. Un identifiant introuvable : la quête est retirée ou reformulée, et listée dans le compte-rendu.
- Ne pas recopier les anciens chapitres : ils servent seulement d'exemple de format.
- Pas de quête sur Open Parties and Claims (retiré), sur l'enchantement Soulbound (retiré), ni sur un mod encore au vote.
- Pas de quête dont la récompense finance la quête suivante.
