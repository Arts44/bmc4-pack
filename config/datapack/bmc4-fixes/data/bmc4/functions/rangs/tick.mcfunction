# Rangs de prestige (BMC-91), à chaque tick. Appelée par bmc4:tick.
#
# Les trois déclencheurs se rouvrent à chaque tick : /trigger ne marche
# qu'une fois par « enable ».
scoreboard players enable @a bmc4_rang
scoreboard players enable @a bmc4_aura
scoreboard players enable @a bmc4_manger

execute as @a[scores={bmc4_rang=1..}] run function bmc4:rangs/demande
execute as @a[scores={bmc4_aura=1..}] run function bmc4:rangs/aura_demande
execute as @a[scores={bmc4_manger=1..}] run function bmc4:rangs/g_manger

# Une connexion (le compteur « quitter la partie » a bougé) : les rangs FTB
# Ranks sont ré-appliqués, au cas où ranks.snbt ou players.snbt aurait été
# remis à zéro. Le score bmc4_rangs fait foi.
execute as @a[scores={bmc4_depart=1..}] run function bmc4:rangs/retour

# Hors raid, un joueur classé sans équipe retrouve celle de son rang : à la
# fin d'un raid (raid_fin vide bmc4_raid_actif), ou à la connexion s'il était
# absent à ce moment-là.
execute unless score #etat bmc4_raid matches 1 as @a[team=] if score @s bmc4_rangs matches 1.. run function bmc4:rangs/g_equipe

# Les auras, toutes les dix ticks.
scoreboard players add #horloge bmc4_calc 1
execute if score #horloge bmc4_calc matches 10.. run function bmc4:rangs/g_aura
execute if score #horloge bmc4_calc matches 10.. run scoreboard players set #horloge bmc4_calc 0
