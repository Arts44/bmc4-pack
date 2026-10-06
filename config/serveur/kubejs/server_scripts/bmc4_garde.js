// priority: 0
// ============================================================
//  bmc4_garde.js — La garde des commandes de FTB Essentials (BMC-91)
//
//  Va dans <serveur>/kubejs/server_scripts/. Lit global.BMC4
//  (bmc4_00_table.js, généré depuis config/rangs/rangs.toml).
//
//  Chaque commande d'un joueur passe ici AVANT d'être exécutée
//  (ServerEvents.command = CommandEvent de Forge). Un refus annule la
//  commande et l'explique : ce qui est refusé, pourquoi, et ce que le
//  joueur peut faire ou quand.
//
//  Les blocages, non négociables (Arthur, 6 octobre) :
//    /home, /back, /tpa, /tpahere, /tpaccept sont refusés
//      · en combat : coup pris d'une créature ou d'un joueur, ou
//        coup donné, dans les 15 dernières secondes ;
//      · pendant un raid, pour les membres des deux factions
//        engagées (l'équipe bmc4_raid_actif, que le bot remplit) ;
//      · dans le claim d'une autre faction ;
//    et la destination ne peut pas être dans le claim d'une autre
//    faction (/sethome, /home, /back, et le joueur rejoint par /tpa).
//  Les claims de l'équipe serveur (le Marché Flottant) ne comptent pas.
//
//  FAIL-CLOSED (6 octobre au soir, après les essais en jeu) : si une vérification
//  lève une erreur, la commande gardée est REFUSÉE avec un message, et
//  l'erreur est écrite une fois dans le journal. « Si un blocage ne peut
//  pas être garanti, la commande n'est pas ouverte. »
//
//  LES NOMS JAVA. Sur ce serveur (Forge, KubeJS 2001.6.5-build.26, Rhino
//  2001.2.3-build.10), les méthodes du jeu portent des noms obfusqués
//  (m_20148_…). Rhino les traduit depuis les noms Mojang (mm.jsmappings),
//  SAUF quand un mixin de KubeJS leur donne son propre nom (@RemapForJS),
//  qui l'emporte : getUUID() n'existe pas, c'est getUuid() ;
//  DamageSource.getEntity() n'existe pas, c'est getActual() ;
//  level.dimension est une propriété (ResourceLocation), la clé de
//  dimension est getDimensionKey(). Toute la garde passe donc par
//  l'objet ACCES ci-dessous, une forme justifiée par appel, et
//  /prestige diagnostic les essaie toutes sur le joueur qui la tape.
// ============================================================

const FTBChunksAPI = Java.loadClass('dev.ftb.mods.ftbchunks.api.FTBChunksAPI')
const ChunkDimPos = Java.loadClass('dev.ftb.mods.ftblibrary.math.ChunkDimPos')
const ChunkPos = Java.loadClass('net.minecraft.world.level.ChunkPos')
const TeamProperties = Java.loadClass('dev.ftb.mods.ftbteams.api.property.TeamProperties')
const FTBEPlayerData = Java.loadClass('dev.ftb.mods.ftbessentials.util.FTBEPlayerData')
const TPACommands = Java.loadClass('dev.ftb.mods.ftbessentials.command.TPACommands')

const COMBAT_MS = 15000

// Dernier coup pris ou donné, par UUID (en mémoire : un redémarrage remet
// tout le monde hors combat, ce qui est sans danger).
const dernierCoup = {}
// Dernière téléportation acceptée, par UUID et par famille.
const derniereTp = {}
// Joueurs à qui le compteur de combat est affiché (pour l'effacer à 0).
const compteurAffiche = {}
// Erreurs déjà écrites dans le journal (une fois chacune).
const erreursDites = {}
// Pour /prestige diagnostic : ce que le gestionnaire de coups a vu.
const suiviCoups = { vus: 0, erreurs: 0, dernierAuteur: '' }

