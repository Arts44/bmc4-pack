# Mémo modération

Publié dans `#staff-général`. Destiné aux modérateurs, pour qu'ils agissent
sans dépendre de l'administrateur.

## Tout passe par `#console`

Le bot exécute la commande sur le serveur et renvoie la réponse. Pas besoin
d'être en jeu, pas besoin du panel.

```
kick <pseudo> <raison>     expulser, il peut revenir
ban <pseudo> <raison>      bannir définitivement
pardon <pseudo>            lever un bannissement
banlist                    voir qui est banni
list                       qui est connecté
say <message>              parler au serveur
tell <pseudo> <message>    message privé en jeu
tp <pseudo1> <pseudo2>     téléporter
gamemode spectator <x>     observer discrètement
```

`stop` est bloquée depuis Discord, volontairement.

## Où passe la frontière

**Le vol au gant est autorisé**, hors base claim, sans accord de la
victime. Ne pas sanctionner quelqu'un qui vole proprement.

**Interdit** : toucher à quoi que ce soit dans un territoire claim, jouer
la taupe dans une faction, tricher.

**En cas de doute, le critère est le claim.** Dedans, rien n'est permis.
Dehors, le gant l'est.

## Avant de sanctionner

Une capture d'écran d'abord : sans preuve, une sanction se conteste.

En cas de doute, demander dans `#staff-général`. Une sanction retardée
d'une heure ne coûte rien ; une sanction injuste coûte un joueur.

## Administration du serveur

Le bot `admin` donne accès à l'API de l'hébergeur depuis `#console` :

```
!admin etat              état, joueurs, ressources
!admin logs              dernières lignes de console
!admin sauvegardes       lister les sauvegardes horaires
!admin restaurer <id>    restaurer, confirmation exigée
!admin snapshot <nom>    créer une snapshot
!admin start / restart / stop / kill
```

⚠️ **Une restauration efface le travail de tout le monde**, pas seulement
le dégât à réparer. Préférer toujours réparer à la main.

⚠️ **« starting » avec un processeur à 0 % signifie que le processus est
mort** — bug de chargement aléatoire de Quark. Dans ce cas `!admin kill`
puis `!admin start` : un simple `restart` ne suffit pas.

## Le registre des factions

Il vit dans un message du bot, dans `#logs`. Il contient tout : factions,
membres, rangs, alliances, chunks, trophées.

⚠️ **Ne pas le supprimer.** Et attribuer un rôle de faction à la main ne
sert à rien : la synchronisation l'annule dans les cinq minutes. Le
registre fait foi.
