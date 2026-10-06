# Répare les dégâts du souffle du Wither Dragon — v2.
#
# ⚠️ La version précédente échouait en silence : fill plafonne à
# 32 768 blocs par appel, et mes zones en faisaient 144 000.
# Aucune erreur visible en jeu, juste rien qui change.
#
# Ici chaque tuile fait 35 × 35 × 25, soit 30 625 blocs.

say === REPARATION v2 ===

# --- minecraft:soul_soil → dirt ---
fill -4280 58 5840 -4246 82 5874 dirt replace minecraft:soul_soil
fill -4280 58 5875 -4246 82 5909 dirt replace minecraft:soul_soil
fill -4280 58 5910 -4246 82 5944 dirt replace minecraft:soul_soil
fill -4280 58 5945 -4246 82 5979 dirt replace minecraft:soul_soil
fill -4280 58 5980 -4246 82 6000 dirt replace minecraft:soul_soil
fill -4245 58 5840 -4211 82 5874 dirt replace minecraft:soul_soil
fill -4245 58 5875 -4211 82 5909 dirt replace minecraft:soul_soil
fill -4245 58 5910 -4211 82 5944 dirt replace minecraft:soul_soil
fill -4245 58 5945 -4211 82 5979 dirt replace minecraft:soul_soil
fill -4245 58 5980 -4211 82 6000 dirt replace minecraft:soul_soil
fill -4210 58 5840 -4176 82 5874 dirt replace minecraft:soul_soil
fill -4210 58 5875 -4176 82 5909 dirt replace minecraft:soul_soil
fill -4210 58 5910 -4176 82 5944 dirt replace minecraft:soul_soil
fill -4210 58 5945 -4176 82 5979 dirt replace minecraft:soul_soil
fill -4210 58 5980 -4176 82 6000 dirt replace minecraft:soul_soil
fill -4175 58 5840 -4141 82 5874 dirt replace minecraft:soul_soil
fill -4175 58 5875 -4141 82 5909 dirt replace minecraft:soul_soil
fill -4175 58 5910 -4141 82 5944 dirt replace minecraft:soul_soil
fill -4175 58 5945 -4141 82 5979 dirt replace minecraft:soul_soil
fill -4175 58 5980 -4141 82 6000 dirt replace minecraft:soul_soil
fill -4140 58 5840 -4120 82 5874 dirt replace minecraft:soul_soil
fill -4140 58 5875 -4120 82 5909 dirt replace minecraft:soul_soil
fill -4140 58 5910 -4120 82 5944 dirt replace minecraft:soul_soil
fill -4140 58 5945 -4120 82 5979 dirt replace minecraft:soul_soil
fill -4140 58 5980 -4120 82 6000 dirt replace minecraft:soul_soil

# --- minecraft:soul_sand → dirt ---
fill -4280 58 5840 -4246 82 5874 dirt replace minecraft:soul_sand
fill -4280 58 5875 -4246 82 5909 dirt replace minecraft:soul_sand
fill -4280 58 5910 -4246 82 5944 dirt replace minecraft:soul_sand
fill -4280 58 5945 -4246 82 5979 dirt replace minecraft:soul_sand
fill -4280 58 5980 -4246 82 6000 dirt replace minecraft:soul_sand
fill -4245 58 5840 -4211 82 5874 dirt replace minecraft:soul_sand
fill -4245 58 5875 -4211 82 5909 dirt replace minecraft:soul_sand
fill -4245 58 5910 -4211 82 5944 dirt replace minecraft:soul_sand
fill -4245 58 5945 -4211 82 5979 dirt replace minecraft:soul_sand
fill -4245 58 5980 -4211 82 6000 dirt replace minecraft:soul_sand
fill -4210 58 5840 -4176 82 5874 dirt replace minecraft:soul_sand
fill -4210 58 5875 -4176 82 5909 dirt replace minecraft:soul_sand
fill -4210 58 5910 -4176 82 5944 dirt replace minecraft:soul_sand
fill -4210 58 5945 -4176 82 5979 dirt replace minecraft:soul_sand
fill -4210 58 5980 -4176 82 6000 dirt replace minecraft:soul_sand
fill -4175 58 5840 -4141 82 5874 dirt replace minecraft:soul_sand
fill -4175 58 5875 -4141 82 5909 dirt replace minecraft:soul_sand
fill -4175 58 5910 -4141 82 5944 dirt replace minecraft:soul_sand
fill -4175 58 5945 -4141 82 5979 dirt replace minecraft:soul_sand
fill -4175 58 5980 -4141 82 6000 dirt replace minecraft:soul_sand
fill -4140 58 5840 -4120 82 5874 dirt replace minecraft:soul_sand
fill -4140 58 5875 -4120 82 5909 dirt replace minecraft:soul_sand
fill -4140 58 5910 -4120 82 5944 dirt replace minecraft:soul_sand
fill -4140 58 5945 -4120 82 5979 dirt replace minecraft:soul_sand
fill -4140 58 5980 -4120 82 6000 dirt replace minecraft:soul_sand