// Les commandes que la configuration de FTB Essentials coupe : sans ce texte,
// le joueur lirait « Unknown or incomplete command ».
const COUPEES = {
  rtp: "elle téléporte n'importe où, claims compris",
  spawn: 'elle permettrait de quitter un raid',
  playerspawn: 'elle permettrait de quitter un raid',
  warp: 'elle permettrait de quitter un raid',
  listwarps: "les warps n'existent pas ici",
  near: 'elle donnerait la position des autres joueurs',
  kickme: "elle n'a pas d'usage ici",
  leaderboard: "elle n'a pas d'usage ici",
}

// Les commandes que ce script examine. Les autres passent sans un appel Java.
const GARDEES = { home: 1, sethome: 1, delhome: 1, listhomes: 1, back: 1, tpa: 1, tpahere: 1, tpaccept: 1, tpdeny: 1,
  hat: 1, trashcan: 1, nickname: 1, enderchest: 1, feed: 1 }

// ------------------------------------------------------------
//  ACCES : chaque appel Java, dans la forme qui existe au runtime
// ------------------------------------------------------------
const ACCES = {
  // EntityMixin.java:87, @RemapForJS("getUsername") sur m_6302_
  nom: e => String(e.getUsername()),
  // EntityMixin.java:79, @RemapForJS("getUuid") sur m_20148_ ; rend un java.util.UUID
  uuid: e => e.getUuid(),
  // EntityKJS.java:93, kjs$isPlayer (préfixe kjs$ retiré par @RemapPrefixForJS)
  estJoueur: e => e.isPlayer() == true,
  // ServerPlayerKJS.java:77, kjs$isOp : la liste des opérateurs du serveur
  estOp: p => p.isOp() == true,
  // EntityKJS.java:228, kjs$isOnScoreboardTeam : l'équipe vanilla du raid
  enRaid: p => p.isOnScoreboardTeam('bmc4_raid_actif') == true,
  // MinecraftServerKJS.java:64, kjs$runCommandSilent rend le résultat de la
  // commande (performPrefixedCommand) : « scoreboard players get » rend le score.
  // « execute if score … matches » d'abord, pour distinguer 0 d'un score absent.
  score: (server, nom, objectif) => {
    if (server.runCommandSilent('execute if score ' + nom + ' ' + objectif + ' matches -2147483648..') < 1) return null
    return server.runCommandSilent('scoreboard players get ' + nom + ' ' + objectif)
  },
  // MinecraftServerKJS.java:77, kjs$getPlayers : une ArrayList de ServerPlayer
  joueurs: server => {
    let liste = server.getPlayers()
    let out = []
    for (let i = 0; i < liste.size(); i++) out.push(liste.get(i))
    return out
  },
  // DamageSourceMixin.java:24, @RemapForJS("getActual") sur m_7639_ (le tireur pour une flèche)
  auteur: source => source.getActual(),
  // ChunkDimPos(Entity) : constructeur de FTB Library 2001.2.13 (javap), non obfusqué
  caseDe: e => new ChunkDimPos(e),
  // TeleportPos de FTB Essentials : getDimension() rend la ResourceKey<Level>,
  // getPos() le BlockPos ; ChunkPos(BlockPos) est un constructeur du jeu
  // (javap du jar 1.20.1) ; ChunkDimPos(ResourceKey, ChunkPos) est de FTB Library.
  caseDeTp: pos => new ChunkDimPos(pos.getDimension(), new ChunkPos(pos.getPos())),
  // FTB Chunks 2001.3.8 (javap) : FTBChunksAPI.api().getManager().getChunk(ChunkDimPos),
  // ClaimedChunk.getTeamData(), ChunkTeamData.getTeam() et isTeamMember(UUID) ;
  // FTB Teams 2001.3.2 : Team.isServerTeam(), getProperty(TeamProperties.DISPLAY_NAME) rend un String.
  claimEtranger: (joueur, cdp) => {
    let chunk = FTBChunksAPI.api().getManager().getChunk(cdp)
    if (chunk == null) return null
    let donnees = chunk.getTeamData()
    let equipe = donnees.getTeam()
    if (equipe.isServerTeam()) return null
    if (donnees.isTeamMember(ACCES.uuid(joueur))) return null
    return String(equipe.getProperty(TeamProperties.DISPLAY_NAME))
  },
  // FTB Essentials 2001.2.4 (source du tag) : FTBEPlayerData.getOrCreate(Player)
  // rend un Optional ; homeManager(), teleportHistory (champ public), TPACommands.REQUESTS.
  essentials: p => {
    let o = FTBEPlayerData.getOrCreate(p)
    return o.isPresent() ? o.get() : null
  },
  // MinecraftServer.getCommands() (m_129892_) et Commands.sendCommands(ServerPlayer)
  // (m_82095_) : noms Mojang traduits par Rhino (mm.jsmappings), qu'aucun mixin
  // de KubeJS ne renomme. Renvoie l'arbre des commandes au client.
  renvoyerCommandes: (server, p) => server.getCommands().sendCommands(p),
}

