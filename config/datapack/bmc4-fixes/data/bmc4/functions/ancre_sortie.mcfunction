# Un joueur encore ancré alors qu'aucun raid ne tourne : déconnecté pendant
# son décompte et revenu après la fin du créneau. On le libère.

function bmc4:ancre_lever
gamemode survival @s
scoreboard players reset @s bmc4_spec
