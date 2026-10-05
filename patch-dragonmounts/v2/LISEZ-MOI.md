# dragonmounts — patch BMC4, version 2

Construit le 29 septembre 2026 à partir de `dragonmounts-1.20.1-10018.jar`
d'origine (3 136 744 octets). **Remplace la version 1 du matin**, qui ne
contenait que la première correction.

Deux fichiers modifiés sur 664. Tout le reste est copié à l'identique.

---

## 1. Probabilité sur les croisements hybrides

`com/github/kay9/dragonmounts/data/CrossBreedingManager.class`

Prologue injecté au début de `getCrossBreed` :

```java
if (Math.random() < 0.25) { /* comportement d'origine : hybride */ }
else return null;
```

Rendre `null` n'est pas un cas d'erreur : c'est déjà ce que la méthode
renvoie quand la paire n'est pas dans la table, et
`TameableDragon.spawnChildFromBreeding` le traite en retombant sur son
propre pile ou face entre les deux parents. **Aucun chemin d'exécution
neuf n'est créé** — on réemprunte celui du mod.

---

## 2. Têtes de wither éternelles

`com/github/kay9/dragonmounts/dragon/WitherBreathBall.class`

### Le défaut

Le mod enregistre cinq types d'entité pour ses souffles —
`black_fire_breath`, `blue_fire_breath`, `storm_breath`, `ice_breath`,
`sculk_breath`. **Le souffle Wither n'en a pas.** `WitherBreathBall`
hérite de `WitherSkull` sans rien enregistrer, donc en jeu ces
projectiles sont des `minecraft:wither_skull` vanilla purs.

La limite de portée de 40 blocs est codée dans le `tick()` de
`WitherBreathBall`. Mais quand un chunk est sauvegardé puis rechargé, le
jeu reconstruit l'entité **depuis son type enregistré** — un
`WitherSkull` vanilla, qui n'a ni cette limite ni aucun minuteur de
disparition. La tête perd la logique du mod et devient permanente.

43 têtes avaient ainsi été semées dans l'Overworld au 29 septembre.

### La correction

Ajout de `save(CompoundTag)` renvoyant `false`.

`EntityStorage.storeEntities` appelle `Entity.m_20223_` et n'écrit
l'entité que si elle rend `true` — vérifié en désassemblant le jar
client de Forge 47.4.20. Le projectile n'est donc **jamais écrit sur
disque**, et ne peut plus revenir orphelin. Un souffle vit deux
secondes : il n'a aucune raison d'être sauvegardé.

### Pourquoi pas la correction « propre »

Enregistrer un vrai type d'entité pour le souffle Wither serait la vraie
correction. Elle est **impossible ici** : les joueurs tournent avec le
jar d'origine et ne connaîtraient pas ce type, le paquet d'apparition
échouerait sur chaque client. Ce patch doit rester purement serveur.

C'est aussi pour ça qu'on n'a pas touché à `getType()` : la moindre
modification du type d'entité sort du périmètre serveur.

---

## Vérifications faites

- `javap` sur les deux classes : bytecode conforme à l'intention
- `StackMapTable` de `getCrossBreed` : frame `same` ajoutée à l'offset
  12, `offset_delta` de la frame suivante recalculé de 72 à 71
- Vérifieur de pile ASM : 5 méthodes de `CrossBreedingManager` et 11 de
  `WitherBreathBall`, aucune incohérence
- Jar : 664 entrées avant et après, **exactement deux** fichiers
  différents, aucune signature à casser

---

## Installation

Déposer ce jar dans `/mods` du serveur, **en écrasant** celui qui s'y
trouve. Redémarrer.

**Côté serveur uniquement** : la version du mod ne change pas, aucun
client n'a à retélécharger quoi que ce soit.

---

## ⚠️ À refaire à chaque mise à jour du pack

Une mise à jour réinstalle le jar d'origine et **efface le patch en
silence** — pas un message d'erreur. Voir BMC-02 dans Todoist.

Repatcher le **nouveau** jar, jamais recopier celui-ci par-dessus une
version plus récente du mod :

```
javac --add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED \
      -d cls PatchJar.java

java  --add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED \
      -cp cls PatchJar <jar-origine> <jar-patche> 0.25
```

Le dernier paramètre est la probabilité : `0.10` pour 10 %, `0.50` pour
un croisement sur deux. Le patcheur **échoue bruyamment** si l'une des
deux méthodes visées a disparu — donc une nouvelle version du mod qui
casserait le patch se signalera d'elle-même.

## Nettoyage en place en attendant

Le planning Minestrator `34190` (« Nettoyage têtes de wither
orphelines ») rejoue un `kill` toutes les dix minutes sur les huit
dimensions. Une fois ce patch installé et le stock existant nettoyé, il
devient inutile et peut être désactivé.
