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

# Le cœur perdu (BMC-90)
function bmc4:coeur_init

# L'arbitrage des raids : compteurs, équipe, numéros de joueur.
# Toutes ses commandes sont sans effet si l'objet existe déjà.
function bmc4:raid_init
