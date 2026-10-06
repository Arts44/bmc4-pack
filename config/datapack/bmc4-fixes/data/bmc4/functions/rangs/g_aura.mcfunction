# Généré par config/rangs/generer.py depuis config/rangs/rangs.toml : ne pas
# modifier à la main.

# Les auras, toutes les 10 ticks. Rien pour un spectateur ni un invisible.

execute as @a[scores={bmc4_aura_choix=1},gamemode=!spectator] unless entity @s[nbt={ActiveEffects:[{Id:14}]}] at @s run particle minecraft:enchant ~ ~1 ~ 0.4 0.6 0.4 0.4 6
execute as @a[scores={bmc4_aura_choix=2},gamemode=!spectator] unless entity @s[nbt={ActiveEffects:[{Id:14}]}] at @s run particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.01 2
execute as @a[scores={bmc4_aura_choix=3},gamemode=!spectator] unless entity @s[nbt={ActiveEffects:[{Id:14}]}] at @s run particle minecraft:soul_fire_flame ~ ~0.2 ~ 0.3 0.1 0.3 0.01 2
execute as @a[scores={bmc4_aura_choix=4},gamemode=!spectator] unless entity @s[nbt={ActiveEffects:[{Id:14}]}] at @s run particle minecraft:cherry_leaves ~ ~1.8 ~ 0.4 0.2 0.4 0 2
execute as @a[scores={bmc4_aura_choix=5},gamemode=!spectator] unless entity @s[nbt={ActiveEffects:[{Id:14}]}] at @s run particle minecraft:glow ~ ~1 ~ 0.4 0.6 0.4 0 2
execute as @a[scores={bmc4_aura_choix=6},gamemode=!spectator] unless entity @s[nbt={ActiveEffects:[{Id:14}]}] at @s run particle minecraft:note ~ ~2.2 ~ 0.3 0 0.3 1 1
execute as @a[scores={bmc4_aura_choix=7},gamemode=!spectator] unless entity @s[nbt={ActiveEffects:[{Id:14}]}] at @s run particle minecraft:dust 1.0 0.85 0.3 1.0 ~ ~2.1 ~ 0.25 0 0.25 0 4
