// priority: 0
// ============================================================
//  bmc4_v64_retraits.js — Ce que la v64 retire du jeu (BMC-101)
//
//  Va dans <serveur>/kubejs/server_scripts/. Pris en compte par /reload :
//  les recettes se rechargent avec les datapacks (« kubejs reload
//  server_scripts » ne recharge pas les recettes).
//
//  Décisions d'Arthur du 11 octobre :
//
//  railways:crafting/remote_lens — la Lentille à distance de Steam 'n'
//    Rails. Liée à un conducteur qui porte des lunettes d'ingénieur, elle
//    montre ce qu'il voit à n'importe quelle distance dans la dimension, le
//    fait marcher et actionner boutons, trappes et leviers : l'intérieur des
//    bases. Aucune option du mod ne la coupe. Seule source dans le pack
//    (les 399 jars de la v64 passés au crible, données et classes, le
//    11 octobre) : cette recette d'établi. Ni loot, ni échange de
//    villageois, ni autre recette.
//
//  kaleidoscope_tavern:barrel/molotov — le Molotov Cocktail de Kaleidoscope
//    Tavern (lave seule dans le tonneau). Seule source : cette recette ; la
//    table de loot du mod ne rend que le bloc déjà posé. Le tonneau cherche
//    ses recettes dans le RecipeManager (BarrelBlockEntity :
//    RecipeManager.createCheck sur ModRecipes.BARREL_RECIPE), le retrait
//    par identifiant suffit.
//
//  Aucune méthode Java : l'événement des recettes de KubeJS et un filtre
//  par identifiant (règle 8 du contrôle sans objet).
// ============================================================

const BMC4_RECETTES_RETIREES = [
  'railways:crafting/remote_lens',
  'kaleidoscope_tavern:barrel/molotov',
]

ServerEvents.recipes(event => {
  BMC4_RECETTES_RETIREES.forEach(id => event.remove({ id: id }))
})
