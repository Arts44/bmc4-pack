# ============================================================
#  Le Marché Flottant — passe déco moddée
#
#  Additive : n'écrit QUE sur des positions que j'ai posées
#  moi-même (sommets d'arches, pavillons, bouts de pontons,
#  jardinières). Rien de ce qui a été bâti à la main n'est
#  touché.
#
#  ⚠️ Les quatre identifiants ci-dessous ont été testés sur le
#  serveur par summon avant d'être écrits ici. Deux candidats
#  ont été écartés parce qu'ils renvoyaient « Air » :
#  galosphere:silver_lantern et pfm:white_kitchen_counter.
# ============================================================

# --- Lumiere de Galosphere : une lumière bleutée que le
#     vanilla n'a pas. Remplace les lanternes marines de
#     l'anneau, gardées ailleurs pour le contraste.
setblock -19 63 -19 galosphere:lumiere_block
setblock 19 63 -19 galosphere:lumiere_block
setblock -19 63 19 galosphere:lumiere_block
setblock 19 63 19 galosphere:lumiere_block
setblock 0 63 -19 galosphere:lumiere_block
setblock 0 63 19 galosphere:lumiere_block
setblock -19 63 0 galosphere:lumiere_block
setblock 19 63 0 galosphere:lumiere_block

# --- Phare : lumiere au sommet, visible de très loin ---
setblock 0 74 0 galosphere:lumiere_block
setblock 0 72 0 galosphere:lumiere_block

# --- Drapeaux de faction sur les pavillons d'angle ---
setblock -17 65 -20 supplementaries:flag_red
setblock 17 65 -20 supplementaries:flag_green
setblock -17 65 20 supplementaries:flag_light_blue
setblock 17 65 20 supplementaries:flag_white

# --- Bougeoirs autour de l'estrade : une lumière chaude qui
#     casse le froid du quartz.
setblock -6 65 0 supplementaries:candle_holder
setblock 6 65 0 supplementaries:candle_holder
setblock 0 65 -6 supplementaries:candle_holder
setblock 0 65 6 supplementaries:candle_holder

# --- Bandeau de bois d'écho : la touche sombre qui donne du
#     relief au tout-quartz. Deeper and Darker, gris-bleu.
fill -24 63 -22 24 63 -22 deeperdarker:echo_planks replace minecraft:smooth_quartz
fill -24 63 22 24 63 22 deeperdarker:echo_planks replace minecraft:smooth_quartz
fill -22 63 -24 -22 63 24 deeperdarker:echo_planks replace minecraft:smooth_quartz
fill 22 63 -24 22 63 24 deeperdarker:echo_planks replace minecraft:smooth_quartz

# --- Bouts de pontons en bois d'écho ---
fill 28 63 -2 30 63 2 deeperdarker:echo_planks replace minecraft:light_gray_concrete
fill -30 63 -2 -28 63 2 deeperdarker:echo_planks replace minecraft:light_gray_concrete
fill -2 63 28 2 63 30 deeperdarker:echo_planks replace minecraft:light_gray_concrete
fill -2 63 -30 2 63 -28 deeperdarker:echo_planks replace minecraft:light_gray_concrete

# --- Bougeoirs au bout de chaque ponton ---
setblock 30 64 0 supplementaries:candle_holder
setblock -30 64 0 supplementaries:candle_holder
setblock 0 64 30 supplementaries:candle_holder
setblock 0 64 -30 supplementaries:candle_holder
