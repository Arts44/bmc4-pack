# /feed autorisé : encore faut-il avoir faim, sinon on ne le consomme pas.
execute store result score #faim bmc4_calc run data get entity @s foodLevel
execute if score #faim bmc4_calc matches 20.. run tellraw @s ["",{"text":"/feed refusé : ","color":"red"},{"text":"ta faim est déjà pleine. ","color":"red"},{"text":"Rien n'a été utilisé : il reste disponible.","color":"gray"}]
execute if score #faim bmc4_calc matches ..19 run function bmc4:rangs/manger_donner
