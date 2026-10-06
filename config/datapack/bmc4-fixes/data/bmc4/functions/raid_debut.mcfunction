# Ouvre le créneau.
#
# L'arbitrage ne vise que les combattants : une équipe de score
# rassemble les membres des deux factions engagées. Quelqu'un qui
# creuse dans son coin et meurt d'une chute pendant le créneau ne
# doit pas se retrouver spectateur cinq minutes.
#
# Le bot remplit l'équipe juste avant d'appeler cette fonction.

scoreboard players set #etat bmc4_raid 1
# « * » vise tous les joueurs suivis, connectés ou non : avec @a, un joueur
# mort hors ligne entre deux créneaux gardait son compteur et perdait cinq
# minutes dès sa reconnexion (BMC-90, 6 octobre).
scoreboard players set * bmc4_morts 0
scoreboard players reset * bmc4_spec

tellraw @a[team=bmc4_raid_actif] ["",{"text":"\n⚔️ Le raid commence.","color":"red","bold":true},{"text":"\nChaque mort coûte cinq minutes en spectateur, dans les deux camps.\n","color":"gray"}]

tellraw @a[team=!bmc4_raid_actif] ["",{"text":"\n⚔️ Un raid est en cours.","color":"gold"},{"text":" Tu n'y participes pas : rien ne change pour toi.\n","color":"gray"}]
