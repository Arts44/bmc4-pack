# /feed du rang Nétherite (g_manger a vérifié le rang) : une fois toutes les
# 30 minutes (36 000 ticks), comptées sur l'horloge du monde, donc aussi
# quand le joueur est déconnecté.
execute store result score #maintenant bmc4_calc run time query gametime
scoreboard players operation @s bmc4_calc = #maintenant bmc4_calc
scoreboard players operation @s bmc4_calc -= @s bmc4_manger_t
execute unless score @s bmc4_manger_t matches 1.. run scoreboard players set @s bmc4_calc 36000

execute if score @s bmc4_calc matches ..35999 run function bmc4:rangs/manger_attente
execute if score @s bmc4_calc matches 36000.. run function bmc4:rangs/manger_faim
