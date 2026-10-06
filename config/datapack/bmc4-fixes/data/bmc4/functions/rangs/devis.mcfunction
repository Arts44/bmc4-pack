# /prestige acheter : le devis, sans rien acheter (exécutée « as » le joueur,
# par KubeJS). Le rang visé, son prix, ce qu'il apporte, ce qui restera, et le
# bouton [Confirmer l'achat]. Le devis est noté (rang visé, heure du monde) :
# /prestige confirmer l'honore pendant 30 secondes (600 ticks).
execute unless score @s bmc4_rangs matches 0.. run scoreboard players set @s bmc4_rangs 0
scoreboard players operation @s bmc4_cible = @s bmc4_rangs
scoreboard players add @s bmc4_cible 1
function bmc4:rangs/g_cout
scoreboard players set @s bmc4_devis 0

# Au-delà du dernier palier préparé, g_cout laisse #cout à -1.
execute if score #cout bmc4_calc matches ..-1 run function bmc4:rangs/g_plafond
execute if score #cout bmc4_calc matches 0.. run function bmc4:rangs/devis_prix
