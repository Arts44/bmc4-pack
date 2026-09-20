# Ouvre le créneau.
#
# L'arbitrage ne vise que les combattants : le bot inscrit les
# membres des deux factions engagées dans bmc4_raid_actif juste
# avant d'appeler cette fonction.

scoreboard players set #etat bmc4_raid 1
scoreboard players set @a bmc4_morts 0
scoreboard players reset * bmc4_spec
