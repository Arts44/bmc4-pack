# Pose l'ancre d'un joueur mort en raid, là où il vient de réapparaître.
# Exécutée « as » le joueur « at » sa position, au premier tick où il est
# vivant et en décompte (raid_tick passe par @e[type=player], qui ignore
# les joueurs encore sur l'écran de mort).
#
# Pourquoi (6 octobre) : sans ancre, le spectateur volait où il voulait
# pendant cinq minutes, traversait les murs, puis redevenait survie sur
# place, par exemple au milieu de la base adverse. Il reste maintenant à
# son point de réapparition ; il peut tourner la tête, pas se déplacer.

execute unless score @s bmc4_id matches 1.. run function bmc4:id_attribuer
summon minecraft:marker ~ ~ ~ {Tags:["bmc4_ancre","bmc4_ancre_neuve"]}
scoreboard players operation @e[type=minecraft:marker,tag=bmc4_ancre_neuve,limit=1] bmc4_id = @s bmc4_id
tag @e[type=minecraft:marker,tag=bmc4_ancre_neuve] remove bmc4_ancre_neuve
tag @s add bmc4_ancre