// ------------------------------------------------------------
//  Outils
// ------------------------------------------------------------
function journal(cle, e) {
  if (erreursDites[cle]) return
  erreursDites[cle] = true
  console.error('bmc4_garde : ' + cle + ' : ' + e)
}

function dire(server, nom, refus, raison, suite) {
  let json = ['',
    { text: refus + ' refusé : ', color: 'red' },
    { text: raison, color: 'red' }]
  if (suite) json.push({ text: ' ' + suite, color: 'gray' })
  server.runCommandSilent('tellraw ' + nom + ' ' + JSON.stringify(json))
}

function nomRang(n) {
  if (n <= 0) return 'aucun rang'
  let r = global.BMC4.rangs[Math.min(n, global.BMC4.rangs.length) - 1]
  return r.affiche
}

// Rhino peut envelopper deux fois le même objet Java : on compare les UUID.
function meme(a, b) {
  return a != null && b != null && String(ACCES.uuid(a)) == String(ACCES.uuid(b))
}

function secondes(ms) {
  return Math.max(1, Math.ceil(ms / 1000))
}

function combatRestant(joueur) {
  let t = dernierCoup[String(ACCES.uuid(joueur))]
  if (!t) return 0
  return Math.max(0, COMBAT_MS - (Date.now() - t))
}

function finDuRaid(server) {
  let h = ACCES.score(server, '#fin_h', 'bmc4_raid')
  let m = ACCES.score(server, '#fin_m', 'bmc4_raid')
  if (h == null || m == null) return 'la fin du créneau'
  return h + ' h ' + (m < 10 ? '0' : '') + m
}

function nomsDesHomes(d) {
  let noms = []
  let it = d.homeManager().getNames().iterator()
  while (it.hasNext()) noms.push(String(it.next()))
  return noms.sort()
}

function homeNomme(d, nom) {
  let it = d.homeManager().destinations().iterator()
  while (it.hasNext()) {
    let e = it.next()
    if (String(e.name()) == nom) return e.destination()
  }
  return null
}

function maxHomes(joueur, rang) {
  if (ACCES.estOp(joueur)) return 10
  let max = 0
  for (const n in global.BMC4.homes) {
    if (rang >= Number(n)) max = Math.max(max, global.BMC4.homes[n])
  }
  return max
}

function prochainPalierHomes(rang) {
  let meilleur = null
  for (const n in global.BMC4.homes) {
    let k = Number(n)
    if (k > rang && (meilleur == null || k < meilleur[0])) meilleur = [k, global.BMC4.homes[n]]
  }
  return meilleur
}

function joueurNomme(server, nom) {
  if (!nom) return null
  let bas = String(nom).toLowerCase()
  let tous = ACCES.joueurs(server)
  for (let i = 0; i < tous.length; i++) if (ACCES.nom(tous[i]).toLowerCase() == bas) return tous[i]
  return null
}

function joueurParUuid(server, uuid) {
  let cible = String(uuid)
  let tous = ACCES.joueurs(server)
  for (let i = 0; i < tous.length; i++) if (String(ACCES.uuid(tous[i])) == cible) return tous[i]
  return null
}

