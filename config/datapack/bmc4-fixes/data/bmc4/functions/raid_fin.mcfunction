# Ferme le créneau : tout le monde revient en survie.
#
# Sans ça, un joueur mort à la 59e minute resterait spectateur
# après la fin du raid.

scoreboard players set #etat bmc4_raid 0

gamemode survival @a[gamemode=spectator]
scoreboard players reset * bmc4_spec
scoreboard players set @a bmc4_morts 0

team empty bmc4_raid_actif
