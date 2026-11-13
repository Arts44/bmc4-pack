// BMC-107 — Tests hors jeu de la règle des coffres (bmc4_garde.js) et de
// l'écouteur Forge des objets en recharge (bmc4_coffres_recharge.js).
//
//   node --test quetes/tests/
//
// Les deux scripts sont exécutés tels quels dans un contexte node:vm, avec de
// FAUX objets à la place de KubeJS, de Forge, de FTB Chunks et de Minecraft.
// Ce qui est testé : la logique des scripts (refuser ou autoriser, un seul
// message, le délai d'une seconde, fail-closed, ce que l'écouteur touche sur
// l'événement). Ce qui ne l'est PAS : KubeJS, Rhino (noms Java, ClassFilter),
// l'ordre réel des écouteurs de Forge, FTB Chunks. L'ordre est simulé par
// clic() d'après le bytecode : Architectury (KubeJS) en HIGH, saute le clic
// si l'objet est en recharge ; l'écouteur de démarrage en NORMAL, sans les
// événements annulés.
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import vm from 'node:vm'

const RACINE = new URL('../../config/serveur/kubejs/', import.meta.url)
const GARDE = readFileSync(new URL('server_scripts/bmc4_garde.js', RACINE), 'utf8')
const RECHARGE = readFileSync(new URL('startup_scripts/bmc4_coffres_recharge.js', RACINE), 'utf8')
const EVENEMENT = 'net.minecraftforge.event.entity.player.PlayerInteractEvent$RightClickBlock'

class EventExit extends Error {}

