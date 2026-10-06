# /feed trop tôt : le temps qui reste, en minutes et secondes.
# @s bmc4_calc = ticks écoulés depuis le dernier /feed.
scoreboard players set #duree bmc4_calc 36000
scoreboard players operation #duree bmc4_calc -= @s bmc4_calc
scoreboard players set #1200 bmc4_calc 1200
scoreboard players set #20 bmc4_calc 20
scoreboard players operation #min bmc4_calc = #duree bmc4_calc
scoreboard players operation #min bmc4_calc /= #1200 bmc4_calc
scoreboard players operation #sec bmc4_calc = #duree bmc4_calc
scoreboard players operation #sec bmc4_calc %= #1200 bmc4_calc
scoreboard players operation #sec bmc4_calc /= #20 bmc4_calc
tellraw @s ["",{"text":"/feed refusé : ","color":"red"},{"text":"une fois toutes les 30 minutes. ","color":"red"},{"text":"Disponible dans ","color":"gray"},{"score":{"name":"#min","objective":"bmc4_calc"},"color":"white"},{"text":" min ","color":"gray"},{"score":{"name":"#sec","objective":"bmc4_calc"},"color":"white"},{"text":" s.","color":"gray"}]
