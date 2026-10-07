# Garder ses réglages en changeant de version du pack

**Brouillon, pas posté.** Procédure manuelle de secours (BMC-93), pour le
salon `#guide` ou `#performances-et-réglages`. Le script `migrer-bmc4` livré
dans le pack fait la même chose tout seul ; cette page sert quand il refuse
ou quand on préfère le faire à la main. Un message, sous 2 000 caractères.

---

**🔁 Nouvelle version du pack : garder ses touches, ses réglages et ses waypoints**

Importer le zip crée une **nouvelle instance** : tes réglages restent dans l'ancienne. Pour les reprendre, **avant de lancer la nouvelle** :

**1.** CurseForge → clic droit sur l'**ancienne** instance BMC4 → **Ouvrir le dossier**. Fais de même avec la **nouvelle**.

**2.** Copie de l'ancienne vers la nouvelle (remplace si on te le demande) :
```
options.txt        touches, langue, vidéo, son
servers.dat        ta liste de serveurs
xaero              waypoints et carte Xaero
local/ftbchunks    waypoints et carte FTB Chunks
```

**3.** Si tu avais réglé un shader : copie aussi `config/oculus.properties` et le fichier `.txt` de ton shader dans `shaderpacks/`.

**4.** Si tu avais **ajouté** toi-même des packs de ressources : copie-les dans `resourcepacks/`. Ne recopie pas ceux du pack.

**5.** Lance la nouvelle instance. Vérifie : langue, une touche que tu avais changée, et tes waypoints (touche **U** : la liste des waypoints Xaero ; touche **M** : la carte).

⚠️ **Ne supprime l'ancienne instance qu'une fois tout vérifié.**

💡 **Plus simple** : dans la nouvelle instance, double-clic sur `migrer-bmc4.command` (Mac) ou `migrer-bmc4.bat` (Windows), **avant le premier lancement**. Il fait tout ça et écrit ce qu'il a repris dans `migration-bmc4.log`.
