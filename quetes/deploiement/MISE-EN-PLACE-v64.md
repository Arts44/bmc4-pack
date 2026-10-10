# v64 — Mise en place côté serveur

Lot : `/bmc4-depot/v64-<date>/`, déposé par
`sh quetes/deploiement/deposer.sh --lot v64-<date>`, sur le feu vert d'Arthur
seulement. Le dépôt ne met rien en place : les déplacements se font avec les
outils MineStrator. `SHA1SUMS` donne l'empreinte de chaque fichier.

⚠️ **Serveur et pack changent ensemble.** Just Outdoor Stuffs, Connectible
Chains, Placebo (et les mods de #mods s'ils sont validés) enregistrent du
contenu ou un canal réseau : un client v62 sera refusé par un serveur v64, et
un client v64 par un serveur v62. Mettre en place le serveur et publier la
release dans la même maintenance.

## Avant tout

1. **Snapshot** du serveur (`create_snapshot`), noté dans le journal.
2. Arrêter le serveur.

## Mise en place

| Fichier du lot | Destination |
|---|---|
| `mods/JustOutdoorStuffs-1.20.1-forge-v1.0.2.jar` | `/mods/` |
| `mods/FastFurnace-1.20.1-8.0.2.jar` | `/mods/` |
| `mods/Placebo-1.20.1-8.6.3.jar` | `/mods/` (dépendance de FastFurnace) |
| `mods/Connectible-Chains-forge-1.20.1-1.1.1.jar` | `/mods/` |
| `mods-si-b-valides/*.jar` | `/mods/` — **seulement** si la revue de #mods les valide (Kaleidoscope Tavern, Kaleidoscope Cookery, Kaleidoscope Immersive Eating, Create: Steam 'n' Rails), et seulement avec la release « avec B » |

Aucun jar existant n'est remplacé : il n'y a rien à sauvegarder dans `/mods`.
Puis le rangement de `A-RETIRER.txt` (XaeroPlus, inactif sur le serveur) :
déplacer, ne pas supprimer, vers `/bmc4-depot/sauvegarde-v64/`.

Les mods client seul de la v64 (Do a Barrel Roll, Leawind's Third Person) ne
vont **pas** sur le serveur. Do a Barrel Roll accepte un serveur sans lui
(prédicats de canal réseau toujours vrais, lus dans le jar) ; sans lui,
l'accélération en élytre reste refusée aux clients.

## Après le démarrage

1. `latest.log` : les modIds `justoutdoorstuffs`, `fastfurnace`, `placebo`,
   `connectiblechains` dans la liste des mods, aucune erreur de mixin.
2. KubeJS : `bmc4_triche.js` toujours chargé (aucun de ces modIds n'est dans
   `BMC4_MODS_REFUSES` ni `BMC4_MODS_ALERTE`).
3. Un client v64 se connecte ; un client v62 est refusé avec la liste des mods.

## Retour arrière

Retirer les jars ajoutés de `/mods`, remettre le snapshot si besoin, et
republier la v62 comme dernière release.
