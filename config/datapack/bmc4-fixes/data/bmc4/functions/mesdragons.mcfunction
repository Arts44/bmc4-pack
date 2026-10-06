# Recense les dragons d'Arts_Vio par race et par dimension.
#
# On ancre une position dans chaque dimension et on borne la
# distance : « execute in » seul ne filtre pas le sélecteur.

say === MES DRAGONS ===

say --- Overworld ---
execute in minecraft:overworld positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000,nbt={Owner:[I;1055725362,1303858954,-1744112143,1845287622]}] run say un dragon

say --- Twilight Forest ---
execute in twilightforest:twilight_forest positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000,nbt={Owner:[I;1055725362,1303858954,-1744112143,1845287622]}] run say un dragon

say --- Aether ---
execute in aether:the_aether positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000,nbt={Owner:[I;1055725362,1303858954,-1744112143,1845287622]}] run say un dragon

say --- Nether ---
execute in minecraft:the_nether positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000,nbt={Owner:[I;1055725362,1303858954,-1744112143,1845287622]}] run say un dragon

say --- End ---
execute in minecraft:the_end positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000,nbt={Owner:[I;1055725362,1303858954,-1744112143,1845287622]}] run say un dragon

say --- Everbright ---
execute in blue_skies:everbright positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000,nbt={Owner:[I;1055725362,1303858954,-1744112143,1845287622]}] run say un dragon

say --- Everdawn ---
execute in blue_skies:everdawn positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000,nbt={Owner:[I;1055725362,1303858954,-1744112143,1845287622]}] run say un dragon

say --- Otherside ---
execute in deeperdarker:otherside positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000,nbt={Owner:[I;1055725362,1303858954,-1744112143,1845287622]}] run say un dragon

say === FIN ===
