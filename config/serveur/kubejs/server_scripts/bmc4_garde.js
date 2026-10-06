// priority: 0
// ============================================================
//  bmc4_garde.js — La garde des commandes de FTB Essentials (BMC-91)
//
//  Va dans <serveur>/kubejs/server_scripts/. Lit global.BMC4
//  (bmc4_00_table.js, généré depuis config/rangs/rangs.toml).
//
//  Chaque commande d'un joueur passe ici AVANT d'être exécutée
//  (ServerEvents.command = CommandEvent de Forge, que Forge lance
//  même quand la commande n'existe pas ou n'est pas permise).
//  Un refus annule la commande et l'explique : ce qui est refusé,
//  pourquoi, et ce que le joueur peut faire ou quand. Jamais le
//  message brut de Minecraft ni l'anglais de FTB Essentials.
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
//  Les claims de l'équipe serveur (le Marché Flottant) ne comptent
//  pas comme ceux d'une faction.
//
//  Sans KubeJS, ces blocages ne tiennent plus : le retour arrière
//  remplace ranks.snbt par ranks-sans-kubejs.snbt, qui ferme ces
//  commandes à tous les joueurs.
// ============================================================

const FTBChunksAPI = Java.loadClass('dev.ftb.mods.ftbchunks.api.FTBChunksAPI')
const ChunkDimPos = Java.loadClass('dev.ftb.mods.ftblibrary.math.ChunkDimPos')
const FTBEPlayerData = Java.loadClass('dev.ftb.mods.ftbessentials.util.FTBEPlayerData')
const TPACommands = Java.loadClass('dev.ftb.mods.ftbessentials.command.TPACommands')

const COMBAT_MS = 15000

// Dernier coup pris ou donné, par UUID (en mémoire : un redémarrage
// remet tout le monde hors combat, ce qui est sans danger).
const dernierCoup = {}
// Dernière téléportation acceptée, par UUID et par famille.
const derniereTp = {}

// Les commandes que la configuration de FTB Essentials coupe : sans
// ce texte, le joueur lirait « Unknown or incomplete command ».
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

// ------------------------------------------------------------
//  Outils
// ------------------------------------------------------------
function dire(server, joueur, refus, raison, suite) {
  let json = ['',
    { text: refus + ' refusé : ', color: 'red' },
    { text: raison, color: 'red' }]
  if (suite) json.push({ text: ' ' + suite, color: 'gray' })
  server.runCommandSilent('tellraw ' + joueur.username + ' ' + JSON.stringify(json))
}

function score(server, nom, objectif) {
  let sb = server.scoreboard
  let obj = sb.getObjective(objectif)
  if (!obj || !sb.hasPlayerScore(nom, obj)) return null
  return sb.getOrCreatePlayerScore(nom, obj).getScore()
}

function rangDe(server, joueur) {
  return score(server, joueur.username, 'bmc4_rangs') || 0
}

function nomRang(n) {
  if (n <= 0) return 'aucun rang'
  let r = global.BMC4.rangs[Math.min(n, global.BMC4.rangs.length) - 1]
  return r.affiche
}

// Rhino peut envelopper deux fois le même objet Java : on compare les UUID,
// jamais les enveloppes.
function meme(a, b) {
  return a != null && b != null && String(a.getUUID()) == String(b.getUUID())
}

function estStaff(joueur) {
  return joueur.hasPermissions(2)
}

function secondes(ms) {
  return Math.max(1, Math.ceil(ms / 1000))
}

// Combat : millisecondes restantes, 0 si hors combat.
function combatRestant(joueur) {
  let t = dernierCoup[String(joueur.uuid)]
  if (!t) return 0
  return Math.max(0, COMBAT_MS - (Date.now() - t))
}

function enRaid(joueur) {
  let equipe = joueur.team
  return equipe != null && equipe.name == 'bmc4_raid_actif'
}

function finDuRaid(server) {
  let h = score(server, '#fin_h', 'bmc4_raid')
  let m = score(server, '#fin_m', 'bmc4_raid')
  if (h == null || m == null) return 'la fin du créneau'
  return h + ' h ' + (m < 10 ? '0' : '') + m
}

// Le nom de la faction si (dimension, x, z) est dans le claim d'une
// équipe dont le joueur n'est pas membre ; null sinon.
function claimEtranger(joueur, dimension, x, z) {
  let chunk = FTBChunksAPI.api().getManager().getChunk(new ChunkDimPos(dimension, x >> 4, z >> 4))
  if (chunk == null) return null
  let donnees = chunk.getTeamData()
  let equipe = donnees.getTeam()
  if (equipe.isServerTeam()) return null
  if (donnees.isTeamMember(joueur.getUUID())) return null
  return equipe.getName().getString()
}

