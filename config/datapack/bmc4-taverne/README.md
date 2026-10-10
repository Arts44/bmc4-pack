# Le datapack `bmc4-taverne`

Seulement si la revue de #mods valide **Kaleidoscope Tavern** (v64). Vit alors
dans `/world/datapacks/bmc4-taverne` sur le serveur.

Kaleidoscope Tavern 1.2.0 n'a aucune option de configuration pour ses effets
(sa config ne règle que la cuve, le robinet de lave et la pose des
bouteilles). Ses effets de boisson sont des données de datapack
(`data/kaleidoscope_tavern/datamap/drink_effect/<boisson>.json`, lues par
`DrinkEffectDataReloadListener`). Ce datapack remplace les quatre boissons qui
donnent les trois effets refusés :

| Boisson | Effet d'origine | Pourquoi |
|---|---|---|
| `emerald` | Long Reach (allonge +3, 2 700 s) | portée au-delà du normal |
| `brass_heart`, `depth_charge` | Ardent Heat (minage 3×3, 300 s) | casse probablement sans passer par la protection des claims FTB Chunks |
| `godfather` | Zenith (téléportation à la surface) | sortie de n'importe quel enclos ou piège |

Chaque boisson donne à la place « Slightly Tipsy » 30 s. La liste d'effets ne
doit jamais être vide : le mod lit `effects.get(min(niveau, taille) - 1)`, et
une liste vide planterait au premier verre. Les cocktails du shaker
additionnent les effets de leurs ingrédients : ils n'héritent donc plus des
trois effets non plus. Les commandes `/effect` restent possibles pour un
opérateur.

## Installation

Copier le dossier `bmc4-taverne` dans `/world/datapacks/`, puis `reload` en
console ; le log doit dire `Successfully loaded drink effect data with 37
entries`. Vérifier avec `datapack list` qu'il est activé, et en jeu qu'un
verre d'Emerald ne donne plus Long Reach.
