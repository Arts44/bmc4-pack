# Exécutée à chaque tick, mais elle ne fait presque rien.

# --- Le kit de départ ---
# « unless score matches 0.. » n'est vrai que pour un joueur dont
# le score n'a jamais été inscrit, donc jamais servi. Dès que le
# kit est donné, le score passe à 1 et la condition devient fausse
# pour toujours. C'est ce qui manquait à la version précédente,
# qui se redéclenchait en boucle.
execute as @a[gamemode=survival] unless score @s bmc4_kit matches 0.. run function bmc4:kit_depart

# --- Les dragons dans leur équipe ---
# Le sélecteur « team= » ne retient que ceux qui n'en ont aucune,
# donc la commande ne fait rien une fois tout le monde inscrit.
execute as @e[type=dragonmounts:dragon,team=] run team join bmc4_dragons @s

# --- L'arbitrage des raids ---
# Ne tourne que pendant un créneau : hors raid, cette ligne ne fait rien.
# C'est elle qui applique la perte de cœur et les cinq minutes en
# spectateur (raid_tick). Elle avait sauté au déploiement de BMC-90 le
# 5 octobre, remise le 6 octobre après le test.
execute if score #etat bmc4_raid matches 1 run function bmc4:raid_tick
# Hors créneau : libère un joueur resté ancré (déconnecté pendant son décompte).
execute if score #etat bmc4_raid matches 0 as @a[tag=bmc4_ancre] run function bmc4:ancre_sortie

# --- Le cœur perdu (BMC-90) : soins à tout moment, migration ---
function bmc4:coeur_tick
