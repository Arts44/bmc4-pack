# Créé une seule fois, au chargement du datapack.

# Le tableau de score garde la trace des joueurs déjà servis :
# contrairement à un advancement révoqué, une valeur inscrite ne
# se réinitialise jamais toute seule.
scoreboard objectives add bmc4_kit dummy

# Tous les dragons dans une même équipe, sans tir allié.
#
# Minecraft ignore les représailles entre entités alliées : un
# dragon touché par le souffle d'un autre ne le prendra plus pour
# cible. C'est ce qui provoquait les bagarres en chaîne.
team add bmc4_dragons
team modify bmc4_dragons friendlyFire false
team modify bmc4_dragons seeFriendlyInvisibles true
team modify bmc4_dragons displayName "Dragons"
