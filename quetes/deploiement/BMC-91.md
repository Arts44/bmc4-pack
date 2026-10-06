# Déployer les rangs de prestige (BMC-91), et revenir en arrière

Préparé le 6 octobre 2026. **Rien de ce qui suit n'a été exécuté.** Arthur
donne le feu vert et déploie pendant une maintenance ; le serveur est fermé
aux autres joueurs pendant toute l'opération (même fermeture que BMC-89,
`LISEZ-MOI.md` § 2).

Serveur MineStrator 486488. Les commandes « console » se tapent dans la console
MineStrator (ou par `send_console_command`), sans « / ». Les déplacements de
fichiers se font avec l'outil `move_files` (ou le gestionnaire de fichiers du
panel), l'extraction avec `extract_archive`.

| Fichier | Rôle |
|---|---|
| `BMC-91.md` | cette marche à suivre |
| `ESSAIS-BMC-91.md` | la fiche de test : journal au démarrage, un essai par script, chaque refus et son message |
| `preparer-bmc91.sh` | télécharge et vérifie les quatre jars, rassemble scripts, configurations et datapack |
| `deposer.sh --bmc91` | dépose ce dossier dans `/bmc4-depot/bmc91-<date>/`, sans rien mettre en place |
| `preparer.sh`, `deposer.sh` | le livre, comme pour BMC-89 |

Ce qui part sur le serveur :

| Quoi | Version, origine | Où |
|---|---|---|
| FTB Ranks | 2001.1.7, maven.ftb.dev, SHA-1 `1ef101b4…`, 87 362 o | `/mods/` |
| FTB Essentials | 2001.2.4, maven.ftb.dev, SHA-1 `4f898578…`, 157 732 o | `/mods/` |
| KubeJS | 2001.6.5-build.26, maven.latvian.dev, SHA-1 `6986aef8…`, 1 658 792 o | `/mods/` **et pack client (v62)** |
| Rhino | 2001.2.3-build.10, maven.latvian.dev, SHA-1 `54db3943…`, 1 798 243 o | `/mods/` **et pack client (v62)** |
| Scripts KubeJS | `config/serveur/kubejs/server_scripts/` (4 fichiers depuis `/prestige`) | `/kubejs/server_scripts/` |
| FTB Essentials | `config/serveur/ftbessentials.snbt` | `/world/serverconfig/ftbessentials.snbt` |
| FTB Ranks | `config/serveur/ftbranks/ranks.snbt` | `/world/serverconfig/ftbranks/ranks.snbt` |
| Datapack | `config/datapack/bmc4-fixes/` : rangs, BMC-90 (`044b818`), `bmc4_anim` | `/world/datapacks/bmc4-fixes/` |
| Livre | Grimoire (`2c6f2b3`) et chapitre « Rangs » | `/config/ftbquests/quests/` |
| Bot | branche `bmc91-rangs` de discord-factions | Railway, à la fusion dans `main` |

**FTB Ranks et FTB Essentials restent sur le serveur seul ; KubeJS et Rhino
vont des deux côtés.** Corrigé le 6 octobre pendant la maintenance : le kit
disait que les quatre tenaient sur le serveur seul, parce que FTB Ranks,
FTB Essentials et KubeJS déclarent `IGNORESERVERONLY` et que leurs canaux
réseau acceptent un client qui ne les a pas. C'est vrai pour les deux mods
FTB. Pour KubeJS, non : il enregistre des entrées dans les registres du jeu,
que Forge synchronise à la connexion. Un client v61 est refusé (« Failed to
synchronize registry data from server », « KubeJS — Vous avez besoin de
2001.6.5-build.26 »). `IGNORESERVERONLY` ne couvre que la vérification de
version, pas les registres. D'où la **v62 du pack** : la v61 plus KubeJS et
Rhino, les mêmes jars que le serveur (voir `decisions.md`, « La v62 »).
**La connexion d'un client v62 est le premier essai** (`ESSAIS-BMC-91.md`, A).

---

## 0. La veille

1. Fabriquer le dossier de déploiement. Le script télécharge les quatre jars
   depuis les dépôts Maven et s'arrête si une empreinte ne correspond pas :

   ```bash
   sh quetes/deploiement/preparer-bmc91.sh
   ```

