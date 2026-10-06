# Les essais de BMC-91, pendant la maintenance

À cocher dans l'ordre, après le redémarrage (`BMC-91.md` § 6). Les messages
attendus sont copiés des sources (KubeJS `bmc4_garde.js`, datapack `rangs/`,
bot `rangs.js`). Un message différent, en anglais, ou une absence de message
est un défaut. Aucun refus ne doit rester muet.

Il faut deux comptes : **A** (Arts_Vio, op) et **B**, un compte sans op d'une
autre faction. Les essais de rang se font **sans op** (`deop` sur soi) : un
opérateur passe la garde des rangs, pas celle des blocages.

Pour donner des niveaux pendant les essais : `xp add <pseudo> <n> levels`.
Pour remettre un compte à zéro après les essais :
`scoreboard players set <pseudo> bmc4_rangs 0`, puis retirer ses rangs FTB
Ranks (`ftbranks remove <pseudo> rang_<n>` pour chaque n) et
`team leave <pseudo>`.

---

## A. Cohabitation avec Connector : le journal au démarrage

### Doit apparaître

- [ ] `FTB Ranks` : `Loading command nodes...`, puis `Loaded <n> command nodes`.
- [ ] `FTB Ranks` : `Loaded 17 ranks` (bmc4_joueur, rang_1 à rang_15, bmc4_staff).
- [ ] KubeJS : les quatre scripts chargés (`bmc4_prestige.js` depuis le 6 octobre au soir), sans erreur. Le détail est dans
      `/logs/kubejs/server.log` : `bmc4_00_table.js`, `bmc4_garde.js`,
      `bmc4_dragons.js`, chacun « Loaded ».
- [ ] Aucune ligne `Failed to load function bmc4:` (le datapack entier se
      charge ; `datapack list` montre `file/bmc4-fixes`).
- [ ] Un client du **pack v62** (v61 plus KubeJS et Rhino, sans FTB Ranks ni
      FTB Essentials) se connecte sans « Mod rejections », « mismatched mod
      channel list », « Incompatible FML modded server » ni « Failed to
      synchronize registry data ». KubeJS et Rhino vont des deux côtés ; FTB
      Ranks et FTB Essentials restent sur le serveur seul. Un client v61 est
      refusé, c'est attendu depuis le 6 octobre (« KubeJS — Vous avez besoin
      de 2001.6.5-build.26 »).

### Liste rouge : une seule de ces lignes, et c'est le retour arrière A ou B

- `Mixin apply failed` ou `MixinApplyError` qui cite `kubejs`, `rhino`,
  `ftbranks` ou `ftbessentials`.
- `Connector` / `sinytra` qui cite un de ces quatre mods (Connector ne devrait
  pas les toucher : ce sont des mods Forge).
- `Error loading` ou `Error in` dans `/logs/kubejs/server.log`.
- Le serveur ne passe pas `Done (` ; ou un crash-report qui cite un des quatre.
- Un client v62 refusé à la connexion.

---

## B. Un essai par script

### Datapack (rangs)

- [ ] **Sans aucun rang.** B (`bmc4_joueur` seul), 0 niveau : `/prestige` →
      « Tu n'as pas encore de rang de prestige. » puis « Prochain : ⬩ Cuivre,
      50 niveaux ; tu en as 0, il t'en manque 50. [Voir l'échelle] » (pas de
      bouton [Acheter]). La commande s'ouvre donc bien à un joueur sans rang.
- [ ] **Devis refusé.** Toujours à 0 niveau : `/prestige acheter` →
      « Rang ⬩ Cuivre : il te manque 50 niveaux (50 requis, tu en as 0). Rien n'a été retiré. Retape /prestige acheter quand tu les auras. »
      Aucun bouton de confirmation ; le nombre de niveaux n'a pas bougé.
- [ ] **`confirmer` sans `acheter`.** `/prestige confirmer` →
      « Aucun achat à confirmer : tape d'abord /prestige acheter. [Acheter] ».
