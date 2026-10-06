# Cherche l'épée en Supremium dans toutes les dimensions.
#
# On ne voit que les chunks chargés. Si rien ne sort, c'est
# qu'elle dort dans une zone où personne ne se trouve — ou
# qu'elle a disparu, cinq minutes après être tombée.

say === EPEE ===

execute in minecraft:overworld positioned 0 0 0 as @e[type=item,distance=..1000000,nbt={Item:{id:"mysticalagriculture:supremium_sword"}}] at @s run say OVERWORLD
execute in minecraft:the_nether positioned 0 0 0 as @e[type=item,distance=..1000000,nbt={Item:{id:"mysticalagriculture:supremium_sword"}}] at @s run say NETHER
execute in minecraft:the_end positioned 0 0 0 as @e[type=item,distance=..1000000,nbt={Item:{id:"mysticalagriculture:supremium_sword"}}] at @s run say END
execute in twilightforest:twilight_forest positioned 0 0 0 as @e[type=item,distance=..1000000,nbt={Item:{id:"mysticalagriculture:supremium_sword"}}] at @s run say TWILIGHT
execute in aether:the_aether positioned 0 0 0 as @e[type=item,distance=..1000000,nbt={Item:{id:"mysticalagriculture:supremium_sword"}}] at @s run say AETHER
execute in blue_skies:everbright positioned 0 0 0 as @e[type=item,distance=..1000000,nbt={Item:{id:"mysticalagriculture:supremium_sword"}}] at @s run say EVERBRIGHT
execute in blue_skies:everdawn positioned 0 0 0 as @e[type=item,distance=..1000000,nbt={Item:{id:"mysticalagriculture:supremium_sword"}}] at @s run say EVERDAWN
execute in deeperdarker:otherside positioned 0 0 0 as @e[type=item,distance=..1000000,nbt={Item:{id:"mysticalagriculture:supremium_sword"}}] at @s run say OTHERSIDE

say --- et dans un coffre ou un cadre a proximite ---
execute at @a[name=Arts_Vio] as @e[type=item_frame,distance=..60] run say CADRE

say === FIN ===
