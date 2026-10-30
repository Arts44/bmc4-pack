# v66 — mise en place côté serveur

Lot : `/bmc4-depot/v66-<date>/`, déposé par `sh quetes/deploiement/deposer.sh --lot
v66-<date>`, sur le feu vert d'Arthur seulement. Le dépôt ne met rien en place. Une
action par ligne. Mot de passe SFTP rangé dans le trousseau.

Contenu : Cinematic Interactions (fork, `e492fee`, SHA-1 `7347340d…`, le même jar que le
pack client) et Refurbished 1.0.20. Framework 0.8.0 est déjà en place. AFK Camera, Light
Overlay, ClickThrough Plus et Pulse Trims sont client seul, sans rien sur le serveur.
**Passthrough Signs n'est pas livré.**

## Avant tout

1. `create_snapshot`, nom `avant-v66`. Attendre qu'il soit terminé.
2. Décider des fermetures de `AUDIT-v66.md` (Refurbished) : aucune n'est appliquée ici.

## Mise en place

3. Arrêter le serveur (`power_action stop`).
4. `move_files` : les deux jars de `/bmc4-depot/v66-<date>/mods/` vers `/mods/`.
5. Démarrer le serveur (`power_action start`).

## Vérifications

6. `latest.log` : `cinematic` et `refurbished_furniture` dans la liste des mods, aucune erreur de mixin, démarrage jusqu'à « Done ».
7. KubeJS : `bmc4_garde.js` et `bmc4_triche.js` chargés sans erreur.
8. Première connexion d'un client v66 : voir « Ce qu'on surveille ».
9. Essais à deux joueurs de factions différentes, dans un claim :
   - four, alambic, juke-box, bibliothèque ciselée, lutrin, balise : la scène se ferme et rien ne s'ouvre ;
   - touche du feu de camp sur un feu du claim adverse : refusé ;
   - frigo, Post Box et boîte aux lettres du mod : refusés ;
   - panneau sur un coffre dans le claim d'une autre faction, avec ClickThrough Plus : la garde refuse ;
   - même essai avec un cadre, puis avec un panneau posé hors claim contre un coffre du claim : la garde refuse ;
   - le propriétaire et ses alliés : tout s'ouvre ; pendant un raid : les fours et les coffres s'ouvrent ;
   - sur l'établi : la scène s'ouvre et les objets sont pris (règle décidée) ;
   - AFK Camera et Oculus, shader actif et coupé : pas de crash.
10. Reporter les résultats dans BMC-98.

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

**Taille du paquet.** Refurbished ajoute environ 150 à 200 Ko bruts à la connexion
(estimation), surtout en recettes. Tout `VarInt too big`, `Payload may not be larger`
ou déconnexion à la connexion : retour arrière de Refurbished, pas d'ouverture.

## Retour arrière

1. Arrêter le serveur.
2. `move_files` : le jar voulu de `/mods/` vers `/bmc4-depot/v66-<date>/mods/`.
3. Démarrer le serveur.

**Cinematic** : les clients qui gardent le mod restent acceptés (`acceptMissingOr("12")`,
`displayTest="IGNORE_ALL_VERSION"`).

**Refurbished** : son retrait **enlève du monde ses blocs et leur contenu** (registres
absents). Retirer le jar seul n'est sûr qu'avant l'ouverture ; ensuite, `restore_snapshot
avant-v66`. Les clients doivent de toute façon revenir au zip correspondant.

⚠️ **Videz vos établis avant un retrait de Cinematic.** Les objets vivent dans
`<dimension>/data/cinematic_tables.dat`, que seul le mod lit : sans lui, ils y restent
invisibles jusqu'à sa réinstallation. L'annoncer avant. Le snapshot ramène tout le monde à
l'instant de la sauvegarde.
