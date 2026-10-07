// priority: 0
// ============================================================
//  bmc4_teleportations.js — Pas de fuite en combat ni en raid (BMC-94)
//
//  Va dans <serveur>/kubejs/startup_scripts/ (un redémarrage du serveur
//  est nécessaire : les écouteurs Forge ne se rechargent pas).
//
//  Décision d'Arthur (7 octobre) : comme /home, /back et /tpa
//  (bmc4_garde.js), les téléportations SANS commande sont refusées
//  pendant les 15 s de combat et pendant un créneau de raid, avec un
//  message qui dit pourquoi. Les perles de l'Ender restent permises.
//
//  Chaque écouteur demande la décision à global.bmc4GardeTeleport,
//  définie par bmc4_garde.js (server_scripts). Si elle n'existe pas
//  (scripts serveur non chargés), la téléportation est REFUSÉE :
//  fail-closed, comme la garde.
//
//  Les événements, lus dans les jars du serveur le 7 octobre :
//    Waystones 14.1.20   WaystoneTeleportEvent$Pre, annulable (BalmEvent
//                        @Cancelable, posté sur MinecraftForge.EVENT_BUS ;
//                        PlayerWaystoneManager teste isCanceled() et
//                        renvoie WaystoneTeleportError$CancelledByEvent).
//                        Couvre pierres, parchemins, warp stone, plaques.
//    Iron's Spells 3.16.3 SpellPreCastEvent, @Cancelable, getSpellId() :
//                        refusé au lancement, parchemin ou livre.
//    Forge               EntityTeleportEvent et ses sous-classes : fruit
//                        de chorus, et SpellTeleportEvent d'Iron's Spells
//                        (l'esquive « evasion », déclenchée par un coup).
//                        Laissés passer : EnderPearl (décision d'Arthur),
//                        TeleportCommand et SpreadPlayersCommand (le staff).
//    Forge               EntityTravelToDimensionEvent : portails qui
//                        passent par Entity.changeDimension (Twilight,
//                        Aether…). Les portails d'Immersive Portals ne
//                        l'émettent pas : non couverts.
// ============================================================

// Les sorts qui déplacent le lanceur par téléportation (descriptions du
// fichier lang du jar). burning_dash et shadow_slash sont des ruées :
// pas de téléportation, laissés.
const BMC4_SORTS_TP = {
  'irons_spellbooks:teleport': 'Le sort Téléportation',
  'irons_spellbooks:blood_step': 'Le sort Pas de sang',
  'irons_spellbooks:frost_step': 'Le sort Pas de givre',
  'irons_spellbooks:thunder_step': 'Le sort Pas de foudre',
  'irons_spellbooks:evasion': 'Le sort Esquive',
  'irons_spellbooks:portal': 'Le sort Portail',
  'irons_spellbooks:recall': 'Le sort Rappel',
  'irons_spellbooks:pocket_dimension': 'Le sort Dimension de poche'
}

let bmc4TpErreur = {}
function bmc4TpJournal(cle, e) {
  if (bmc4TpErreur[cle]) return
  bmc4TpErreur[cle] = true
  console.error('bmc4_teleportations : ' + cle + ' : ' + e)
}

// true = refusé. Le message au joueur est envoyé par la garde ; sans
// garde, on le dit ici.
function bmc4TpRefuse(joueur, refus) {
  try {
    if (joueur == null || !joueur.isPlayer()) return false
    if (typeof global.bmc4GardeTeleport !== 'function') {
      bmc4TpJournal('garde absente', 'global.bmc4GardeTeleport non défini')
      joueur.tell(Text.red(refus + ' refusé : la garde ne répond pas. Préviens le staff.'))
      return true
    }
    return global.bmc4GardeTeleport(joueur, refus) == true
  } catch (e) {
    bmc4TpJournal(refus, e)
    return true
  }
}

ForgeEvents.onEvent('net.blay09.mods.waystones.api.WaystoneTeleportEvent$Pre', event => {
  let ctx = event.getContext()
  if (bmc4TpRefuse(ctx.getEntity(), 'La téléportation par waystone')) event.setCanceled(true)
})

ForgeEvents.onEvent('io.redspace.ironsspellbooks.api.events.SpellPreCastEvent', event => {
  let nom = BMC4_SORTS_TP[String(event.getSpellId())]
  if (nom == null) return
  if (bmc4TpRefuse(event.getEntity(), nom)) event.setCanceled(true)
})

ForgeEvents.onEvent('net.minecraftforge.event.entity.EntityTeleportEvent', event => {
  let sorte = String(event.getClass().getName())
  if (sorte.endsWith('$EnderPearl') || sorte.endsWith('$TeleportCommand') || sorte.endsWith('$SpreadPlayersCommand')) return
  let refus = sorte.endsWith('$ChorusFruit') ? 'Le fruit de chorus'
    : sorte.indexOf('SpellTeleportEvent') >= 0 ? 'La téléportation par sort'
    : 'La téléportation'
  if (bmc4TpRefuse(event.getEntity(), refus)) event.setCanceled(true)
})

ForgeEvents.onEvent('net.minecraftforge.event.entity.EntityTravelToDimensionEvent', event => {
  if (bmc4TpRefuse(event.getEntity(), 'Le passage de portail')) event.setCanceled(true)
})