2. Fabriquer les archives du livre (Grimoire et Rangs) :

   ```bash
   sh quetes/deploiement/preparer.sh
   ```

3. Bot : la branche `bmc91-rangs` de discord-factions est prête, pas fusionnée.
   Relancer `node audit.js`, `node verifier.js` et `node --test` dessus.

## 1. Sauvegarde, puis arrêt

1. **Snapshot MineStrator** : `create_snapshot`, nom `avant-bmc91`. Attendre
   qu'il soit terminé.
2. Fermer le serveur aux autres joueurs (`LISEZ-MOI.md` § 2).
3. **Arrêter** le serveur (`power_action stop`). Les étapes 2 à 5 se font
   serveur arrêté : un mod ou un datapack à moitié posé ne doit jamais tourner.

## 2. Les jars

1. Déposer le dossier préparé (sur le feu vert d'Arthur) :

   ```bash
   sh quetes/deploiement/deposer.sh --bmc91
   ```

   Il crée `/bmc4-depot/bmc91-<date>/`, y dépose tout, et compare chaque taille
   au local. Il refuse si ce dossier existe déjà.
2. Déplacer les quatre jars de `/bmc4-depot/bmc91-<date>/mods/` vers `/mods/`.
   Aucun n'y est aujourd'hui (vérifié le 6 octobre) : rien n'est remplacé.

## 3. Les configurations

1. Créer `/kubejs/server_scripts/` et y déplacer les trois scripts
   (`bmc4_00_table.js`, `bmc4_garde.js`, `bmc4_dragons.js`). KubeJS crée le
   reste de son dossier au premier démarrage.
2. Déplacer `world/serverconfig/ftbessentials.snbt` vers
   `/world/serverconfig/ftbessentials.snbt`.
3. Créer `/world/serverconfig/ftbranks/` et y déplacer `ranks.snbt`.
   `retour-arriere/ranks-sans-kubejs.snbt` reste dans le dépôt de
   `/bmc4-depot` : il ne sert qu'au retour arrière A.

## 4. Le datapack

1. Déplacer `/world/datapacks/bmc4-fixes` vers
   `/bmc4-depot/bmc91-<date>/ancien/bmc4-fixes`. **Hors de `/world/datapacks/`** :
   un dossier renommé sur place serait chargé lui aussi.
2. Extraire `/bmc4-depot/bmc91-<date>/bmc4-fixes.zip` dans `/world/datapacks/`.
3. Vérifier la présence de `/world/datapacks/bmc4-fixes/pack.mcmeta` et de
   `/world/datapacks/bmc4-fixes/data/bmc4/functions/rangs/` (25 fichiers).

Ce datapack contient aussi les trois corrections BMC-90 (`044b818`) et la
création de `bmc4_anim` avec la relance du cycle des animaux.

## 5. Le livre

Comme `LISEZ-MOI.md` § 3, avec des noms datés (un `quests-ancien` existe peut-être
déjà) :

1. Déposer les archives : `sh quetes/deploiement/deposer.sh <date>`.
2. Renommer `/config/ftbquests/quests` en `/config/ftbquests/quests-avant-bmc91`.
3. Extraire `livre-complet-<date>.zip` dans `/config/ftbquests/`.
4. Vérifier `quests/chapters/` : 91 chapitres, dont `factions_rangs.snbt`.

## 6. Redémarrage

1. Démarrer (`power_action start`).
2. Lire le journal (`ESSAIS-BMC-91.md`, § « Le journal au démarrage »).
   **Une seule ligne de la liste rouge : retour arrière A ou B.**
3. Bot : fusionner `bmc91-rangs` dans `main` et pousser. Railway redéploie.
   Dans les journaux Railway : `[rangs] connecté`, puis `[rangs] rôle créé`
   seize fois et `[rangs] salon créé : #cercle-des-anciens` au premier passage.

## 7. Les essais

`ESSAIS-BMC-91.md`, dans l'ordre. Chaque refus doit afficher le message
attendu, mot pour mot à la ponctuation près.

---

## Retour arrière

### A. KubeJS ne cohabite pas avec Connector (ou un script casse)

_Écarté par Arthur le 6 octobre : KubeJS est gardé, et ajouté au pack client
(v62). Si on y revenait un jour, les clients auraient KubeJS et le serveur
non : ce cas n'a pas été essayé, il faudrait tester la connexion d'un client
v62 avant de rouvrir._

On retire les deux jars et on redémarre (consigne d'Arthur), **et** on ferme
les téléportations : sans KubeJS, aucun blocage (combat, raid, claim) ne tient
plus. La règle est « si un blocage ne peut pas être garanti, la commande n'est
pas ouverte ».

1. Arrêter le serveur.
2. Déplacer `kubejs-forge-2001.6.5-build.26.jar` et
   `rhino-forge-2001.2.3-build.10.jar` de `/mods/` vers
   `/bmc4-depot/bmc91-<date>/retires/`.
3. Remplacer `/world/serverconfig/ftbranks/ranks.snbt` par
   `/bmc4-depot/bmc91-<date>/retour-arriere/ranks-sans-kubejs.snbt` (renommé
   `ranks.snbt`). `/home`, `/sethome`, `/delhome`, `/listhomes`, `/back`, `/tpa`,
   `/tpahere`, `/tpaccept`, `/tpdeny` sont alors fermés à tous les joueurs.
4. Redémarrer.

Ce qui marche encore : achat des rangs, préfixes, équipes de rang, kits, auras,
`/trigger bmc4_manger` (le `/feed` des joueurs passait par KubeJS), `/hat`,
`/trashcan`, `/nickname`, `/enderchest`, annonces du bot. Ce qui ne marche plus :
les téléportations, la résurrection (plus aucune mort de dragon n'est notée ;
`!resurrection` répond qu'il n'y en a aucune), les messages en français pour
une commande d'un rang trop bas (Minecraft répond « Unknown or incomplete
command »).

### B. Tout retirer

1. Arrêter le serveur.
2. Déplacer les quatre jars de `/mods/` vers `/bmc4-depot/bmc91-<date>/retires/`.
3. Le datapack peut rester : sans FTB Ranks, seule la fonction
   `bmc4:rangs/g_ftbranks` ne se charge pas (toutes les commandes `ftbranks` y
   sont regroupées, une ligne d'erreur dans le journal). L'arbitrage des raids,
   le cœur perdu, les corrections BMC-90 et les animaux continuent.
   Pour revenir aussi sur le datapack : supprimer `/world/datapacks/bmc4-fixes`
   et remettre `/bmc4-depot/bmc91-<date>/ancien/bmc4-fixes` à sa place (les
   corrections BMC-90 repartent avec).
4. Livre : renommer `quests` en `quests-bmc91`, puis `quests-avant-bmc91` en
   `quests`.
5. Bot : revenir sur la fusion (`git revert`) et pousser.
6. Redémarrer.

### C. Dernier recours

Restaurer le snapshot `avant-bmc91`. Il ramène tout, y compris la progression
des joueurs à l'instant de la sauvegarde.

---

## À savoir avant d'y aller

- **L'équipe Minecraft « Apex »** (lue le 6 octobre : `team list` → Dragons,
  En raid, Apex ; `team list Apex` → 1 membre, HelXo14). Rien dans le dépôt ni
  dans le bot ne la crée. Un joueur ne peut être que dans une équipe : à son
  premier achat de rang, HelXo14 passera dans l'équipe de son rang et quittera
  « Apex ». Tant qu'il n'a pas de rang, rien ne change pour lui.
- **Le chat** montre le préfixe par l'équipe de rang. Minecraft met toujours le
  préfixe d'équipe devant le nom dans le chat. Un `name_format` de FTB Ranks
  l'aurait affiché deux fois, il n'est donc pas utilisé. Pendant un raid,
  l'équipe « En raid » remplace le préfixe partout, chat compris.
- **Les messages de FTB Essentials qui restent en anglais** ne sont pas des
  refus : « Home set! », « Home deleted! », « TPA request! » (avec ses boutons « Accept ✔ » et « Deny ❌ »),
  « Request sent! », « Request denied! ». Leurs textes sont écrits en dur dans
  le jar (`Component.literal`), sans fichier de langue à traduire. Tous les
  refus passent par KubeJS, en français.

---

## Mise à jour du 6 octobre au soir : `/prestige`

Décision d'Arthur : `/trigger bmc4_rang` est trop obscur ; la commande s'appelle
`/prestige`, et l'achat passe par une confirmation.

| Commande | Effet | Fonction lancée « as » le joueur |
|---|---|---|
| `/prestige` | rang, suivant, prix, niveaux, manque ; [Acheter] [Voir l'échelle] | `bmc4:rangs/etat` |
| `/prestige acheter` | devis : prix, apport, reste ; [Confirmer l'achat], ou le manque | `bmc4:rangs/devis` |
| `/prestige confirmer` | achète si le devis a moins de 30 s et vise le même rang | `bmc4:rangs/confirmer`, puis `acheter` |
| `/prestige liste` | l'échelle, ✔ rangs acquis, ◀ rang actuel | `bmc4:rangs/g_liste` |
| `/prestige aura <n\|couper>` | choisir ou couper son aura | `bmc4:rangs/aura_demande` |

Le script `bmc4_prestige.js` ne fait que lancer ces fonctions ; l'achat est celui
de `/trigger bmc4_rang`, qui marche toujours. Le devis est noté dans deux scores
(`bmc4_devis` : rang visé, `bmc4_devis_t` : heure du monde), créés par `g_init`.

**Permissions** : aucune ligne à ajouter dans `ranks.snbt`. FTB Ranks emballe
chaque nœud de commande à la fin du constructeur de `Commands`
(`CommandsMixin.java:13-15`, FTB Ranks 2001.1.7), donc aussi `/prestige`, sous
`command.prestige`. Aucun rang ne définit ce nœud ni `command` : la recherche
remonte jusqu'à « absent » (`RankManagerImpl.java:161-180`) et le prédicat
retombe sur l'exigence d'origine (`RankCommandPredicate.java`,
`orElseGet(() -> original.test(source))`), vide pour une commande KubeJS. À
chaque `/reload`, `Commands` est recréé, KubeJS réenregistre `/prestige`
(`CommandRegistrationEvent`) et FTB Ranks l'emballe de nouveau.

**Ce qui part** (déposé dans `/bmc4-depot/bmc91-<date>-prestige/`) :
`kubejs/server_scripts/` (les quatre scripts, dont `bmc4_prestige.js` nouveau et
`bmc4_garde.js` modifié), `bmc4-fixes.zip`, et les deux archives du livre.
`ranks.snbt` ne change pas.

1. Scripts : déplacer les quatre dans `/kubejs/server_scripts/` (remplacer).
2. Datapack : comme § 4, l'actuel rangé dans `/bmc4-depot/bmc91-<date>-prestige/ancien/`.
3. Livre : comme § 5, avec `quests-avant-prestige`.
4. Redémarrer : le livre l'exige (§ 3 de `LISEZ-MOI.md`), et un nouveau script
   qui enregistre une commande n'est pas garanti au premier `reload` (l'ordre
   entre le rechargement des scripts et la reconstruction des commandes n'a pas
   été vérifié). L'essai « Après `/reload` » vérifie ensuite qu'elle survit.
5. Essais : `ESSAIS-BMC-91.md`, section Datapack, de « Sans aucun rang » à
   « L'Infini », et lignes 42 à 47 du tableau.

---

## Correctifs du 6 octobre au soir, avant la réouverture du 7

Les essais en jeu du 6 au soir ont montré quatre défauts.

1. **`bmc4_garde.js` appelait des noms Java absents au runtime.** Ce n'est pas la
   table de Rhino qui manque (`latest.log` : « Loading mappings for 1.20.1 …
   Done ») : les mixins de KubeJS donnent leur propre nom à certaines méthodes
   (`@RemapForJS`), et ce nom l'emporte. `getUUID()` est `getUuid()`,
   `DamageSource.getEntity()` est `getActual()`, la clé de dimension est
   `getDimensionKey()` (`level.dimension` est un `ResourceLocation`). Le script
   est réécrit autour d'un objet `ACCES` (une forme justifiée par appel),
   **fail-closed** (toute erreur refuse la commande gardée), et
   `/prestige diagnostic` (op) essaie chaque appel. `bmc4_dragons.js` lit le NBT
   par son texte SNBT. Règle 8 du contrôle : les formes prouvées absentes sont
   refusées.
2. **Les quinze rangs FTB Ranks ne s'activaient jamais** : `condition:
   "rank_added"` veut dire « actif si un autre rang, nommé dans `rank`, est
   ajouté » (`RankAddedCondition.java:12-27`) ; sans `rank`, jamais. Sans clé
   `condition`, FTB Ranks pose la condition par défaut, active si ajouté
   (`RankImpl.java:32-35`, `DefaultCondition.java:27-30`). `ftbranks add`, lui,
   ajoute toujours (`PlayerRankData.java:39-46`). Générateur corrigé ; règle 7
   du contrôle.
3. **L'autocomplétion** : le datapack pose l'étiquette `bmc4_resync` à l'achat
   et à la connexion ; `bmc4_garde.js` renvoie l'arbre des commandes
   (`server.getCommands().sendCommands(joueur)`) dans la seconde.
4. **Le compteur de combat** : « ⚔ En combat : 12 s » dans la barre d'action,
   chaque seconde, effacé à 0.

**Ce qui part** (`/bmc4-depot/bmc91-2026-10-06-correctifs/`) : les quatre scripts
KubeJS, `bmc4-fixes.zip`, `ranks.snbt` et `ranks-sans-kubejs.snbt`. Le livre ne
change pas.

1. Scripts : remplacer les quatre dans `/kubejs/server_scripts/`.
2. Rangs : remplacer `/world/serverconfig/ftbranks/ranks.snbt`, puis
   `ftbranks reload`.
3. Datapack : comme § 4.
4. Redémarrer, puis **`/prestige diagnostic`** : toutes les lignes en OK.
   Sinon, `ranks-sans-kubejs.snbt` à la place de `ranks.snbt`, `ftbranks reload` :
   `/home`, `/back`, `/tpa` fermés à tous, `/prestige` reste actif.

### Le 6 octobre, 22 h 30 : `getProfileCache` en ÉCHEC

`/prestige diagnostic` a tout donné en OK, sauf « cache des profils
(getProfileCache) ». `/nickname` essaie désormais cinq voies dans l'ordre et
garde la première qui fonctionne : `getProfileCache()`, `server.profileCache`,
les noms SRG bruts `m_129927_().m_10996_()`, `usercache.json` lu par `JsonIO`
(KubeJS autorise la lecture dans le dossier du jeu, `KubeJS.java:190-196`), et
FTB Teams `getKnownPlayerTeams()`. Si aucune ne fonctionne, il ne vérifie que
les joueurs en ligne (correctif d'Arthur, gardé). Le diagnostic teste la voie
retenue (ligne OK/ÉCHEC) et affiche les cinq en INFO. Le devis de
`/prestige acheter` finit maintenant par un point.

Dépôt : **`/bmc4-depot/bmc91-2026-10-06-final/`**, qui remplace
`bmc91-2026-10-06-nickname/` (déposé avant la décision sur les opérateurs).

### Le 6 octobre, 22 h 28 : un opérateur n'a que ce que son rang donne

Décision d'Arthur, déjà appliquée par lui sur le serveur, reportée au dépôt :
`bmc4_staff` sans aucune permission de prestige, plus d'exemption d'op dans
`bmc4_garde.js` hors de `/prestige diagnostic` (règle 9 du contrôle).

Dans `/bmc4-depot/bmc91-2026-10-06-final/` : `bmc4_garde.js` (cinq voies de
`/nickname` et opérateurs), `bmc4-fixes.zip` (devis avec son point),
`ranks.snbt`, `ranks-sans-kubejs.snbt`. Remplacer le script et `ranks.snbt`,
extraire le datapack comme § 4, `ftbranks reload`, redémarrage (ou `reload`),
puis `/prestige diagnostic`.

