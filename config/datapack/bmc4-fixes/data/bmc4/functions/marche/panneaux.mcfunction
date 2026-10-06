# ============================================================
#  Le Marché Flottant — la signalétique
#
#  Quatre panneaux, un par ponton, pour que la règle soit lue
#  en arrivant plutôt que citée après coup. C'est une zone
#  neutre sans protection technique : le texte EST la
#  protection.
#
#  ⚠️ Les panneaux 1.20 veulent front_text/messages, avec des
#  composants JSON échappés. Un guillemet mal placé et le bloc
#  se pose vide, sans erreur.
# ============================================================

# --- Ponton est ---
setblock 19 64 0 minecraft:spruce_sign{front_text:{messages:['{"text":"MARCHÉ FLOTTANT","bold":true}','{"text":"Zone neutre"}','{"text":"Ni PvP ni vol"}','{"text":"50 blocs autour"}']}}

# --- Ponton ouest ---
setblock -19 64 0 minecraft:spruce_sign{front_text:{messages:['{"text":"MARCHÉ FLOTTANT","bold":true}','{"text":"Zone neutre"}','{"text":"Ni PvP ni vol"}','{"text":"50 blocs autour"}']}}

# --- Ponton sud ---
setblock 0 64 19 minecraft:spruce_sign{front_text:{messages:['{"text":"MARCHÉ FLOTTANT","bold":true}','{"text":"Zone neutre"}','{"text":"Ni PvP ni vol"}','{"text":"50 blocs autour"}']}}

# --- Ponton nord ---
setblock 0 64 -19 minecraft:spruce_sign{front_text:{messages:['{"text":"MARCHÉ FLOTTANT","bold":true}','{"text":"Zone neutre"}','{"text":"Ni PvP ni vol"}','{"text":"50 blocs autour"}']}}

# --- Les quatre étals, nommés ---
setblock -7 65 -7 minecraft:spruce_wall_sign[facing=south]{front_text:{messages:['{"text":""}','{"text":"APEX","color":"red","bold":true}','{"text":"étal libre"}','{"text":""}']}}
setblock 7 65 -7 minecraft:spruce_wall_sign[facing=south]{front_text:{messages:['{"text":""}','{"text":"FARMERS","color":"green","bold":true}','{"text":"étal libre"}','{"text":""}']}}
setblock -7 65 7 minecraft:spruce_wall_sign[facing=north]{front_text:{messages:['{"text":""}','{"text":"INDÉPENDANTS","color":"aqua","bold":true}','{"text":"étal libre"}','{"text":""}']}}
setblock 7 65 7 minecraft:spruce_wall_sign[facing=north]{front_text:{messages:['{"text":""}','{"text":"ÉTAL LIBRE","bold":true}','{"text":"pour une faction"}','{"text":"à venir"}']}}
