# Vérifie que l'équipe des dragons est en place et peuplée.

say === EQUIPE DES DRAGONS ===
execute if entity @e[type=dragonmounts:dragon,team=bmc4_dragons] run say AU MOINS UN DRAGON DANS L EQUIPE
execute if entity @e[type=dragonmounts:dragon,team=] run say ATTENTION UN DRAGON SANS EQUIPE
execute as @e[type=dragonmounts:dragon,team=bmc4_dragons] run say inscrit
say === FIN ===
