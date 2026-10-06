# Cherche l'épée en Supremium éveillé : inventaire, sol, alentours.

say === EPEE EVEILLEE ===

execute if entity @a[name=Arts_Vio,nbt={Inventory:[{id:"mysticalagriculture:awakened_supremium_sword"}]}] run say DANS L INVENTAIRE
execute if entity @a[name=Arts_Vio,nbt={EnderItems:[{id:"mysticalagriculture:awakened_supremium_sword"}]}] run say DANS L ENDER CHEST

say --- au sol, partout ---
execute as @e[type=item,nbt={Item:{id:"mysticalagriculture:awakened_supremium_sword"}}] at @s run tp @s ~ ~ ~

say --- tous les objets au sol a moins de 40 blocs ---
execute at @a[name=Arts_Vio] as @e[type=item,distance=..40] at @s run tp @s ~ ~ ~

say === FIN ===
