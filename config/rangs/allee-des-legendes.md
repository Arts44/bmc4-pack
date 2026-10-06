# L'Allée des Légendes, au Marché Flottant (BMC-91)

Plan pour le staff, qui construit. **Rien n'est posé.** La tête et la plaque
d'un joueur Suprême (rang 11), puis la statue d'un Absolu (rang 15), sont
ajoutées à la main, à chaque nouvel ayant droit (le bot l'annonce dans
`#faits-d-armes` à partir du rang 12 ; le rang 11 se voit dans le rôle Discord
« ✦ Suprême »).

## Où

Lu sur le serveur le 6 octobre 2026 :

- le claim du Marché appartient à l'**équipe serveur** FTB
  (`/world/ftbteams/server/93fc8ae1-….snbt`), chunks x et z de −3 à 3,
  donc les **blocs −48 à 63** sur les deux axes, dans l'Overworld ;
- le Marché est centré sur (0, 63, 0) ; l'esplanade va de −24 à 24, le ponton
  **est** va jusqu'à x = 30, de z = −2 à 2, en béton gris clair à y = 63
  (`marche/extension.mcfunction`), avec une lanterne de mer en (30, 64, 0).

L'Allée prolonge le ponton est, **de x = 31 à x = 58, de z = −3 à 3**, à
y = 63 : elle reste dans le claim (x ≤ 63), donc protégée, sans PvP (le
panneau du Marché le dit : « Ni PvP ni vol »), et `/home` y reste permis.
**À vérifier sur place avant de construire** : ce qu'il y a aujourd'hui entre
x = 31 et 63 (océan attendu, comme autour du Marché ; non lu).

```
  z=-3  P   P   P   P   P   P   P        Suprême, côté nord (7 places)
  z=-2..2  ════ allée ════════════════  [ statues Absolu, x = 59 à 62 ]
  z= 3  P   P   P   P   P   P   P        Suprême, côté sud (7 places)
      x=33  37  41  45  49  53  57
```

Quatorze places Suprême (x = 33, 37, …, 57, de chaque côté), dans l'ordre
d'arrivée, en alternant nord et sud. Les statues Absolu au bout, sur une
terrasse de x = 59 à 62.

## Le pont de l'Allée

```
fill 31 63 -3 58 63 3 minecraft:light_gray_concrete replace minecraft:water
fill 31 63 -3 58 63 -3 minecraft:polished_deepslate replace minecraft:light_gray_concrete
fill 31 63 3 58 63 3 minecraft:polished_deepslate replace minecraft:light_gray_concrete
fill 59 63 -6 62 63 6 minecraft:polished_deepslate replace minecraft:water
```

## Une place Suprême (exemple : x = 33, côté nord)

Socle, tête tournée vers l'allée, plaque sur la face sud du socle :

```
setblock 33 64 -3 minecraft:polished_deepslate
setblock 33 65 -3 minecraft:player_head[rotation=0]{SkullOwner:"<Pseudo>"}
setblock 33 64 -2 minecraft:dark_oak_wall_sign[facing=south]{front_text:{messages:['{"text":"✦ Suprême","color":"#E02424","bold":true}','{"text":"<Pseudo>"}','{"text":"<date d\'achat>"}','{"text":""}']}}
```

Côté sud (z = 3) : `rotation=8` pour la tête, plaque en `z = 2` avec
`facing=north`.

## Une statue Absolu (exemple : x = 60, z = −3)

La version minimale, sans bloc à sculpter : un porte-armure figé, à la tête du
joueur, dont rien ne peut être retiré (`DisabledSlots:4144959`).

```
summon minecraft:armor_stand 60 64 -3 {NoGravity:1b,Invulnerable:1b,ShowArms:1b,NoBasePlate:1b,DisabledSlots:4144959,Rotation:[90f,0f],CustomNameVisible:1b,CustomName:'{"text":"♛ Absolu <Pseudo>","color":"#9B111E","bold":true}',ArmorItems:[{id:"minecraft:netherite_boots",Count:1b},{id:"minecraft:netherite_leggings",Count:1b},{id:"minecraft:netherite_chestplate",Count:1b},{id:"minecraft:player_head",Count:1b,tag:{SkullOwner:"<Pseudo>"}}]}
```

Une statue sculptée en blocs, à l'échelle, reste au choix du staff ; la plaque
se pose comme pour une place Suprême.
