// priority: 0
// ============================================================
//  bmc4_triche.js — Le journal des commandes des ops, et les mods de
//  triche refusés à la connexion (BMC-94, décisions 7 et 8 d'Arthur)
//
//  Va dans <serveur>/kubejs/server_scripts/ (rechargeable à chaud :
//  « kubejs reload server_scripts »).
//
//  Chaque ligne destinée au staff est écrite dans le journal de KubeJS
//  (logs/kubejs/server.log, et latest.log), avec un marqueur que le bot
//  (journal-kubejs.js) relit par SFTP et publie :
//    [bmc4-ops] {...}     → #console
//    [bmc4-alerte] {...}  → #anti-triche
//
//  1. LE JOURNAL DES OPS. Toute commande tapée par un joueur de niveau
//     d'opérateur 2 ou plus, quel que soit son nom (xp, data, ftbranks,
//     kill… compris : le filtre ignoredCommands de Discord Integration
//     les cache toutes depuis le 6 octobre). Ni la console du panel ni RCON :
//     la console porte le même nom de source (« Server ») que les commandes
//     internes de KubeJS (runCommandSilent), des milliers par jour, et
//     RCON est le bot.
//     Le niveau, pas isOp() : c'est ce que le jeu vérifie pour une
//     commande, et la règle 9 du contrôle garde isOp() pour les exemptions
//     (il n'y en a aucune ici : on écrit, on ne laisse rien passer).
//     Noms SRG publics de CommandSourceStack (javap du jar srg 1.20.1) :
//     m_230896_ getPlayer (null si ce n'est pas un joueur), m_6761_
//     hasPermission.
//
//  2. LES MODS DE TRICHE. À la connexion, la liste des identifiants de mods
//     que le client a déclarés (handshake FML) : Forge 47.4.20,
//     NetworkHooks.getConnectionData(Connection).getModList(). La Connection
//     du joueur : ServerPlayer.f_8906_ (connection) puis
//     ServerGamePacketListenerImpl.f_9742_ (connection), rendu public par
//     l'accesstransformer de Forge (« public …ServerGamePacketListenerImpl
//     f_9742_ # connection »).
//     REFUS : trois identifiants seulement, prouvés « triche seule » par le
//     mods.toml de leur source (point d'étape BMC-94, 7 octobre). Le joueur
//     est déconnecté avec le nom du mod et la marche à suivre ; le staff est
//     prévenu. Un client modifié peut retirer un identifiant de sa liste :
//     ceci n'attrape que les tricheurs naïfs.
//     ALERTE SEULE : les mods à double usage dont l'identifiant est prouvé.
//     Si la liste est illisible : alerte, jamais de refus (« quand c'est
//     certain » seulement).
// ============================================================

const BMC4_MODS_REFUSES = {
  cheatutils: 'CheatUtils (X-ray, kill aura)',
  atianxray: 'Xray Mod',
  xray: 'Advanced XRay'
}
const BMC4_MODS_ALERTE = {
  zergatulfreecam: 'FreeCam (Zergatul)',
  autoclickermod: 'AutoClicker Mod'
}

let bmc4TricheErreurs = {}
function bmc4TricheJournal(cle, e) {
  if (bmc4TricheErreurs[cle]) return
  bmc4TricheErreurs[cle] = true
  console.error('bmc4_triche : ' + cle + ' : ' + e)
}

function bmc4Alerte(objet) {
  objet.heure = Date.now()
  console.info('[bmc4-alerte] ' + JSON.stringify(objet))
}

// La liste des identifiants de mods déclarés par le client, ou null.
global.bmc4ModsDuClient = p => {
  let NetworkHooks = Java.loadClass('net.minecraftforge.network.NetworkHooks')
  let donnees = NetworkHooks.getConnectionData(p.f_8906_.f_9742_)
  if (donnees == null) return null
  let liste = donnees.getModList()
  let out = []
  for (let i = 0; i < liste.size(); i++) out.push(String(liste.get(i)))
  return out
}

// ---------- 1. Le journal des ops ----------
ServerEvents.command(event => {
  try {
    let source = event.getParseResults().getContext().getSource()
    let joueur = source.m_230896_()
    if (joueur == null || !source.m_6761_(2)) return
    console.info('[bmc4-ops] ' + JSON.stringify({ qui: String(joueur.getUsername()), commande: String(event.getInput()), heure: Date.now() }))
  } catch (e) {
    bmc4TricheJournal('journal des ops', e)
  }
})

// ---------- 2. Les mods de triche ----------
PlayerEvents.loggedIn(event => {
  let p = event.getPlayer()
  let nom = String(p.getUsername())
  let mods = null
  try {
    mods = global.bmc4ModsDuClient(p)
  } catch (e) {
    bmc4TricheJournal('liste des mods', e)
    bmc4Alerte({ type: 'liste-illisible', joueur: nom, erreur: String(e) })
    return
  }
  if (mods == null) {
    bmc4Alerte({ type: 'liste-absente', joueur: nom })
    return
  }
  let refuses = mods.filter(m => BMC4_MODS_REFUSES[m] != null)
  let douteux = mods.filter(m => BMC4_MODS_ALERTE[m] != null)
  if (douteux.length) bmc4Alerte({ type: 'mod-a-surveiller', joueur: nom, mods: douteux.map(m => BMC4_MODS_ALERTE[m] + ' (' + m + ')') })
  if (!refuses.length) return
  let noms = refuses.map(m => BMC4_MODS_REFUSES[m] + ' (' + m + ')').join(', ')
  bmc4Alerte({ type: 'refus-mod', joueur: nom, mods: refuses.map(m => BMC4_MODS_REFUSES[m] + ' (' + m + ')') })
  try {
    p.getServer().runCommandSilent('kick ' + nom + ' Mod interdit sur BMC4 : ' + noms +
      '. Retire-le du dossier mods de ton instance, puis reconnecte-toi.')
  } catch (e) {
    bmc4TricheJournal('déconnexion', e)
    bmc4Alerte({ type: 'refus-echoue', joueur: nom, erreur: String(e) })
  }
})
