# Un repas ou une Pierre de Soin consommé : un cœur de vie maximale rendu,
# jusqu'à dix. Marche à tout moment, créneau ou pas.
# Le compte est tenu dans le score bmc4_pvmax (voir coeur_fixer).
execute unless score @s bmc4_pvmax matches 1.. store result score @s bmc4_pvmax run attribute @s minecraft:generic.max_health base get
scoreboard players operation @s bmc4_hp = @s bmc4_pvmax
execute if score @s bmc4_hp matches ..19 run scoreboard players add @s bmc4_pvmax 2
execute if score @s bmc4_pvmax matches 21.. run scoreboard players set @s bmc4_pvmax 20
function bmc4:coeur_fixer
execute if score @s bmc4_hp matches ..19 run tellraw @s {"text":"Un coeur de vie maximale retrouve.","color":"green"}
