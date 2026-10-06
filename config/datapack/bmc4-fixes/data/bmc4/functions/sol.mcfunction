# Identifie les blocs sombres autour du joueur.
#
# La commande précédente n'a rien changé : soit les blocs ne sont
# pas du sable des âmes vanilla, soit ils sont hors de la zone
# traitée. On teste avant de retoucher quoi que ce soit.

say === SONDAGE DU SOL ===

execute at @a[name=Arts_Vio] positioned ~ ~-1 ~ if block ~ ~ ~ minecraft:soul_sand run say SOUS MOI soul_sand
execute at @a[name=Arts_Vio] positioned ~ ~-1 ~ if block ~ ~ ~ minecraft:soul_soil run say SOUS MOI soul_soil
execute at @a[name=Arts_Vio] positioned ~ ~-1 ~ if block ~ ~ ~ minecraft:dirt run say SOUS MOI dirt
execute at @a[name=Arts_Vio] positioned ~ ~-1 ~ if block ~ ~ ~ minecraft:grass_block run say SOUS MOI grass_block
execute at @a[name=Arts_Vio] positioned ~ ~-1 ~ if block ~ ~ ~ minecraft:podzol run say SOUS MOI podzol
execute at @a[name=Arts_Vio] positioned ~ ~-1 ~ if block ~ ~ ~ minecraft:coarse_dirt run say SOUS MOI coarse_dirt
execute at @a[name=Arts_Vio] positioned ~ ~-1 ~ if block ~ ~ ~ minecraft:rooted_dirt run say SOUS MOI rooted_dirt
execute at @a[name=Arts_Vio] positioned ~ ~-1 ~ if block ~ ~ ~ minecraft:mud run say SOUS MOI mud
execute at @a[name=Arts_Vio] positioned ~ ~-1 ~ if block ~ ~ ~ deeperdarker:gloomy_sculk run say SOUS MOI gloomy_sculk
execute at @a[name=Arts_Vio] positioned ~ ~-1 ~ if block ~ ~ ~ minecraft:sculk run say SOUS MOI sculk

say --- les fleurs noires ---
execute at @a[name=Arts_Vio] as @e[type=item,distance=..5] run say OBJET
execute at @a[name=Arts_Vio] if block ~ ~ ~ minecraft:wither_rose run say DANS UNE ROSE DE WITHER
execute at @a[name=Arts_Vio] if block ~1 ~ ~ minecraft:wither_rose run say ROSE a cote
execute at @a[name=Arts_Vio] if block ~ ~ ~1 minecraft:wither_rose run say ROSE a cote

say --- la biome ---
execute at @a[name=Arts_Vio] run say position sondee

say === FIN DU SONDAGE ===
