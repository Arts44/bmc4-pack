#!/usr/bin/env python3
"""Inventaire des conteneurs posés par les structures NBT de chaque mod
(BMC-88). Parcourt data/<mod>/structures/**/*.nbt dans chaque jar, lit la
palette (NBT gzip) et compte les blocs contenant chest/barrel/shulker/
crate/casket/pot/vault. Sort un JSON : {mod: {bloc: nb_pieces}}."""
import gzip, struct, sys, os, glob, zipfile, json, io

def read_nbt(data):
    pos = [0]
    def rd(fmt):
        s = struct.calcsize(fmt); v = struct.unpack('>' + fmt, data[pos[0]:pos[0]+s]); pos[0] += s; return v[0]
    def rstr():
        n = rd('H'); s = data[pos[0]:pos[0]+n].decode('utf-8', 'replace'); pos[0] += n; return s
    def payload(t):
        if t == 1: return rd('b')
        if t == 2: return rd('h')
        if t == 3: return rd('i')
        if t == 4: return rd('q')
        if t == 5: return rd('f')
        if t == 6: return rd('d')
        if t == 7:
            n = rd('i'); pos[0] += n; return None
        if t == 8: return rstr()
        if t == 9:
            et = rd('b'); n = rd('i'); return [payload(et) for _ in range(n)]
        if t == 10:
            d = {}
            while True:
                tt = rd('b')
                if tt == 0: return d
                name = rstr(); d[name] = payload(tt)
        if t == 11:
            n = rd('i'); pos[0] += 4*n; return None
        if t == 12:
            n = rd('i'); pos[0] += 8*n; return None
        raise ValueError(t)
    t = rd('b'); rstr(); return payload(t)

MOTS = ('chest', 'barrel', 'shulker', 'crate', 'casket', 'pot', 'vault', 'urn', 'coffin', 'sarcophag')
out = {}
for jar in sorted(glob.glob(os.path.join(sys.argv[1], '*.jar'))):
    try: z = zipfile.ZipFile(jar)
    except Exception: continue
    for n in z.namelist():
        if n.startswith('data/') and '/structures/' in n and n.endswith('.nbt'):
            mod = n.split('/')[1]
            try:
                d = read_nbt(gzip.decompress(z.read(n)))
            except Exception as e:
                out.setdefault(mod, {}).setdefault('__erreur__', 0); out[mod]['__erreur__'] += 1; continue
            for p in d.get('palette', []) or []:
                name = p.get('Name', '') if isinstance(p, dict) else ''
                if any(m in name for m in MOTS):
                    out.setdefault(mod, {}).setdefault(name, 0); out[mod][name] += 1
json.dump(out, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
for mod in sorted(out): print(mod, out[mod])
