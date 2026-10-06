# ============================================================
#  Le Marché Flottant — BMC-09
#
#  Au point zéro, en pleine mer. Deuxième zone neutre du
#  serveur : ni PvP, ni piège, ni vol, et aucun claim.
#
#  La structure le dit d'elle-même : quatre étals aux couleurs
#  des trois camps plus un neutre, une place centrale ouverte,
#  et quatre pontons qui arrivent des quatre directions — aucun
#  camp n'a « son » côté.
#
#  ⚠️ Chaque fill reste sous 32 768 blocs. La limite est un
#  échec SILENCIEUX : la commande ne fait rien et ne dit rien.
#  Le plus gros bloc ici fait 25×25 = 625.
# ============================================================

# --- Dégager l'eau et l'air au-dessus de la zone ---
fill -14 63 -14 14 70 14 air replace water

# --- Le pont principal, 25×25 ---
fill -12 63 -12 12 63 12 minecraft:dark_oak_planks

# --- Bordure de rondins, pour la silhouette vue de loin ---
fill -12 64 -12 12 64 12 minecraft:spruce_fence hollow

# --- Quatre ouvertures, une par direction ---
fill 12 64 -1 12 64 1 air
fill -12 64 -1 -12 64 1 air
fill -1 64 12 1 64 12 air
fill -1 64 -12 1 64 -12 air

# --- Les quatre pontons, vers le large ---
fill 13 63 -1 19 63 1 minecraft:dark_oak_planks
fill -19 63 -1 -13 63 1 minecraft:dark_oak_planks
fill -1 63 13 1 63 19 minecraft:dark_oak_planks
fill -1 63 -19 1 63 -13 minecraft:dark_oak_planks

# --- Place centrale, en pierre polie ---
fill -3 63 -3 3 63 3 minecraft:polished_andesite
fill -1 63 -1 1 63 1 minecraft:polished_diorite

# --- Éclairage de la place ---
setblock -3 64 -3 minecraft:sea_lantern
setblock 3 64 -3 minecraft:sea_lantern
setblock -3 64 3 minecraft:sea_lantern
setblock 3 64 3 minecraft:sea_lantern
