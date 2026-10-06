# Ferme le créneau : tout le monde revient en survie.
#
# Sans ça, un joueur mort à la 59e minute resterait spectateur
# après la fin du raid.

scoreboard players set #etat bmc4_raid 0

# Une mort survenue entre le dernier tick d'arbitrage et la fermeture
# compte quand même pour le cœur (BMC-90).
execute as @a[team=bmc4_raid_actif,scores={bmc4_morts=1..}] run function bmc4:coeur_perte

execute as @a[tag=bmc4_ancre] run function bmc4:ancre_lever
gamemode survival @a[gamemode=spectator]
scoreboard players reset * bmc4_spec
scoreboard players set @a bmc4_morts 0

team empty bmc4_raid_actif