// ------------------------------------------------------------
//  Les contrôles : combat, raid, claim du lieu actuel, destination
// ------------------------------------------------------------
// Rend true si un refus a été dit.
function bloque(server, joueur, refus, quiEstConcerne) {
  let autre = quiEstConcerne != null && !meme(quiEstConcerne, joueur)
  let qui = autre ? quiEstConcerne : joueur
  let nomJ = ACCES.nom(joueur)
  let reste = combatRestant(qui)
  if (reste > 0) {
    if (autre) dire(server, nomJ, refus, ACCES.nom(qui) + ' est en combat.', 'Réessaie dans ' + secondes(reste) + ' s.')
    else dire(server, nomJ, refus, 'tu as pris ou donné un coup il y a moins de 15 secondes.', 'Réessaie dans ' + secondes(reste) + ' s.')
    return true
  }
  if (ACCES.enRaid(qui)) {
    if (autre) dire(server, nomJ, refus, ACCES.nom(qui) + ' est engagé dans un raid, jusqu\'à ' + finDuRaid(server) + '.', 'Réessaie après le raid.')
    else dire(server, nomJ, refus, 'un raid est en cours pour ta faction, jusqu\'à ' + finDuRaid(server) + '.', 'Les téléportations reviennent à la fin du raid.')
    return true
  }
  return false
}

function bloqueClaim(server, joueur, refus, quiBouge) {
  let qui = quiBouge || joueur
  let faction = ACCES.claimEtranger(qui, ACCES.caseDe(qui))
  if (faction == null) return false
  if (meme(qui, joueur)) dire(server, ACCES.nom(joueur), refus, 'tu es dans le claim de ' + faction + '.', 'Sors de leur territoire pour l\'utiliser.')
  else dire(server, ACCES.nom(joueur), refus, ACCES.nom(qui) + ' est dans le claim de ' + faction + '.', 'Il doit d\'abord en sortir.')
  return true
}

function bloqueDelai(server, joueur, refus, famille, enregistrer) {
  let delai = (global.BMC4.delais[famille] || 0) * 1000
  let cle = String(ACCES.uuid(joueur)) + ':' + famille
  let depuis = Date.now() - (derniereTp[cle] || 0)
  if (depuis < delai) {
    dire(server, ACCES.nom(joueur), refus, 'une téléportation par ' + (delai / 1000) + ' secondes.', 'Réessaie dans ' + secondes(delai - depuis) + ' s.')
    return true
  }
  if (enregistrer) derniereTp[cle] = Date.now()
  return false
}

// ------------------------------------------------------------
//  Les commandes une à une. Chacune rend true si elle a refusé.
// ------------------------------------------------------------
function garderHome(server, joueur, args) {
  let nomJ = ACCES.nom(joueur)
  let d = ACCES.essentials(joueur)
  if (d == null) throw 'données FTB Essentials introuvables'
  let nom = (args.join(' ') || 'home').toLowerCase()
  let pos = homeNomme(d, nom)
  if (pos == null) {
    let noms = nomsDesHomes(d)
    dire(server, nomJ, '/home', 'tu n\'as pas de home nommé « ' + nom + ' ».', noms.length ? 'Tes homes : ' + noms.join(', ') + '.' : 'Pose-en un avec /sethome <nom>.')
    return true
  }
  if (bloque(server, joueur, '/home')) return true
  if (bloqueClaim(server, joueur, '/home')) return true
  let faction = ACCES.claimEtranger(joueur, ACCES.caseDeTp(pos))
  if (faction != null) {
    dire(server, nomJ, '/home', 'ton home « ' + nom + ' » est dans le claim de ' + faction + '.',
      'Un home ne ramène pas dans le territoire d\'une autre faction : supprime-le (/delhome ' + nom + ').')
    return true
  }
  return bloqueDelai(server, joueur, '/home', 'home', true)
}

function garderSethome(server, joueur, args, rang) {
  let nomJ = ACCES.nom(joueur)
  let d = ACCES.essentials(joueur)
  if (d == null) throw 'données FTB Essentials introuvables'
  let nom = (args.join(' ') || 'home').toLowerCase()
  let faction = ACCES.claimEtranger(joueur, ACCES.caseDe(joueur))
  if (faction != null) {
    dire(server, nomJ, '/sethome', 'tu ne peux pas poser de home dans le claim d\'une autre faction (ici, ' + faction + ').', 'Pose-le dans ton claim ou hors claim.')
    return true
  }
  let noms = nomsDesHomes(d)
  let max = maxHomes(joueur, rang)
  if (noms.indexOf(nom) < 0 && noms.length >= max) {
    let suivant = prochainPalierHomes(rang)
    dire(server, nomJ, '/sethome', 'tu as déjà ' + noms.length + ' home' + (noms.length > 1 ? 's' : '') + ', le maximum de ton rang (' + nomRang(rang) + ').',
      'Remplace-en un (/sethome ' + (noms[0] || 'home') + ') ou supprime-le (/delhome <nom>)' + (suivant ? ' ; le rang ' + nomRang(suivant[0]) + ' en donne ' + suivant[1] + '.' : '.'))
    return true
  }
  return false
}

