# Mémo modération

Publié dans `#staff-général`. Destiné aux modérateurs, pour qu'ils
agissent sans dépendre de l'administrateur.

## Modérer depuis `#console`

Le bot exécute la commande sur le serveur et renvoie la réponse. Pas
besoin d'être en jeu, pas besoin du panel.

```
list                       qui est connecté
kick <pseudo> <raison>     expulser, il peut revenir
ban <pseudo> <raison>      bannir
pardon <pseudo>            lever un bannissement
banlist                    voir les bannis
say <message>              parler au serveur
tell <pseudo> <message>    message privé en jeu
tp <pseudo1> <pseudo2>     téléporter
gamemode spectator <x>     observer discrètement
```

⚠️ `stop`, `ban-ip` et `pardon-ip` sont bloquées depuis Discord,
volontairement : trop faciles à taper par erreur.

## Où passe la frontière

**Le vol au gant est autorisé**, hors claim, sans accord de la
victime. Ne pas sanctionner quelqu'un qui vole proprement.

**Le déguisement aussi** — sauf dans une conversation, ou contre sa
propre faction, ce qui relève de la taupe.

**Interdit** : toucher à quoi que ce soit dans un territoire claim,
jouer la taupe dans une faction, tricher.

**En cas de doute, le critère est le claim.** Dedans, rien n'est
permis. Dehors, tout ce que le règlement autorise l'est.

## Administrer la machine

```
!admin etat              état, joueurs, ressources
!admin online            qui joue
!admin semaine           incidents, rejets, fréquentation
!admin logs              dernières lignes de console
!admin sauvegardes       lister les sauvegardes horaires
!admin restaurer <id>    restaurer, confirmation exigée
!admin snapshot <nom>    créer une snapshot
!admin start / restart / stop / kill
```

⚠️ **Une restauration efface le travail de tout le monde**, pas
seulement le dégât à réparer. Préférer toujours réparer à la main.

⚠️ **« starting » avec un processeur à 0 % signifie que le processus
est mort** — bug de chargement aléatoire de Quark. Dans ce cas
`!admin kill` puis `!admin start` : un simple `restart` ne suffit pas.

## Vérifier les rôles

```
!niveaux              temps de jeu, niveau attendu, niveau porté
!niveaux appliquer    corriger sans attendre le cycle de 15 min
!factions             effectifs et chunks, lus des fichiers du jeu
!faction sync         forcer la synchronisation des rôles
```

`!niveaux` signale d'un ⚠️ les écarts entre le niveau attendu et le
rôle réellement porté, et **liste ceux qui n'ont pas lié leur compte
Minecraft** : ceux-là ne recevront jamais de rôle, et rien d'autre ne
le montre.

`!factions` lit les fichiers du serveur, pas le registre Discord.
C'est ce qui permet de repérer un écart entre les deux.

## Avant de sanctionner

Une capture d'écran d'abord : sans preuve, une sanction se conteste.

En cas de doute, demander dans `#staff-général`. Une sanction retardée
d'une heure ne coûte rien ; une sanction injuste coûte un joueur.

## Les registres

Ils vivent dans des messages de `#logs`, un par système : factions,
chantiers, lieux, réserve des mods, instantanés du classement.

⚠️ **Ne pas les supprimer.** Et attribuer un rôle de faction à la main
ne sert à rien : la synchronisation l'annule dans les cinq minutes. Le
registre fait foi.
