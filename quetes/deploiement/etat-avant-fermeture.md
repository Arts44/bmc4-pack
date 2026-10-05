# État du serveur avant fermeture — relevé le 5 octobre 2026

Lu sur le serveur MineStrator 486488, en lecture seule. **À relire le jour
même de la fermeture** : si une valeur a changé, c'est la nouvelle qu'il
faudra rendre à la réouverture.

## Liste blanche

| Élément | Valeur |
|---|---|
| `server.properties` → `white-list` | `false` |
| `server.properties` → `enforce-whitelist` | `false` |
| `whitelist.json` | `[]` (vide) |

À la réouverture, l'état à rendre est donc : liste blanche **désactivée** et
**vide**.

## Opérateurs (`ops.json`)

| Joueur | UUID | Niveau | `bypassesPlayerLimit` |
|---|---|---|---|
| HelXo1 | b377bec2-1900-47c6-8a42-5893a66f1da2 | 4 | false |
| Arts_Vio | 3eed1732-4db7-4f0a-980a-f5f16dfcdac6 | 4 | false |

`op-permission-level=4` dans `server.properties` : la commande `op` redonne
le niveau 4, donc l'état d'avant à l'identique.

⚠️ Dans Minecraft, un opérateur peut entrer même s'il n'est pas sur la
liste blanche. HelXo1 pourrait donc se connecter pendant la fermeture
(décision d'Arthur : il garde son op, rien n'est fait).

## Livre de quêtes en place

`/config/ftbquests/quests/` : le livre de Better Minecraft (titre « Better
Minecraft [FORGE] 1.20.1 »), 14 chapitres, 3 tables de récompense,
2 groupes, 471 identifiants. Copie exacte dans
`sauvegarde-ancien-livre-2026-10-05/` : tailles comparées fichier par
fichier ; le chapitre Twilight Forest du serveur avait une quête de plus
(le Château final) que la copie `ancien-livre-bmc-1.19.2/` du dépôt, elle
a été reprise telle qu'elle est sur le serveur (6 622 octets, identique).

## Progression des joueurs

`/world/ftbquests/` : 10 fichiers d'équipe (un par équipe FTB). Ils ne
contiennent que des identifiants de quêtes et de tâches. Aucun des 471
identifiants de l'ancien livre ne se retrouve parmi les 10 531 du livre
complet ni les 3 479 du livre léger : rien de l'ancienne progression ne
se reportera sur le nouveau livre.
