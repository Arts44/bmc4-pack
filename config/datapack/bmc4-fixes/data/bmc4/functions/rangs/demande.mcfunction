# /trigger bmc4_rang : 1 achète le rang suivant, 2 affiche où on en est.
execute if score @s bmc4_rang matches 1 run function bmc4:rangs/acheter
execute if score @s bmc4_rang matches 2 run function bmc4:rangs/etat
execute unless score @s bmc4_rang matches 1..2 run tellraw @s ["",{"text":"/trigger bmc4_rang refusé : ","color":"red"},{"text":"cette valeur n'existe pas. ","color":"red"},{"text":"/trigger bmc4_rang achète le rang suivant, /trigger bmc4_rang set 2 montre où tu en es.","color":"gray"}]
scoreboard players set @s bmc4_rang 0
