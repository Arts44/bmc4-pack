# Une mort en raid : un cœur de vie maximale en moins, plancher trois cœurs.
# Appelée par raid_tick et raid_fin, uniquement sur l'équipe bmc4_raid_actif.
execute store result score @s bmc4_hp run attribute @s minecraft:generic.max_health base get
execute if score @s bmc4_hp matches 19.. run attribute @s minecraft:generic.max_health base set 18
execute if score @s bmc4_hp matches 17..18 run attribute @s minecraft:generic.max_health base set 16
execute if score @s bmc4_hp matches 15..16 run attribute @s minecraft:generic.max_health base set 14
execute if score @s bmc4_hp matches 13..14 run attribute @s minecraft:generic.max_health base set 12
execute if score @s bmc4_hp matches 11..12 run attribute @s minecraft:generic.max_health base set 10
execute if score @s bmc4_hp matches 9..10 run attribute @s minecraft:generic.max_health base set 8
execute if score @s bmc4_hp matches 7..8 run attribute @s minecraft:generic.max_health base set 6
execute if score @s bmc4_hp matches 7.. run tellraw @s {"text":"Tu as perdu un coeur de vie maximale. Un repas de Farmer's Delight ou une Pierre de Soin le rend.","color":"gold"}
execute if score @s bmc4_hp matches ..6 run tellraw @s {"text":"Trois coeurs : le plancher. Tu ne descendras pas plus bas.","color":"gold"}