- [ ] **Devis, puis achat.** `xp add B 60 levels`, `/prestige` → « Prochain :
      ⬩ Cuivre, 50 niveaux ; tu en as 60. [Acheter] [Voir l'échelle] ».
      Clic sur **[Acheter]** → « Rang ⬩ Cuivre : 50 niveaux. Il apporte : Préfixe en jeu, rôle Discord et kit de rang. Après l'achat, il te restera 10 niveaux. [Confirmer l'achat] (valable 30 secondes) ».
      **Rien n'est encore retiré** (60 niveaux). Clic sur **[Confirmer l'achat]**
      dans les 30 s → « Rang ⬩ Cuivre obtenu : 50 niveaux retirés, il t'en reste 10. … Ton kit est dans ton inventaire… ».
      B a 10 niveaux, l'étendard du Cuivre, 32 torches, 16 pains ;
      le préfixe « ⬩ Cuivre » orange est devant son nom **dans le chat, la liste
      Tab et au-dessus de sa tête** ; `ftbranks list_ranks_of B` montre rang_1.
- [ ] **Un devis ne sert qu'une fois.** Re-cliquer sur [Confirmer l'achat] →
      « Aucun achat à confirmer : tape d'abord /prestige acheter. [Acheter] ».
- [ ] **Confirmation expirée.** `xp add B 100 levels`, `/prestige acheter`
      (Fer), attendre **plus de 30 s**, `/prestige confirmer` →
      « Confirmation expirée : retape /prestige acheter. [Acheter] » ; rien de retiré.
- [ ] **Rang changé entre-temps.** `/prestige acheter` (Fer), puis
      `/trigger bmc4_rang` (achète le Fer directement), puis `/prestige confirmer`
      → « Confirmation expirée : ton rang a changé depuis /prestige acheter. Retape /prestige acheter. [Acheter] ».
- [ ] **L'échelle.** `/prestige liste` → l'en-tête, « ✔ ⬩ Cuivre — 50 »,
      « ✔ ⬩ Fer — 100  ◀ ton rang », « · ⬩ Or — 200 »… jusqu'à l'Absolu, la
      ligne de l'Infini, puis [Où j'en suis] [Acheter].
- [ ] **Mot inconnu.** `/prestige truc` → « /prestige refusé : « truc » n'existe pas. Essaie [/prestige] [/prestige acheter] [/prestige liste] ».
- [ ] **Après `/reload`.** `reload` en console, puis `/prestige` : la commande
      répond toujours (elle est réenregistrée avec les commandes).
- [ ] **`/trigger bmc4_rang` marche encore** (achat direct, sans confirmation) ;
      `/trigger bmc4_rang set 7` → « /trigger bmc4_rang refusé : cette valeur n'existe pas. Utilise plutôt /prestige. [Où j'en suis] ».
