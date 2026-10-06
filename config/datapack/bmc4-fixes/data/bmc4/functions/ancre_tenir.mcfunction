# Ramène chaque tick le spectateur sur son ancre.
# Exécutée « as » l'ancre (un marker) « at » sa position : le tp vise donc
# la position et la dimension de l'ancre, et garde l'orientation du joueur.

scoreboard players operation #cible bmc4_id = @s bmc4_id
# Seulement s'il s'est éloigné de plus d'un bloc : un tp à chaque tick
# rejouait l'animation de téléportation en continu (retour d'Arthur).
execute as @a[tag=bmc4_ancre,gamemode=spectator] if score @s bmc4_id = #cible bmc4_id unless entity @s[distance=..1] run tp @s ~ ~ ~
