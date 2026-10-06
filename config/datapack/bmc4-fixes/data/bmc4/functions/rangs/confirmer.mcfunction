# /prestige confirmer : achète, si le devis de ce joueur a moins de 30 secondes
# et vise toujours le rang suivant. L'achat lui-même est celui de
# /trigger bmc4_rang (acheter), sans rien de plus.
execute unless score @s bmc4_rangs matches 0.. run scoreboard players set @s bmc4_rangs 0
scoreboard players operation #suivant bmc4_calc = @s bmc4_rangs
scoreboard players add #suivant bmc4_calc 1
execute store result score #maintenant bmc4_calc run time query gametime
scoreboard players operation #age bmc4_calc = #maintenant bmc4_calc
scoreboard players operation #age bmc4_calc -= @s bmc4_devis_t

# #etat_devis : 0 aucun devis, 1 rang changé depuis, 2 trop tard, 3 valable.
scoreboard players set #etat_devis bmc4_calc 0
execute if score @s bmc4_devis matches 1.. run scoreboard players set #etat_devis bmc4_calc 1
execute if score @s bmc4_devis matches 1.. if score @s bmc4_devis = #suivant bmc4_calc run scoreboard players set #etat_devis bmc4_calc 2
execute if score #etat_devis bmc4_calc matches 2 if score #age bmc4_calc matches 0..600 run scoreboard players set #etat_devis bmc4_calc 3

execute if score #etat_devis bmc4_calc matches 0 run tellraw @s ["",{"text":"Aucun achat à confirmer : ","color":"red"},{"text":"tape d'abord /prestige acheter. ","color":"gray"},{"text":"[Acheter]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/prestige acheter"},"hoverEvent":{"action":"show_text","contents":"Voir le prix et ce qu'apporte le rang suivant, puis confirmer"}}]
execute if score #etat_devis bmc4_calc matches 1 run tellraw @s ["",{"text":"Confirmation expirée : ","color":"red"},{"text":"ton rang a changé depuis /prestige acheter. Retape /prestige acheter. ","color":"gray"},{"text":"[Acheter]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/prestige acheter"},"hoverEvent":{"action":"show_text","contents":"Voir le prix et ce qu'apporte le rang suivant, puis confirmer"}}]
execute if score #etat_devis bmc4_calc matches 2 run tellraw @s ["",{"text":"Confirmation expirée : ","color":"red"},{"text":"retape /prestige acheter. ","color":"gray"},{"text":"[Acheter]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/prestige acheter"},"hoverEvent":{"action":"show_text","contents":"Voir le prix et ce qu'apporte le rang suivant, puis confirmer"}}]

# Un devis ne sert qu'une fois : effacé avant l'achat.
scoreboard players set @s bmc4_devis 0
execute if score #etat_devis bmc4_calc matches 3 run function bmc4:rangs/acheter