function claimIci(joueur) {
  let p = joueur.blockPosition()
  return claimEtranger(joueur, joueur.level.dimension(), p.getX(), p.getZ())
}

function claimDe(joueur, pos) {   // pos : TeleportPos de FTB Essentials
  let b = pos.getPos()
  return claimEtranger(joueur, pos.getDimension(), b.getX(), b.getZ())
}

function donneesEss(joueur) {
  let o = FTBEPlayerData.getOrCreate(joueur)
  return o.isPresent() ? o.get() : null
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
  if (estStaff(joueur)) return 10
  let max = 0
  for (const n in global.BMC4.homes) {
    if (rang >= Number(n)) max = Math.max(max, global.BMC4.homes[n])
  }
  return max
}

// Le prochain rang qui donne plus de homes : [rang, nombre], ou null.
function prochainPalierHomes(rang) {
  let meilleur = null
  for (const n in global.BMC4.homes) {
    let k = Number(n)
    if (k > rang && (meilleur == null || k < meilleur[0])) meilleur = [k, global.BMC4.homes[n]]
  }
  return meilleur
}

// ------------------------------------------------------------
//  Les contrôles d'état : combat, raid, claim du lieu actuel
// ------------------------------------------------------------
// Rend true si un refus a été dit.
function bloque(server, joueur, refus, quiEstConcerne) {
  let autre = quiEstConcerne != null && !meme(quiEstConcerne, joueur)
  let qui = autre ? quiEstConcerne : joueur
  let reste = combatRestant(qui)
  if (reste > 0) {
    if (autre) {
      dire(server, joueur, refus, qui.username + ' est en combat.', 'Réessaie dans ' + secondes(reste) + ' s.')
    } else {
      dire(server, joueur, refus, 'tu as pris ou donné un coup il y a moins de 15 secondes.',
        'Réessaie dans ' + secondes(reste) + ' s.')
    }
    return true
  }
  if (enRaid(qui)) {
    if (autre) {
      dire(server, joueur, refus, qui.username + ' est engagé dans un raid, jusqu\'à ' + finDuRaid(server) + '.',
        'Réessaie après le raid.')
    } else {
      dire(server, joueur, refus, 'un raid est en cours pour ta faction, jusqu\'à ' + finDuRaid(server) + '.',
        'Les téléportations reviennent à la fin du raid.')
    }
    return true
  }
  return false
}

function bloqueClaim(server, joueur, refus, quiBouge) {
  let qui = quiBouge || joueur
  let faction = claimIci(qui)
  if (faction == null) return false
  if (meme(qui, joueur)) {
    dire(server, joueur, refus, 'tu es dans le claim de ' + faction + '.',
      'Sors de leur territoire pour l\'utiliser.')
  } else {
    dire(server, joueur, refus, qui.username + ' est dans le claim de ' + faction + '.',
      'Il doit d\'abord en sortir.')
  }
  return true
}

function bloqueDelai(server, joueur, refus, famille, enregistrer) {
  let delai = (global.BMC4.delais[famille] || 0) * 1000
  let cle = String(joueur.uuid) + ':' + famille
  let depuis = Date.now() - (derniereTp[cle] || 0)
  if (depuis < delai) {
    dire(server, joueur, refus, 'une téléportation par ' + (delai / 1000) + ' secondes.',
      'Réessaie dans ' + secondes(delai - depuis) + ' s.')
    return true
  }
  if (enregistrer) derniereTp[cle] = Date.now()
  return false
}

// ------------------------------------------------------------
//  Les commandes une à une
// ------------------------------------------------------------
function garderHome(server, joueur, args) {
  let d = donneesEss(joueur)
  if (d == null) return false
  let nom = (args.join(' ') || 'home').toLowerCase()
  let pos = homeNomme(d, nom)
  if (pos == null) {
    let noms = nomsDesHomes(d)
    dire(server, joueur, '/home', 'tu n\'as pas de home nommé « ' + nom + ' ».',
      noms.length ? 'Tes homes : ' + noms.join(', ') + '.' : 'Pose-en un avec /sethome <nom>.')
    return true
  }
  if (bloque(server, joueur, '/home')) return true
  if (bloqueClaim(server, joueur, '/home')) return true
  let faction = claimDe(joueur, pos)
  if (faction != null) {
    dire(server, joueur, '/home', 'ton home « ' + nom + ' » est dans le claim de ' + faction + '.',
      'Un home ne ramène pas dans le territoire d\'une autre faction : supprime-le (/delhome ' + nom + ').')
    return true
  }
  return bloqueDelai(server, joueur, '/home', 'home', true)
}

