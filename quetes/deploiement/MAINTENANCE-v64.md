# Maintenance v64 — dimanche 11 octobre 2026

Une action par ligne, dans l'ordre. On ne passe à la suivante qu'après avoir
vu le résultat attendu. Si une étape rate : **§ Retour arrière**, sauf
indication contraire.

Serveur MineStrator 486488. Les actions « console » passent par
`send_console_command`. Le compte de test est Arts_Vio. Lot :
`quetes/deploiement/v64-2026-10-10/` (préparé le 10 octobre, `SHA1SUMS`
vérifié). Zips : `releases/BMC4-v64.zip`, ou `releases/BMC4-v64-avec-b.zip`
si la revue de 20 h 30 valide les mods de #mods.

**Le choix B se fait avant l'étape 1** : il décide quel zip on importe, et si
`mods-si-b-valides/` et `datapack-si-b-valides/` sont mis en place.

## 1. Fermeture

1. Console : `whitelist add Arts_Vio` → « Added Arts_Vio to the whitelist » (ou « already whitelisted »).
2. Console : `whitelist on` → « Whitelist is now turned on ».
3. Console : `kick @a[name=!Arts_Vio] Le serveur ferme un moment pour la v64. Réouverture annoncée dans #annonces.`
4. Console : `list` → personne, ou Arts_Vio, ou HelXo1 (op, il passe la whitelist).

## 2. Sauvegarde

5. `create_snapshot`, nom `avant-v64`. Attendre qu'il soit terminé (`list_snapshots`).
6. Noter le nom du snapshot dans `journal-migration.md`.

## 3. Dépôt du lot (whitelist active)

7. Sur le Mac, depuis la racine du dépôt : `sh quetes/deploiement/deposer.sh --lot v64-2026-10-10`.
8. Lire la sortie : chaque fichier « identique », puis « Dépôt vérifié dans /bmc4-depot/v64-2026-10-10 ». Un « DIFFÉRENT » : on s'arrête là, rien n'est encore en place.

## 4. Mise en place

9. `power_action stop`. Attendre l'état arrêté (`get_server_live`).
10. `move_files` : les 4 jars de `/bmc4-depot/v64-2026-10-10/mods/` vers `/mods/` (Just Outdoor Stuffs, FastFurnace, Placebo, Connectible Chains).
11. **Seulement si B est validé** : `move_files` des 4 jars de `/bmc4-depot/v64-2026-10-10/mods-si-b-valides/` vers `/mods/`.
12. **Seulement si B est validé** : `move_files` du dossier `/bmc4-depot/v64-2026-10-10/datapack-si-b-valides/bmc4-taverne` vers `/world/datapacks/`.
13. `move_files` des trois fichiers de `A-RETIRER.txt` (XaeroPlus) vers `/bmc4-depot/sauvegarde-v64/`, mêmes chemins relatifs. Déplacer, ne pas supprimer.
14. `list_files /mods` : les nouveaux jars y sont, aucun jar de Do a Barrel Roll, Leawind ou Studious Keybinds (client seul).

## 5. Redémarrage

15. `power_action start`.
16. `get_console_logs` jusqu'à « Done » : pas de crash, pas d'erreur de mixin.
17. Dans le journal : les modIds `justoutdoorstuffs`, `fastfurnace`, `placebo`, `connectiblechains` (et si B : `kaleidoscope_tavern`, `kaleidoscope_cookery`, `food`, `railways`).
18. Dans le journal : `bmc4_triche.js` chargé par KubeJS, sans erreur.
19. **Si B** : console `datapack list` → `[file/bmc4-taverne]` dans les packs activés.

## 6. Import réel du zip (vérifie aussi la distribution)

20. Sur ton Mac, app CurseForge : **Minecraft → Créer → Importer** → le zip v64 choisi.
21. Regarder la fin de l'import :
    - tout se télécharge seul → étape suivante ;
    - **Studious Keybinds** seul est refusé, ou demandé en téléchargement manuel → annuler l'import ; je retire le mod, reconstruis le zip, et tu recommences à l'étape 20 ;
    - un autre mod est refusé ou manuel → on s'arrête et on en parle avant de continuer.
22. Clic droit sur la nouvelle instance → **Ouvrir le dossier** : `migrer-bmc4.command` et `migrer-bmc4.bat` sont là. **Ne pas** lancer le script : on essaie un client neuf.

## 7. Connexion d'un client v64 neuf

23. Lancer la nouvelle instance.
24. **Options → Contrôles… → Assignation des touches…** : FTB Chunks / Open Map sur **ù**, Chat vocal / Couper le microphone sur **²**, la carte Xaero sur **M**, aucune ligne en rouge. Le bouton **Keyboard** (Studious Keybinds) ouvre le clavier dessiné sans erreur.
25. Rejoindre le serveur avec Arts_Vio → connexion acceptée.
26. (Contrôle de refus) Avec l'ancienne instance v62 : la connexion doit être refusée avec la liste des mods. Fermer ensuite l'ancienne instance.

