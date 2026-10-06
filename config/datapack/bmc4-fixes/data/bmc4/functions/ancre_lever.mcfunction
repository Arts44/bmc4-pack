# Retire l'ancre d'un joueur (exécutée « as » le joueur).
# Le joueur est déjà sur son ancre : le chunk est chargé, le marker trouvable.

scoreboard players operation #cible bmc4_id = @s bmc4_id
execute as @e[type=minecraft:marker,tag=bmc4_ancre] if score @s bmc4_id = #cible bmc4_id run kill @s
tag @s remove bmc4_ancre
