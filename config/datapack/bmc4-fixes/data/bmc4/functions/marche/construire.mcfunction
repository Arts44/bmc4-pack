# ============================================================
#  Le Marché Flottant — BMC-09
#
#  Plan validé hors du jeu avant d'exister ici : chaque couche
#  a été relue sur une prévisualisation, pas devinée.
#
#  ⚠️ LA LEÇON DU PREMIER ESSAI
#  `fill ... hollow` sur une région d'UN SEUL bloc de haut ne
#  creuse rien : tous les blocs touchent une face du volume,
#  donc tous comptent comme paroi. Les 625 cases du pont
#  s'étaient remplies de barrières, sans la moindre erreur.
#  Ici, la bordure est faite de huit fill explicites.
#
#  Rejouable tel quel si quelqu'un casse quelque chose.
# ============================================================

# --- Dégager l'emprise ---
fill -21 63 -21 21 70 21 air
fill -21 62 -21 21 62 21 minecraft:water

# --- Le pont, 25x25, avec lattes d'épicéa tous les 4 blocs ---
fill -12 63 -12 12 63 12 minecraft:dark_oak_planks
fill -12 63 -10 12 63 -10 minecraft:spruce_planks
fill -12 63 -6 12 63 -6 minecraft:spruce_planks
fill -12 63 -2 12 63 -2 minecraft:spruce_planks
fill -12 63 2 12 63 2 minecraft:spruce_planks
fill -12 63 6 12 63 6 minecraft:spruce_planks
fill -12 63 10 12 63 10 minecraft:spruce_planks

# --- Pilotis visibles sous la surface ---
setblock -12 62 -12 minecraft:dark_oak_log[axis=y]
setblock -12 62 0 minecraft:dark_oak_log[axis=y]
setblock -12 62 12 minecraft:dark_oak_log[axis=y]
setblock 0 62 -12 minecraft:dark_oak_log[axis=y]
setblock 0 62 12 minecraft:dark_oak_log[axis=y]
setblock 12 62 -12 minecraft:dark_oak_log[axis=y]
setblock 12 62 0 minecraft:dark_oak_log[axis=y]
setblock 12 62 12 minecraft:dark_oak_log[axis=y]

# --- Bordure en dalles basses, coupée aux 4 entrées ---
fill -12 64 -12 -2 64 -12 minecraft:dark_oak_slab[type=bottom]
fill 2 64 -12 12 64 -12 minecraft:dark_oak_slab[type=bottom]
fill -12 64 12 -2 64 12 minecraft:dark_oak_slab[type=bottom]
fill 2 64 12 12 64 12 minecraft:dark_oak_slab[type=bottom]
fill -12 64 -12 -12 64 -2 minecraft:dark_oak_slab[type=bottom]
fill -12 64 2 -12 64 12 minecraft:dark_oak_slab[type=bottom]
fill 12 64 -12 12 64 -2 minecraft:dark_oak_slab[type=bottom]
fill 12 64 2 12 64 12 minecraft:dark_oak_slab[type=bottom]

# --- Les quatre pontons ---
fill 13 63 -1 18 63 1 minecraft:dark_oak_planks
fill -18 63 -1 -13 63 1 minecraft:dark_oak_planks
fill -1 63 13 1 63 18 minecraft:dark_oak_planks
fill -1 63 -18 1 63 -13 minecraft:dark_oak_planks
setblock 18 64 0 minecraft:lantern[hanging=false]
setblock -18 64 0 minecraft:lantern[hanging=false]
setblock 0 64 18 minecraft:lantern[hanging=false]
setblock 0 64 -18 minecraft:lantern[hanging=false]

# --- La place centrale ---
fill -3 63 -3 3 63 3 minecraft:polished_andesite
fill -1 63 -1 1 63 1 minecraft:polished_diorite
setblock -3 64 -3 minecraft:sea_lantern
setblock 3 64 -3 minecraft:sea_lantern
setblock -3 64 3 minecraft:sea_lantern
setblock 3 64 3 minecraft:sea_lantern

# --- Étal Apex, nord-ouest ---
fill -9 64 -9 -9 65 -9 minecraft:spruce_fence
fill -9 64 -5 -9 65 -5 minecraft:spruce_fence
fill -5 64 -9 -5 65 -9 minecraft:spruce_fence
fill -5 64 -5 -5 65 -5 minecraft:spruce_fence
fill -9 66 -9 -5 66 -5 minecraft:red_wool
fill -9 66 -7 -5 66 -7 minecraft:red_stained_glass
fill -5 67 -9 -5 67 -5 minecraft:red_wool
fill -8 64 -9 -6 64 -9 minecraft:spruce_stairs[facing=south]
setblock -7 64 -7 minecraft:barrel[facing=up]
setblock -7 65 -6 minecraft:lantern[hanging=false]

# --- Étal Farmer's, nord-est ---
fill 5 64 -9 5 65 -9 minecraft:spruce_fence
fill 5 64 -5 5 65 -5 minecraft:spruce_fence
fill 9 64 -9 9 65 -9 minecraft:spruce_fence
fill 9 64 -5 9 65 -5 minecraft:spruce_fence
fill 5 66 -9 9 66 -5 minecraft:green_wool
fill 5 66 -7 9 66 -7 minecraft:green_stained_glass
fill 9 67 -9 9 67 -5 minecraft:green_wool
fill 6 64 -9 8 64 -9 minecraft:spruce_stairs[facing=south]
setblock 7 64 -7 minecraft:barrel[facing=up]
setblock 7 65 -6 minecraft:lantern[hanging=false]

# --- Étal Indépendants, sud-ouest ---
fill -9 64 5 -9 65 5 minecraft:spruce_fence
fill -9 64 9 -9 65 9 minecraft:spruce_fence
fill -5 64 5 -5 65 5 minecraft:spruce_fence
fill -5 64 9 -5 65 9 minecraft:spruce_fence
fill -9 66 5 -5 66 9 minecraft:light_blue_wool
fill -9 66 7 -5 66 7 minecraft:light_blue_stained_glass
fill -5 67 5 -5 67 9 minecraft:light_blue_wool
fill -8 64 9 -6 64 9 minecraft:spruce_stairs[facing=north]
setblock -7 64 7 minecraft:barrel[facing=up]
setblock -7 65 6 minecraft:lantern[hanging=false]

# --- Étal libre, sud-est : pour une 4e faction ---
fill 5 64 5 5 65 5 minecraft:spruce_fence
fill 5 64 9 5 65 9 minecraft:spruce_fence
fill 9 64 5 9 65 5 minecraft:spruce_fence
fill 9 64 9 9 65 9 minecraft:spruce_fence
fill 5 66 5 9 66 9 minecraft:white_wool
fill 5 66 7 9 66 7 minecraft:white_stained_glass
fill 9 67 5 9 67 9 minecraft:white_wool
fill 6 64 9 8 64 9 minecraft:spruce_stairs[facing=north]
setblock 7 64 7 minecraft:barrel[facing=up]
setblock 7 65 6 minecraft:lantern[hanging=false]

# --- La waystone, à NOMMER en jeu ---
setblock 0 64 0 waystones:waystone
