# Kit de départ — donné une seule fois par joueur.
#
# La première ligne est la plus importante : on marque le joueur
# AVANT de lui donner quoi que ce soit. Si la suite échoue, il
# n'aura pas son kit, mais le serveur ne partira pas en boucle.

scoreboard players set @s bmc4_kit 1

give @s minecraft:stone_pickaxe
give @s minecraft:stone_axe
give @s minecraft:stone_shovel
give @s minecraft:stone_sword

give @s minecraft:cooked_beef 32
give @s minecraft:torch 64
give @s minecraft:oak_planks 64
give @s minecraft:compass

# Le premier vrai sac : 9 emplacements, teintable.
# Identifiant vérifié le 15 septembre — « leather » n'existe pas,
# les paliers sont baby, frayed, plated, gilded, bejeweled,
# blazing, withered, endless.
give @s inmis:frayed_backpack

tellraw @s ["",{"text":"\n"},{"text":"Bienvenue sur BMC4 ","color":"gold","bold":true},{"text":"\n"},{"text":"Un kit de départ vient d'arriver dans ton inventaire.","color":"yellow"},{"text":"\n"},{"text":"Pense à claim ta base avec FTB Chunks : ","color":"gray"},{"text":"touche M","color":"aqua","bold":true},{"text":"\n"},{"text":"Les guides sont sur le Discord, dans la catégorie GUIDE.","color":"gray"},{"text":"\n"}]