function garderDelhome(server, joueur, args) {
  let d = ACCES.essentials(joueur)
  if (d == null) throw 'données FTB Essentials introuvables'
  let nom = (args.join(' ') || 'home').toLowerCase()
  let noms = nomsDesHomes(d)
  if (noms.indexOf(nom) < 0) {
    dire(server, ACCES.nom(joueur), '/delhome', 'tu n\'as pas de home nommé « ' + nom + ' ».', noms.length ? 'Tes homes : ' + noms.join(', ') + '.' : 'Tu n\'en as aucun.')
    return true
  }
  return false
}

function garderBack(server, joueur) {
  let nomJ = ACCES.nom(joueur)
  let d = ACCES.essentials(joueur)
  if (d == null) throw 'données FTB Essentials introuvables'
  if (d.teleportHistory.isEmpty()) {
    dire(server, nomJ, '/back', 'il n\'y a aucun lieu où revenir.', '/back ramène à ta dernière téléportation ou à ta dernière mort.')
    return true
  }
  if (bloque(server, joueur, '/back')) return true
  if (bloqueClaim(server, joueur, '/back')) return true
  let faction = ACCES.claimEtranger(joueur, ACCES.caseDeTp(d.teleportHistory.getLast()))
  if (faction != null) {
    dire(server, nomJ, '/back', 'ton dernier lieu est dans le claim de ' + faction + '.', '/back ne ramène pas dans le territoire d\'une autre faction : rejoins-le à pied.')
    return true
  }
  return bloqueDelai(server, joueur, '/back', 'back', true)
}

// Contrôle commun à /tpa, /tpahere et /tpaccept : « bouge » rejoint « vers ».
function garderTrajet(server, joueur, refus, bouge, vers, enregistrer) {
  if (bloque(server, joueur, refus, bouge)) return true
  if (bloque(server, joueur, refus, vers)) return true
  if (bloqueClaim(server, joueur, refus, bouge)) return true
  // La destination : la case où se tient « vers », vue depuis la faction de « bouge ».
  let faction = ACCES.claimEtranger(bouge, ACCES.caseDe(vers))
  if (faction != null) {
    dire(server, ACCES.nom(joueur), refus, (meme(vers, joueur) ? 'tu es' : ACCES.nom(vers) + ' est') + ' dans le claim de ' + faction
      + (meme(bouge, joueur) ? '' : ', une autre faction pour ' + ACCES.nom(bouge)) + '.', 'Pas de téléportation dans le territoire d\'une autre faction.')
    return true
  }
  return bloqueDelai(server, bouge, refus, 'tpa', enregistrer)
}

function garderTpa(server, joueur, args, ici) {
  let refus = ici ? '/tpahere' : '/tpa'
  let nomJ = ACCES.nom(joueur)
  let cible = joueurNomme(server, args[0])
  if (cible == null) {
    dire(server, nomJ, refus, args[0] ? 'aucun joueur nommé « ' + args[0] + ' » n\'est connecté.' : 'il manque le pseudo.', 'Écris ' + refus + ' <pseudo exact> d\'un joueur connecté.')
    return true
  }
  if (meme(cible, joueur)) {
    dire(server, nomJ, refus, 'c\'est toi.', 'Écris le pseudo d\'un autre joueur.')
    return true
  }
  let src = ACCES.essentials(joueur)
  let dst = ACCES.essentials(cible)
  if (src == null || dst == null) throw 'données FTB Essentials introuvables'
  let it = TPACommands.REQUESTS.values().iterator()
  while (it.hasNext()) {
    let r = it.next()
    if (String(r.source().getUuid()) == String(src.getUuid()) && String(r.target().getUuid()) == String(dst.getUuid())) {
      dire(server, nomJ, refus, 'une demande vers ' + ACCES.nom(cible) + ' attend déjà sa réponse.', 'Attends qu\'il l\'accepte ou la refuse.')
      return true
    }
  }
  return ici ? garderTrajet(server, joueur, refus, cible, joueur, false) : garderTrajet(server, joueur, refus, joueur, cible, false)
}

