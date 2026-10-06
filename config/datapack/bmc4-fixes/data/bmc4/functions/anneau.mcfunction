# Anneau complet autour du joueur, au niveau des pieds puis à
# hauteur de tête. Huit directions, quatre distances.
#
# Une entrée se reconnaît à deux blocs d'air superposés : le
# passage doit laisser tenir debout. Les points signalés aux deux
# hauteurs sont donc les candidats sérieux.

say === ANNEAU AUTOUR DU JOUEUR ===
say --- niveau des pieds ---

execute at Arts_Vio if block ~3 ~ ~ air run say N ... E 3
execute at Arts_Vio if block ~6 ~ ~ air run say E 6
execute at Arts_Vio if block ~12 ~ ~ air run say E 12
execute at Arts_Vio if block ~20 ~ ~ air run say E 20

execute at Arts_Vio if block ~-3 ~ ~ air run say O 3
execute at Arts_Vio if block ~-6 ~ ~ air run say O 6
execute at Arts_Vio if block ~-12 ~ ~ air run say O 12
execute at Arts_Vio if block ~-20 ~ ~ air run say O 20

execute at Arts_Vio if block ~ ~ ~3 air run say S 3
execute at Arts_Vio if block ~ ~ ~6 air run say S 6
execute at Arts_Vio if block ~ ~ ~12 air run say S 12
execute at Arts_Vio if block ~ ~ ~20 air run say S 20

execute at Arts_Vio if block ~ ~ ~-3 air run say N 3
execute at Arts_Vio if block ~ ~ ~-6 air run say N 6
execute at Arts_Vio if block ~ ~ ~-12 air run say N 12
execute at Arts_Vio if block ~ ~ ~-20 air run say N 20

execute at Arts_Vio if block ~6 ~ ~6 air run say SE 6
execute at Arts_Vio if block ~-6 ~ ~6 air run say SO 6
execute at Arts_Vio if block ~6 ~ ~-6 air run say NE 6
execute at Arts_Vio if block ~-6 ~ ~-6 air run say NO 6
execute at Arts_Vio if block ~12 ~ ~12 air run say SE 12
execute at Arts_Vio if block ~-12 ~ ~12 air run say SO 12
execute at Arts_Vio if block ~12 ~ ~-12 air run say NE 12
execute at Arts_Vio if block ~-12 ~ ~-12 air run say NO 12

say --- hauteur de tete, un cran plus haut ---

execute at Arts_Vio if block ~3 ~1 ~ air run say tete E 3
execute at Arts_Vio if block ~6 ~1 ~ air run say tete E 6
execute at Arts_Vio if block ~12 ~1 ~ air run say tete E 12
execute at Arts_Vio if block ~-3 ~1 ~ air run say tete O 3
execute at Arts_Vio if block ~-6 ~1 ~ air run say tete O 6
execute at Arts_Vio if block ~-12 ~1 ~ air run say tete O 12
execute at Arts_Vio if block ~ ~1 ~3 air run say tete S 3
execute at Arts_Vio if block ~ ~1 ~6 air run say tete S 6
execute at Arts_Vio if block ~ ~1 ~12 air run say tete S 12
execute at Arts_Vio if block ~ ~1 ~-3 air run say tete N 3
execute at Arts_Vio if block ~ ~1 ~-6 air run say tete N 6
execute at Arts_Vio if block ~ ~1 ~-12 air run say tete N 12

say === FIN ===
