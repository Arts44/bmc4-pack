# Cherche les objets au sol autour du joueur et signale ceux qui
# pourraient être la pioche perdue.
#
# Les objets sont des entités : contrairement aux blocs, on peut
# les chercher par rayon en une seule commande.

say === OBJETS AU SOL AUTOUR DE TOI ===

execute at Arts_Vio if entity @e[type=item,distance=..8] run say IL Y A DES OBJETS DANS 8 BLOCS
execute at Arts_Vio if entity @e[type=item,distance=..16] run say ... DANS 16 BLOCS
execute at Arts_Vio if entity @e[type=item,distance=..32] run say ... DANS 32 BLOCS
execute at Arts_Vio if entity @e[type=item,distance=..64] run say ... DANS 64 BLOCS
execute at Arts_Vio if entity @e[type=item,distance=..128] run say ... DANS 128 BLOCS

say --- la pioche en particulier ---

execute at Arts_Vio if entity @e[type=item,distance=..128,nbt={Item:{id:"mysticalagriculture:imperium_pickaxe"}}] run say PIOCHE IMPERIUM TROUVEE DANS 128
execute at Arts_Vio if entity @e[type=item,distance=..32,nbt={Item:{id:"mysticalagriculture:imperium_pickaxe"}}] run say PIOCHE IMPERIUM DANS 32
execute at Arts_Vio if entity @e[type=item,distance=..8,nbt={Item:{id:"mysticalagriculture:imperium_pickaxe"}}] run say PIOCHE IMPERIUM DANS 8

say === FIN ===
