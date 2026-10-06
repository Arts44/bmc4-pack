# Repeuplement des animaux vanilla — le cycle.
#
# Minecraft ne fait naître les animaux qu'à la génération d'un
# chunk, puis presque plus jamais. Autour d'une base habitée depuis
# des semaines, ils ont été mangés et ne reviennent pas.
#
# Toutes les trois minutes, pour chaque joueur de l'Overworld, on
# regarde combien d'animaux vanilla l'entourent. S'il y en a peu,
# une paire apparaît sur l'herbe, à distance, en plein jour — les
# conditions où le jeu en ferait naître lui-même.

execute as @a[gamemode=!spectator] at @s if dimension minecraft:overworld if predicate bmc4:jour run function bmc4:animaux/joueur

schedule function bmc4:animaux/cycle 3600t
