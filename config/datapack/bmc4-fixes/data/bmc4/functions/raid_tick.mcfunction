# Arbitrage du raid, exécuté à chaque tick pendant un créneau.
#
# Pourquoi côté serveur et non dans le bot : la règle des cinq
# minutes doit s'appliquer même si Discord est injoignable ou si
# le bot redémarre au mauvais moment. Un arbitre qui s'absente
# pendant un raid ne sert à rien.

# --- Une mort vient d'arriver ---
# deathCount s'incrémente seul. L'ordre compte : on pose le
# décompte et le mode AVANT de remettre le compteur à zéro,
# sinon la mort est oubliée avant d'être traitée.
execute as @a[scores={bmc4_morts=1..}] run scoreboard players set @s bmc4_spec 6000
execute as @a[scores={bmc4_morts=1..}] run gamemode spectator @s
execute as @a[scores={bmc4_morts=1..}] run scoreboard players set @s bmc4_morts 0

# --- Le décompte tourne ---
execute as @a[scores={bmc4_spec=1..}] run scoreboard players remove @s bmc4_spec 1

# --- Retour en survie ---
execute as @a[scores={bmc4_spec=0},gamemode=spectator] run gamemode survival @s
execute as @a[scores={bmc4_spec=0}] run scoreboard players reset @s bmc4_spec
