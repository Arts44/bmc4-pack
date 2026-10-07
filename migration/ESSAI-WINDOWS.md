# Essai réel du script Windows — pas-à-pas pour Arthur (BMC-93)

Sur le Dell Latitude 5500. **Version Windows : non essayée** tant que ce
pas-à-pas n'a pas été suivi jusqu'au bout et que `migration-bmc4.log` n'a pas
été rapporté mot pour mot.

Le script n'a pas pu être lancé, ni même vérifié syntaxiquement, sur le Mac :
PowerShell n'y est pas installé.

## 1. Préparer deux instances

Au choix.

**A. Depuis CurseForge (le vrai chemin des joueurs)**
1. Installe CurseForge (curseforge.com/download/app), puis Minecraft dans
   CurseForge.
2. Importe le zip **v61** (Créer → Importer). Lance-la une fois, va sur le
   serveur, pose **deux waypoints Xaero** (touche U) et **un waypoint FTB
   Chunks** (carte, touche M), change **une touche** (par exemple
   « Sauter » sur une autre touche) et mets la langue en français. Quitte.
3. Importe le zip d'essai **v62 avec migration** (fourni par le staff :
   `BMC4-v62-essai.zip`). **Ne la lance pas.**

**B. Depuis le Mac (plus rapide, sans téléchargement des mods)**
1. Sur le Mac, copie les dossiers `BMC4 v61` et `BMC4 v62` de
   `~/curseforge/minecraft/Instances/` sur une clé.
2. Sur le Dell, colle-les dans `%USERPROFILE%\curseforge\minecraft\Instances\`.
3. Dans la copie `BMC4 v62` : supprime `options.txt`, le dossier `logs`, et
   ouvre `minecraftinstance.json` dans le Bloc-notes pour remplacer
   `"playedCount":3` par `"playedCount":0`. C'est ce qui la rend « neuve ».
4. Copie dedans `migrer-bmc4.bat` et le dossier `bmc4-migration`, depuis la
   branche `bmc93-migration` du dépôt (dossier `migration/`).

## 2. Lancer le script

1. CurseForge → clic droit sur l'instance v62 → **Ouvrir le dossier**.
2. Double-clic sur **`migrer-bmc4.bat`**.
3. Si Windows affiche « Windows a protégé votre ordinateur » (SmartScreen) :
   **Informations complémentaires → Exécuter quand même**. Note-le.

## 3. Ce que tu dois voir à l'écran

Une fenêtre noire, puis, dans cet ordre :
- `Version : v62`, puis `Ancienne instance : …\BMC4 v61 (v61)` ;
- `1. Ce que le pack ne livre pas` : `copié : options.txt`, `servers.dat`,
  `xaero`, `local/ftbchunks` ;
- `2. Ce que le pack livre aussi` : une ligne `N copié(s), N gardé(s)…` ;
- `Bilan` : les waypoints Xaero **0 → le nombre que tu as posés**
  (avec la voie B : **0 → 18**), FTB Chunks **0 → 1** (voie B : **0 → 5**),
  `langue : fr_fr`, un nombre de touches (voie B : **272**) ;
- `✅ Terminé`, puis « Appuie sur Entrée ».

**Les accents doivent s'afficher correctement** (« copié », « gardé »). Des
caractères bizarres à leur place, c'est un échec à rapporter.

**Contre-essai** : relance `migrer-bmc4.bat` une seconde fois après avoir
lancé le jeu. Il doit refuser : « ❌ Cette instance a déjà été lancée ».

## 4. Ce que tu dois voir en jeu

Lance la v62 depuis CurseForge et va sur le serveur :
- le menu est **en français** ;
- la touche que tu avais changée **marche** ;
- **U** liste tes waypoints Xaero ; la carte FTB Chunks montre le tien.

## 5. Ce qu'il faut rapporter

1. Le fichier **`migration-bmc4.log`** (dans le dossier de l'instance v62),
   **en entier, mot pour mot**.
2. Le texte du contre-essai.
3. Si SmartScreen ou un antivirus s'est manifesté, et ce qu'il disait.
4. Les trois vérifications en jeu : oui ou non pour chacune.
