# Prépare l'arbitrage des raids.
#
# Trois compteurs et une équipe :
#   bmc4_raid   drapeau global, 1 pendant un créneau
#   bmc4_morts  les morts de chaque joueur (deathCount)
#   bmc4_spec   décompte en ticks avant le retour en survie

scoreboard objectives add bmc4_raid dummy
scoreboard objectives add bmc4_morts deathCount
scoreboard objectives add bmc4_spec dummy

scoreboard players add #etat bmc4_raid 0

# L'équipe des combattants, remplie par le bot à l'ouverture du
# créneau. Sans elle, l'arbitrage frapperait tout le serveur.
team add bmc4_raid_actif
team modify bmc4_raid_actif friendlyFire true
team modify bmc4_raid_actif displayName "En raid"
