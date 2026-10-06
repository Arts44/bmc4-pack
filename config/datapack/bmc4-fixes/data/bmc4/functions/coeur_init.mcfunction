# BMC-90 — le cœur perdu, version datapack (5 octobre 2026).
#
# Pourquoi : le mod Mediumcore 1.0.0 n'a qu'une règle de jeu globale
# (mediumcoreMode) : impossible de ne viser que les combattants. Pire, son
# soin (balise mediumcore:restores_max_health) ne marche que quand la règle
# est active, donc jamais hors créneau. On ne s'en sert plus : la règle
# reste à false et ce datapack porte la perte, le plancher et le soin.
#
# Les mêmes chiffres que la config du mod : un cœur (2 PV) par mort, plancher
# 6 PV (trois cœurs), plafond 20 PV, un cœur rendu par objet consommé.
# La vie maximale est portée par la VALEUR DE BASE de l'attribut
# generic.max_health, sauvegardée avec le joueur : elle survit à la
# déconnexion, au redémarrage et à la fin du créneau.

# Vie maximale lue à l'instant (copie de travail)
scoreboard objectives add bmc4_hp dummy

# Vie maximale de référence, en PV (20 = dix cœurs). Contrairement à la
# valeur de base de l'attribut, un score survit à la mort (6 octobre).
scoreboard objectives add bmc4_pvmax dummy

# Un compteur « objet consommé » par plat de la balise #farmersdelight:meals
# (37 plats, lus dans l'index des jars le 5 octobre) et pour la Pierre de Soin.
scoreboard objectives add bmc4_repas1 minecraft.used:delightful.cactus_chili
scoreboard objectives add bmc4_repas2 minecraft.used:delightful.cactus_soup
scoreboard objectives add bmc4_repas3 minecraft.used:delightful.coconut_curry
scoreboard objectives add bmc4_repas4 minecraft.used:delightful.field_salad
scoreboard objectives add bmc4_repas5 minecraft.used:delightful.sinigang
scoreboard objectives add bmc4_repas6 minecraft.used:delightful.stuffed_cantaloupe
scoreboard objectives add bmc4_repas7 minecraft.used:delightful.venison_stew
scoreboard objectives add bmc4_repas8 minecraft.used:farmersdelight.bacon_and_eggs
scoreboard objectives add bmc4_repas9 minecraft.used:farmersdelight.baked_cod_stew
scoreboard objectives add bmc4_repas10 minecraft.used:farmersdelight.beef_stew
scoreboard objectives add bmc4_repas11 minecraft.used:farmersdelight.bone_broth
scoreboard objectives add bmc4_repas12 minecraft.used:farmersdelight.chicken_soup
scoreboard objectives add bmc4_repas13 minecraft.used:farmersdelight.cooked_rice
scoreboard objectives add bmc4_repas14 minecraft.used:farmersdelight.fish_stew
scoreboard objectives add bmc4_repas15 minecraft.used:farmersdelight.fried_rice
scoreboard objectives add bmc4_repas16 minecraft.used:farmersdelight.gleaming_salad
scoreboard objectives add bmc4_repas17 minecraft.used:farmersdelight.grilled_salmon
scoreboard objectives add bmc4_repas18 minecraft.used:farmersdelight.honey_glazed_ham
scoreboard objectives add bmc4_repas19 minecraft.used:farmersdelight.mixed_salad
scoreboard objectives add bmc4_repas20 minecraft.used:farmersdelight.mushroom_rice
scoreboard objectives add bmc4_repas21 minecraft.used:farmersdelight.noodle_soup
scoreboard objectives add bmc4_repas22 minecraft.used:farmersdelight.onion_soup
scoreboard objectives add bmc4_repas23 minecraft.used:farmersdelight.pasta_with_meatballs
scoreboard objectives add bmc4_repas24 minecraft.used:farmersdelight.pasta_with_mutton_chop
scoreboard objectives add bmc4_repas25 minecraft.used:farmersdelight.pumpkin_soup
scoreboard objectives add bmc4_repas26 minecraft.used:farmersdelight.ratatouille
scoreboard objectives add bmc4_repas27 minecraft.used:farmersdelight.roast_chicken
scoreboard objectives add bmc4_repas28 minecraft.used:farmersdelight.roasted_mutton_chops
scoreboard objectives add bmc4_repas29 minecraft.used:farmersdelight.shepherds_pie
scoreboard objectives add bmc4_repas30 minecraft.used:farmersdelight.squid_ink_pasta
scoreboard objectives add bmc4_repas31 minecraft.used:farmersdelight.steak_and_potatoes
scoreboard objectives add bmc4_repas32 minecraft.used:farmersdelight.stuffed_pumpkin
scoreboard objectives add bmc4_repas33 minecraft.used:farmersdelight.vegetable_noodles
scoreboard objectives add bmc4_repas34 minecraft.used:farmersdelight.vegetable_soup
scoreboard objectives add bmc4_repas35 minecraft.used:minecraft.beetroot_soup
scoreboard objectives add bmc4_repas36 minecraft.used:minecraft.mushroom_stew
scoreboard objectives add bmc4_repas37 minecraft.used:minecraft.rabbit_stew
scoreboard objectives add bmc4_repas38 minecraft.used:aether.healing_stone
