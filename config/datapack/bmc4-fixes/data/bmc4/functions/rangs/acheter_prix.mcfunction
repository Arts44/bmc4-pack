# Le rang visé existe et #cout bmc4_calc est son prix : assez de niveaux ?
execute store result score @s bmc4_niveaux run experience query @s levels
scoreboard players operation @s bmc4_calc = #cout bmc4_calc
scoreboard players operation @s bmc4_calc -= @s bmc4_niveaux

# bmc4_calc = ce qui manque. Plus que zéro : refus, rien n'est retiré.
execute if score @s bmc4_calc matches 1.. run function bmc4:rangs/g_manque
execute if score @s bmc4_calc matches ..0 run function bmc4:rangs/payer
