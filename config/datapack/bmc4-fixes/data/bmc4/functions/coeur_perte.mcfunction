# Une mort en raid : un cœur de vie maximale en moins, plancher trois cœurs.
# Appelée par raid_tick et raid_fin, uniquement sur l'équipe bmc4_raid_actif.
#
# Le compte est tenu dans le score bmc4_pvmax (PV, 20 = dix cœurs), qui
# survit à la mort ; coeur_tick le réapplique à la réapparition (6 octobre).
execute unless score @s bmc4_pvmax matches 1.. store result score @s bmc4_pvmax run attribute @s minecraft:generic.max_health base get
scoreboard players operation @s bmc4_hp = @s bmc4_pvmax
execute if score @s bmc4_hp matches 7.. run scoreboard players remove @s bmc4_pvmax 2
execute if score @s bmc4_pvmax matches ..5 run scoreboard players set @s bmc4_pvmax 6
function bmc4:coeur_fixer
execute if score @s bmc4_hp matches 7.. run tellraw @s {"text":"Tu as perdu un coeur de vie maximale. Un repas de Farmer's Delight ou une Pierre de Soin le rend.","color":"gold"}
execute if score @s bmc4_hp matches ..6 run tellraw @s {"text":"Trois coeurs : le plancher. Tu ne descendras pas plus bas.","color":"gold"}
