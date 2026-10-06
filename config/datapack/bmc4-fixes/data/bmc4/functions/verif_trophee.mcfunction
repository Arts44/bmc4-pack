# Vérifie qui détient les têtes-trophées, en annonçant le résultat
# dans la console — « data get » n'y apparaît pas.

say === VERIFICATION DES TROPHEES ===
execute if entity @a[nbt={Inventory:[{tag:{bmc4_trophee:"farmers"}}]}] run say TROPHEE FARMERS EN INVENTAIRE
execute if entity @a[nbt={Inventory:[{tag:{bmc4_trophee:"apex"}}]}] run say TROPHEE APEX EN INVENTAIRE
execute as @a[nbt={Inventory:[{tag:{bmc4_trophee:"farmers"}}]}] run say JE PORTE LE TROPHEE FARMERS
execute if entity @e[type=item,nbt={Item:{tag:{bmc4_trophee:"farmers"}}}] run say TROPHEE FARMERS PAR TERRE
say === FIN ===
