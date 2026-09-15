# Le datapack `bmc4-fixes`

Vit dans `/world/datapacks/bmc4-fixes` sur le serveur. Cette copie sert de
sauvegarde : le dossier `world` n'est pas versionné.

## Ce qu'il fait

**Le kit de départ.** Outils en pierre, nourriture, torches, boussole,
donnés une seule fois par joueur à sa première connexion en survie.

Le suivi passe par un tableau de score `bmc4_kit`, pas par un advancement.
Une première version utilisait un advancement révoqué après usage : il se
redéclenchait au tick suivant, donnait le kit vingt fois par seconde, et a
généré 4 120 objets en deux minutes avant d'être coupé.

**L'équipe des dragons.** Tous les dragons rejoignent `bmc4_dragons`, avec
`friendlyFire false`. Minecraft ignore les représailles entre alliés, ce
qui arrête les bagarres en chaîne entre dragons de joueurs différents.

**Le modificateur `bmc4:reparer`.** Remet la durabilité à neuf :

```
item modify entity <pseudo> armor.chest bmc4:reparer
```

Emplacements : `armor.head`, `armor.chest`, `armor.legs`, `armor.feet`,
`weapon.mainhand`, `weapon.offhand`, `hotbar.0` à `hotbar.8`,
`inventory.0` à `inventory.26`.

## Installation

Copier le dossier `bmc4-fixes` dans `/world/datapacks/`, puis `reload` en
console. Le tableau de score et l'équipe se créent au chargement.
