# Le rang visé existe, #cout bmc4_calc est son prix.
execute store result score @s bmc4_niveaux run experience query @s levels
scoreboard players operation @s bmc4_calc = #cout bmc4_calc
scoreboard players operation @s bmc4_calc -= @s bmc4_niveaux

# Il en manque : le même message que pour un achat refusé, sans bouton.
execute if score @s bmc4_calc matches 1.. run function bmc4:rangs/g_manque
execute if score @s bmc4_calc matches ..0 run function bmc4:rangs/devis_noter
