# Inventaire des objets accumulés autour de la base des Farmer's
# Chaque ligne teste la présence d'un type et l'annonce.
# Temporaire — à supprimer après diagnostic.

say === INVENTAIRE DE L AMAS ===

execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:cobblestone"}}] run say cobblestone
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:dirt"}}] run say dirt
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:stone"}}] run say stone
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:gravel"}}] run say gravel
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:sand"}}] run say sand
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:flint"}}] run say flint

execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:wheat_seeds"}}] run say wheat_seeds
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:wheat"}}] run say wheat
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:bone_meal"}}] run say bone_meal
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:sugar_cane"}}] run say sugar_cane
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:bamboo"}}] run say bamboo
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:kelp"}}] run say kelp

execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:rotten_flesh"}}] run say rotten_flesh
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:bone"}}] run say bone
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:arrow"}}] run say arrow
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:string"}}] run say string
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:gunpowder"}}] run say gunpowder

execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:diamond"}}] run say DIAMOND
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:iron_ingot"}}] run say IRON_INGOT
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:gold_ingot"}}] run say GOLD_INGOT
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:emerald"}}] run say EMERALD
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:netherite_ingot"}}] run say NETHERITE

execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:oak_log"}}] run say oak_log
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:oak_sapling"}}] run say oak_sapling
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:stick"}}] run say stick
execute in minecraft:overworld positioned -2427 102 -1677 if entity @e[type=item,distance=..250,nbt={Item:{id:"minecraft:apple"}}] run say apple

say === FIN ===
