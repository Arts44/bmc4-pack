// priority: 0
// ============================================================
//  bmc4_prestige.js — La commande /prestige (BMC-91)
//
//  Va dans <serveur>/kubejs/server_scripts/.
//
//    /prestige               où j'en suis, boutons [Acheter] [Voir l'échelle]
//    /prestige acheter       le devis : prix, apport, reste ; [Confirmer l'achat]
//    /prestige confirmer     achète, si le devis a moins de 30 secondes
//    /prestige liste         l'échelle complète
//    /prestige aura <n>      choisir son aura (1 à 7), ou « couper »
//
//  Toute la logique reste dans le datapack (fonctions bmc4:rangs/*) :
//  la commande ne fait que les lancer « as » le joueur, dans le même
//  tick. L'achat confirmé est exactement celui de /trigger bmc4_rang.
//
//  Ni exigence ni niveau de permission : FTB Ranks emballe ce nœud
//  sous « command.prestige », qu'aucun rang ne définit, et retombe
//  alors sur l'exigence d'origine (RankCommandPredicate), donc ouvert
//  à tous. Les commandes sont réenregistrées à chaque /reload
//  (CommandRegistrationEvent), ce script avec.
// ============================================================

ServerEvents.commandRegistry(event => {
  let Commands = event.getCommands()
  let Arguments = event.getArguments()

  // Lance une fonction du datapack « as » le joueur qui a tapé la commande.
  let lancer = (ctx, fonction) => {
    let joueur = ctx.getSource().getPlayerOrException()
    ctx.getSource().getServer().runCommandSilent('execute as ' + joueur.getUsername() + ' run function bmc4:rangs/' + fonction)
    return 1
  }

  let dire = (ctx, json) => {
    let joueur = ctx.getSource().getPlayerOrException()
    ctx.getSource().getServer().runCommandSilent('tellraw ' + joueur.getUsername() + ' ' + JSON.stringify(json))
    return 1
  }

  let bouton = (texte, commande) => ({
    text: texte, color: 'aqua', bold: true,
    clickEvent: { action: 'run_command', value: commande },
  })

  let aura = (ctx, choix) => {
    let joueur = ctx.getSource().getPlayerOrException()
    let c = String(choix).trim().toLowerCase()
    // 10 coupe l'aura ; un numéro inconnu (99) reçoit le message du datapack.
    let n = c == 'couper' ? 10 : (/^\d+$/.test(c) ? parseInt(c, 10) : 99)
    let server = ctx.getSource().getServer()
    server.runCommandSilent('scoreboard players set ' + joueur.getUsername() + ' bmc4_aura ' + n)
    server.runCommandSilent('execute as ' + joueur.getUsername() + ' run function bmc4:rangs/aura_demande')
    return 1
  }

  event.register(Commands.literal('prestige')
    .executes(ctx => lancer(ctx, 'etat'))
    .then(Commands.literal('acheter').executes(ctx => lancer(ctx, 'devis')))
    .then(Commands.literal('confirmer').executes(ctx => lancer(ctx, 'confirmer')))
    .then(Commands.literal('liste').executes(ctx => lancer(ctx, 'g_liste')))
    .then(Commands.literal('aura')
      .executes(ctx => dire(ctx, ['',
        { text: '/prestige aura : ', color: 'gold' },
        { text: 'choisis un numéro, de 1 à 6 au rang Diamant, 7 au rang Divin, ou « couper ». La liste est dans le chapitre Rangs du livre.', color: 'gray' }]))
      .then(Commands.argument('choix', Arguments.GREEDY_STRING.create(event))
        .executes(ctx => aura(ctx, Arguments.GREEDY_STRING.getResult(ctx, 'choix')))))
    // Un mot inconnu après /prestige : un refus expliqué, pas l'erreur de Minecraft.
    .then(Commands.argument('inconnu', Arguments.GREEDY_STRING.create(event))
      .executes(ctx => dire(ctx, ['',
        { text: '/prestige refusé : ', color: 'red' },
        { text: '« ' + Arguments.GREEDY_STRING.getResult(ctx, 'inconnu') + ' » n\'existe pas. ', color: 'red' },
        { text: 'Essaie ', color: 'gray' },
        bouton('[/prestige]', '/prestige'), { text: ' ', color: 'gray' },
        bouton('[/prestige acheter]', '/prestige acheter'), { text: ' ', color: 'gray' },
        bouton('[/prestige liste]', '/prestige liste')]))))
})
