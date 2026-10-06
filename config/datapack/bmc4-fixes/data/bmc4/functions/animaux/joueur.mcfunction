# Repeuplement — pour un joueur.
#
# Huit animaux vanilla dans un rayon de 64 blocs, c'est la densité
# d'une plaine fraîchement générée. Au-dessus, on ne fait rien :
# le but est de compenser la disparition, pas de surpeupler — un
# élevage près de la base ne doit pas déclencher de nouvelles
# apparitions.

execute store result score @s bmc4_anim if entity @e[type=#bmc4:animaux_vanilla,distance=..64]
execute if score @s bmc4_anim matches ..7 run function bmc4:animaux/tenter
