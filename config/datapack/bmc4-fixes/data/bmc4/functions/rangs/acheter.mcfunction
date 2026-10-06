# Acheter le rang suivant (exécutée « as » le joueur).
#
# Tout se passe dans le même tick : niveaux lus, comparés, puis retirés d'un
# seul coup. Personne ne peut dépenser ses niveaux entre la lecture et le
# retrait.
execute unless score @s bmc4_rangs matches 0.. run scoreboard players set @s bmc4_rangs 0
scoreboard players operation @s bmc4_cible = @s bmc4_rangs
scoreboard players add @s bmc4_cible 1
function bmc4:rangs/g_cout

# Au-delà du dernier palier préparé, g_cout laisse #cout à -1.
execute if score #cout bmc4_calc matches ..-1 run function bmc4:rangs/g_plafond
execute if score #cout bmc4_calc matches 0.. run function bmc4:rangs/acheter_prix
