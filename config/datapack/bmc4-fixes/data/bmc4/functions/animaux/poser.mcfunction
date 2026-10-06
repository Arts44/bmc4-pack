# Repeuplement — la naissance.
#
# Une espèce au hasard, une chance sur quatre chacune. Par paire,
# comme les troupeaux de la génération du monde : un animal seul
# ne sert à rien, deux permettent un élevage.
#
# Le tirage se fait en cascade — 1/4, puis 1/3 du reste, puis la
# moitié, puis ce qui reste —, ce qui donne quatre parts égales.

scoreboard players set #choix bmc4_anim 0
execute if predicate bmc4:chance_25 run scoreboard players set #choix bmc4_anim 1
execute if score #choix bmc4_anim matches 0 if predicate bmc4:chance_33 run scoreboard players set #choix bmc4_anim 2
execute if score #choix bmc4_anim matches 0 if predicate bmc4:chance_50 run scoreboard players set #choix bmc4_anim 3
execute if score #choix bmc4_anim matches 0 run scoreboard players set #choix bmc4_anim 4

execute if score #choix bmc4_anim matches 1 run summon minecraft:sheep ~ ~ ~
execute if score #choix bmc4_anim matches 1 run summon minecraft:sheep ~1 ~ ~
execute if score #choix bmc4_anim matches 2 run summon minecraft:cow ~ ~ ~
execute if score #choix bmc4_anim matches 2 run summon minecraft:cow ~1 ~ ~
execute if score #choix bmc4_anim matches 3 run summon minecraft:pig ~ ~ ~
execute if score #choix bmc4_anim matches 3 run summon minecraft:pig ~1 ~ ~
execute if score #choix bmc4_anim matches 4 run summon minecraft:chicken ~ ~ ~
execute if score #choix bmc4_anim matches 4 run summon minecraft:chicken ~1 ~ ~
