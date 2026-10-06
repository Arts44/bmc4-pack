# ============================================================
#  Le Marché Flottant — version hub moderne
#
#  Inspiré des spawns « 4 portals » : palette claire, symétrie
#  stricte, une arche par point cardinal. Ici les quatre arches
#  portent les couleurs des camps.
#
#    nord   rouge        ⚔️ Apex
#    est    vert         🌾 Farmer's
#    sud    bleu clair   🧭 Indépendants
#    ouest  blanc        libre, pour une faction à venir
#
#  ⚠️ Aucun `fill ... hollow` : sur une couche plate il remplit
#  tout au lieu de creuser. Chaque bordure est faite de quatre
#  fill explicites, coupés aux entrées.
# ============================================================

# --- Table rase sur l'ancienne version ---
fill -21 63 -21 21 75 21 air
fill -21 62 -21 21 62 21 minecraft:water

# --- Socle : 29x29 en quartz lisse, bord gris ---
fill -14 63 -14 14 63 14 minecraft:smooth_quartz
fill -14 63 -14 14 63 -14 minecraft:light_gray_concrete
fill -14 63 14 14 63 14 minecraft:light_gray_concrete
fill -14 63 -14 -14 63 14 minecraft:light_gray_concrete
fill 14 63 -14 14 63 14 minecraft:light_gray_concrete

# --- Bandes lumineuses encastrées, en croix ---
fill -13 63 -1 13 63 -1 minecraft:sea_lantern
fill -13 63 1 13 63 1 minecraft:sea_lantern
fill -1 63 -13 -1 63 13 minecraft:sea_lantern
fill 1 63 -13 1 63 13 minecraft:sea_lantern
fill -13 63 0 13 63 0 minecraft:smooth_quartz
fill 0 63 -13 0 63 13 minecraft:smooth_quartz

# --- Pilotis sous le socle ---
fill -13 58 -13 -13 62 -13 minecraft:polished_deepslate
fill -13 58 0 -13 62 0 minecraft:polished_deepslate
fill -13 58 13 -13 62 13 minecraft:polished_deepslate
fill 0 58 -13 0 62 -13 minecraft:polished_deepslate
fill 0 58 13 0 62 13 minecraft:polished_deepslate
fill 13 58 -13 13 62 -13 minecraft:polished_deepslate
fill 13 58 0 13 62 0 minecraft:polished_deepslate
fill 13 58 13 13 62 13 minecraft:polished_deepslate

# --- Garde-corps en vitre, coupé aux 4 entrées ---
fill -14 64 -14 -3 64 -14 minecraft:glass_pane
fill 3 64 -14 14 64 -14 minecraft:glass_pane
fill -14 64 14 -3 64 14 minecraft:glass_pane
fill 3 64 14 14 64 14 minecraft:glass_pane
fill -14 64 -14 -14 64 -3 minecraft:glass_pane
fill -14 64 3 -14 64 14 minecraft:glass_pane
fill 14 64 -14 14 64 -3 minecraft:glass_pane
fill 14 64 3 14 64 14 minecraft:glass_pane

# --- Arche nord, Apex ---
fill -3 64 -14 -3 68 -14 minecraft:quartz_pillar[axis=y]
fill 3 64 -14 3 68 -14 minecraft:quartz_pillar[axis=y]
fill -3 69 -14 3 69 -14 minecraft:red_concrete
fill -2 68 -14 2 68 -14 minecraft:red_concrete
fill -1 67 -14 1 67 -14 minecraft:glass
setblock -3 70 -14 minecraft:sea_lantern
setblock 3 70 -14 minecraft:sea_lantern

# --- Arche est, Farmer's ---
fill 14 64 -3 14 68 -3 minecraft:quartz_pillar[axis=y]
fill 14 64 3 14 68 3 minecraft:quartz_pillar[axis=y]
fill 14 69 -3 14 69 3 minecraft:green_concrete
fill 14 68 -2 14 68 2 minecraft:green_concrete
fill 14 67 -1 14 67 1 minecraft:glass
setblock 14 70 -3 minecraft:sea_lantern
setblock 14 70 3 minecraft:sea_lantern

# --- Arche sud, Indépendants ---
fill -3 64 14 -3 68 14 minecraft:quartz_pillar[axis=y]
fill 3 64 14 3 68 14 minecraft:quartz_pillar[axis=y]
fill -3 69 14 3 69 14 minecraft:light_blue_concrete
fill -2 68 14 2 68 14 minecraft:light_blue_concrete
fill -1 67 14 1 67 14 minecraft:glass
setblock -3 70 14 minecraft:sea_lantern
setblock 3 70 14 minecraft:sea_lantern

# --- Arche ouest, libre ---
fill -14 64 -3 -14 68 -3 minecraft:quartz_pillar[axis=y]
fill -14 64 3 -14 68 3 minecraft:quartz_pillar[axis=y]
fill -14 69 -3 -14 69 3 minecraft:white_concrete
fill -14 68 -2 -14 68 2 minecraft:white_concrete
fill -14 67 -1 -14 67 1 minecraft:glass
setblock -14 70 -3 minecraft:sea_lantern
setblock -14 70 3 minecraft:sea_lantern

# --- Les quatre pontons vers le large ---
fill 15 63 -2 20 63 2 minecraft:light_gray_concrete
fill -20 63 -2 -15 63 2 minecraft:light_gray_concrete
fill -2 63 15 2 63 20 minecraft:light_gray_concrete
fill -2 63 -20 2 63 -15 minecraft:light_gray_concrete

# --- Le cœur : estrade en gradins et waystone ---
fill -5 63 -5 5 63 5 minecraft:quartz_block
fill -4 64 -4 4 64 4 minecraft:smooth_quartz
fill -2 65 -2 2 65 2 minecraft:chiseled_quartz_block
fill -4 64 -4 4 64 -4 minecraft:smooth_quartz_slab[type=top]
fill -4 64 4 4 64 4 minecraft:smooth_quartz_slab[type=top]
fill -4 64 -4 -4 64 4 minecraft:smooth_quartz_slab[type=top]
fill 4 64 -4 4 64 4 minecraft:smooth_quartz_slab[type=top]
setblock 0 66 0 waystones:waystone
setblock -2 66 -2 minecraft:sea_lantern
setblock 2 66 -2 minecraft:sea_lantern
setblock -2 66 2 minecraft:sea_lantern
setblock 2 66 2 minecraft:sea_lantern

# --- Quatre comptoirs d'échange, aux angles ---
fill -11 64 -11 -7 64 -7 minecraft:red_concrete
fill -10 64 -10 -8 64 -8 minecraft:smooth_quartz
setblock -9 64 -9 minecraft:barrel[facing=up]
setblock -9 65 -9 minecraft:lantern[hanging=false]
fill 7 64 -11 11 64 -7 minecraft:green_concrete
fill 8 64 -10 10 64 -8 minecraft:smooth_quartz
setblock 9 64 -9 minecraft:barrel[facing=up]
setblock 9 65 -9 minecraft:lantern[hanging=false]
fill -11 64 7 -7 64 11 minecraft:light_blue_concrete
fill -10 64 8 -8 64 10 minecraft:smooth_quartz
setblock -9 64 9 minecraft:barrel[facing=up]
setblock -9 65 9 minecraft:lantern[hanging=false]
fill 7 64 7 11 64 11 minecraft:white_concrete
fill 8 64 8 10 64 10 minecraft:smooth_quartz
setblock 9 64 9 minecraft:barrel[facing=up]
setblock 9 65 9 minecraft:lantern[hanging=false]
