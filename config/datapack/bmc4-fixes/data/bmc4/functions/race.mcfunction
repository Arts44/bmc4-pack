# Cherche la bonne clé NBT pour la race d'un dragon.
# On teste contre les dragons déjà présents : celui qui répond
# nous donne le format à utiliser pour l'invocation.

say === FORMAT DE LA RACE ===

execute if entity @e[type=dragonmounts:dragon,nbt={Breed:"fire"}] run say Breed fire
execute if entity @e[type=dragonmounts:dragon,nbt={breed:"fire"}] run say breed minuscule
execute if entity @e[type=dragonmounts:dragon,nbt={Breed:"dragonmounts:fire"}] run say Breed prefixe
execute if entity @e[type=dragonmounts:dragon,nbt={DragonBreed:"fire"}] run say DragonBreed
execute if entity @e[type=dragonmounts:dragon,nbt={Breed:"ice"}] run say Breed ice
execute if entity @e[type=dragonmounts:dragon,nbt={Breed:"ghost"}] run say Breed ghost
execute if entity @e[type=dragonmounts:dragon,nbt={Breed:"aether"}] run say Breed aether

say === FIN ===
