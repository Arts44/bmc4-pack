# Retire #cout bmc4_calc niveaux, puis donne le rang.
#
# Minecraft 1.20.1 n'a pas de macros : « experience add » ne prend pas un
# score. Le prix est donc décomposé en puissances de deux (jusqu'à 2^16 :
# le dernier palier de l'Infini coûte 82 500 niveaux), chacune retirée si
# elle tient dans ce qui reste. Le total retiré est exactement le prix.

scoreboard players operation #reste bmc4_calc = #cout bmc4_calc
execute if score #reste bmc4_calc matches 65536.. run experience add @s -65536 levels
execute if score #reste bmc4_calc matches 65536.. run scoreboard players remove #reste bmc4_calc 65536
execute if score #reste bmc4_calc matches 32768.. run experience add @s -32768 levels
execute if score #reste bmc4_calc matches 32768.. run scoreboard players remove #reste bmc4_calc 32768
execute if score #reste bmc4_calc matches 16384.. run experience add @s -16384 levels
execute if score #reste bmc4_calc matches 16384.. run scoreboard players remove #reste bmc4_calc 16384
execute if score #reste bmc4_calc matches 8192.. run experience add @s -8192 levels
execute if score #reste bmc4_calc matches 8192.. run scoreboard players remove #reste bmc4_calc 8192
execute if score #reste bmc4_calc matches 4096.. run experience add @s -4096 levels
execute if score #reste bmc4_calc matches 4096.. run scoreboard players remove #reste bmc4_calc 4096
execute if score #reste bmc4_calc matches 2048.. run experience add @s -2048 levels
execute if score #reste bmc4_calc matches 2048.. run scoreboard players remove #reste bmc4_calc 2048
execute if score #reste bmc4_calc matches 1024.. run experience add @s -1024 levels
execute if score #reste bmc4_calc matches 1024.. run scoreboard players remove #reste bmc4_calc 1024
execute if score #reste bmc4_calc matches 512.. run experience add @s -512 levels
execute if score #reste bmc4_calc matches 512.. run scoreboard players remove #reste bmc4_calc 512
execute if score #reste bmc4_calc matches 256.. run experience add @s -256 levels
execute if score #reste bmc4_calc matches 256.. run scoreboard players remove #reste bmc4_calc 256
execute if score #reste bmc4_calc matches 128.. run experience add @s -128 levels
execute if score #reste bmc4_calc matches 128.. run scoreboard players remove #reste bmc4_calc 128
execute if score #reste bmc4_calc matches 64.. run experience add @s -64 levels
execute if score #reste bmc4_calc matches 64.. run scoreboard players remove #reste bmc4_calc 64
execute if score #reste bmc4_calc matches 32.. run experience add @s -32 levels
execute if score #reste bmc4_calc matches 32.. run scoreboard players remove #reste bmc4_calc 32
execute if score #reste bmc4_calc matches 16.. run experience add @s -16 levels
execute if score #reste bmc4_calc matches 16.. run scoreboard players remove #reste bmc4_calc 16
execute if score #reste bmc4_calc matches 8.. run experience add @s -8 levels
execute if score #reste bmc4_calc matches 8.. run scoreboard players remove #reste bmc4_calc 8
execute if score #reste bmc4_calc matches 4.. run experience add @s -4 levels
execute if score #reste bmc4_calc matches 4.. run scoreboard players remove #reste bmc4_calc 4
execute if score #reste bmc4_calc matches 2.. run experience add @s -2 levels
execute if score #reste bmc4_calc matches 2.. run scoreboard players remove #reste bmc4_calc 2
execute if score #reste bmc4_calc matches 1.. run experience add @s -1 levels
execute if score #reste bmc4_calc matches 1.. run scoreboard players remove #reste bmc4_calc 1

execute store result score @s bmc4_niveaux run experience query @s levels
scoreboard players add @s bmc4_rangs 1

# Permissions (FTB Ranks), équipe du rang (sauf en plein raid : l'équipe du
# raid reste prioritaire, tick la rendra à la fin), kit, message, annonce.
function bmc4:rangs/g_ftbranks
# Le client garde l'ancienne liste de commandes (/home en rouge) : KubeJS
# (bmc4_garde.js) renvoie l'arbre aux joueurs portant cette étiquette.
tag @s add bmc4_resync
execute unless entity @s[team=bmc4_raid_actif] run function bmc4:rangs/g_equipe
function bmc4:rangs/g_kit
function bmc4:rangs/g_obtenu
function bmc4:rangs/g_annonce
