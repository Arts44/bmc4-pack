# dragonmounts — patch « chance sur les hybrides »

Construit le 29 septembre 2026 à partir de `dragonmounts-1.20.1-10018.jar`
(3 136 744 octets, identique à l'octet près au jar du serveur).

## Ce qui change

Un seul fichier sur 664 est modifié :
`com/github/kay9/dragonmounts/data/CrossBreedingManager.class`

Un prologue est injecté au début de `getCrossBreed` :

```java
if (Math.random() < 0.25) { /* comportement d'origine : hybride */ }
else return null;
```

Rendre `null` n'est pas un cas d'erreur : c'est déjà ce que la méthode
renvoie quand la paire n'est pas dans la table, et
`TameableDragon.spawnChildFromBreeding` le traite en retombant sur son
propre pile ou face entre les deux parents. **Aucun chemin d'exécution
neuf n'est créé** — on réemprunte celui du mod.

Résultat : 25 % de chance d'obtenir la race hybride, 75 % une des deux
races parentes.

## Pourquoi du bytecode et pas une recompilation

Forge 1.20.1 tourne en **noms SRG** en production. Une classe recompilée
depuis les noms Mojang ne se lierait à rien au chargement. Éditer le
bytecode existant préserve les références telles quelles.

## Vérifications faites

- `javap` : prologue conforme, saut vers l'offset 12
- `StackMapTable` : frame `same` ajoutée à l'offset 12, `offset_delta` de
  la frame suivante ajusté de 72 à 71 — recalcul automatique par ASM
- Vérifieur de pile sur les 5 méthodes de la classe : aucune incohérence
- Jar : 664 entrées avant et après, un seul fichier différent

## Installation

Déposer ce jar dans `/mods` du serveur, **en écrasant** celui qui s'y
trouve (même nom). Redémarrer.

**Côté serveur uniquement.** `spawnChildFromBreeding` ne tourne que
serveur, les clients n'ont pas besoin du jar patché, et la version du mod
ne change pas — Forge ne refusera aucune connexion.

## ⚠️ À refaire à chaque mise à jour du pack

Une mise à jour réinstalle le jar d'origine et efface le patch. Garder ce
dossier, et rejouer l'opération — voir BMC-55 dans Todoist.

## Pour changer le pourcentage

Le patcheur prend la chance en paramètre. 0.25 ici ; `0.10` pour 10 %,
`0.50` pour un croisement sur deux.