// ------------------------------------------------------------------
//  Un faux monde : deux factions, un raid, des blocs, une horloge.
// ------------------------------------------------------------------
function monde() {
  const m = {
    t: 1_000_000,
    messages: [],          // { a, texte }
    journal: [],
    chunksLus: 0,
    raid: new Set(),       // pseudos de l'équipe bmc4_raid_actif
    blocs: {},             // 'x,y,z' -> { id, be, tags }
    claims: {},            // 'cx,cz' -> équipe
    equipes: {},
    joueurs: {},
    listeners: {},
    kubejsClic: null,
    global: {},
    niveauCasse: false,
  }
  const uuid = s => ({ toString: () => s })
  const pos = (x, y, z) => ({ x, y, z, toString: () => `BlockPos{x=${x}, y=${y}, z=${z}}` })
  m.pos = pos

  m.equipe = (nom, membres, allies = []) => {
    m.equipes[nom] = {
      nom, membres, allies,
      isServerTeam: () => false,
      getProperty: () => nom,
      getRankForPlayer: u => ({ isAllyOrBetter: () => membres.includes(String(u)) || allies.includes(String(u)) }),
      getMembers: () => ({ toArray: () => membres.map(uuid) }),
    }
    return m.equipes[nom]
  }
  m.claim = (cx, cz, nom) => { m.claims[cx + ',' + cz] = m.equipes[nom] }
  m.bloc = (p, id, be, tags = []) => { m.blocs[`${p.x},${p.y},${p.z}`] = { id, be, tags } }

  const server = {
    runCommandSilent: cmd => {
      const r = /^tellraw (\S+) (.*)$/.exec(cmd)
      if (r) m.messages.push({ a: r[1], texte: JSON.parse(r[2]).map(x => (typeof x === 'string' ? x : x.text)).join('') })
      return 1
    },
    getScoreboard: () => ({
      getPlayerTeam: n => (n === 'bmc4_raid_actif' && m.raid.size ? { getPlayers: () => ({ contains: p => m.raid.has(String(p)) }) } : null),
    }),
  }
  const niveau = {
    getDimensionKey: () => 'minecraft:overworld',
    isClientSide: () => false,
    getBlock: p => {
      if (m.niveauCasse) throw new Error('getBlock indisponible')
      const b = m.blocs[`${p.x},${p.y},${p.z}`] || { id: 'minecraft:air', be: false, tags: [] }
      return {
        getEntity: () => (b.be ? {} : null),
        getId: () => b.id,
        hasTag: t => b.tags.includes(t),
        getLevel: () => niveau,
        getPos: () => p,
      }
    },
    getBlockEntity: p => ((m.blocs[`${p.x},${p.y},${p.z}`] || {}).be ? {} : null),
  }
  m.niveau = niveau
  m.joueur = (nom, u) => {
    m.joueurs[nom] = {
      getUuid: () => uuid(u),
      getUsername: () => nom,
      getServer: () => server,
      getLevel: () => niveau,
      isPlayer: () => true,
      isOnScoreboardTeam: t => t === 'bmc4_raid_actif' && m.raid.has(nom),
      tell: c => m.messages.push({ a: nom, texte: String(c.rouge) }),
    }
    return m.joueurs[nom]
  }

  const classes = {
    'dev.ftb.mods.ftbchunks.api.FTBChunksAPI': {
      api: () => ({ getManager: () => ({ getChunk: cdp => {
        m.chunksLus++
        const e = m.claims[cdp.cp.x + ',' + cdp.cp.z]
        if (!e) return null
        return { getTeamData: () => ({ getTeam: () => e, isTeamMember: u => e.membres.includes(String(u)) }) }
      } }) }),
    },
    'dev.ftb.mods.ftblibrary.math.ChunkDimPos': function (dim, cp) { this.dim = dim; this.cp = cp },
    'net.minecraft.world.level.ChunkPos': function (p) { this.x = p.x >> 4; this.z = p.z >> 4 },
    'dev.ftb.mods.ftbteams.api.property.TeamProperties': { DISPLAY_NAME: 'DISPLAY_NAME' },
  }
  // Deux portées, comme KubeJS : une pour les scripts de démarrage, une neuve
  // pour les scripts serveur à chaque chargement (/reload). Seul `global` est commun.
  const fabrique = () => ({
    Java: { loadClass: n => classes[n] || {} },
    ServerEvents: { command() {}, tick() {}, commandRegistry() {} },
    EntityEvents: { hurt() {} },
    BlockEvents: { rightClicked: cb => { m.kubejsClic = cb } },
    ForgeEvents: { onEvent: (nom, cb) => { m.listeners[nom] = cb } },
    JsonIO: { readString: () => JSON.stringify(Object.values(m.joueurs).map(j => ({ uuid: String(j.getUuid()), name: j.getUsername() }))) },
    Text: { red: s => ({ rouge: s }), of: s => s },
    console: { error: s => m.journal.push(String(s)), log() {}, info() {} },
    global: m.global,
  })
  const portee = () => {
    const c = vm.createContext(fabrique())
    vm.runInContext('Date.now = () => __horloge()', c)
    c.__horloge = () => m.t
    return c
  }
  m.chargerGarde = () => {
    m.ctxServeur = portee()
    vm.runInContext(GARDE, m.ctxServeur, { filename: 'bmc4_garde.js' })
  }
  m.chargerRecharge = () => {
    m.ctxDemarrage = portee()
    vm.runInContext(RECHARGE, m.ctxDemarrage, { filename: 'bmc4_coffres_recharge.js' })
  }

  // Un clic droit sur un bloc, pour une main, comme Forge l'enchaîne :
  // Architectury (KubeJS) en HIGH, puis l'écouteur de démarrage en NORMAL.
  m.clic = (joueur, p, { recharge = false, client = false } = {}) => {
    const touche = []
    let annule = false
    let kubejsVu = false
    let forgeVu = false
    if (!recharge && m.kubejsClic) {
      kubejsVu = true
      const ev = {
        getPlayer: () => joueur,
        getBlock: () => niveau.getBlock(p),
        cancel: () => { annule = true; throw new EventExit() },
      }
      try { m.kubejsClic(ev) } catch (e) { if (!(e instanceof EventExit)) throw e }
    }
    const forge = {
      getLevel: () => (client ? { ...niveau, isClientSide: () => true } : niveau),
      getEntity: () => joueur,
      getPos: () => p,
      setCanceled: b => { annule = b },
    }
    const espion = new Proxy(forge, {
      get: (o, k) => {
        touche.push(String(k))
        if (!(k in o)) throw new Error('écouteur : appel inattendu ' + String(k))
        return o[k]
      },
    })
    const ecouteur = m.listeners[EVENEMENT]
    if (!annule && ecouteur) {
      forgeVu = true
      ecouteur(espion)    // une exception ici ferait échouer le test : l'écouteur ne doit jamais lever
    }
    return { annule, kubejsVu, forgeVu, touche }
  }
  m.messagesDe = nom => m.messages.filter(x => x.a === nom)
  return m
}

