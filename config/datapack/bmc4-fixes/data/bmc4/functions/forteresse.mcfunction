# Localise la forteresse la plus proche et l'annonce au chat.
#
# `locate` renvoie sa réponse à l'émetteur de la commande, pas au
# journal : lancée par la console, elle est invisible ici. En
# l'exécutant comme le joueur, la réponse s'affiche dans SON chat.
#
# Le pack remplace les forteresses vanilla par celles de Yung's
# Better Strongholds — d'où l'identifiant betterstrongholds.

execute as @a[name=Arts_Vio] at @s run locate structure betterstrongholds:stronghold
execute as @a[name=Arts_Vio] at @s run locate structure minecraft:stronghold
