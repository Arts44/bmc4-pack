# Le joueur vient de se reconnecter : ses rangs FTB Ranks sont ré-appliqués.
scoreboard players reset @s bmc4_depart
execute if score @s bmc4_rangs matches 1.. run function bmc4:rangs/g_ftbranks
# Et l'arbre des commandes renvoyé par KubeJS (bmc4_garde.js), rangs à jour.
execute if score @s bmc4_rangs matches 1.. run tag @s add bmc4_resync
