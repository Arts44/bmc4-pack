# Arbitrage du raid, exécuté à chaque tick pendant un créneau.
#
# Pourquoi côté serveur et non dans le bot : la règle des cinq
# minutes doit s'appliquer même si Discord est injoignable ou si
# le bot redémarre au mauvais moment. Un arbitre qui s'absente
# pendant un raid ne sert à rien.

# --- Une mort vient d'arriver ---
# deathCount s'incrémente seul. L'ordre compte : on pose le
# décompte et le mode AVANT de remettre le compteur à zéro,
# sinon la mort est oubliée avant d'être traitée.
#
# Périmètre (BMC-90, 5 octobre) : SEULE l'équipe bmc4_raid_actif, remplie
# par le bot avec les membres des deux factions engagées. Avant, le
# sélecteur visait @a : les cinq minutes frappaient aussi les joueurs
# étrangers au raid. Le cœur perdu suit le même périmètre.
execute as @a[team=bmc4_raid_actif,scores={bmc4_morts=1..}] run function bmc4:coeur_perte
execute as @a[team=bmc4_raid_actif,scores={bmc4_morts=1..}] run scoreboard players set @s bmc4_spec 6000
execute as @a[team=bmc4_raid_actif,scores={bmc4_morts=1..}] run gamemode spectator @s
# L'étiquette survit à la déconnexion : un joueur parti depuis l'écran de
# mort n'a pas encore d'ancre, mais il sera libéré hors créneau (tick).
execute as @a[team=bmc4_raid_actif,scores={bmc4_morts=1..}] run tag @s add bmc4_spectateur
execute as @a[scores={bmc4_morts=1..}] run scoreboard players set @s bmc4_morts 0

# --- Le décompte tourne ---
execute as @a[scores={bmc4_spec=1..}] run scoreboard players remove @s bmc4_spec 1

# --- Avertissements : 2 minutes (2 400 ticks) et 30 secondes (600) ---
# Annoncés le 17 septembre, construits le 6 octobre (BMC-90).
execute as @a[scores={bmc4_spec=2400}] run tellraw @s {"text":"⏳ Plus que 2 minutes en spectateur.","color":"yellow"}
execute as @a[scores={bmc4_spec=600}] run tellraw @s {"text":"⏳ Plus que 30 secondes en spectateur.","color":"gold"}

# --- Le spectateur reste à son point de réapparition (6 octobre) ---
# @e[type=player] ignore les joueurs encore sur l'écran de mort : l'ancre
# se pose donc au premier tick après la réapparition, pas sur le lieu de
# la mort.
execute as @e[type=minecraft:player,scores={bmc4_spec=1..},tag=!bmc4_ancre] at @s run function bmc4:ancre_poser
execute as @e[type=minecraft:marker,tag=bmc4_ancre] at @s run function bmc4:ancre_tenir

# --- Retour en survie, sur place : c'est-à-dire sur l'ancre ---
execute as @a[scores={bmc4_spec=0},tag=bmc4_ancre] run function bmc4:ancre_lever
execute as @a[scores={bmc4_spec=0},gamemode=spectator] run gamemode survival @s
execute as @a[scores={bmc4_spec=0}] run tag @s remove bmc4_spectateur
execute as @a[scores={bmc4_spec=0}] run scoreboard players reset @s bmc4_spec
