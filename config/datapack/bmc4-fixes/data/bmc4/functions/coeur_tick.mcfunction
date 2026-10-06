# Chaque tick : les soins, et la migration des joueurs marqués par l'ancien mod.

# --- Migration (une fois par joueur) ---
execute as @a[tag=!bmc4_hp_migre] run function bmc4:coeur_migration

# --- La vie maximale : le score bmc4_pvmax fait foi (6 octobre) ---
# La valeur de base retombe à 20 à chaque réapparition. On la repose
# d'après le score dès que le joueur est vivant (@e[type=player] ignore
# l'écran de mort). Premier passage : le score prend la valeur actuelle.
execute as @e[type=minecraft:player] unless score @s bmc4_pvmax matches 1.. store result score @s bmc4_pvmax run attribute @s minecraft:generic.max_health base get
execute as @e[type=minecraft:player] store result score @s bmc4_hp run attribute @s minecraft:generic.max_health base get
execute as @e[type=minecraft:player] unless score @s bmc4_hp = @s bmc4_pvmax run function bmc4:coeur_fixer

# --- Soins : un objet consommé = un cœur ---
execute as @a[scores={bmc4_repas1=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas1=1..}] bmc4_repas1
execute as @a[scores={bmc4_repas2=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas2=1..}] bmc4_repas2
execute as @a[scores={bmc4_repas3=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas3=1..}] bmc4_repas3
execute as @a[scores={bmc4_repas4=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas4=1..}] bmc4_repas4
execute as @a[scores={bmc4_repas5=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas5=1..}] bmc4_repas5
execute as @a[scores={bmc4_repas6=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas6=1..}] bmc4_repas6
execute as @a[scores={bmc4_repas7=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas7=1..}] bmc4_repas7
execute as @a[scores={bmc4_repas8=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas8=1..}] bmc4_repas8
execute as @a[scores={bmc4_repas9=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas9=1..}] bmc4_repas9
execute as @a[scores={bmc4_repas10=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas10=1..}] bmc4_repas10
execute as @a[scores={bmc4_repas11=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas11=1..}] bmc4_repas11
execute as @a[scores={bmc4_repas12=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas12=1..}] bmc4_repas12
execute as @a[scores={bmc4_repas13=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas13=1..}] bmc4_repas13
execute as @a[scores={bmc4_repas14=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas14=1..}] bmc4_repas14
execute as @a[scores={bmc4_repas15=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas15=1..}] bmc4_repas15
execute as @a[scores={bmc4_repas16=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas16=1..}] bmc4_repas16
execute as @a[scores={bmc4_repas17=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas17=1..}] bmc4_repas17
execute as @a[scores={bmc4_repas18=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas18=1..}] bmc4_repas18
execute as @a[scores={bmc4_repas19=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas19=1..}] bmc4_repas19
execute as @a[scores={bmc4_repas20=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas20=1..}] bmc4_repas20
execute as @a[scores={bmc4_repas21=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas21=1..}] bmc4_repas21
execute as @a[scores={bmc4_repas22=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas22=1..}] bmc4_repas22
execute as @a[scores={bmc4_repas23=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas23=1..}] bmc4_repas23
execute as @a[scores={bmc4_repas24=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas24=1..}] bmc4_repas24
execute as @a[scores={bmc4_repas25=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas25=1..}] bmc4_repas25
execute as @a[scores={bmc4_repas26=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas26=1..}] bmc4_repas26
execute as @a[scores={bmc4_repas27=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas27=1..}] bmc4_repas27
execute as @a[scores={bmc4_repas28=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas28=1..}] bmc4_repas28
execute as @a[scores={bmc4_repas29=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas29=1..}] bmc4_repas29
execute as @a[scores={bmc4_repas30=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas30=1..}] bmc4_repas30
execute as @a[scores={bmc4_repas31=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas31=1..}] bmc4_repas31
execute as @a[scores={bmc4_repas32=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas32=1..}] bmc4_repas32
execute as @a[scores={bmc4_repas33=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas33=1..}] bmc4_repas33
execute as @a[scores={bmc4_repas34=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas34=1..}] bmc4_repas34
execute as @a[scores={bmc4_repas35=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas35=1..}] bmc4_repas35
execute as @a[scores={bmc4_repas36=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas36=1..}] bmc4_repas36
execute as @a[scores={bmc4_repas37=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas37=1..}] bmc4_repas37
execute as @a[scores={bmc4_repas38=1..}] run function bmc4:coeur_soin
scoreboard players reset @a[scores={bmc4_repas38=1..}] bmc4_repas38