# --- minecraft:wither_rose → air ---
fill -4280 58 5840 -4246 82 5874 air replace minecraft:wither_rose
fill -4280 58 5875 -4246 82 5909 air replace minecraft:wither_rose
fill -4280 58 5910 -4246 82 5944 air replace minecraft:wither_rose
fill -4280 58 5945 -4246 82 5979 air replace minecraft:wither_rose
fill -4280 58 5980 -4246 82 6000 air replace minecraft:wither_rose
fill -4245 58 5840 -4211 82 5874 air replace minecraft:wither_rose
fill -4245 58 5875 -4211 82 5909 air replace minecraft:wither_rose
fill -4245 58 5910 -4211 82 5944 air replace minecraft:wither_rose
fill -4245 58 5945 -4211 82 5979 air replace minecraft:wither_rose
fill -4245 58 5980 -4211 82 6000 air replace minecraft:wither_rose
fill -4210 58 5840 -4176 82 5874 air replace minecraft:wither_rose
fill -4210 58 5875 -4176 82 5909 air replace minecraft:wither_rose
fill -4210 58 5910 -4176 82 5944 air replace minecraft:wither_rose
fill -4210 58 5945 -4176 82 5979 air replace minecraft:wither_rose
fill -4210 58 5980 -4176 82 6000 air replace minecraft:wither_rose
fill -4175 58 5840 -4141 82 5874 air replace minecraft:wither_rose
fill -4175 58 5875 -4141 82 5909 air replace minecraft:wither_rose
fill -4175 58 5910 -4141 82 5944 air replace minecraft:wither_rose
fill -4175 58 5945 -4141 82 5979 air replace minecraft:wither_rose
fill -4175 58 5980 -4141 82 6000 air replace minecraft:wither_rose
fill -4140 58 5840 -4120 82 5874 air replace minecraft:wither_rose
fill -4140 58 5875 -4120 82 5909 air replace minecraft:wither_rose
fill -4140 58 5910 -4120 82 5944 air replace minecraft:wither_rose
fill -4140 58 5945 -4120 82 5979 air replace minecraft:wither_rose
fill -4140 58 5980 -4120 82 6000 air replace minecraft:wither_rose

# --- minecraft:soul_fire → air ---
fill -4280 58 5840 -4246 82 5874 air replace minecraft:soul_fire
fill -4280 58 5875 -4246 82 5909 air replace minecraft:soul_fire
fill -4280 58 5910 -4246 82 5944 air replace minecraft:soul_fire
fill -4280 58 5945 -4246 82 5979 air replace minecraft:soul_fire
fill -4280 58 5980 -4246 82 6000 air replace minecraft:soul_fire
fill -4245 58 5840 -4211 82 5874 air replace minecraft:soul_fire
fill -4245 58 5875 -4211 82 5909 air replace minecraft:soul_fire
fill -4245 58 5910 -4211 82 5944 air replace minecraft:soul_fire
fill -4245 58 5945 -4211 82 5979 air replace minecraft:soul_fire
fill -4245 58 5980 -4211 82 6000 air replace minecraft:soul_fire
fill -4210 58 5840 -4176 82 5874 air replace minecraft:soul_fire
fill -4210 58 5875 -4176 82 5909 air replace minecraft:soul_fire
fill -4210 58 5910 -4176 82 5944 air replace minecraft:soul_fire
fill -4210 58 5945 -4176 82 5979 air replace minecraft:soul_fire
fill -4210 58 5980 -4176 82 6000 air replace minecraft:soul_fire
fill -4175 58 5840 -4141 82 5874 air replace minecraft:soul_fire
fill -4175 58 5875 -4141 82 5909 air replace minecraft:soul_fire
fill -4175 58 5910 -4141 82 5944 air replace minecraft:soul_fire
fill -4175 58 5945 -4141 82 5979 air replace minecraft:soul_fire
fill -4175 58 5980 -4141 82 6000 air replace minecraft:soul_fire
fill -4140 58 5840 -4120 82 5874 air replace minecraft:soul_fire
fill -4140 58 5875 -4120 82 5909 air replace minecraft:soul_fire
fill -4140 58 5910 -4120 82 5944 air replace minecraft:soul_fire
fill -4140 58 5945 -4120 82 5979 air replace minecraft:soul_fire
fill -4140 58 5980 -4120 82 6000 air replace minecraft:soul_fire

# --- Les crânes figés ---
kill @e[type=minecraft:wither_skull]

say === FIN v2 ===
