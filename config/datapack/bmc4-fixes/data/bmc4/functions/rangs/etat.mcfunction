# /trigger bmc4_rang set 2 : le rang actuel, le suivant, son prix, ce qui manque.
execute unless score @s bmc4_rangs matches 0.. run scoreboard players set @s bmc4_rangs 0
scoreboard players operation @s bmc4_cible = @s bmc4_rangs
scoreboard players add @s bmc4_cible 1
function bmc4:rangs/g_cout
execute store result score @s bmc4_niveaux run experience query @s levels
scoreboard players operation @s bmc4_calc = #cout bmc4_calc
scoreboard players operation @s bmc4_calc -= @s bmc4_niveaux
execute if score @s bmc4_calc matches ..0 run scoreboard players set @s bmc4_calc 0
function bmc4:rangs/g_etat
execute if score #cout bmc4_calc matches ..-1 run tellraw @s ["",{"text":"Tu as atteint le dernier palier préparé. ","color":"gray"},{"text":"Préviens le staff pour les suivants.","color":"gray"}]