// Deux factions : F1 (Apex, claim en 0,0) et F2 (Farmer's, claim en 2,0).
// A est de F1, B de F2, C d'une troisième faction, D allié de F1.
function partie({ garde = true, recharge = true } = {}) {
  const m = monde()
  const A = m.joueur('Alice', 'uuid-a')
  const B = m.joueur('Bob', 'uuid-b')
  const C = m.joueur('Chloe', 'uuid-c')
  const D = m.joueur('Dan', 'uuid-d')
  m.equipe('Apex', ['uuid-a'], ['uuid-d'])
  m.equipe('Farmers', ['uuid-b'])
  m.equipe('Tierce', ['uuid-c'])
  m.claim(0, 0, 'Apex')
  m.claim(2, 0, 'Farmers')
  const coffreF1 = m.pos(3, 64, 3)
  const coffreF2 = m.pos(35, 64, 3)
  const porteF1 = m.pos(4, 64, 3)
  const terreF1 = m.pos(5, 64, 3)
  m.bloc(coffreF1, 'minecraft:chest', true)
  m.bloc(coffreF2, 'minecraft:chest', true)
  m.bloc(porteF1, 'minecraft:oak_door', true, ['minecraft:doors'])
  m.bloc(terreF1, 'minecraft:dirt', false)
  if (garde) m.chargerGarde()
  if (recharge) m.chargerRecharge()
  return { m, A, B, C, D, coffreF1, coffreF2, porteF1, terreF1 }
}

// ------------------------------------------------------------------
//  1. La logique pure (bmc4GardeCoffres), sans le reste
// ------------------------------------------------------------------
function logique({ interdit, lever = {} } = {}) {
  const m = monde()
  m.chargerGarde()
  const s = { appels: 0, dits: [], journal: [], t: 0 }
  const decider = m.ctxServeur.bmc4GardeCoffres({
    interdit: (j, b) => { s.appels++; if (lever.interdit) throw new Error('boum'); return interdit(j, b) },
    cle: j => { if (lever.cle) throw new Error('uuid'); return j.u },
    lieu: b => { if (lever.lieu) throw new Error('pos'); return b.p },
    maintenant: () => s.t,
    journal: (c, e) => s.journal.push(c + ' : ' + e),
    dire: (j, f) => { if (lever.dire) throw new Error('tellraw'); s.dits.push(j.u + ' ' + f) },
  })
  return { decider, s }
}

test('logique : autorisé, aucun message', () => {
  const { decider, s } = logique({ interdit: () => null })
  assert.equal(decider({ u: 'a' }, { p: '1' }), false)
  assert.deepEqual(s.dits, [])
})

test('logique : refusé, un message', () => {
  const { decider, s } = logique({ interdit: () => 'F1' })
  assert.equal(decider({ u: 'a' }, { p: '1' }), true)
  assert.deepEqual(s.dits, ['a F1'])
})

test('logique : même clic vu deux fois (deux chemins ou deux mains) : une décision, un message', () => {
  const { decider, s } = logique({ interdit: () => 'F1' })
  assert.equal(decider({ u: 'a' }, { p: '1' }), true)
  s.t += 2
  assert.equal(decider({ u: 'a' }, { p: '1' }), true)
  assert.equal(s.appels, 1)
  assert.deepEqual(s.dits, ['a F1'])
})

test('logique : même clic autorisé, repris sans nouveau calcul', () => {
  const { decider, s } = logique({ interdit: () => null })
  decider({ u: 'a' }, { p: '1' })
  s.t += 1
  assert.equal(decider({ u: 'a' }, { p: '1' }), false)
  assert.equal(s.appels, 1)
})

test('logique : un autre bloc dans la même milliseconde est recalculé', () => {
  let n = 0
  const { decider, s } = logique({ interdit: () => (n++ === 0 ? null : 'F1') })
  assert.equal(decider({ u: 'a' }, { p: '1' }), false)
  assert.equal(decider({ u: 'a' }, { p: '2' }), true)
  assert.equal(s.appels, 2)
})

