# Configurations modifiées

Ce que nous avons changé par rapport au pack d'origine. **Ces valeurs sont
écrasées à chaque mise à jour du pack** — cette page sert à les remettre.

Le raisonnement derrière chaque choix est dans [`decisions.md`](../decisions.md).

---

## Les mods ajoutés par le serveur — v60

Ils ne font pas partie du pack Better MC d'origine. Un export du pack
client doit les contenir, sinon Forge refuse la connexion.

```
irons_spellbooks-1.20.1-3.16.3.jar
irons_lib-1.20.1-2.1.0.jar                  dépendance
player-animation-lib-forge-1.0.2-rc1+1.20.jar   dépendance
hazennstuff-watered-down-edition-1.1.2.jar
gtbcs_spell_lib-2.2.0-1.20.1.jar            dépendance
cc-tweaked-1.20.1-forge-1.120.2.jar
pipez-forge-1.20.1-1.2.26.jar
cinematic_respawn-1.20.1-forge-1.3.0.jar
immersive-portals-3.0.7-all.jar
```

⚠️ **CC: Tweaked doit venir de Modrinth**, pas de CurseForge. La
dernière version publiée sur CurseForge pour 1.20.1 est la 1.113.1,
incompatible avec Create 6.0.8 — elle fait planter le serveur au
chargement. La 1.120.2 de Modrinth corrige le problème.

⚠️ **Ne pas réinstaller GeckoLib ni Curios** : ils sont déjà dans le
pack, et deux versions chargées cassent le démarrage.

---

## `server.properties`

```properties
motd=§7§oBMC4\n§8§kArts_Vio & HelXo14§f§a§i§r§x§a§e§r§o
difficulty=normal
simulation-distance=6
max-tick-time=300000
white-list=false
pvp=true
online-mode=true
```

---

## `config/dragonmounts-common.toml`

```toml
# Chances d'apparition des œufs, par structure
aether_in_simple_dungeon_chance     = 0.25   # défaut 0.15
fire_in_desert_pyramid_chance       = 0.2    # défaut 0.075
forest_in_jungle_temple_chance      = 0.4    # défaut 0.3
ghost_in_woodland_mansion_chance    = 0.3    # défaut 0.2
ghost_in_abandoned_mineshaft_chance = 0.2    # défaut 0.095
ice_in_igloo_chest_chance           = 0.3    # défaut 0.2
nether_in_bastion_treasure_chance   = 0.45   # défaut 0.35
water_in_buried_treasure_chance     = 0.3    # défaut 0.175

dragon_wander_range = 8                      # défaut 30
global_breath_damage = 3.0                   # défaut 6.0
```

⚠️ Section marquée « requires restart ».

**Le souffle fait 1,5 cœur au lieu de 3**, depuis le 24 septembre. Il
touche les dragons entre eux autant que les joueurs : avec treize
dragons entassés près de la base, la valeur d'origine en tuait.

**Reproduction** : chaque dragon ne peut se reproduire que deux fois
(`[reproduction_limits]`, toutes races à 2). Les œufs changent de race
selon l'environnement où on les pose (`update_habitats = true`) —
c'est le vrai moyen de choisir la race obtenue, plus que le choix des
parents.

---

## `config/theft-common.toml`

Aucune modification conservée. Le mod tourne avec ses valeurs par défaut :

```
5 objets maximum par vol
16 secondes de maintien
10 secondes de recharge
gant : 50 % dans épaves, avant-postes et mineshafts
la victime voit l'emplacement vidé
```

Une modification a été faite puis **annulée** : `generate_loot = false`,
qui coupait la source des gants. Le règlement a été réécrit à la place.

---

## `world/serverconfig/ftbchunks-world.snbt`

```
def_claim_visibility: "private"    # défaut "public"
```

⚠️ Ne vaut que pour les **nouvelles** équipes. Les équipes existantes ont
leur propre propriété, dans `world/ftbteams/party/<uuid>.snbt` :

```
"ftbchunks:claim_visibility": "private"
```

⚠️ **Serveur arrêté obligatoire** pour modifier un fichier d'équipe : FTB
Teams garde ses données en mémoire et réécrit le fichier en sauvegardant.

---

## `world/serverconfig/openpartiesandclaims-server.toml`

```toml
[serverConfig.parties]
    enabled = false      # défaut true
[serverConfig.claims]
    enabled = false      # défaut true
```

✅ **Le mod a été retiré du pack** lors de la mise à jour du
20 septembre — son jar n'est plus dans `/mods`. Ces fichiers de
configuration subsistent dans le monde, sans effet. Les laisser ne
coûte rien ; les supprimer serait sans conséquence non plus.

---

## Valeurs d'origine qu'il vaut mieux connaître

Ces réglages n'ont pas été modifiés, mais ils surprennent.

### `config/inmis.json`

```
baby 3 · frayed 9 · plated 18 · gilded 27
bejeweled 45 · blazing 54 (ignifugé) · withered 66 · endless 90

disableShulkers: true              shulkers interdits dans les sacs
spillMainBackpacksOnDeath: false   le contenu ne se perd pas à la mort
allowBackpacksInChestplate: true
```

### `config/galosphere-common.toml`

