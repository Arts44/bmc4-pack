#!/usr/bin/env python3
# ============================================================
#  liste-crash-assistant.py — Regénère config/crash_assistant/modlist.json
#  pour une version du pack (v64, 10 octobre 2026)
#
#  python3 releases/liste-crash-assistant.py <version de Forge> <sortie.json> <jar ou dossier>…
#
#  Crash Assistant compare la liste des mods au lancement à ce fichier et
#  affiche l'écart dans son rapport de crash : livré à jour, l'écart montre
#  seulement ce que le joueur a ajouté ou retiré lui-même.
#  Une entrée par jar, clé = nom du jar, triées sans tenir compte de la casse,
#  comme le fichier que Crash Assistant écrit :
#    modId, name, version   le premier [[mods]] de META-INF/mods.toml
#                           (${file.jarVersion} = Implementation-Version),
#                           ou fabric.mod.json pour un mod Fabric (Connector)
#    curseForgeHash         empreinte CurseForge : murmur2 (graine 1) du jar
#                           privé des octets 9, 10, 13 et 32
#    modrinthHash           SHA-1 du jar
#  Un jar sans [[mods]] (fournisseur de langage, bibliothèque) n'a que
#  jarName et les deux empreintes. Algorithme vérifié sur la liste de la v62 :
#  315 entrées sur 315 jars identiques.
# ============================================================
import hashlib, json, os, re, sys, zipfile

def murmur2(data, seed=1):
    m = 0x5bd1e995
    h = (seed ^ len(data)) & 0xffffffff
    i = 0
    while len(data) - i >= 4:
        k = (int.from_bytes(data[i:i + 4], 'little') * m) & 0xffffffff
        k = ((k ^ (k >> 24)) * m) & 0xffffffff
        h = ((h * m) & 0xffffffff) ^ k
        i += 4
    reste = len(data) - i
    if reste == 3:
        h ^= data[i + 2] << 16
    if reste >= 2:
        h ^= data[i + 1] << 8
    if reste >= 1:
        h = ((h ^ data[i]) * m) & 0xffffffff
    h = ((h ^ (h >> 13)) * m) & 0xffffffff
    return h ^ (h >> 15)

def premier_mod(toml):
    """Les clés du premier bloc [[mods]] de mods.toml (Python 3.9 : pas de tomllib)."""
    bloc, vu = {}, False
    for ligne in toml.splitlines():
        ligne = ligne.strip()
        if ligne.startswith('['):
            if vu:
                break
            vu = ligne.split('#')[0].replace(' ', '') == '[[mods]]'
            continue
        if not vu:
            continue
        r = re.match(r'([A-Za-z]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', ligne)
        if r:
            bloc.setdefault(r.group(1), r.group(2) if r.group(2) is not None else r.group(3))
    if 'modId' not in bloc:
        # forme en ligne : mods = [ { modId = '…', version = '…', … } ]
        r = re.search(r'^\s*mods\s*=\s*\[\s*\{(.*?)\}', toml, re.M | re.S)
        if r:
            for c, v1, v2 in re.findall(r'([A-Za-z]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', r.group(1)):
                bloc.setdefault(c, v1 or v2)
    return bloc if 'modId' in bloc else None

def entree(chemin):
    brut = open(chemin, 'rb').read()
    nom = os.path.basename(chemin)
    e = {'jarName': nom}
    with zipfile.ZipFile(chemin) as z:
        if 'fabric.mod.json' in z.namelist() and 'META-INF/mods.toml' not in z.namelist():
            fmj = json.loads(z.read('fabric.mod.json').decode('utf-8', 'replace'), strict=False)
            e.update(modId=fmj['id'], name=fmj.get('name', fmj['id']), version=fmj.get('version', ''))
        elif 'META-INF/mods.toml' in z.namelist():
            mod = premier_mod(z.read('META-INF/mods.toml').decode('utf-8', 'replace'))
            if mod:
                version = str(mod.get('version', ''))
                if '${file.jarVersion}' in version:
                    mf = z.read('META-INF/MANIFEST.MF').decode('utf-8', 'replace') if 'META-INF/MANIFEST.MF' in z.namelist() else ''
                    iv = re.search(r'^Implementation-Version: *(.+?)\s*$', mf, re.M)
                    version = version.replace('${file.jarVersion}', iv.group(1) if iv else '0.0NONE')
                e.update(modId=mod['modId'], name=mod.get('displayName', mod['modId']), version=version)
    e['curseForgeHash'] = murmur2(bytes(b for b in brut if b not in (9, 10, 13, 32)))
    e['modrinthHash'] = hashlib.sha1(brut).hexdigest()
    return e

def main(forge, sortie, *sources):
    jars = []
    for s in sources:
        if os.path.isdir(s):
            jars += [os.path.join(s, f) for f in os.listdir(s) if f.endswith('.jar')]
        else:
            jars.append(s)
    noms = [os.path.basename(j) for j in jars]
    doubles = {n for n in noms if noms.count(n) > 1}
    if doubles:
        raise SystemExit(f'jars en double : {sorted(doubles)}')
    cle = f'fmlloader-1.20.1-{forge}.jar (modloader)'
    liste = {cle: {'jarName': cle, 'modId': 'forge', 'name': 'forge', 'version': f'fmlloader-1.20.1-{forge}.jar'}}
    for j in sorted(jars, key=lambda p: os.path.basename(p).lower()):
        liste[os.path.basename(j)] = entree(j)
    with open(sortie, 'w', encoding='utf-8') as f:
        json.dump(liste, f, indent=2, ensure_ascii=False)
    print(f'{sortie} : {len(liste) - 1} jars')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise SystemExit('usage : liste-crash-assistant.py <version de Forge> <sortie.json> <jar ou dossier>…')
    main(*sys.argv[1:])
