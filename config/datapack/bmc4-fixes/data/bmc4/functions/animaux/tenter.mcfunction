# Repeuplement — une tentative.
#
# Un marqueur invisible est lancé entre 24 et 48 blocs du joueur,
# à la surface. Comme en vanilla : jamais sous le nez du joueur,
# jamais trop loin pour qu'il les croise.
#
# On ne pose rien si le marqueur ne tombe pas sur de l'herbe —
# ni sur un toit, ni dans l'eau, ni dans une base en pierre.

summon minecraft:marker ~ ~ ~ {Tags:["bmc4_point"]}
spreadplayers ~ ~ 24 48 false @e[type=minecraft:marker,tag=bmc4_point,limit=1,sort=nearest]

execute as @e[type=minecraft:marker,tag=bmc4_point,limit=1,sort=nearest] at @s if block ~ ~-1 ~ minecraft:grass_block run function bmc4:animaux/poser

kill @e[type=minecraft:marker,tag=bmc4_point]