```
slowedBuddingAmethystMiningSpeed = true
spectreFlareAncientCityLoot      = true
pillagerDropPalladiumNugget      = true
```

### `config/bountiful/bountiful.json`

```
boardUpdateFrequency: 45     renouvellement, en secondes
maxNumRewards: 2
shouldBountiesHaveTimersAndExpire: true
```

### `config/paxi/datapacks/create-galosphere-fix/`

Datapack qui fait cohabiter l'argent de Galosphere avec les recettes de
Create, en fusion et en cuisson.

### `world/serverconfig/pylons-server.toml`

Exile Pylon désactivé. ⚠️ **À refaire si le monde est réinitialisé** : ce
fichier vit dans le monde, pas dans la configuration globale.

## `config/Discord-Integration.toml`

```toml
[webhook]
  enable = true
```

Le mode webhook poste chaque message **sous le pseudo et la tête de
skin du joueur**, au lieu du bot. Beaucoup plus lisible dans
`#chat-ingame`, où l'on voit qui parle d'un coup d'œil.

⚠️ **Correction du 22 septembre** : je l'avais désactivé la veille en
croyant qu'il empêchait la traduction de `#journal-serveur`. C'était
faux — `journal-fr.js` accepte les messages de webhook depuis le
début. Les messages anglais de cette nuit-là venaient de **Railway à
l'arrêt** à la fin de l'essai, et de l'absence de règle pour
« Server Started! », ajoutée depuis.

S'applique à chaud : `discord reload`

## Planning de 5 h — annonces en `tellraw`, pas en `say`

Discord Integration relaie **tout `say`** dans `#chat-ingame` comme un
message de chat. Les trois annonces du redémarrage couvraient chaque
matin les conversations, et donnaient l'impression d'un salon mort.

`tellraw @a` affiche le même texte en jeu sans passer par le chat :
rien n'est relayé.

⚠️ **Toute annonce automatique doit utiliser `tellraw`.** Un `say`
ajouté plus tard dans un planning ou une fonction réapparaîtra dans
le salon.

## `config/alexsmobs.toml` — section `[spawning]`

Dix-sept poids divisés par deux, le 21 septembre. Seuls ceux de 20 et
plus, parmi les créatures terrestres de l'Overworld — celles qui
occupent la place des animaux vanilla dans leurs biomes.

```toml
gazelleSpawnWeight = 20                 # 40
rockyRollerSpawnWeight = 30             # 60
elephantSpawnWeight = 15                # 30
tigerSpawnWeight = 15                   # 30
caimanSpawnWeight = 14                  # 29
capuchinMonkeySpawnWeight = 14          # 28
mudskipperSpawnWeight = 14              # 28
gorillaSpawnWeight = 12                 # 25
kangarooSpawnWeight = 12                # 25
rhinocerosSpawnWeight = 12              # 24
toucanSpawnWeight = 11                  # 23
seagullSpawnWeight = 10                 # 21
crocodileSpawnWeight = 10               # 20
alligatorSnappingTurtleSpawnWeight = 10 # 20
emuSpawnWeight = 10                     # 20
platypusSpawnWeight = 10                # 20
froststalkerSpawnWeight = 10            # 20
```

⚠️ **Prend effet au redémarrage**, pas au `reload`.

Pour comparer, en plaine vanilla : mouton 12, cochon 10, poule 10,
vache 8. Les créatures d'Alex's Mobs puisent dans le même quota que
les animaux vanilla ; avec des poids de 40 ou 60, elles les
évinçaient de leurs biomes.

## Datapack — repeuplement des animaux vanilla

`data/bmc4/functions/animaux/` : toutes les trois minutes, en plein
jour, pour chaque joueur de l'Overworld entouré de moins de huit
animaux vanilla dans 64 blocs, une paire apparaît sur l'herbe entre
24 et 48 blocs de lui — mouton, vache, cochon ou poule, une chance
sur quatre chacun.

**Pourquoi** : Minecraft ne fait naître les animaux qu'à la génération
d'un chunk. Autour d'une base habitée, ils disparaissent et ne
reviennent pas — y compris en vanilla. Ce cycle compense sans
surpeupler : au-dessus de huit animaux, il ne fait rien, donc un
élevage ne déclenche pas de nouvelles apparitions.

## Mode fair-play de Xaero's Minimap

Le code `§f§a§i§r§x§a§e§r§o`, en fin de `motd`, active le **mode
fair-play** de Xaero : le radar d'entités et le mode grotte sont
coupés sur toutes les minimaps. La carte, les waypoints et
l'exploration restent intacts.

Les codes de couleur ne s'affichent pas dans la liste des serveurs :
le message reste identique à l'œil. Xaero les lit à la connexion.

**Pourquoi** : le radar montrait chaque joueur dans un rayon d'une
soixantaine de blocs, à travers les murs et **même invisible** — la
cape d'invisibilité ne servait à rien. Sur un serveur en factions, il
rendait aussi toute approche surprise impossible avant un raid.

⚠️ **Prend effet au redémarrage du serveur**, puis à la reconnexion
de chaque joueur. Le serveur ne peut pas masquer seulement les
joueurs invisibles : c'est tout le radar ou rien.

