# Reprend les cœurs perdus sous l'ancien mod Mediumcore et les reporte sur
# la valeur de base, puis retire ses deux modificateurs (UUID calculés depuis
# les graines du code du mod : 2929292911123 et 111222333441249).
# Le modificateur « MediumcoreHealthMod » vaut le delta cumulé (−2 par mort).
scoreboard players set @s bmc4_hp 0
execute store result score @s bmc4_hp run attribute @s minecraft:generic.max_health modifier value get 588b03a7-325f-478d-a75a-26cd97f2a846
scoreboard players add @s bmc4_hp 20
attribute @s minecraft:generic.max_health modifier remove 588b03a7-325f-478d-a75a-26cd97f2a846
attribute @s minecraft:generic.max_health modifier remove da72a85f-a4a3-4260-bafe-fdbd34aa7e16
execute if score @s bmc4_hp matches 18 run attribute @s minecraft:generic.max_health base set 18
execute if score @s bmc4_hp matches 16 run attribute @s minecraft:generic.max_health base set 16
execute if score @s bmc4_hp matches 14 run attribute @s minecraft:generic.max_health base set 14
execute if score @s bmc4_hp matches 12 run attribute @s minecraft:generic.max_health base set 12
execute if score @s bmc4_hp matches 10 run attribute @s minecraft:generic.max_health base set 10
execute if score @s bmc4_hp matches 8 run attribute @s minecraft:generic.max_health base set 8
execute if score @s bmc4_hp matches 6 run attribute @s minecraft:generic.max_health base set 6
execute if score @s bmc4_hp matches ..5 run attribute @s minecraft:generic.max_health base set 6
tag @s add bmc4_hp_migre
