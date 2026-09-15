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
