# Sonde les champs d'un dragon : chaque lecture réussie écrit une
# ligne dans le journal, chaque champ absent n'écrit rien.
# C'est la façon la plus sûre de découvrir le format du mod.

execute as @e[type=dragonmounts:dragon,limit=1,sort=random] run data get entity @s ReproCount
execute as @e[type=dragonmounts:dragon,limit=1,sort=random] run data get entity @s Breed
execute as @e[type=dragonmounts:dragon,limit=1,sort=random] run data get entity @s Age
execute as @e[type=dragonmounts:dragon,limit=1,sort=random] run data get entity @s AgeTicks
execute as @e[type=dragonmounts:dragon,limit=1,sort=random] run data get entity @s growth
execute as @e[type=dragonmounts:dragon,limit=1,sort=random] run data get entity @s LifeStageTicks
execute as @e[type=dragonmounts:dragon,limit=1,sort=random] run data get entity @s InLove
execute as @e[type=dragonmounts:dragon,limit=1,sort=random] run data get entity @s Sitting
execute as @e[type=dragonmounts:dragon,limit=1,sort=random] run data get entity @s CustomName
