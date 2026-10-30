# v66 — mise en place côté serveur

Lot : `/bmc4-depot/v66-<date>/`, déposé par `sh quetes/deploiement/deposer.sh --lot
v66-<date>`, sur le feu vert d'Arthur seulement. Le dépôt ne met rien en place. Une
action par ligne. Mot de passe SFTP rangé dans le trousseau.

**Snapshot avant le dépôt** : retirer Refurbished après l'ouverture exige `restore_snapshot`.

Contenu : Cinematic Interactions (fork, `e492fee`, SHA-1 `7347340d…`, le même jar que le
pack client), Refurbished 1.0.20, sa config serveur, `everycomp-hazardous.toml` et
`bmc4_v66_retraits.js`. Framework
0.8.0 est déjà en place. AFK Camera, Light Overlay, ClickThrough Plus et Glowing Trims sont client
seul, sans rien sur le serveur.

## Avant tout

1. `create_snapshot`, nom `avant-v66`. Attendre qu'il soit terminé. **Avant `deposer.sh`.**

## Mise en place

3. Arrêter le serveur (`power_action stop`).
4. `move_files` : les deux jars de `/bmc4-depot/v66-<date>/mods/` vers `/mods/`.
5. `move_files` : `/bmc4-depot/v66-<date>/config/refurbished_furniture.server.toml` vers `/config/`.
   `move_files` : `/config/everycomp-hazardous.toml` vers `/bmc4-depot/sauvegarde-v66/`, puis `/bmc4-depot/v66-<date>/config/everycomp-hazardous.toml` vers `/config/`. Il doit rester identique à celui du pack : un écart empêche de rejoindre.
6. `move_files` : `/bmc4-depot/v66-<date>/kubejs/server_scripts/bmc4_v66_retraits.js` vers `/kubejs/server_scripts/`.
7. Démarrer le serveur (`power_action start`).

## Vérifications

8. `latest.log` : `cinematic` et `refurbished_furniture` dans la liste des mods, aucune erreur de mixin, démarrage jusqu'à « Done ».
   `latest.log` : Every Compat n'écrit plus de ligne `Refurbished` parmi ses « registered … WoodType blocks ».
9. KubeJS : `bmc4_garde.js`, `bmc4_triche.js` et `bmc4_v66_retraits.js` chargés sans erreur.
10. `read_file /config/refurbished_furniture.server.toml` : Framework a complété le fichier, et `deliveryQueueSize = 8` et `everythingIsPowered = true` y sont toujours.
11. Console : `recipe give Arts_Vio refurbished_furniture:wrench`, avec `constructing/computer`, `television_remote` et `constructing/oak_light_ceiling_fan` : recette inconnue pour les quatre.
12. Première connexion d'un client v66 : voir « Ce qu'on surveille ».
13. Essais à deux joueurs de factions différentes, dans un claim :
   - four, alambic, juke-box, bibliothèque ciselée, lutrin, balise : la scène se ferme et rien ne s'ouvre ;
   - touche du feu de camp sur un feu du claim adverse : refusé ;
   - frigo, Post Box et boîte aux lettres du mod : refusés ;
   - cuisinière et micro-ondes marchent sans générateur ; une lampe s'allume seule ;
   - panneau sur un coffre dans le claim d'une autre faction, avec ClickThrough Plus : la garde refuse ;
   - même essai avec un cadre, puis avec un panneau posé hors claim contre un coffre du claim : la garde refuse ;
   - le propriétaire et ses alliés : tout s'ouvre ; pendant un raid : les fours et les coffres s'ouvrent ;
   - sur l'établi : la scène s'ouvre et les objets sont pris (règle décidée) ;
   - AFK Camera et Oculus, shader actif et coupé : pas de crash.
14. Reporter les résultats dans BMC-98.

## Ce qu'on surveille à la première connexion (Forge 47.4.20)

Le portage de Cinematic note un blocage non expliqué entre un client 47.4.20 et un
serveur 47.4.10 : `lost connection: Disconnected` avant l'apparition du joueur.

Dans `latest.log` du serveur, l'ordre attendu est :

    UUID of player <pseudo> is …
    <pseudo>[/…] logged in with entity id …
    <pseudo> joined the game

Si `lost connection: Disconnected` arrive entre `UUID of player` et `logged in`, ou juste
après `logged in` sans `joined the game` : relever l'heure, le `latest.log` du client, et
recommencer une fois. S'il se répète, retour arrière.

**Le paquet de connexion.** Refurbished ajoute 150 à 200 Ko bruts (estimation, module Every
Compat coupé). `latest.log` n'écrit pas cette taille par défaut : on ne peut
pas la lire, seulement voir si elle passe. Côté client comme côté serveur, chercher `VarInt too
big`, `Payload may not be larger`, `Packet too big`, `Connection lost during login` ou une déconnexion
avant `joined the game`. Le moindre de ces messages : retour arrière de Refurbished, pas d'ouverture.

**Les mixins, dans le `latest.log` du client.** Aucune ligne `Critical injection failure` ni
`Mixin apply for mod clickthrough failed`, et pas de plantage au lancement : GlitchCore redirige
le même appel que ClickThrough Plus (`AUDIT-v66.md`). Si le client plante sur
`switchCrosshairTargetItemUse`, repli sur ClickThrough Forge 1.0.0. Le log ne dit pas que les deux
mixins ont agi : le vérifier en jeu, par un clic à travers un panneau, puis par un usage d'objet
normal (nourriture, seau).

## Retour arrière

1. Arrêter le serveur.
2. **Cinematic seul** : `move_files` du jar de `/mods/` vers `/bmc4-depot/v66-<date>/mods/`. **Refurbished** : `restore_snapshot avant-v66` après l'ouverture ; avant, déplacer son jar, sa config et `bmc4_v66_retraits.js`, et remettre `everycomp-hazardous.toml` depuis `/bmc4-depot/sauvegarde-v66/`.
3. Démarrer le serveur.

**Cinematic** : les clients qui gardent le mod restent acceptés (`acceptMissingOr("12")`,
`displayTest="IGNORE_ALL_VERSION"`).

**Refurbished** : son retrait **enlève du monde ses blocs et leur contenu** (registres
absents). Les clients doivent de toute façon revenir au zip correspondant.

⚠️ **Videz vos établis avant un retrait de Cinematic.** Les objets vivent dans
`<dimension>/data/cinematic_tables.dat`, que seul le mod lit : sans lui, ils y restent
invisibles jusqu'à sa réinstallation. L'annoncer avant. Le snapshot ramène tout le monde à
l'instant de la sauvegarde.
