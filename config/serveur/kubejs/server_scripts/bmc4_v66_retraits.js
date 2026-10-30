// priority: 0
// ============================================================
//  bmc4_v66_retraits.js — Ce que la v66 retire de Refurbished (BMC-106)
//
//  Va dans <serveur>/kubejs/server_scripts/. Pris en compte par /reload :
//  les recettes se rechargent avec les datapacks (« kubejs reload
//  server_scripts » ne recharge pas les recettes).
//
//  Décisions d'Arthur du 30 octobre :
//
//  refurbished_furniture:wrench — la clé de câblage. Elle relie deux nœuds
//    jusqu'à 512 blocs, à travers les claims, et coupe les liens adverses
//    (WrenchItem.use et MessageDeleteLink passent à côté de FTB Chunks et de
//    la garde). Sans clé, le serveur tourne avec
//    electricity.cheats.everythingIsPowered = true.
//
//  refurbished_furniture:constructing/computer — l'ordinateur et son Home
//    Control, qui bascule à distance les appareils d'un réseau.
//
//  refurbished_furniture:television_remote — la télécommande, 16 blocs à
//    travers les claims.
//
//  Les 30 recettes des ventilateurs de plafond (20 de l'établi du mod, 10 de
//  teinture). Avec everythingIsPowered, ils tournent sans interrupteur et
//  performDamage frappe tout ce qui est dans leur zone, 0,5 par coup.
//
//  Seules sources dans le pack (les jars de l'instance v66 passés au crible,
//  données, structures et classes, le 30 octobre) : ces recettes. Ni loot
//  hors du bloc lui-même, ni échange de villageois, ni autre recette ; le
//  module Refurbished d'Every Compat est coupé (everycomp-hazardous.toml).
//
//  Aucune méthode Java : l'événement des recettes de KubeJS et un filtre
//  par identifiant (règle 8 du contrôle sans objet).
// ============================================================

const BMC4_RECETTES_RETIREES_V66 = [
  'refurbished_furniture:wrench',
  'refurbished_furniture:constructing/computer',
  'refurbished_furniture:television_remote',
]

const BMC4_BOIS_VENTILATEURS = ['oak', 'spruce', 'birch', 'jungle', 'acacia', 'dark_oak',
  'mangrove', 'cherry', 'crimson', 'warped']

BMC4_BOIS_VENTILATEURS.forEach(bois => {
  BMC4_RECETTES_RETIREES_V66.push('refurbished_furniture:' + bois + '_dark_ceiling_fan')
  BMC4_RECETTES_RETIREES_V66.push('refurbished_furniture:constructing/' + bois + '_dark_ceiling_fan')
  BMC4_RECETTES_RETIREES_V66.push('refurbished_furniture:constructing/' + bois + '_light_ceiling_fan')
})

ServerEvents.recipes(event => {
  BMC4_RECETTES_RETIREES_V66.forEach(id => event.remove({ id: id }))
})
