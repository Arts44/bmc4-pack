# Configurations modifiées

Ce que nous avons changé par rapport au pack d'origine. **Ces valeurs sont
écrasées à chaque mise à jour du pack** — cette page sert à les remettre.

Le raisonnement derrière chaque choix est dans [`decisions.md`](../decisions.md).

---

## `server.properties`

```properties
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
```

⚠️ Section marquée « requires restart ».

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

Le mod reste chargé mais inerte. À retirer du pack — **des deux côtés**,
serveur et client, sinon Forge refuse les connexions.

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