function garderTpaccept(server, joueur, args) {
  let nomJ = ACCES.nom(joueur)
  let r = TPACommands.REQUESTS.get(args[0] || '')
  if (r == null) {
    dire(server, nomJ, '/tpaccept', 'cette demande n\'existe pas ou n\'est plus valable.', 'Demande à l\'autre joueur de la refaire.')
    return true
  }
  let source = joueurParUuid(server, r.source().getUuid())
  if (source == null) {
    dire(server, nomJ, '/tpaccept', 'le joueur qui a fait la demande s\'est déconnecté.', null)
    return true
  }
  // r.here() : la cible (celui qui accepte) rejoint l'auteur de la demande.
  return r.here() ? garderTrajet(server, joueur, '/tpaccept', joueur, source, true) : garderTrajet(server, joueur, '/tpaccept', source, joueur, true)
}

function garderNickname(server, joueur, args) {
  let nom = args.join(' ').trim()
  if (!nom) return false
  let pris = null
  let enLigne = joueurNomme(server, nom)
  if (enLigne != null) pris = ACCES.nom(enLigne)
  else {
    // MinecraftServer.getProfileCache() (m_129927_) : nom Mojang traduit par Rhino.
    let trouve = server.getProfileCache().get(nom)
    if (trouve != null && trouve.isPresent()) pris = String(trouve.get().getName())
  }
  if (pris != null && pris.toLowerCase() != ACCES.nom(joueur).toLowerCase()) {
    dire(server, ACCES.nom(joueur), '/nickname', '« ' + nom + ' » est le pseudo d\'un autre joueur.',
      'Le règlement interdit de prendre le pseudo d\'un autre : choisis-en un qui n\'appartient à personne.')
    return true
  }
  return false
}

