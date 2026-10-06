# ============================================================
#  Le Marché Flottant — correction du 24 septembre
#
#  ⚠️ LA LEÇON : `fill ... hollow` sur une région d'UN SEUL bloc
#  de haut ne creuse rien. Tous les blocs touchent une face du
#  volume, donc tous comptent comme paroi — les 625 cases se
#  sont remplies de barrières au lieu de former un contour.
#
#  Pour un contour plat, il faut quatre fill de bordure, pas un
#  fill hollow.
# ============================================================

# --- Retirer les barrières de l'intérieur, garder le contour ---
fill -11 64 -11 11 64 11 air replace minecraft:spruce_fence

# --- Les quatre montants de chaque étal, effacés au passage ---
setblock -9 64 -9 minecraft:spruce_fence
setblock -5 64 -9 minecraft:spruce_fence
setblock -9 64 -5 minecraft:spruce_fence
setblock -5 64 -5 minecraft:spruce_fence

setblock 9 64 -9 minecraft:spruce_fence
setblock 5 64 -9 minecraft:spruce_fence
setblock 9 64 -5 minecraft:spruce_fence
setblock 5 64 -5 minecraft:spruce_fence

setblock -9 64 9 minecraft:spruce_fence
setblock -5 64 9 minecraft:spruce_fence
setblock -9 64 5 minecraft:spruce_fence
setblock -5 64 5 minecraft:spruce_fence

setblock 9 64 9 minecraft:spruce_fence
setblock 5 64 9 minecraft:spruce_fence
setblock 9 64 5 minecraft:spruce_fence
setblock 5 64 5 minecraft:spruce_fence

# --- Les comptoirs, en escaliers tournés vers le centre ---
fill -8 64 -6 -6 64 -6 minecraft:spruce_stairs[facing=south]
fill 6 64 -6 8 64 -6 minecraft:spruce_stairs[facing=south]
fill -8 64 6 -6 64 6 minecraft:spruce_stairs[facing=north]
fill 6 64 6 8 64 6 minecraft:spruce_stairs[facing=north]

# --- Une lanterne suspendue sous chaque toile ---
setblock -7 64 -8 minecraft:lantern[hanging=false]
setblock 7 64 -8 minecraft:lantern[hanging=false]
setblock -7 64 8 minecraft:lantern[hanging=false]
setblock 7 64 8 minecraft:lantern[hanging=false]
