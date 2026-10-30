# BMC-103 — Cinematic Interactions : mise en place côté serveur

Lot : `/bmc4-depot/cinematic-<date>/`, déposé par
`sh quetes/deploiement/deposer.sh --lot cinematic-<date>`, sur le feu vert
d'Arthur seulement. Le dépôt ne met rien en place. Une action par ligne.

Jar : fork `Arts44/CinematicInteractions`, branche `bmc4`, commit `e492fee`
(amont `bb1bca1`, 0.18.30, plus le patch de protection), SHA-1
`7347340db99202e5a4781c1c2ba832485520e077`. Le jar client du pack doit être le
même : un serveur sans ce patch rouvre la faille, un client sans le mod reste
accepté.

## Avant tout

1. `create_snapshot`, nom `avant-cinematic`. Attendre qu'il soit terminé.

## Mise en place

2. Arrêter le serveur (`power_action stop`).
3. `move_files` : `/bmc4-depot/cinematic-<date>/mods/Cinematic-Interaction-Forge-1.20.1-0.18.30-bmc4.jar` vers `/mods/`.
4. Démarrer le serveur (`power_action start`). Un mod ne se charge pas sans redémarrage.

## Vérifications

5. `latest.log` : `cinematic` dans la liste des mods, aucune erreur de mixin, démarrage jusqu'à « Done ».
6. KubeJS : `bmc4_garde.js` et `bmc4_triche.js` chargés sans erreur.
7. Première connexion d'un client : voir « Ce qu'on surveille ».
8. Essais à deux joueurs de factions différentes, dans un claim :
   - four, alambic, juke-box, bibliothèque ciselée, lutrin, balise : la scène se ferme et rien ne s'ouvre ;
   - touche du feu de camp (s'asseoir) sur un feu du claim adverse : refusé ;
   - le propriétaire et ses alliés : tout s'ouvre ;
   - hors claim : tout s'ouvre ;
   - pendant un raid entre les deux factions : les fours s'ouvrent, comme les coffres.

## Ce qu'on surveille à la première connexion (Forge 47.4.20)

Le portage note un blocage non expliqué : un client 47.4.20 sur un serveur
47.4.10 est une fois resté bloqué avant l'apparition du joueur, et le serveur a
écrit `lost connection: Disconnected` (`docs/ports/1.20.1-forge/TESTING.md`,
candidat 0.18.28). Cause non établie, rien ne la rattache au code du mod.

Dans `latest.log` du serveur, pour le joueur qui se connecte, l'ordre attendu est :

    UUID of player <pseudo> is …
    <pseudo>[/…] logged in with entity id …
    <pseudo> joined the game

Si `lost connection: Disconnected` arrive entre `UUID of player` et
`logged in`, ou juste après `logged in` sans `joined the game`, c'est ce
blocage : relever l'heure, le `latest.log` du client et recommencer une fois.
S'il se répète, retour arrière. Noter aussi tout `VarInt too big` : le mod ajoute
un canal réseau à la liste échangée à la connexion (BMC-104).

## Retour arrière

1. Arrêter le serveur.
2. `move_files` : le jar de `/mods/` vers `/bmc4-depot/cinematic-<date>/mods/`.
3. Démarrer le serveur.

Les clients qui gardent le mod restent acceptés : le canal est déclaré en
`NetworkRegistry.acceptMissingOr("12")` des deux côtés (`net/Network.java`, vu
dans le bytecode du jar), et `displayTest="IGNORE_ALL_VERSION"`.

⚠️ **Les objets posés sur un établi ne sont pas rendus par le retrait.** Ils
vivent dans `<dimension>/data/cinematic_tables.dat`, que seul le mod lit.
Sans lui, ils restent dans le fichier, invisibles, jusqu'à sa réinstallation.
Annoncer avant le retrait qu'il faut vider les établis. Le snapshot `avant-cinematic`
ramène tout le monde, objets et progression, à l'instant de la sauvegarde.
