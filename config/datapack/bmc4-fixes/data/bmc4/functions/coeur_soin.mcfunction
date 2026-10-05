# Un repas ou une Pierre de Soin consommé : un cœur de vie maximale rendu,
# jusqu'à dix. Marche à tout moment, créneau ou pas.
execute store result score @s bmc4_hp run attribute @s minecraft:generic.max_health base get
execute if score @s bmc4_hp matches 18..19 run attribute @s minecraft:generic.max_health base set 20
execute if score @s bmc4_hp matches 16..17 run attribute @s minecraft:generic.max_health base set 18
execute if score @s bmc4_hp matches 14..15 run attribute @s minecraft:generic.max_health base set 16
execute if score @s bmc4_hp matches 12..13 run attribute @s minecraft:generic.max_health base set 14
execute if score @s bmc4_hp matches 10..11 run attribute @s minecraft:generic.max_health base set 12
execute if score @s bmc4_hp matches 8..9 run attribute @s minecraft:generic.max_health base set 10
execute if score @s bmc4_hp matches 6..7 run attribute @s minecraft:generic.max_health base set 8
execute if score @s bmc4_hp matches ..19 run tellraw @s {"text":"Un coeur de vie maximale retrouve.","color":"green"}
