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
//
//  LES NOMS JAVA (6 octobre au soir) : seules des formes qui existent au runtime.
//    event.getEntity()          LivingEntityDeathEventJS.java:23
//    dragon.getUuid()           EntityMixin.java:79, @RemapForJS("getUuid")
//    dragon.getNbt()            EntityKJS (kjs$getNbt), un CompoundTag
//    String(nbt)                toString() de Java : le texte SNBT, lu ici
//                               par expressions régulières (aucune méthode
//                               de CompoundTag, dont les noms sont obfusqués)
//    dragon.getServer()         EntityKJS.java:48 (kjs$getServer)
//    server.runCommandSilent()  MinecraftServerKJS.java:64
//  Une erreur ne remonte jamais : elle est écrite une fois au journal.
// ============================================================

let bmc4DragonsErreur = false

// [I;a,b,c,d] → « xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx »
function bmc4UuidDepuisEntiers(texte) {
  let n = texte.split(',').map(x => parseInt(x.trim(), 10))
  if (n.length != 4 || n.some(x => isNaN(x))) return null
  let hex = n.map(x => ('00000000' + (x >>> 0).toString(16)).slice(-8)).join('')
  return hex.slice(0, 8) + '-' + hex.slice(8, 12) + '-' + hex.slice(12, 16) + '-' + hex.slice(16, 20) + '-' + hex.slice(20)
}

// Le texte d'un composant JSON : « {"text":"Ignis"} » → « Ignis ».
function bmc4TexteDuComposant(json) {
  try {
    let c = JSON.parse(json)
    if (typeof c == 'string') return c
    let out = c.text || ''
    if (c.extra) for (let i = 0; i < c.extra.length; i++) out += bmc4TexteDuComposant(JSON.stringify(c.extra[i]))
    return out
  } catch (e) {
    return ''
  }
}

EntityEvents.death('dragonmounts:dragon', event => {
  try {
    let dragon = event.getEntity()
    let snbt = String(dragon.getNbt())
    let owner = snbt.match(/\bOwner:\[I;([^\]]*)\]/)
    if (!owner) return   // sauvage : rien à ressusciter
    let proprio = bmc4UuidDepuisEntiers(owner[1])
    if (!proprio) return
    let breed = snbt.match(/\bBreed:"((?:[^"\\]|\\.)*)"/)
    let custom = snbt.match(/\bCustomName:'((?:[^'\\]|\\.)*)'/) || snbt.match(/\bCustomName:"((?:[^"\\]|\\.)*)"/)
    let nom = custom ? bmc4TexteDuComposant(custom[1].replace(/\\(['"\\])/g, '$1')) : ''

    // Le texte SNBT accepte \" et \\, pas les caractères de contrôle.
    let propre = s => JSON.stringify(String(s).replace(/[\u0000-\u001f]/g, ''))
    let entree = '{Uuid:' + propre(dragon.getUuid()) +
      ',Proprio:' + propre(proprio) +
      ',Race:' + propre(breed ? breed[1] : '') +
      ',Nom:' + propre(nom) +
      ',Quand:' + Date.now() + 'L}'

    let server = dragon.getServer()
    server.runCommandSilent('data modify storage bmc4:dragons morts append value ' + entree)
    // Deux cents morts au plus : la plus ancienne part.
    server.runCommandSilent('execute if data storage bmc4:dragons morts[200] run data remove storage bmc4:dragons morts[0]')
  } catch (e) {
    if (!bmc4DragonsErreur) {
      bmc4DragonsErreur = true
      console.error('bmc4_dragons : mort de dragon non notée : ' + e)
    }
  }
})