function garderSethome(server, joueur, args, rang) {
  let d = donneesEss(joueur)
  if (d == null) return false
  let nom = (args.join(' ') || 'home').toLowerCase()
  let faction = claimIci(joueur)
  if (faction != null) {
    dire(server, joueur, '/sethome', 'tu ne peux pas poser de home dans le claim d\'une autre faction (ici, ' + faction + ').',
      'Pose-le dans ton claim ou hors claim.')
    return true
  }
  let noms = nomsDesHomes(d)
  let max = maxHomes(joueur, rang)
  if (noms.indexOf(nom) < 0 && noms.length >= max) {
    let suivant = prochainPalierHomes(rang)
    dire(server, joueur, '/sethome', 'tu as déjà ' + noms.length + ' home' + (noms.length > 1 ? 's' : '')
      + ', le maximum de ton rang (' + nomRang(rang) + ').',
      'Remplace-en un (/sethome ' + (noms[0] || 'home') + ') ou supprime-le (/delhome <nom>)'
      + (suivant ? ' ; le rang ' + nomRang(suivant[0]) + ' en donne ' + suivant[1] + '.' : '.'))
    return true
  }
  return false
}

function garderDelhome(server, joueur, args) {
  let d = donneesEss(joueur)
  if (d == null) return false
  let nom = (args.join(' ') || 'home').toLowerCase()
  let noms = nomsDesHomes(d)
  if (noms.indexOf(nom) < 0) {
    dire(server, joueur, '/delhome', 'tu n\'as pas de home nommé « ' + nom + ' ».',
      noms.length ? 'Tes homes : ' + noms.join(', ') + '.' : 'Tu n\'en as aucun.')
    return true
  }
  return false
}

function garderBack(server, joueur) {
  let d = donneesEss(joueur)
  if (d == null) return false
  if (d.teleportHistory.isEmpty()) {
    dire(server, joueur, '/back', 'il n\'y a aucun lieu où revenir.',
      '/back ramène à ta dernière téléportation ou à ta dernière mort.')
    return true
  }
  if (bloque(server, joueur, '/back')) return true
  if (bloqueClaim(server, joueur, '/back')) return true
  let faction = claimDe(joueur, d.teleportHistory.getLast())
  if (faction != null) {
    dire(server, joueur, '/back', 'ton dernier lieu est dans le claim de ' + faction + '.',
      '/back ne ramène pas dans le territoire d\'une autre faction : rejoins-le à pied.')
    return true
  }
  return bloqueDelai(server, joueur, '/back', 'back', true)
}

function joueurNomme(server, nom) {
  if (!nom) return null
  return server.getPlayerList().getPlayerByName(nom)
}

// Contrôle commun à /tpa, /tpahere et /tpaccept : « bouge » rejoint « vers ».
function garderTrajet(server, joueur, refus, bouge, vers, enregistrer) {
  if (bloque(server, joueur, refus, bouge)) return true
  if (bloque(server, joueur, refus, vers)) return true
  if (bloqueClaim(server, joueur, refus, bouge)) return true
  // La destination : le lieu où se tient « vers », vu depuis la faction de « bouge ».
  let p = vers.blockPosition()
  let faction = claimEtranger(bouge, vers.level.dimension(), p.getX(), p.getZ())
  if (faction != null) {
    dire(server, joueur, refus, (meme(vers, joueur) ? 'tu es' : vers.username + ' est') + ' dans le claim de ' + faction
      + (meme(bouge, joueur) ? '' : ', une autre faction pour ' + bouge.username) + '.',
      'Pas de téléportation dans le territoire d\'une autre faction.')
    return true
  }
  return bloqueDelai(server, bouge, refus, 'tpa', enregistrer)
}

function garderTpa(server, joueur, args, ici) {
  let refus = ici ? '/tpahere' : '/tpa'
  let cible = joueurNomme(server, args[0])
  if (cible == null) {
    dire(server, joueur, refus, args[0] ? 'aucun joueur nommé « ' + args[0] + ' » n\'est connecté.' : 'il manque le pseudo.',
      'Écris ' + refus + ' <pseudo exact> d\'un joueur connecté.')
    return true
  }
  if (meme(cible, joueur)) {
    dire(server, joueur, refus, 'c\'est toi.', 'Écris le pseudo d\'un autre joueur.')
    return true
  }
  let src = donneesEss(joueur)
  let dst = donneesEss(cible)
  let it = TPACommands.REQUESTS.values().iterator()
  while (it.hasNext()) {
    let r = it.next()
    if (r.source().equals(src) && r.target().equals(dst)) {
      dire(server, joueur, refus, 'une demande vers ' + cible.username + ' attend déjà sa réponse.',
        'Attends qu\'il l\'accepte ou la refuse.')
      return true
    }
  }
  return ici ? garderTrajet(server, joueur, refus, cible, joueur, false)
    : garderTrajet(server, joueur, refus, joueur, cible, false)
}