test('logique : délai d\'un message par seconde, par joueur', () => {
  const { decider, s } = logique({ interdit: () => 'F1' })
  decider({ u: 'a' }, { p: '1' })      // t = 0 : premier message
  s.t = 250; decider({ u: 'a' }, { p: '1' })   // nouveau clic : refusé, sans message
  s.t = 900; decider({ u: 'a' }, { p: '1' })
  s.t = 900; decider({ u: 'b' }, { p: '1' })   // un autre joueur a son propre délai
  s.t = 1000; decider({ u: 'a' }, { p: '1' })  // une seconde : nouveau message
  assert.deepEqual(s.dits, ['a F1', 'b F1', 'a F1'])
  assert.equal(s.appels, 5)
})

test('logique : la règle lève, refus fail-closed avec « la garde ne répond pas » (?)', () => {
  const { decider, s } = logique({ interdit: () => null, lever: { interdit: true } })
  assert.equal(decider({ u: 'a' }, { p: '1' }), true)
  assert.deepEqual(s.dits, ['a ?'])
  assert.match(s.journal[0], /^coffres : Error: boum/)
})

test('logique : le message lève, le refus tient et rien ne sort', () => {
  const { decider, s } = logique({ interdit: () => 'F1', lever: { dire: true } })
  assert.equal(decider({ u: 'a' }, { p: '1' }), true)
  assert.match(s.journal[0], /^message des coffres/)
})

test('logique : UUID illisible, refus sans message', () => {
  const { decider, s } = logique({ interdit: () => null, lever: { cle: true } })
  assert.equal(decider({ u: 'a' }, { p: '1' }), true)
  assert.deepEqual(s.dits, [])
  assert.equal(s.appels, 0)
})

test('logique : position illisible, refus avec « ? »', () => {
  const { decider, s } = logique({ interdit: () => null, lever: { lieu: true } })
  assert.equal(decider({ u: 'a' }, { p: '1' }), true)
  assert.deepEqual(s.dits, ['a ?'])
})

// ------------------------------------------------------------------
//  2. Les deux scripts ensemble, le vrai coffreInterdit, de faux objets
// ------------------------------------------------------------------
const refusF1 = /^Ouvrir ce bloc refusé : il est dans le claim de Apex\./

test('essai 1 : perle en recharge, coffre d\'une autre faction : refusé, un seul message', () => {
  const { m, B, coffreF1 } = partie()
  const r = m.clic(B, coffreF1, { recharge: true })
  assert.equal(r.kubejsVu, false)
  assert.equal(r.forgeVu, true)
  assert.equal(r.annule, true)
  assert.equal(m.messagesDe('Bob').length, 1)
  assert.match(m.messagesDe('Bob')[0].texte, refusF1)
  // Pour refuser, seulement setCanceled : ni setUseBlock, ni setUseItem (BMC-108).
  assert.ok(r.touche.includes('setCanceled'))
  assert.ok(!r.touche.some(k => /^setUse|Result/.test(k)), r.touche.join(','))
})

test('essai 1 bis : clics répétés en recharge, un message par seconde', () => {
  const { m, B, coffreF1 } = partie()
  for (let i = 0; i < 5; i++) {
    assert.equal(m.clic(B, coffreF1, { recharge: true }).annule, true)
    m.t += 200
  }
  assert.equal(m.messagesDe('Bob').length, 1)
  m.t += 200
  m.clic(B, coffreF1, { recharge: true })
  assert.equal(m.messagesDe('Bob').length, 2)
})

test('essai 2 : son propre coffre, en recharge : ouvert, l\'événement n\'est pas touché', () => {
  const { m, A, coffreF1 } = partie()
  const r = m.clic(A, coffreF1, { recharge: true })
  assert.equal(r.annule, false)
  assert.ok(!r.touche.some(k => k.startsWith('set')), r.touche.join(','))
  assert.equal(m.messages.length, 0)
})

test('essai 3 : raid en cours entre les deux factions, en recharge : ouvert', () => {
  const { m, B, coffreF1 } = partie()
  m.raid.add('Alice'); m.raid.add('Bob')
  assert.equal(m.clic(B, coffreF1, { recharge: true }).annule, false)
  assert.equal(m.messages.length, 0)
})

