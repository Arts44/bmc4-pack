// priority: 0
// ============================================================
//  bmc4_v64_sculk.js — Le cri du Sculk Special bridé (BMC-101)
//
//  Va dans <serveur>/kubejs/startup_scripts/ : un REDÉMARRAGE est
//  nécessaire, les écouteurs Forge ne se rechargent pas.
//
//  Décision d'Arthur (11 octobre) : le cocktail Sculk Special de
//  Kaleidoscope Tavern reste, mais son cri est plafonné à 8 points de vie
//  (4 cœurs) contre un joueur, et il ne peut pas l'achever.
//
//  Ce que fait le cri, lu dans le jar (ShriekAttackEffect,
//  kaleidoscopetavern 1.2.0) : dans l'axe du regard, jusqu'à 32 blocs,
//  chaque créature touchée prend 1,2 × la vie ACTUELLE du buveur
//  (LivingEntity.getHealth), en dégâts DamageSources.sonicBoom(buveur) :
//  type minecraft:sonic_boom, qui ignore l'armure. Aucune option du mod.
//
//  Reconnaître le cri. Les dégâts sonic_boom (msgId « sonic_boom »,
//  DamageTypes du jar 1.20.1 ; aucun autre type de dégâts du pack n'a ce
//  msgId) ont trois autres sources dans le pack :
//    - le Warden : l'auteur est le Warden, pas un joueur ;
//    - le souffle du dragon de sculk de Dragon Mounts
//      (SculkDragonBreathBall) : sonicBoom(cible), l'auteur est la victime
//      elle-même ;
//    - le Sonorous Staff de Deeper and Darker (SonorousStaffItem.releaseUsing) :
//      l'auteur est le joueur, qui tient encore le bâton à ce moment-là
//      (releaseUsing précède stopUsingItem).
//  Est donc traité comme le cri : sonic_boom, victime joueur, auteur un
//  AUTRE joueur, qui ne tient de Sonorous Staff dans aucune main.
//
//  Où plafonner. LivingDamageEvent, lu dans LivingEntity.actuallyHurt du
//  jar Forge 47.4.20 : il passe APRÈS l'armure, l'absorption magique et
//  les cœurs d'absorption, juste avant setHealth. Le montant y est la vie
//  réellement perdue : min(montant, 8, vie − 1), jamais négatif.
//
//  FAIL-CLOSED : si l'examen de l'auteur lève une erreur, des dégâts
//  sonic_boom sur un joueur sont plafonnés quand même, et l'erreur est
//  écrite une fois dans le journal.
//
//  LES NOMS JAVA (règle 8) : getSource, getEntity, getAmount, setAmount
//  (LivingDamageEvent, Forge, non obfusqué) ; getType() pour getMsgId et
//  getActual() pour getEntity (DamageSourceMixin de KubeJS, @RemapForJS) ;
//  isPlayer, getMainHandItem, getOffHandItem, getId (EntityKJS,
//  LivingEntityKJS, ItemStackKJS) ; getUuid (EntityMixin, @RemapForJS) ;
//  getHealth (nom Mojang, traduit par Rhino).
// ============================================================

const BMC4_SCULK_PLAFOND = 8
const BMC4_SCULK_BATON = 'deeperdarker:sonorous_staff'

let bmc4SculkErreurs = {}
function bmc4SculkJournal(cle, e) {
  if (bmc4SculkErreurs[cle]) return
  bmc4SculkErreurs[cle] = true
  console.error('bmc4_v64_sculk : ' + cle + ' : ' + e)
}

// true si les dégâts viennent du cri d'un autre joueur.
function bmc4SculkEstLeCri(victime, source) {
  let auteur = source.getActual()
  if (auteur == null || !auteur.isPlayer()) return false
  if (String(auteur.getUuid()) == String(victime.getUuid())) return false
  if (String(auteur.getMainHandItem().getId()) == BMC4_SCULK_BATON) return false
  if (String(auteur.getOffHandItem().getId()) == BMC4_SCULK_BATON) return false
  return true
}

ForgeEvents.onEvent('net.minecraftforge.event.entity.living.LivingDamageEvent', event => {
  let source = event.getSource()
  if (String(source.getType()) != 'sonic_boom') return
  let victime = event.getEntity()
  if (victime == null || !victime.isPlayer()) return
  let cri = true
  try {
    cri = bmc4SculkEstLeCri(victime, source)
  } catch (e) {
    bmc4SculkJournal('auteur', e)
  }
  if (!cri) return
  let permis = Math.max(0, Math.min(BMC4_SCULK_PLAFOND, victime.getHealth() - 1))
  if (event.getAmount() > permis) event.setAmount(permis)
})
