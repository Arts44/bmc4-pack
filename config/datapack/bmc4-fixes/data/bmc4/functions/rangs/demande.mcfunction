# /trigger bmc4_rang : 1 achète le rang suivant, 2 affiche où on en est. Gardé
# pour qui le connaît ; les messages citent désormais /prestige.
execute if score @s bmc4_rang matches 1 run function bmc4:rangs/acheter
execute if score @s bmc4_rang matches 2 run function bmc4:rangs/etat
execute unless score @s bmc4_rang matches 1..2 run tellraw @s ["",{"text":"/trigger bmc4_rang refusé : ","color":"red"},{"text":"cette valeur n'existe pas. ","color":"red"},{"text":"Utilise plutôt /prestige. ","color":"gray"},{"text":"[Où j'en suis]","color":"aqua","bold":true,"clickEvent":{"action":"run_command","value":"/prestige"},"hoverEvent":{"action":"show_text","contents":"Ton rang, le suivant, ce qu'il te manque"}}]
scoreboard players set @s bmc4_rang 0
