// priority: 0
// ============================================================
//  bmc4_dragons.js — Noter chaque dragon mort (BMC-91)
//
//  Va dans <serveur>/kubejs/server_scripts/.
//
//  La résurrection draconique (rang Draconique et plus, une fois
//  par semaine) passe par le bot : `!resurrection <nom>`. Pour ne
//  ressusciter QUE des dragons morts — jamais un dragon qui dort
//  dans un chunk déchargé, ce qui ferait un double —, la mort est
//  notée ici, au moment où elle arrive :
//
//    storage bmc4:dragons morts : [{Uuid, Proprio, Race, Nom, Quand}]
//
//  Uuid    l'entité morte (le bot retire l'entrée qu'il a servie) ;
//  Proprio l'UUID du propriétaire, en texte ;
//  Race    la valeur de Breed, par exemple « dragonmounts:fire »,
//          celle que `!dragon` met dans son summon ;
//  Nom     le nom donné au dragon, vide s'il n'en a pas ;
//  Quand   l'heure de la mort, en millisecondes.
//
//  Rien d'autre n'est gardé : ni selle, ni armure, ni coffre. Ils
//  sont tombés au sol à la mort ; les rendre serait une duplication.
// ============================================================

EntityEvents.death('dragonmounts:dragon', event => {
  let dragon = event.getEntity()
  let nbt = dragon.getNbt()
  if (nbt == null || !nbt.hasUUID('Owner')) return   // sauvage : rien à ressusciter

  // Le texte SNBT accepte \" et \\, pas les caractères de contrôle.
  let propre = s => JSON.stringify(String(s).replace(/[\u0000-\u001f]/g, ''))
  let nom = dragon.getCustomName() == null ? '' : dragon.getCustomName().getString()

  let entree = '{Uuid:' + propre(dragon.getUUID()) +
    ',Proprio:' + propre(nbt.getUUID('Owner')) +
    ',Race:' + propre(nbt.getString('Breed')) +
    ',Nom:' + propre(nom) +
    ',Quand:' + Date.now() + 'L}'

  let server = dragon.getServer()
  server.runCommandSilent('data modify storage bmc4:dragons morts append value ' + entree)
  // Deux cents morts au plus : la plus ancienne part.
  server.runCommandSilent('execute if data storage bmc4:dragons morts[200] run data remove storage bmc4:dragons morts[0]')
})
