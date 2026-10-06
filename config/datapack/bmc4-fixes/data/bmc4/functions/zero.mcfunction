# Sonde la zone du point zéro : relief et waystone éventuelle.

say === POINT ZERO ===
execute in minecraft:overworld if block 0 50 0 air run say AIR a Y50
execute in minecraft:overworld if block 0 55 0 air run say AIR a Y55
execute in minecraft:overworld if block 0 60 0 air run say AIR a Y60
execute in minecraft:overworld if block 0 62 0 air run say AIR a Y62
execute in minecraft:overworld if block 0 64 0 air run say AIR a Y64
execute in minecraft:overworld if block 0 66 0 air run say AIR a Y66
execute in minecraft:overworld if block 0 70 0 air run say AIR a Y70
execute in minecraft:overworld if block 0 75 0 air run say AIR a Y75
execute in minecraft:overworld if block 0 80 0 air run say AIR a Y80
execute in minecraft:overworld if block 0 90 0 air run say AIR a Y90
execute in minecraft:overworld if block 0 100 0 air run say AIR a Y100

say --- eau ou lave au point zero ---
execute in minecraft:overworld if block 0 62 0 water run say EAU a Y62
execute in minecraft:overworld if block 0 55 0 water run say EAU a Y55
execute in minecraft:overworld if block 0 50 0 water run say EAU a Y50

say --- waystone dans les environs ---
execute in minecraft:overworld if entity @e[type=item,distance=..1] run say ignorer
execute in minecraft:overworld if block 0 64 0 waystones:waystone run say WAYSTONE en 0 64 0
execute in minecraft:overworld if block 0 65 0 waystones:waystone run say WAYSTONE en 0 65 0
execute in minecraft:overworld if block 0 70 0 waystones:waystone run say WAYSTONE en 0 70 0

say === FIN ===
