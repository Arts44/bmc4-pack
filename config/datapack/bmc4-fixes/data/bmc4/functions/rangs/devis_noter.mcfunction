# Assez de niveaux : bmc4_calc devient ce qui restera, le devis est noté (rang
# visé et heure du monde), puis affiché avec son bouton.
scoreboard players operation @s bmc4_calc = @s bmc4_niveaux
scoreboard players operation @s bmc4_calc -= #cout bmc4_calc
scoreboard players operation @s bmc4_devis = @s bmc4_cible
execute store result score @s bmc4_devis_t run time query gametime
function bmc4:rangs/g_devis
