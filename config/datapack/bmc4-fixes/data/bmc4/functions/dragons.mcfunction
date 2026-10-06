# Recense les dragons par dimension et par race.
#
# « execute in <dim> as @e » ne filtre pas : il faut ancrer une
# position dans la dimension et borner la distance pour que le
# sélecteur s'y limite vraiment.

say === DRAGONS PAR DIMENSION ===

execute in minecraft:overworld positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000] run say OVERWORLD
execute in twilightforest:twilight_forest positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000] run say TWILIGHT
execute in minecraft:the_nether positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000] run say NETHER
execute in minecraft:the_end positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000] run say END
execute in aether:the_aether positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000] run say AETHER
execute in blue_skies:everbright positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000] run say EVERBRIGHT
execute in blue_skies:everdawn positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000] run say EVERDAWN
execute in deeperdarker:otherside positioned 0 0 0 as @e[type=dragonmounts:dragon,distance=..1000000] run say OTHERSIDE

say --- les tiens, tous dimensions confondues ---
execute as @e[type=dragonmounts:dragon,nbt={Owner:[I;1055725362,1303858954,-1744112143,1845287622]}] run say A TOI

say === FIN ===
