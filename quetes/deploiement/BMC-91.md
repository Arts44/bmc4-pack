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
| Scripts KubeJS | `config/serveur/kubejs/server_scripts/` (3 fichiers) | `/kubejs/server_scripts/` |
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