- [ ] **Paiement exact sur un gros montant** (vérifie la décomposition en
      puissances de deux). Sur A sans op : `scoreboard players set A bmc4_rangs 9`,
      `xp set A 0 levels`, `xp add A 2345 levels`, `/prestige acheter`,
      [Confirmer l'achat] → il reste **345** niveaux et le rang ✦ Céleste.
      Remettre A à son état après.
- [ ] **L'Infini.** Sur A sans op : `scoreboard players set A bmc4_rangs 15`,
      `xp add A 10000 levels`, `/prestige` → « Ton rang : ♛ Absolu (15/15). »
      et « Prochain : ∞ Infini I, 10 000 niveaux… [Acheter] » ; `/prestige acheter`
      → « Il apporte : le palier Infini I dans ton préfixe, une annonce dans #faits-d-armes et à ta connexion » ;
      [Confirmer l'achat] → préfixe « ∞ Infini I », annonce dans `#faits-d-armes`
      sous 30 s ; `/prestige liste` → « ◀ ton palier : ∞ Infini I ». Puis
      `scoreboard players set A bmc4_rangs 45`, `/prestige acheter` →
      « Achat refusé : tu as atteint ∞ Infini XXX, le dernier palier préparé. Préviens le staff : les suivants seront ajoutés. Rien n'a été retiré. [Voir l'échelle] ».
      Remettre A à son état après.
- [ ] **Le kit n'est donné qu'une fois** : rien de neuf au-delà de l'achat.
- [ ] **Fin de raid** : pendant un raid de test, B (dans `bmc4_raid_actif`)
      perd son préfixe de rang ; à `function bmc4:raid_fin` il le retrouve dans la
      seconde. Un joueur déconnecté pendant la fin le retrouve à sa connexion.
- [ ] **Connexion** : B se déconnecte et revient ; `ftbranks list_ranks_of B`
      montre toujours ses rangs.
- [ ] **Auras.** B au rang Diamant : `/prestige aura 2` →
      « Aura choisie : Bâtons de l'End. Couper : /prestige aura couper » ; les
      particules apparaissent, pas en spectateur ni invisible.
      `/prestige aura couper` → « Aura coupée. La remettre : /prestige aura <numéro> ».
      `/prestige aura` seul → l'aide « /prestige aura : choisis un numéro… ».
- [ ] **`bmc4_anim`** : `scoreboard objectives list` contient `bmc4_anim` ;
      `schedule` : le cycle des animaux tourne (des moutons, vaches ou cochons
      apparaissent au bout de quelques cycles près d'un joueur de l'Overworld).

### KubeJS : `bmc4_garde.js`

- [ ] Un joueur sans rang tape `/home` → le message de rang (§ C), pas
      « Unknown or incomplete command ».
- [ ] B au rang Fer, hors claim, hors combat : `/sethome base` → « Home set! »
      (message de FTB Essentials), puis `/home base` le ramène.
- [ ] Les trois blocages et la destination, un par un (§ C, lignes 3 à 9).
- [ ] `/feed` sans op passe par le datapack (§ C, lignes 21 à 24).

### KubeJS : `bmc4_dragons.js`

- [ ] Un dragon apprivoisé et nommé de A (un dragon de test) : le tuer
      (`kill @e[type=dragonmounts:dragon,name=<nom>,limit=1]`), puis
      `data get storage bmc4:dragons morts` → une entrée avec `Uuid`,
      `Proprio` (UUID de A), `Race` (« dragonmounts:… »), `Nom`, `Quand`.
- [ ] Un dragon sauvage tué : aucune entrée.

### Bot : `rangs.js`

- [ ] Rôles : seize rôles « ⬩ Cuivre » … « ∞ Infini » créés ; B (compte lié)
      reçoit « ⬩ Cuivre » au plus tard dix minutes après l'achat.
- [ ] Salon `#cercle-des-anciens` créé, invisible pour B.
- [ ] Annonce : avec `scoreboard players set A bmc4_rangs 11` puis un achat
      (rang 12), `#faits-d-armes` reçoit en moins de 30 s
      « ♛ **Arts_Vio** atteint le rang **Éternel** (12/15). », et
      `data get storage bmc4:rangs annonces` est vide ensuite.
- [ ] Connexion d'un rang 12 : dans `#journal-serveur`, la ligne devient
      « ♛ **Arts_Vio**, l'Éternel, est arrivé. » ; en jeu, titre doré
      « Arts_Vio l'Éternel est arrivé ». Refaire avec 13, 14, 15, 16 (rangs) :
      Primordial (vert sombre), Divin (blanc et cloche), Absolu (rouge sombre,
      tonnerre, flash, **aucun dégât ni feu**), Infini I (violet, Ender Dragon).
- [ ] **Résurrection** (A au rang 9 ou plus, le dragon de test mort ci-dessus) :
      `!resurrection` dans `#commandes` liste le mort ; `!resurrection <nom>` le
      ramène aux pieds de A : même race, même nom, **adulte**, **apprivoisé et
      lié à A** (il le suit, A peut le monter et lui donner des ordres),
      **sans selle, armure ni coffre**. L'entrée disparaît de `storage`.
- [ ] **Le vrai pseudo reste lisible** : B au rang Émeraude,
      `/nickname Le Barde` ; dans le chat, survoler « Le Barde » montre le vrai
      pseudo de B (bulle d'entité de Minecraft).

---

## C. Chaque refus et son message

« X » est le pseudo de l'autre joueur, « Farmer's » le nom de l'équipe FTB du
claim, les nombres sont des exemples.

| # | Situation | Message attendu |
|---|---|---|
| 1 | `/tpa` sans rang Céleste | /tpa refusé : elle s'obtient au rang ✦ Céleste (ton rang : ⬩ Fer). Voir ce qu'il te manque : /prestige. |
| 2 | même chose pour `/hat` (Fer), `/home` `/sethome` `/delhome` `/listhomes` (Fer), `/trashcan` (Or), `/nickname` (Émeraude), `/enderchest` (Ender), `/back` (Abyssal), `/tpahere` (Céleste) | /<commande> refusé : elle s'obtient au rang <rang> (ton rang : <rang ou « aucun rang »>). Voir ce qu'il te manque : /prestige. |
| 3 | `/home` moins de 15 s après un coup pris d'une créature ou d'un joueur, ou donné | /home refusé : tu as pris ou donné un coup il y a moins de 15 secondes. Réessaie dans 9 s. |
| 4 | `/back` pendant un raid de sa faction | /back refusé : un raid est en cours pour ta faction, jusqu'à 21 h 00. Les téléportations reviennent à la fin du raid. |
| 5 | `/home` debout dans un claim adverse | /home refusé : tu es dans le claim de Farmer's. Sors de leur territoire pour l'utiliser. |
| 6 | `/sethome` dans un claim adverse | /sethome refusé : tu ne peux pas poser de home dans le claim d'une autre faction (ici, Farmer's). Pose-le dans ton claim ou hors claim. |
| 7 | `/home base` quand ce home est dans un claim adverse (claim posé après coup) | /home refusé : ton home « base » est dans le claim de Farmer's. Un home ne ramène pas dans le territoire d'une autre faction : supprime-le (/delhome base). |
| 8 | `/back` vers un lieu dans un claim adverse | /back refusé : ton dernier lieu est dans le claim de Farmer's. /back ne ramène pas dans le territoire d'une autre faction : rejoins-le à pied. |
| 9 | `/tpa X` quand X est dans un claim qui n'est pas celui de ta faction | /tpa refusé : X est dans le claim de Farmer's. Pas de téléportation dans le territoire d'une autre faction. |
| 10 | `/tpa X` quand X est en combat | /tpa refusé : X est en combat. Réessaie dans 6 s. |
| 11 | `/tpa X` quand X est en raid | /tpa refusé : X est engagé dans un raid, jusqu'à 21 h 00. Réessaie après le raid. |
| 12 | `/tpa Personne` (pas connecté) | /tpa refusé : aucun joueur nommé « Personne » n'est connecté. Écris /tpa <pseudo exact> d'un joueur connecté. |
| 13 | `/tpa` soi-même | /tpa refusé : c'est toi. Écris le pseudo d'un autre joueur. |
| 14 | `/tpa X` deux fois | /tpa refusé : une demande vers X attend déjà sa réponse. Attends qu'il l'accepte ou la refuse. |
| 15 | `/tpaccept` d'une demande inconnue ou expirée | /tpaccept refusé : cette demande n'existe pas ou n'est plus valable. Demande à l'autre joueur de la refaire. |
| 16 | `/tpaccept` quand l'auteur est parti | /tpaccept refusé : le joueur qui a fait la demande s'est déconnecté. |
| 17 | deuxième `/home` en moins de 10 s (`/back` : 30 s, `/tpaccept` : 10 s) | /home refusé : une téléportation par 10 secondes. Réessaie dans 4 s. |
| 18 | `/home inconnu` | /home refusé : tu n'as pas de home nommé « inconnu ». Tes homes : base. |
| 19 | `/sethome` au-delà du maximum du rang | /sethome refusé : tu as déjà 1 home, le maximum de ton rang (⬩ Fer). Remplace-en un (/sethome base) ou supprime-le (/delhome <nom>) ; le rang ⬩ Diamant en donne 2. |
| 20 | `/back` sans lieu où revenir | /back refusé : il n'y a aucun lieu où revenir. /back ramène à ta dernière téléportation ou à ta dernière mort. |
| 21 | `/feed` sans rang Nétherite | /feed refusé : il s'obtient au rang ⬩ Nétherite. Voir ce qu'il te manque : [Où j'en suis] |
| 22 | `/feed` moins de 30 min après le précédent | /feed refusé : une fois toutes les 30 minutes. Disponible dans 12 min 30 s. |
| 23 | `/feed` la faim pleine | /feed refusé : ta faim est déjà pleine. Rien n'a été utilisé : il reste disponible. |
| 24 | `/feed` accepté | Rassasié. Prochain /feed dans 30 minutes. |
| 25 | `/delhome inconnu` | /delhome refusé : tu n'as pas de home nommé « inconnu ». Tes homes : base. |
| 26 | `/nickname Arts_Vio` (pseudo d'un autre joueur) | /nickname refusé : « Arts_Vio » est le pseudo d'un autre joueur. Le règlement interdit de prendre le pseudo d'un autre : choisis-en un qui n'appartient à personne. |
| 27 | `/spawn`, `/playerspawn`, `/warp` | /spawn refusé : commande coupée sur BMC4, elle permettrait de quitter un raid. Les waystones restent là pour voyager. |
| 28 | `/rtp` | /rtp refusé : commande coupée sur BMC4, elle téléporte n'importe où, claims compris. |
| 29 | `/near`, `/kickme`, `/leaderboard`, `/listwarps` | /near refusé : commande coupée sur BMC4, elle donnerait la position des autres joueurs. (et les raisons de `COUPEES`) |
| 30 | rang : niveaux insuffisants | Rang ✦ Céleste : il te manque 412 niveaux (2 000 requis, tu en as 1588). Rien n'a été retiré. Retape /prestige acheter quand tu les auras. |
| 31 | rang : dernier palier préparé atteint | Achat refusé : tu as atteint ∞ Infini XXX, le dernier palier préparé. Préviens le staff : les suivants seront ajoutés. Rien n'a été retiré. [Voir l'échelle] |
| 32 | aura d'un rang trop bas (`/prestige aura 7` sans Divin) | Aura refusée : « Halo divin » s'obtient au rang ♛ Divin. Voir ce qu'il te manque : [Où j'en suis] |
| 33 | aura inconnue (`/prestige aura 8`) | Aura inconnue. Les numéros vont de 1 à 7 (voir le chapitre Rangs du livre) ; /prestige aura couper la coupe. |
| 34 | `!resurrection` sans compte lié | **Résurrection draconique refusée** : ton compte Discord n'est pas lié à ton compte Minecraft. Lie-le en jeu avec `/discord link`, puis relance. |
| 35 | `!resurrection` sous Draconique | **Résurrection draconique refusée** : elle s'obtient au rang **✦ Draconique** (ton rang : ⬩ Fer). En jeu : `/trigger bmc4_rang set 2` pour voir ce qu'il te manque. |
| 36 | `!resurrection` une deuxième fois la même semaine | **Résurrection draconique refusée** : déjà utilisée cette semaine. Prochaine disponible lundi 12 octobre à 00 h 00. |
| 37 | `!resurrection` hors ligne | **Résurrection draconique refusée** : **X** n'est pas connecté. Le dragon revient à tes pieds : connecte-toi, puis relance. |
| 38 | `!resurrection` pendant un raid | **Résurrection draconique refusée** : tu es engagé dans un raid. Relance après la fin du raid ; rien n'a été utilisé. |
| 39 | `!resurrection` sans dragon mort noté | **Résurrection draconique refusée** : aucun de tes dragons n'est mort depuis l'installation du registre des morts. Seules les morts notées par le serveur peuvent être réparées. |
| 40 | `!resurrection Inconnu` | **Résurrection draconique refusée** : aucun de tes dragons morts ne s'appelle « Inconnu ». Tes dragons morts : (liste numérotée) |
| 41 | `!resurrection` hors des salons permis | le message habituel du bot : « `!resurrection` ne s'utilise pas ici. Va dans … » |
| 42 | `/prestige confirmer` sans `/prestige acheter` | Aucun achat à confirmer : tape d'abord /prestige acheter. [Acheter] |
| 43 | `/prestige confirmer` plus de 30 s après `/prestige acheter` | Confirmation expirée : retape /prestige acheter. [Acheter] |
| 44 | `/prestige confirmer` après un achat fait entre-temps | Confirmation expirée : ton rang a changé depuis /prestige acheter. Retape /prestige acheter. [Acheter] |
| 45 | `/prestige acheter` sans assez de niveaux | (comme la ligne 30, sans bouton de confirmation) |
| 46 | `/prestige truc` | /prestige refusé : « truc » n'existe pas. Essaie [/prestige] [/prestige acheter] [/prestige liste] |
| 47 | `/trigger bmc4_rang set 7` | /trigger bmc4_rang refusé : cette valeur n'existe pas. Utilise plutôt /prestige. [Où j'en suis] |

Les chiffres de Minecraft s'affichent sans espace des milliers (« 1588 ») : un
score ne se met pas en forme dans `tellraw`. Les prix, écrits dans le texte,
gardent l'espace (« 2 000 »).
