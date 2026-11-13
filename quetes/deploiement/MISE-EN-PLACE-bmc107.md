# BMC-107 — La garde des coffres, même avec un objet en recharge en main

Lot : `/bmc4-depot/bmc107-<date>/`, déposé par `sh quetes/deploiement/deposer.sh
--lot bmc107-<date>`, sur le feu vert d'Arthur seulement. Le dépôt ne met rien en
place. Une action par ligne. **Rien de ceci n'a été essayé en jeu ni sur un
serveur** : le constat vient du bytecode, la logique des scripts est testée hors
jeu avec de faux objets (`node --test quetes/tests/garde-coffres.test.mjs`).

## Le trou

`KubeJSBlockEventHandler.rightClick` (KubeJS 2001.6.5-build.26) ne poste pas
`BlockEvents.rightClicked` si `player.getCooldowns().isOnCooldown(objet en main)`.
Avec une perle de l'Ender ou un bouclier en recharge dans la main, la règle des
coffres de `bmc4_garde.js` ne voit pas le clic. Apex et Farmer's sont en
`block_interact_mode = public` dans FTB Chunks : pour leurs coffres, la garde est
la seule protection. Ce relais passe par Architectury
(`EventHandlerImplCommon.eventPlayerInteractEvent`, `@SubscribeEvent` priorité HIGH).

Trouvé en plus : `event.cancel()` de KubeJS lève `EventExit`. Dans la version en
service, le message de refus venait après `event.cancel()` : il ne partait pas
(lu dans le bytecode, pas observé).

## Les fichiers

| Fichier du lot | Va dans | Octets | SHA-1 |
|---|---|---|---|
| `kubejs/server_scripts/bmc4_garde.js` | `/kubejs/server_scripts/` (remplace) | 44 607 | `35f3d3473d115f1dfdf4d5ca29f41d85ea6c2e6c` |
| `kubejs/startup_scripts/bmc4_coffres_recharge.js` | `/kubejs/startup_scripts/` (nouveau) | 4 746 | `80ecf15348f15068965ca520bba8cac1e0ca1e58` |

La version en service de `bmc4_garde.js` fait 39 982 octets, SHA-1
`2bedcfb323a43f2188eedca7ebbab0f4fe1e6b7e` (commit `354dbea` de cette branche). Une
autre taille sur le serveur : s'arrêter, le fichier a changé depuis le 13 novembre.

- `bmc4_garde.js` : la règle `coffreInterdit` ne change pas. Elle est appelée par
  une seule fonction (`bmc4GardeCoffres`), qui garde la décision du clic et le
  délai d'un message par seconde. Les deux chemins passent par elle : KubeJS
  (`BlockEvents.rightClicked`) et `global.bmc4GardeCoffre`.
- `bmc4_coffres_recharge.js` : un écouteur Forge de
  `PlayerInteractEvent$RightClickBlock` (`ForgeEvents.onEvent`, priorité NORMAL,
  ne reçoit pas les événements déjà annulés). Il ne décide rien : il appelle
  `global.bmc4GardeCoffre`. Pour refuser, `setCanceled(true)` seulement ; pour
  autoriser, rien.

## Un redémarrage est nécessaire

`ForgeEvents.onEvent` n'inscrit son écouteur qu'au premier chargement des scripts de
démarrage (`ForgeEventWrapper.onEvent` teste `ScriptManager.firstLoad`). Un
`/reload` ne suffit pas pour l'installer. Après le redémarrage, un `/reload` met à
jour la règle (`bmc4_garde.js`) sans redémarrer : `global` est le même objet pour
les deux types de scripts.

## Avant tout

1. `create_snapshot`, nom `avant-bmc107`. Attendre qu'il soit terminé.
2. `read_file` `/kubejs/server_scripts/bmc4_garde.js` : 39 982 octets (voir plus haut).

## Mise en place

3. Arrêter le serveur (`power_action stop`).
4. Créer le dossier `/bmc4-depot/bmc107-<date>/ancien/`.
5. `move_files` : `/kubejs/server_scripts/bmc4_garde.js` vers `/bmc4-depot/bmc107-<date>/ancien/`.
6. `move_files` : `/bmc4-depot/bmc107-<date>/kubejs/server_scripts/bmc4_garde.js` vers `/kubejs/server_scripts/`.
7. `move_files` : `/bmc4-depot/bmc107-<date>/kubejs/startup_scripts/bmc4_coffres_recharge.js` vers `/kubejs/startup_scripts/`.
8. Démarrer le serveur (`power_action start`).