function garderTpaccept(server, joueur, args) {
  let r = TPACommands.REQUESTS.get(args[0] || '')
  if (r == null) {
    dire(server, joueur, '/tpaccept', 'cette demande n\'existe pas ou n\'est plus valable.',
      'Demande à l\'autre joueur de la refaire.')
    return true
  }
  let source = server.getPlayerList().getPlayer(r.source().getUuid())
  if (source == null) {
    dire(server, joueur, '/tpaccept', 'le joueur qui a fait la demande s\'est déconnecté.', null)
    return true
  }
  // r.here() : la cible (celui qui accepte) rejoint l'auteur de la demande.
  return r.here() ? garderTrajet(server, joueur, '/tpaccept', joueur, source, true)
    : garderTrajet(server, joueur, '/tpaccept', source, joueur, true)
}

function garderNickname(server, joueur, args) {
  let nom = args.join(' ').trim()
  if (!nom) return false
  let cache = server.getProfileCache()
  let trouve = cache == null ? null : cache.get(nom)
  if (trouve != null && trouve.isPresent() && String(trouve.get().getName()).toLowerCase() != String(joueur.username).toLowerCase()) {
    dire(server, joueur, '/nickname', '« ' + nom + ' » est le pseudo d\'un autre joueur.',
      'Le règlement interdit de prendre le pseudo d\'un autre : choisis-en un qui n\'appartient à personne.')
    return true
  }
  return false
}

// ------------------------------------------------------------
//  L'aiguillage
// ------------------------------------------------------------
ServerEvents.command(event => {
  let source = event.getParseResults().getContext().getSource()
  let joueur = source.getPlayer()
  if (joueur == null) return   // console, bot (RCON), fonctions : pas concernés

  let server = source.getServer()
  let mots = String(event.getInput()).trim().replace(/^\//, '').split(/\s+/)
  let commande = mots[0].toLowerCase()
  let args = mots.slice(1)

  if (COUPEES[commande]) {
    dire(server, joueur, '/' + commande, 'commande coupée sur BMC4, ' + COUPEES[commande] + '.',
      commande == 'spawn' || commande == 'playerspawn' || commande == 'warp' ? 'Les waystones restent là pour voyager.' : null)
    event.cancel()
  }

  // /feed des joueurs : le datapack (rang, délai de 30 minutes, messages).
  // Celui de FTB Essentials reste au staff.
  if (commande == 'feed' && !estStaff(joueur)) {
    server.runCommandSilent('execute as ' + joueur.username + ' run function bmc4:rangs/g_manger')
    event.cancel()
  }

  let requis = global.BMC4.commandes[commande]
  if (requis == null) return

  let rang = rangDe(server, joueur)
  if (requis > 0 && rang < requis && !estStaff(joueur)) {
    dire(server, joueur, '/' + commande, 'elle s\'obtient au rang ' + nomRang(requis)
      + ' (ton rang : ' + nomRang(rang) + ').',
      'Voir ce qu\'il te manque : /prestige.')
    event.cancel()
  }

  let refuse = false
  if (commande == 'home') refuse = garderHome(server, joueur, args)
  else if (commande == 'sethome') refuse = garderSethome(server, joueur, args, rang)
  else if (commande == 'delhome') refuse = garderDelhome(server, joueur, args)
  else if (commande == 'back') refuse = garderBack(server, joueur)
  else if (commande == 'tpa') refuse = garderTpa(server, joueur, args, false)
  else if (commande == 'tpahere') refuse = garderTpa(server, joueur, args, true)
  else if (commande == 'tpaccept') refuse = garderTpaccept(server, joueur, args)
  else if (commande == 'nickname') refuse = garderNickname(server, joueur, args)
  if (refuse) event.cancel()
})

// ------------------------------------------------------------
//  Le combat : un coup pris d'une créature ou d'un joueur, ou donné
// ------------------------------------------------------------
EntityEvents.hurt(event => {
  let victime = event.getEntity()
  let auteur = event.getSource().getEntity()   // le tireur pour une flèche
  if (auteur == null) return                      // chute, lave, faim : pas un coup
  let maintenant = Date.now()
  if (victime.isPlayer()) dernierCoup[String(victime.getUUID())] = maintenant
  if (auteur.isPlayer() && !meme(auteur, victime)) dernierCoup[String(auteur.getUUID())] = maintenant
})
