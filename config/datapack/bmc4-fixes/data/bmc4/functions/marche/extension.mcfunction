# ============================================================
#  Le Marché Flottant — extension
#
#  S'ajoute au hub existant sans rien casser : l'esplanade est
#  posée avec `replace minecraft:water`, donc elle ne remplit
#  que ce qui est encore de l'océan. Le socle, les arches et
#  l'estrade restent intacts.
#
#  ⚠️ Rejouable : relancer cette fonction ne double rien.
# ============================================================

# --- Esplanade 49x49, uniquement sur l'eau ---
fill -24 63 -24 24 63 24 minecraft:light_gray_concrete replace minecraft:water
fill -24 63 -24 24 63 24 minecraft:smooth_quartz replace minecraft:light_gray_concrete

# --- Liseré extérieur en deepslate poli ---
fill -24 63 -24 24 63 -24 minecraft:polished_deepslate
fill -24 63 24 24 63 24 minecraft:polished_deepslate
fill -24 63 -24 -24 63 24 minecraft:polished_deepslate
fill 24 63 -24 24 63 24 minecraft:polished_deepslate

# --- Anneau gris à mi-distance, ponctué de lanternes ---
fill -19 63 -19 19 63 -19 minecraft:light_gray_concrete
fill -19 63 19 19 63 19 minecraft:light_gray_concrete
fill -19 63 -19 -19 63 19 minecraft:light_gray_concrete
fill 19 63 -19 19 63 19 minecraft:light_gray_concrete
setblock -19 63 -19 minecraft:sea_lantern
setblock 19 63 -19 minecraft:sea_lantern
setblock -19 63 19 minecraft:sea_lantern
setblock 19 63 19 minecraft:sea_lantern
setblock 0 63 -19 minecraft:sea_lantern
setblock 0 63 19 minecraft:sea_lantern
setblock -19 63 0 minecraft:sea_lantern
setblock 19 63 0 minecraft:sea_lantern

# --- Pavillon d'angle, Apex ---
fill -20 63 -20 -14 63 -14 minecraft:quartz_block
fill -19 63 -19 -15 63 -15 minecraft:smooth_quartz
fill -20 64 -20 -20 67 -20 minecraft:quartz_pillar[axis=y]
fill -20 64 -14 -20 67 -14 minecraft:quartz_pillar[axis=y]
fill -14 64 -20 -14 67 -20 minecraft:quartz_pillar[axis=y]
fill -14 64 -14 -14 67 -14 minecraft:quartz_pillar[axis=y]
fill -20 68 -20 -14 68 -14 minecraft:red_concrete
fill -19 68 -19 -15 68 -15 minecraft:glass
setblock -17 67 -17 minecraft:sea_lantern
setblock -17 64 -17 minecraft:barrel[facing=up]

# --- Pavillon d'angle, Farmer's ---
fill 14 63 -20 20 63 -14 minecraft:quartz_block
fill 15 63 -19 19 63 -15 minecraft:smooth_quartz
fill 14 64 -20 14 67 -20 minecraft:quartz_pillar[axis=y]
fill 14 64 -14 14 67 -14 minecraft:quartz_pillar[axis=y]
fill 20 64 -20 20 67 -20 minecraft:quartz_pillar[axis=y]
fill 20 64 -14 20 67 -14 minecraft:quartz_pillar[axis=y]
fill 14 68 -20 20 68 -14 minecraft:green_concrete
fill 15 68 -19 19 68 -15 minecraft:glass
setblock 17 67 -17 minecraft:sea_lantern
setblock 17 64 -17 minecraft:barrel[facing=up]

# --- Pavillon d'angle, Indépendants ---
fill -20 63 14 -14 63 20 minecraft:quartz_block
fill -19 63 15 -15 63 19 minecraft:smooth_quartz
fill -20 64 14 -20 67 14 minecraft:quartz_pillar[axis=y]
fill -20 64 20 -20 67 20 minecraft:quartz_pillar[axis=y]
fill -14 64 14 -14 67 14 minecraft:quartz_pillar[axis=y]
fill -14 64 20 -14 67 20 minecraft:quartz_pillar[axis=y]
fill -20 68 14 -14 68 20 minecraft:light_blue_concrete
fill -19 68 15 -15 68 19 minecraft:glass
setblock -17 67 17 minecraft:sea_lantern
setblock -17 64 17 minecraft:barrel[facing=up]

# --- Pavillon d'angle, libre ---
fill 14 63 14 20 63 20 minecraft:quartz_block
fill 15 63 15 19 63 19 minecraft:smooth_quartz
fill 14 64 14 14 67 14 minecraft:quartz_pillar[axis=y]
fill 14 64 20 14 67 20 minecraft:quartz_pillar[axis=y]
fill 20 64 14 20 67 14 minecraft:quartz_pillar[axis=y]
fill 20 64 20 20 67 20 minecraft:quartz_pillar[axis=y]
fill 14 68 14 20 68 20 minecraft:white_concrete
fill 15 68 15 19 68 19 minecraft:glass
setblock 17 67 17 minecraft:sea_lantern
setblock 17 64 17 minecraft:barrel[facing=up]

# --- Pontons prolongés jusqu'à 30 blocs ---
fill 25 63 -2 30 63 2 minecraft:light_gray_concrete replace minecraft:water
fill -30 63 -2 -25 63 2 minecraft:light_gray_concrete replace minecraft:water
fill -2 63 25 2 63 30 minecraft:light_gray_concrete replace minecraft:water
fill -2 63 -30 2 63 -25 minecraft:light_gray_concrete replace minecraft:water
setblock 30 64 0 minecraft:sea_lantern
setblock -30 64 0 minecraft:sea_lantern
setblock 0 64 30 minecraft:sea_lantern
setblock 0 64 -30 minecraft:sea_lantern

# --- Phare central : la waystone se repère de loin ---
fill -1 67 -1 1 71 1 minecraft:quartz_pillar[axis=y] replace minecraft:air
fill 0 67 0 0 71 0 minecraft:air
fill -1 72 -1 1 72 1 minecraft:glass
setblock 0 72 0 minecraft:sea_lantern
fill -1 73 -1 1 73 1 minecraft:chiseled_quartz_block
setblock 0 74 0 minecraft:sea_lantern

# --- Bancs autour de l'estrade ---
fill -6 64 -4 -6 64 4 minecraft:quartz_stairs[facing=east]
fill 6 64 -4 6 64 4 minecraft:quartz_stairs[facing=west]
fill -4 64 -6 4 64 -6 minecraft:quartz_stairs[facing=south]
fill -4 64 6 4 64 6 minecraft:quartz_stairs[facing=north]

# --- Jardinières aux quatre axes ---
fill -9 64 -1 -7 64 1 minecraft:smooth_quartz_slab[type=top]
setblock -8 64 0 minecraft:mangrove_leaves[persistent=true]
fill 7 64 -1 9 64 1 minecraft:smooth_quartz_slab[type=top]
setblock 8 64 0 minecraft:mangrove_leaves[persistent=true]
fill -1 64 -9 1 64 -7 minecraft:smooth_quartz_slab[type=top]
setblock 0 64 -8 minecraft:mangrove_leaves[persistent=true]
fill -1 64 7 1 64 9 minecraft:smooth_quartz_slab[type=top]
setblock 0 64 8 minecraft:mangrove_leaves[persistent=true]
