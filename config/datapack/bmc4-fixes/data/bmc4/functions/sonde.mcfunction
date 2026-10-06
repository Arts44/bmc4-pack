# Sonde la colonne verticale au-dessus du joueur pour trouver
# l'ouverture de la tour.
#
# On monte bloc par bloc et on annonce ce qu'on rencontre : de
# l'air veut dire un passage, un bloc plein veut dire un plancher
# ou un mur. C'est le moyen le plus direct de savoir par où entrer
# quand on se tient sous la structure.

say === SONDAGE VERTICAL ===

execute at Arts_Vio if block ~ ~1 ~ air run say +1 AIR
execute at Arts_Vio if block ~ ~2 ~ air run say +2 AIR
execute at Arts_Vio if block ~ ~3 ~ air run say +3 AIR
execute at Arts_Vio if block ~ ~4 ~ air run say +4 AIR
execute at Arts_Vio if block ~ ~5 ~ air run say +5 AIR
execute at Arts_Vio if block ~ ~6 ~ air run say +6 AIR
execute at Arts_Vio if block ~ ~8 ~ air run say +8 AIR
execute at Arts_Vio if block ~ ~10 ~ air run say +10 AIR
execute at Arts_Vio if block ~ ~12 ~ air run say +12 AIR
execute at Arts_Vio if block ~ ~15 ~ air run say +15 AIR
execute at Arts_Vio if block ~ ~20 ~ air run say +20 AIR

say --- autour de toi, au niveau des pieds ---

execute at Arts_Vio if block ~5 ~ ~ air run say EST 5 AIR
execute at Arts_Vio if block ~-5 ~ ~ air run say OUEST 5 AIR
execute at Arts_Vio if block ~ ~ ~5 air run say SUD 5 AIR
execute at Arts_Vio if block ~ ~ ~-5 air run say NORD 5 AIR
execute at Arts_Vio if block ~10 ~ ~ air run say EST 10 AIR
execute at Arts_Vio if block ~-10 ~ ~ air run say OUEST 10 AIR
execute at Arts_Vio if block ~ ~ ~10 air run say SUD 10 AIR
execute at Arts_Vio if block ~ ~ ~-10 air run say NORD 10 AIR

say === FIN ===
