# Journal des décisions — BMC4

Pourquoi le serveur est réglé comme il l'est. Chaque entrée dit ce qui a
été décidé, quand, et surtout **pourquoi** — c'est le pourquoi qui se perd.

---

## Serveur et performances

### Difficulté en normal — 7 septembre

Le serveur tournait en `easy`. Le pack est équilibré pour `normal`, et
Cataclysm comme l'Aether n'ont aucun sens en facile.

### Distance de simulation à 6 — 7 septembre

Ramenée de 10 à 6. Moins d'entités calculées autour de chaque joueur, en
prévision de la montée en charge. La distance de vue reste à 10 : aucune
différence visible pour les joueurs.

### 32 mods clients retirés du serveur — 7 septembre

Des mods purement graphiques étaient chargés côté serveur pour rien :
fancymenu (24 Mo), EuphoriaPatcher, les trois Xaero, entityculling,
chat_heads, MouseTweaks et 25 autres. Déplacés dans `/mods-clients`,
restaurables en une commande.

Résultat : journal de démarrage de 10 067 à 6 396 lignes, démarrage en
4,6 secondes.

Gardés malgré tout : pingwheel, watut et nochatreports, qui ont besoin du
serveur ; la famille JEI, qui sert de dépendance ; et Jade.

### Watchdog à 300 secondes — 8 septembre

`max-tick-time` passé de 60 000 à 300 000 ms.

Le serveur se tuait au bout d'une minute de blocage. Avec cinq minutes, il
a le temps de se dépêtrer d'un pic au lieu de mourir. C'est un pansement,
mais il a évité une coupure le jour même.

### Prégénération de huit dimensions — 7 septembre

Chunky, environ 175 000 chunks. Overworld rayon 2000, les sept autres
dimensions rayon 1000. Disque de 3,2 à 4,4 Go.

La génération de terrain à la volée était la première source de pics CPU.

### Redémarrage quotidien à 5 h

Planning MineStrator, avec préavis à 5 min et à 1 min, forceload des deux
bases, suppression des objets au sol, `save-all`, `stop`, puis `start`
90 secondes après.

**Stop + start plutôt que restart** : le bug de chargement aléatoire de
Quark laisse parfois le serveur en état zombie, et `restart` n'en sort pas.

---

## Claims et factions

### Open Parties and Claims désactivé — 8 septembre

Deux systèmes de claim tournaient en parallèle. Seul Arts_Vio utilisait
OPAC, avec 9 chunks (x −35 à −33, z 64 à 66). Ils ont été migrés vers FTB
Chunks, puis OPAC désactivé — claims **et** parties.

Sans ça, le règlement de raid était ambigu sur ce qui est « hors claim ».

Le mod reste chargé ; à retirer à la prochaine mise à jour du pack.

### Visibilité des claims en privé — 9 septembre

`def_claim_visibility` passé de `public` à `private`, et les deux équipes
existantes modifiées.

Par défaut, chacun voyait les revendications de tous sur la carte sans
avoir exploré. Incompatible avec la règle sur le secret des coordonnées.

⚠️ **FTB Teams garde ses données en mémoire et réécrit ses fichiers en
sauvegardant.** Une première tentative serveur allumé a été écrasée. Toute
modification des fichiers d'équipe exige un arrêt.

### Alliance HelXo1 ↔ Farmer's supprimée — 9 septembre

HelXo1 figurait comme `ally` de l'équipe Farmer's depuis fin août, ce qui
lui donnait accès à leurs claims et rendait sa position visible — alors
qu'il joue pour Apex. Personne ne l'avait décidé.

---

## Équilibrage

### Vol autorisé, mod Theft conservé — 8 septembre

Première réaction : couper la génération des gants, le mod contredisant la
règle « pas de vol ». **Décision inverse après discussion** : le vol au
gant fait partie du jeu, et c'est le règlement qui a été réécrit.

La frontière est le claim, pas l'objet. Dedans, rien n'est permis ; dehors,
le gant l'est, sans accord de la victime.

### Chances d'œufs de dragon relevées — 8 septembre

Les huit structures de `dragonmounts-common.toml` :

```
Bastion              35 → 45 %
Temple de la jungle  30 → 40 %
Manoir               20 → 30 %
Igloo                20 → 30 %
Trésor enfoui      17,5 → 30 %
Donjon simple        15 → 25 %
Mineshaft           9,5 → 20 %
Pyramide           7,5 → 20 %
```

Impossible d'ajouter les structures modées : les clés de configuration sont
fixes.

### Errance des dragons réduite — 9 septembre

`dragon_wander_range` de 30 à 8, soit un cube de 16 blocs au lieu de 60.
Les dragons montaient à trente blocs et disparaissaient.

### Dragons dans une équipe sans tir allié — 9 septembre

Datapack : tous les dragons rejoignent l'équipe `bmc4_dragons`, avec
`friendlyFire false`.

Minecraft ignore les représailles entre alliés. Un dragon touché par le
souffle d'un autre ne le prend plus pour cible — ça arrêtait les bagarres
en chaîne entre dragons de joueurs différents.

---

## Incidents

### 4 597 objets au sol — 8 septembre

Le serveur a planté deux fois le matin, 96 puis 70 secondes après la
connexion de GhostFrost016, puis est resté hors ligne trois heures.

Cause : des os et des flèches accumulés autour de la base des Farmer's,
chargés d'un coup à son arrivée. Chaque objet déclenchait l'événement
`onEntityStep` de Blueprint, et le tick partait à 60 secondes.

**Mécanisme à retenir** : un objet au sol ne disparaît que pendant que son
chunk est chargé. Quand les joueurs partent, le compteur se fige et tout
s'accumule d'une session à l'autre.

### Kit de départ en boucle — 8 septembre

Un advancement déclenché à chaque tick donnait le kit, se révoquait, et se
redéclenchait. **4 120 objets générés en deux minutes**, serveur figé huit
secondes, joueur déconnecté.

Réécrit avec un compteur de tableau de score : `unless score matches 0..`
n'est vrai que pour un score jamais inscrit, et un score écrit reste écrit.

**Leçon** : ne jamais déployer un datapack non testé sur un serveur en
production.