## Vérifications dans les journaux

9. `/logs/kubejs/startup.log` : `Loaded script startup_scripts:bmc4_coffres_recharge.js`,
   puis `Loaded 4/4 KubeJS startup scripts … with 0 errors and 0 warnings`.
10. `/logs/kubejs/server.log` : `Loaded script server_scripts:bmc4_garde.js`, sans erreur.
11. `latest.log` et `/logs/kubejs/*.log` : aucune ligne `bmc4_coffres_recharge :` ni
    `bmc4_garde : coffres`. Chacune n'est écrite qu'une fois par sorte d'erreur :
    - `bmc4_coffres_recharge : garde absente` : les scripts serveur ne sont pas
      chargés ; tous les blocs à inventaire sont refusés à tout le monde. Corriger
      `bmc4_garde.js`, puis `/reload` ;
    - `bmc4_coffres_recharge : côté client ou serveur` : `isClientSide()` ne se lit
      pas ; l'écouteur fait comme côté serveur, rien n'est cassé, mais le signaler ;
    - `bmc4_coffres_recharge : écouteur` ou `décision`, `bmc4_garde : coffres` ou
      `coffres (recharge)` : un nom Java ne marche pas ; les clics sont refusés
      avec « la garde ne répond pas ». Retour arrière.

## Essais en jeu, à deux joueurs de factions différentes

A est de la faction F1, B de F2. B se place dans le claim de F1, devant un coffre de
F1. « En recharge » : lancer une perle de l'Ender, garder la pile de perles dans la
main principale et cliquer le coffre aussitôt (la recharge dure une seconde ; un
bouclier frappé par une hache donne cinq secondes).

| # | Essai | Attendu |
|---|---|---|
| 1 | B, perle en recharge en main, clic droit sur le coffre de F1 | refusé, **un seul** message « Ouvrir ce bloc refusé : il est dans le claim de F1. » |
| 2 | A, perle en recharge en main, son propre coffre | s'ouvre |
| 3 | Raid en cours entre F1 et F2 (`bmc4_raid_actif` rempli comme le fait le bot), B, perle en recharge | s'ouvre |
| 4 | B, sans recharge (main vide, puis une épée), coffre de F1 | refusé, un seul message |
| 5 | B, cinq clics rapides en recharge | refusé à chaque fois, un message par seconde au plus |
| 6 | B, perle en recharge, porte, levier, établi de F1 | marchent |
| 7 | A, four de son claim (BMC-108, Cinematic) | la scène reste ouverte |

Reporter le résultat dans BMC-107. Si l'essai 1 ouvre le coffre : retour arrière,
et lire `latest.log`.

## Retour arrière

Les deux fichiers partent ensemble. `bmc4_coffres_recharge.js` seul, sans la
nouvelle garde, refuse tous les blocs à inventaire à tout le monde.

1. Arrêter le serveur.
2. `move_files` : `/kubejs/startup_scripts/bmc4_coffres_recharge.js` vers `/bmc4-depot/bmc107-<date>/kubejs/startup_scripts/`.
3. `move_files` : `/kubejs/server_scripts/bmc4_garde.js` vers `/bmc4-depot/bmc107-<date>/kubejs/server_scripts/`.
4. `move_files` : `/bmc4-depot/bmc107-<date>/ancien/bmc4_garde.js` vers `/kubejs/server_scripts/`.
5. Démarrer le serveur. Le trou de la recharge revient (et le message de refus ne part plus).

## Ce qui n'est pas vérifiable hors jeu

- Les noms Java au runtime : `event.getLevel().isClientSide()` (méthode et champ du
  même nom sur `Level`), `getBlockEntity(pos)`, `joueur.getLevel().getBlock(pos)` côté
  serveur. Aucun nom SRG brut (règle 8 du contrôle : 0 défaut sur les deux scripts).
- L'appel d'une fonction des scripts serveur depuis un écouteur de démarrage :
  même forme que `global.bmc4GardeTeleport` (en service depuis le 7 octobre), mais
  pas observé pour celle-ci.
- L'ordre réel des écouteurs : KubeJS (HIGH, Architectury) avant celui-ci (NORMAL),
  et l'événement annulé non transmis. Lu dans le bytecode ; les tests le simulent.
- Le message de la garde en service : jamais observé qu'il manque, seulement lu.
