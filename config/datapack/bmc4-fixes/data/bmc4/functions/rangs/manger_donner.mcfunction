# Rassasie (l'effet Saturation remplit la faim en une seconde) et note l'heure.
effect give @s minecraft:saturation 1 9 true
execute store result score @s bmc4_manger_t run time query gametime
tellraw @s ["",{"text":"Rassasié. ","color":"green"},{"text":"Prochain /feed dans 30 minutes.","color":"gray"}]
