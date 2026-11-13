// priority: 0
// ============================================================
//  bmc4_coffres_recharge.js — Les coffres des autres factions, même
//  avec un objet en recharge en main (BMC-107)
//
//  Va dans <serveur>/kubejs/startup_scripts/. Un REDÉMARRAGE du serveur
//  est nécessaire : ForgeEvents.onEvent n'inscrit son écouteur qu'au
//  premier chargement des scripts de démarrage (ForgeEventWrapper.onEvent
//  teste ScriptManager.firstLoad ; ensuite il ne fait qu'un avertissement).
//
//  Le trou : KubeJSBlockEventHandler.rightClick (KubeJS 2001.6.5-build.26)
//  ne poste pas BlockEvents.rightClicked quand
//  player.getCooldowns().isOnCooldown(objet en main) : avec une perle de
//  l'Ender ou un bouclier en recharge en main, la règle des coffres de
//  bmc4_garde.js ne voyait pas le clic. Apex et Farmer's sont en
//  block_interact_mode public dans FTB Chunks : la garde est leur seule
//  protection.
//
//  Cet écouteur reçoit PlayerInteractEvent$RightClickBlock de Forge
//  directement, priorité NORMAL, sans les événements déjà annulés
//  (ForgeEventWrapper.onEvent : addListener(NORMAL, false, classe, …)).
//  La décision n'est pas ici : il appelle global.bmc4GardeCoffre, définie
//  par server_scripts/bmc4_garde.js (même coffreInterdit, même message,
//  même délai d'un message par seconde, et la décision du même clic n'est
//  pas reprise deux fois). `global` est un seul HashMap Java pour tous les
//  types de scripts (BuiltinKubeJSPlugin.GLOBAL) : /reload met à jour la
//  règle sans redémarrage. Même forme que bmc4_teleportations.js
//  (global.bmc4GardeTeleport), en service depuis le 7 octobre.
//
//  Refuser = event.setCanceled(true), rien d'autre. Sous Forge 47.4.20,
//  annuler RightClickBlock met aussi useBlock et useItem à DENY (BMC-108).
//  Autoriser = ne toucher à rien.
//
//  Côté serveur seulement (event.getLevel().isClientSide() faux).
//  FAIL-CLOSED : si la garde manque (scripts serveur non chargés), un bloc
//  à BlockEntity est refusé ; toute erreur refuse, avec « la garde ne
//  répond pas ». Aucune exception ne sort de l'écouteur.
//
//  LES NOMS JAVA (règle 8 du contrôle) : getLevel, getEntity, getPos et
//  setCanceled sont des méthodes de Forge (non obfusquées) ; isClientSide()
//  et getBlockEntity() sont des noms Mojang que Rhino traduit
//  (mm.jsmappings) ; tell et isPlayer viennent de KubeJS (EntityKJS).
//  Aucun nom SRG brut, aucun Java.loadClass.
// ============================================================

const BMC4_RECHARGE_REFUS_MS = 1000
let bmc4RechargeErreur = {}
let bmc4RechargeRefusDit = {}

function bmc4RechargeJournal(cle, e) {
  if (bmc4RechargeErreur[cle]) return
  bmc4RechargeErreur[cle] = true
  console.error('bmc4_coffres_recharge : ' + cle + ' : ' + e)
}

// Le message quand la garde ne peut pas décider, au plus un par seconde.
function bmc4RechargeDire(joueur) {
  try {
    let cle = String(joueur.getUuid())
    let maintenant = Date.now()
    if (maintenant - (bmc4RechargeRefusDit[cle] || 0) < BMC4_RECHARGE_REFUS_MS) return
    bmc4RechargeRefusDit[cle] = maintenant
    joueur.tell(Text.red('Ouvrir ce bloc refusé : la garde ne répond pas. Préviens le staff.'))
  } catch (e) {
    bmc4RechargeJournal('message', e)
  }
}

// true côté client. Si la question elle-même échoue, on fait comme côté
// serveur (le seul où ce script est déployé) : la garde décide.
function bmc4RechargeCoteClient(event) {
  try {
    return event.getLevel().isClientSide() == true
  } catch (e) {
    bmc4RechargeJournal('côté client ou serveur', e)
    return false
  }
}

// true = refusé.
function bmc4RechargeRefuse(event) {
  let joueur = event.getEntity()
  if (joueur == null) return false
  if (typeof global.bmc4GardeCoffre !== 'function') {
    bmc4RechargeJournal('garde absente', 'global.bmc4GardeCoffre non défini')
    let aInventaire = true
    try {
      aInventaire = event.getLevel().getBlockEntity(event.getPos()) != null
    } catch (e) {
      bmc4RechargeJournal('BlockEntity', e)
    }
    if (aInventaire) bmc4RechargeDire(joueur)
    return aInventaire
  }
  return global.bmc4GardeCoffre(joueur, event.getPos()) == true
}

ForgeEvents.onEvent('net.minecraftforge.event.entity.player.PlayerInteractEvent$RightClickBlock', event => {
  try {
    if (bmc4RechargeCoteClient(event)) return
    let refuse = true
    try {
      refuse = bmc4RechargeRefuse(event)
    } catch (e) {
      bmc4RechargeJournal('décision', e)
      try {
        bmc4RechargeDire(event.getEntity())
      } catch (e2) {
        bmc4RechargeJournal('message', e2)
      }
    }
    if (refuse) event.setCanceled(true)
  } catch (e) {
    bmc4RechargeJournal('écouteur', e)
  }
})
