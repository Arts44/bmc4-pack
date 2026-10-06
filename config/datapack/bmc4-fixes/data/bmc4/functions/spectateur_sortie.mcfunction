# Un joueur passé spectateur en raid, encore étiqueté alors qu'aucun raid ne
# tourne : il s'était déconnecté sur l'écran de mort, avant que son ancre
# soit posée, et raid_fin ne l'a pas vu. On le remet en survie (BMC-90).

gamemode survival @s
scoreboard players reset @s bmc4_spec
tag @s remove bmc4_spectateur