## 8. Les quatre essais en jeu

Dans une zone sans claim, loin des bases. Pour compter les objets, en survie : `/gamemode survival`.

**Essai 1 — l'assise (Just Outdoor Stuffs)**

27. Poser un siège de Just Outdoor Stuffs et faire clic droit dessus.
28. Attendu : tu es assis, pas de crash ni de texture violette et noire ; Maj te relève.

**Essai 2 — dupe de chaînes (Connectible Chains)**. Le serveur n'ouvre pas sans ces trois résultats.

29. Inventaire vide, puis exactement **10 chaînes** et **10 pierres taillées** (`/give Arts_Vio minecraft:chain 10`, `/give Arts_Vio minecraft:cobblestone 10`).
30. Poser deux clôtures à 5 blocs l'une de l'autre.
31. *Dupe de l'issue #78* : chaînes en **main gauche**, pierres en **main droite**. Clic droit sur une clôture.
32. Clic droit une deuxième fois sur la même clôture.
33. Compter : chaînes + pierres = 20 au total, et pas une pierre de plus que 10. Une pierre en plus et une chaîne en moins = la dupe existe → **le serveur n'ouvre pas** (§ Retour arrière).
34. Annuler le lien en cours s'il y en a un (clic droit dans le vide), vider l'inventaire, reprendre 10 chaînes.
35. *Lien normal* : chaîne en main droite, clic droit sur la clôture A, puis sur la clôture B. Une chaîne tendue apparaît ; tu as 9 chaînes.
36. Casser la clôture B. Ramasser ce qui tombe : tu reviens à **10 chaînes**, pas plus.
37. *Dupe de l'issue #86* : refaire le lien A → B (9 chaînes en main), puis `/give Arts_Vio minecraft:tnt 1` et `/give Arts_Vio minecraft:flint_and_steel 1`.
38. Poser la TNT juste sous le milieu de la chaîne, l'allumer au briquet, s'éloigner d'au moins 10 blocs.
39. Ramasser tout ce qui est tombé : **une seule** chaîne au sol (total 10). Douze chaînes = la dupe existe → **le serveur n'ouvre pas**.
40. Relancer un lien A → B, se déconnecter, se reconnecter : la chaîne est toujours là, une seule.

**Essai 3 — Do a Barrel Roll avec Elytra Slot**

41. Mettre une élytre dans l'emplacement **Elytra Slot** (pas sur le torse).
42. F7 pour activer Do a Barrel Roll, puis s'envoler.
43. Attendu : le roulis fonctionne en vol, pas de crash, pas d'élytre dupliquée ; l'accélération du mod reste refusée (le serveur n'a pas le mod).

**Essai 4 — Leawind sur un dragon**

44. F5 jusqu'à la vue par-dessus l'épaule.
45. Monter sur un dragon et voler le long d'un mur.
46. Attendu : la caméra s'arrête au mur et ne passe jamais à travers ; pas de crash. Maintenir F8 permet de déplacer la caméra.

## 9. Publication

47. Si B n'est pas validé : publier `releases/BMC4-v64.zip` avec `releases/v64.md`. Si B l'est : `releases/BMC4-v64-avec-b.zip`, et décommenter le paragraphe B de `releases/v64.md` avant.
    Si B l'est, `migration/empreintes/v64.txt` du dépôt doit être celle du zip avec B (la liste Crash Assistant et les touches y diffèrent) : relancer `python3 migration/assembler.py <BMC4-v64-avec-b-exporte.zip> releases/BMC4-v64-avec-b.zip` en dernier, et commiter l'empreinte.
48. Release GitHub v64 publiée ; `releases/latest` pointe dessus.
49. Éditer le message #informations (1549946063392079954) avec `releases/v64/informations-v64.md`.
50. Poster le changelog dans #annonces (lien de la release).

## 10. Ouverture

51. Console : `whitelist off`.
52. Console : `whitelist remove Arts_Vio`.
53. Vérifier `white-list=false` dans `server.properties`, `whitelist.json` vaut `[]`, et `ops.json` contient toujours HelXo1 et Arts_Vio.
54. Une ligne dans `journal-migration.md` : snapshot, lot, zip publié, résultats des quatre essais.

## Retour arrière

1. Ne pas ouvrir : la whitelist reste active.
2. `power_action stop`.
3. Remettre les jars ajoutés (et le datapack si B) dans `/bmc4-depot/v64-2026-10-10/`, et XaeroPlus à sa place depuis `/bmc4-depot/sauvegarde-v64/`.
4. Si le monde a souffert (essais, explosion) : `restore_snapshot avant-v64`.
5. `power_action start`, puis § Ouverture : les joueurs restent en v62, aucune release v64 publiée.
