# ============================================================
#  Le Marché Flottant — les quatre étals
#
#  Un étal par camp, placés aux quatre coins, à distance égale
#  du centre. Les couleurs reprennent celles des rôles Discord :
#
#    rouge      ⚔️ Apex
#    vert       🌾 Farmer's
#    bleu clair 🧭 Indépendants
#    blanc      libre — pour une faction à venir
#
#  ⚠️ Le blanc n'est pas décoratif : le jour où une quatrième
#  faction se crée, elle a déjà sa place. C'est plus simple que
#  de redessiner le marché à ce moment-là.
# ============================================================

# --- Étal Apex, nord-ouest ---
fill -9 64 -9 -5 64 -9 minecraft:spruce_fence
fill -9 64 -9 -9 64 -5 minecraft:spruce_fence
fill -9 65 -9 -5 65 -5 minecraft:red_wool
fill -8 64 -8 -6 64 -6 air
fill -8 63 -8 -6 63 -6 minecraft:spruce_planks
setblock -7 64 -7 minecraft:barrel

# --- Étal Farmer's, nord-est ---
fill 5 64 -9 9 64 -9 minecraft:spruce_fence
fill 9 64 -9 9 64 -5 minecraft:spruce_fence
fill 5 65 -9 9 65 -5 minecraft:green_wool
fill 6 64 -8 8 64 -6 air
fill 6 63 -8 8 63 -6 minecraft:spruce_planks
setblock 7 64 -7 minecraft:barrel

# --- Étal des indépendants, sud-ouest ---
fill -9 64 5 -5 64 5 minecraft:spruce_fence
fill -9 64 5 -9 64 9 minecraft:spruce_fence
fill -9 65 5 -5 65 9 minecraft:light_blue_wool
fill -8 64 6 -6 64 8 air
fill -8 63 6 -6 63 8 minecraft:spruce_planks
setblock -7 64 7 minecraft:barrel

# --- Étal libre, sud-est ---
fill 5 64 9 9 64 9 minecraft:spruce_fence
fill 9 64 5 9 64 9 minecraft:spruce_fence
fill 5 65 5 9 65 9 minecraft:white_wool
fill 6 64 6 8 64 8 air
fill 6 63 6 8 63 8 minecraft:spruce_planks
setblock 7 64 7 minecraft:barrel

# --- Une lanterne par étal ---
setblock -9 65 -5 minecraft:lantern
setblock 9 65 -5 minecraft:lantern
setblock -9 65 5 minecraft:lantern
setblock 9 65 5 minecraft:lantern
