# Les rangs de prestige

**Brouillon, pas posté.** Proposé pour un nouveau salon `#rangs-de-prestige`
dans la catégorie GUIDE (plutôt que `#ftb` : les rangs ne sont pas un mod FTB
pour le joueur, ce sont des niveaux qu'il dépense). Trois messages, chacun sous
2 000 caractères. À poster par Arthur après la maintenance BMC-91, quand les
essais sont passés.

Sources : `config/rangs/rangs.toml` (échelle, avantages, kits), datapack
`bmc4-fixes/rangs/`, scripts KubeJS `bmc4_garde.js` et `bmc4_dragons.js`, bot
`rangs.js`.

---

## Message 1/3

**💠 Les rangs de prestige — dépenser ses niveaux**

Tes niveaux d'XP qui dorment s'échangent contre un **rang**. Chaque rang **retire** des niveaux, s'affiche devant ton pseudo (chat, liste Tab, au-dessus de la tête) et donne du **confort et du prestige**. Jamais de force au combat, jamais de claims en plus.

**Où j'en suis** : `/prestige` (ton rang, le suivant, son prix, ce qu'il te manque)
**Acheter** le rang suivant : `/prestige acheter`, puis le bouton **[Confirmer l'achat]**, valable 30 secondes
**L'échelle** : `/prestige liste`

Rien n'est acheté sans confirmation. À la confirmation, les niveaux sont vérifiés puis retirés d'un seul coup. S'il en manque, **rien n'est retiré** et le message dit combien il en manque. Les rangs s'achètent dans l'ordre, chacun donne son **kit une seule fois**, à l'achat. Le rang est personnel : il ne se partage pas avec ta faction.

Le détail de chaque rang est dans le livre de quêtes, chapitre **Les rangs de prestige** (groupe Factions).

## Message 2/3

**L'échelle** (prix en niveaux, cumul entre parenthèses)

⬩ Cuivre 50 (50) · préfixe, rôle Discord, kit
⬩ Fer 100 (150) · `/hat`, 1 home
⬩ Or 200 (350) · `/trashcan`
⬩ Émeraude 350 (700) · `/nickname`
⬩ Diamant 500 (1 200) · aura au choix, 2 homes
⬩ Nétherite 750 (1 950) · `/feed` toutes les 30 min
✦ Ender 1 000 (2 950) · `/enderchest`, 3 homes
✦ Abyssal 1 250 (4 200) · `/back`
✦ Draconique 1 500 (5 700) · résurrection draconique
✦ Céleste 2 000 (7 700) · `/tpa`, `/tpahere`, 4 homes
✦ Suprême 2 500 (10 200) · ta tête dans l'Allée des Légendes
♛ Éternel 3 000 (13 200) · annonce à la connexion
♛ Primordial 4 000 (17 200) · salon réservé, 5 homes
♛ Divin 5 000 (22 200) · aura exclusive, 6 homes
♛ Absolu 7 500 (29 700) · ta statue dans l'Allée
∞ Infini I, II, III… · 10 000, puis 2 500 de plus à chaque palier

**Auras** (Diamant) : `/prestige aura 1` à `6`, `/prestige aura couper` pour l'éteindre. Le Divin a la `7`.
**`/home`** : `/sethome <nom>`, `/home <nom>`, `/delhome <nom>`, `/listhomes`.

## Message 3/3

**Ce qui est bloqué, et pourquoi**

`/home`, `/back`, `/tpa`, `/tpahere` et `/tpaccept` sont refusés :
• **en combat** : un coup pris d'une créature ou d'un joueur, ou donné, dans les 15 dernières secondes ;
• **pendant un raid**, pour les membres des deux factions engagées ;
• **dans le claim d'une autre faction**. Ton claim, le Marché Flottant et la nature restent permis.

On ne pose pas non plus de home dans le claim d'une autre faction, et ni `/home`, ni `/back`, ni `/tpa` ne t'y emmènent. Chaque refus dit pourquoi et quand réessayer.

`/spawn`, `/warp` et `/rtp` n'existent pas ici : ils permettraient de quitter un raid ou d'arriver n'importe où. Les waystones restent là.

**Résurrection draconique** (Draconique et plus) : sur Discord, `!resurrection` liste tes dragons morts, `!resurrection <nom>` en ramène un à tes pieds : même race, même nom, adulte, apprivoisé et lié à toi. Une fois par semaine, remise à zéro le lundi à 0 h. Il faut être connecté, et hors raid. **Sans équipement** : selle, armure et coffre sont tombés au sol à sa mort.

**`/nickname`** (Émeraude) change le nom affiché, pas l'identité : le vrai pseudo reste visible au survol. Prendre le pseudo d'un autre est interdit (règlement, Identité).
