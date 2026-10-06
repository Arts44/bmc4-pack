# Pose la vie maximale de base d'après le score bmc4_pvmax (exécutée « as » un
# joueur vivant dont la valeur de base ne correspond pas au score).
#
# Pourquoi un score (6 octobre) : la valeur de base de l'attribut ne survit
# PAS à la mort. À la réapparition, le jeu recrée le joueur avec 20 PV de
# base : le cœur perdu revenait tout seul. Le score, lui, survit à tout ;
# coeur_tick le réapplique dès que le joueur réapparaît.
execute if score @s bmc4_pvmax matches 20.. run attribute @s minecraft:generic.max_health base set 20
execute if score @s bmc4_pvmax matches 18..19 run attribute @s minecraft:generic.max_health base set 18
execute if score @s bmc4_pvmax matches 16..17 run attribute @s minecraft:generic.max_health base set 16
execute if score @s bmc4_pvmax matches 14..15 run attribute @s minecraft:generic.max_health base set 14
execute if score @s bmc4_pvmax matches 12..13 run attribute @s minecraft:generic.max_health base set 12
execute if score @s bmc4_pvmax matches 10..11 run attribute @s minecraft:generic.max_health base set 10
execute if score @s bmc4_pvmax matches 8..9 run attribute @s minecraft:generic.max_health base set 8
execute if score @s bmc4_pvmax matches ..7 run attribute @s minecraft:generic.max_health base set 6