// ------------------------------------------------------------
//  L'aiguillage
// ------------------------------------------------------------
ServerEvents.command(event => {
  // CommandEventJS.java:21 (getInput) : le texte tapé, sans appel au jeu.
  let mots = String(event.getInput()).trim().replace(/^\//, '').split(/\s+/)
  let commande = mots[0].toLowerCase()
  if (!COUPEES[commande] && !GARDEES[commande]) return
  let args = mots.slice(1)
  // ServerEventJS.java:13 (getServer).
  let server = event.getServer()

  // Le joueur : getPlayerOrException() de CommandSourceStack (nom Mojang traduit
  // par Rhino, déjà sollicité avec succès par /prestige le 6 octobre). Pour la
  // console ou une fonction, il lève une exception de Minecraft : pas de joueur.
  // Une TypeError, elle, voudrait dire que l'appel n'existe pas : refus.
  let joueur = null
  try {
    joueur = event.getParseResults().getContext().getSource().getPlayerOrException()
  } catch (e) {
    if (String(e).indexOf('TypeError') >= 0) {
      journal('identifier le joueur', e)
      event.cancel()
    }
    return
  }

  let nomJ = '@a'
  let refuse = false
  try {
    nomJ = ACCES.nom(joueur)

    if (COUPEES[commande]) {
      dire(server, nomJ, '/' + commande, 'commande coupée sur BMC4, ' + COUPEES[commande] + '.',
        commande == 'spawn' || commande == 'playerspawn' || commande == 'warp' ? 'Les waystones restent là pour voyager.' : null)
      refuse = true
    } else if (commande == 'feed' && !ACCES.estOp(joueur)) {
      // /feed des joueurs : le datapack (rang, 30 minutes, messages).
      server.runCommandSilent('execute as ' + nomJ + ' run function bmc4:rangs/g_manger')
      refuse = true
    } else {
      let requis = global.BMC4.commandes[commande]
      let rang = ACCES.score(server, nomJ, 'bmc4_rangs') || 0
      if (requis != null && requis > 0 && rang < requis && !ACCES.estOp(joueur)) {
        dire(server, nomJ, '/' + commande, 'elle s\'obtient au rang ' + nomRang(requis) + ' (ton rang : ' + nomRang(rang) + ').', 'Voir ce qu\'il te manque : /prestige.')
        refuse = true
      } else if (commande == 'home') refuse = garderHome(server, joueur, args)
      else if (commande == 'sethome') refuse = garderSethome(server, joueur, args, rang)
      else if (commande == 'delhome') refuse = garderDelhome(server, joueur, args)
      else if (commande == 'back') refuse = garderBack(server, joueur)
      else if (commande == 'tpa') refuse = garderTpa(server, joueur, args, false)
      else if (commande == 'tpahere') refuse = garderTpa(server, joueur, args, true)
      else if (commande == 'tpaccept') refuse = garderTpaccept(server, joueur, args)
      else if (commande == 'nickname') refuse = garderNickname(server, joueur, args)
    }
  } catch (e) {
    // Fail-closed : la vérification n'a pas pu se faire, la commande n'est pas ouverte.
    journal('/' + commande, e)
    dire(server, nomJ, '/' + commande, 'la vérification de sécurité a échoué.', 'Réessaie dans un instant ; si ça se répète, préviens le staff.')
    refuse = true
  }
  if (refuse) event.cancel()
})

// ------------------------------------------------------------
//  Le combat : un coup pris d'une créature ou d'un joueur, ou donné.
//  Jamais une exception qui remonte (le gestionnaire est appelé à
//  chaque dégât du serveur, une erreur ici inonde le journal).
// ------------------------------------------------------------
EntityEvents.hurt(event => {
  try {
    // LivingEntityHurtEventJS.java:23 et 28 (getEntity, getSource)
    let auteur = ACCES.auteur(event.getSource())
    if (auteur == null) return          // chute, lave, faim, suffocation : pas un coup
    let victime = event.getEntity()
    let maintenant = Date.now()
    suiviCoups.vus++
    if (ACCES.estJoueur(victime)) dernierCoup[String(ACCES.uuid(victime))] = maintenant
    if (ACCES.estJoueur(auteur) && !meme(auteur, victime)) {
      dernierCoup[String(ACCES.uuid(auteur))] = maintenant
      suiviCoups.dernierAuteur = ACCES.nom(auteur)
    } else if (ACCES.estJoueur(victime)) {
      suiviCoups.dernierAuteur = 'une créature, sur ' + ACCES.nom(victime)
    }
  } catch (e) {
    suiviCoups.erreurs++
    journal('combat', e)
  }
})

// ------------------------------------------------------------
//  Chaque seconde : le compteur de combat dans la barre d'action, et
//  l'arbre des commandes renvoyé aux joueurs marqués par le datapack
//  (étiquette bmc4_resync, posée à l'achat d'un rang et à la connexion).
// ------------------------------------------------------------
let horloge = 0
ServerEvents.tick(event => {
  horloge++
  if (horloge % 20 != 0) return
  let server = event.getServer()
  let tous
  try {
    tous = ACCES.joueurs(server)
  } catch (e) {
    journal('liste des joueurs', e)
    return
  }
  for (let i = 0; i < tous.length; i++) {
    let p = tous[i]
    try {
      let nom = ACCES.nom(p)
      let cle = String(ACCES.uuid(p))
      let reste = combatRestant(p)
      if (reste > 0) {
        server.runCommandSilent('title ' + nom + ' actionbar ' + JSON.stringify({ text: '⚔ En combat : ' + secondes(reste) + ' s', color: 'red' }))
        compteurAffiche[cle] = true
      } else if (compteurAffiche[cle]) {
        server.runCommandSilent('title ' + nom + ' actionbar ""')
        delete compteurAffiche[cle]
      }
      if (server.runCommandSilent('execute if entity @a[name=' + nom + ',tag=bmc4_resync]') > 0) {
        server.runCommandSilent('tag ' + nom + ' remove bmc4_resync')
        ACCES.renvoyerCommandes(server, p)
      }
    } catch (e) {
      journal('boucle de la seconde', e)
    }
  }
})

// ------------------------------------------------------------
//  /prestige diagnostic : réservé à l'op. Essaie chaque appel de ACCES
//  sur le joueur qui la tape, une ligne OK / ÉCHEC par appel.
// ------------------------------------------------------------
ServerEvents.commandRegistry(event => {
  let Commands = event.getCommands()
  event.register(Commands.literal('prestige').then(Commands.literal('diagnostic').executes(ctx => {
    let source = ctx.getSource()
    let server = source.getServer()
    let p = source.getPlayerOrException()
    let nom = ACCES.nom(p)
    let ligne = (ok, quoi, detail) => server.runCommandSilent('tellraw ' + nom + ' ' + JSON.stringify(['',
      { text: ok ? 'OK     ' : 'ÉCHEC  ', color: ok ? 'green' : 'red', bold: true },
      { text: quoi + ' : ', color: 'gray' }, { text: String(detail), color: 'white' }]))
    if (!ACCES.estOp(p)) {
      server.runCommandSilent('tellraw ' + nom + ' ' + JSON.stringify(['', { text: '/prestige diagnostic refusé : ', color: 'red' },
        { text: 'réservé aux opérateurs.', color: 'red' }, { text: ' Pour ton rang : /prestige.', color: 'gray' }]))
      return 1
    }
    let essai = (quoi, f) => {
      try { ligne(true, quoi, f()) } catch (e) { ligne(false, quoi, e) }
    }
    server.runCommandSilent('tellraw ' + nom + ' ' + JSON.stringify({ text: '— Diagnostic de bmc4_garde.js —', color: 'gold' }))
    essai('getUsername()', () => ACCES.nom(p))
    essai('getUuid()', () => String(ACCES.uuid(p)))
    essai('isPlayer()', () => ACCES.estJoueur(p))
    essai('isOp()', () => ACCES.estOp(p))
    essai('équipe du raid (isOnScoreboardTeam)', () => ACCES.enRaid(p))
    essai('score bmc4_rangs (runCommandSilent)', () => { let s = ACCES.score(server, nom, 'bmc4_rangs'); return s == null ? 'aucun score' : s })
    essai('getPlayers()', () => ACCES.joueurs(server).length + ' joueur(s)')
    essai('dimension (getLevel().getDimensionKey())', () => String(p.getLevel().getDimensionKey()))
    essai('position (getBlock().getPos())', () => String(p.getBlock().getPos()))
    essai('case FTB (ChunkDimPos(Entity))', () => String(ACCES.caseDe(p)))
    essai('claim de la case actuelle', () => { let f = ACCES.claimEtranger(p, ACCES.caseDe(p)); return f == null ? 'aucun claim étranger ici' : 'claim de ' + f })
    essai('case d\'une position (ChunkDimPos(ResourceKey, ChunkPos))', () => String(new ChunkDimPos(p.getLevel().getDimensionKey(), new ChunkPos(p.getBlock().getPos()))))
    essai('FTB Essentials : homes', () => { let d = ACCES.essentials(p); return d == null ? 'aucune donnée' : nomsDesHomes(d).length + ' home(s)' })
    essai('FTB Essentials : /back', () => { let d = ACCES.essentials(p); return d == null ? 'aucune donnée' : d.teleportHistory.size() + ' lieu(x) en mémoire' })
    essai('FTB Essentials : demandes TPA', () => TPACommands.REQUESTS.size() + ' en attente')
    essai('auteur d\'un coup (DamageSource.getActual())', () => suiviCoups.vus + ' coup(s) suivi(s), ' + suiviCoups.erreurs + ' erreur(s), dernier : ' + (suiviCoups.dernierAuteur || 'aucun encore'))
    essai('combat restant', () => (combatRestant(p) > 0 ? secondes(combatRestant(p)) + ' s' : 'hors combat'))
    essai('cache des profils (getProfileCache)', () => server.getProfileCache().get(nom).isPresent())
    essai('arbre des commandes renvoyé (sendCommands)', () => { ACCES.renvoyerCommandes(server, p); return 'envoyé' })
    return 1
  })))
})