test('essai 3 bis : raid en cours, mais pas avec F1 (troisième faction) : refusé', () => {
  const { m, C, coffreF1 } = partie()
  m.raid.add('Bob'); m.raid.add('Chloe')
  assert.equal(m.clic(C, coffreF1, { recharge: true }).annule, true)
  assert.equal(m.messagesDe('Chloe').length, 1)
})

test('essai 4 : sans recharge, coffre d\'une autre faction : refusé par KubeJS, un seul message', () => {
  const { m, B, coffreF1 } = partie()
  const r = m.clic(B, coffreF1)
  assert.equal(r.kubejsVu, true)
  assert.equal(r.annule, true)
  assert.equal(r.forgeVu, false)    // annulé en HIGH : Forge ne le passe plus en NORMAL
  assert.equal(m.messagesDe('Bob').length, 1)   // le message part avant event.cancel()
  assert.match(m.messagesDe('Bob')[0].texte, refusF1)
})

test('sans recharge, autorisé : les deux chemins passent, la règle n\'est calculée qu\'une fois', () => {
  const { m, A, coffreF1 } = partie()
  const r = m.clic(A, coffreF1)
  assert.equal(r.kubejsVu, true)
  assert.equal(r.forgeVu, true)
  assert.equal(r.annule, false)
  assert.equal(m.chunksLus, 1)
})

test('deux mains : main principale en recharge puis main secondaire, un seul message', () => {
  const { m, B, coffreF1 } = partie()
  assert.equal(m.clic(B, coffreF1, { recharge: true }).annule, true)   // main principale
  m.t += 1
  assert.equal(m.clic(B, coffreF1).annule, true)                       // main secondaire
  assert.equal(m.messagesDe('Bob').length, 1)
})

test('allié de la faction, en recharge : ouvert ; porte et bloc sans inventaire : ouverts', () => {
  const { m, B, D, coffreF1, porteF1, terreF1 } = partie()
  assert.equal(m.clic(D, coffreF1, { recharge: true }).annule, false)
  assert.equal(m.clic(B, porteF1, { recharge: true }).annule, false)
  m.t += 100
  assert.equal(m.clic(B, terreF1, { recharge: true }).annule, false)
  assert.equal(m.messages.length, 0)
})

test('côté client : l\'écouteur ne fait rien', () => {
  const { m, B, coffreF1 } = partie()
  const r = m.clic(B, coffreF1, { recharge: true, client: true })
  assert.equal(r.annule, false)
  assert.deepEqual(r.touche, ['getLevel'])
})

test('erreur dans la garde (bloc illisible) : refusé, « la garde ne répond pas », rien ne sort', () => {
  const { m, B, coffreF1 } = partie()
  m.niveauCasse = true
  assert.equal(m.clic(B, coffreF1, { recharge: true }).annule, true)
  assert.match(m.messagesDe('Bob')[0].texte, /la garde ne répond pas/)
  assert.ok(m.journal.some(l => /coffres \(recharge\)/.test(l)))
})

test('scripts serveur absents : un bloc à inventaire est refusé (fail-closed), le reste passe', () => {
  const { m, A, coffreF1, terreF1 } = partie({ garde: false })
  assert.equal(m.clic(A, coffreF1, { recharge: true }).annule, true)
  assert.match(m.messagesDe('Alice')[0].texte, /la garde ne répond pas/)
  m.t += 100
  assert.equal(m.clic(A, terreF1, { recharge: true }).annule, false)
  assert.ok(m.journal.some(l => /garde absente/.test(l)))
})

test('/reload : l\'écouteur appelle la règle rechargée', () => {
  const { m, B, coffreF1 } = partie()
  const avant = m.global.bmc4GardeCoffre
  m.chargerGarde()      // /reload : les scripts serveur sont réévalués
  assert.notEqual(m.global.bmc4GardeCoffre, avant)
  m.global.bmc4GardeCoffre = () => false   // une règle « tout permis », pour voir laquelle est appelée
  assert.equal(m.clic(B, coffreF1, { recharge: true }).annule, false)
})
