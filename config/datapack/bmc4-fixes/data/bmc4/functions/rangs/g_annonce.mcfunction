# Généré par config/rangs/generer.py depuis config/rangs/rangs.toml : ne pas
# modifier à la main.
# À l'achat d'un rang 12 ou plus, une ligne pour le bot (#faits-d-armes) :
# il lit storage bmc4:rangs annonces par RCON, puis retire ce qu'il a lu.

execute if score @s bmc4_rangs matches 12.. run data modify storage bmc4:rangs annonces append value {Rang:0}
execute if score @s bmc4_rangs matches 12.. run data modify storage bmc4:rangs annonces[-1].UUID set from entity @s UUID
execute if score @s bmc4_rangs matches 12.. store result storage bmc4:rangs annonces[-1].Rang int 1 run scoreboard players get @s bmc4_rangs
