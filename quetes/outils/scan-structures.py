#!/usr/bin/env python3
"""Pour chaque mod : blocs d'invocation (spawner, altar, summon, boss, totem, trial…)
dans les palettes des structures NBT, et entités posées (liste `entities`)."""
import gzip, struct, sys, os, glob, zipfile, json
sys.path.insert(0, os.path.expanduser('~/bmc4-pack-depot/quetes/outils'))
def read_nbt(data):
    pos=[0]
    def rd(f):
        s=struct.calcsize(f); v=struct.unpack('>'+f,data[pos[0]:pos[0]+s]); pos[0]+=s; return v[0]
    def rstr():
        n=rd('H'); s=data[pos[0]:pos[0]+n].decode('utf-8','replace'); pos[0]+=n; return s
    def payload(t):
        if t==1: return rd('b')
        if t==2: return rd('h')
        if t==3: return rd('i')
        if t==4: return rd('q')
        if t==5: return rd('f')
        if t==6: return rd('d')
        if t==7: n=rd('i'); pos[0]+=n; return None
        if t==8: return rstr()
        if t==9:
            et=rd('b'); n=rd('i'); return [payload(et) for _ in range(n)]
        if t==10:
            d={}
            while True:
                tt=rd('b')
                if tt==0: return d
                name=rstr(); d[name]=payload(tt)
        if t==11: n=rd('i'); pos[0]+=4*n; return None
        if t==12: n=rd('i'); pos[0]+=8*n; return None
        raise ValueError(t)
    t=rd('b'); rstr(); return payload(t)
MOTS=('spawner','altar','summon','boss','totem','trial','ritual','obelisk','statue','portal','egg','nest','cocoon','sarcophag','grave','relic')
out={}
def walk(d, found):
    if isinstance(d, dict):
        for k,v in d.items():
            if k=='id' and isinstance(v,str) and ':' in v: found.add(v)
            if k in ('SpawnData','SpawnPotentials','entity'): walk(v, found)
            else: walk(v, found)
    elif isinstance(d, list):
        for x in d: walk(x, found)
for jar in sorted(glob.glob(os.path.join(sys.argv[1],'*.jar'))):
    try: z=zipfile.ZipFile(jar)
    except Exception: continue
    for n in z.namelist():
        if n.startswith('data/') and '/structures/' in n and n.endswith('.nbt'):
            mod=n.split('/')[1]; o=out.setdefault(mod,{'blocs':{},'entites':{},'spawners':{}})
            try: d=read_nbt(gzip.decompress(z.read(n)))
            except Exception: o.setdefault('erreurs',0); o['erreurs']=o.get('erreurs',0)+1; continue
            for p in d.get('palette',[]) or []:
                name=p.get('Name','') if isinstance(p,dict) else ''
                if any(m in name for m in MOTS): o['blocs'][name]=o['blocs'].get(name,0)+1
            for b in d.get('blocks',[]) or []:
                nbt=b.get('nbt') if isinstance(b,dict) else None
                if nbt:
                    f=set(); walk(nbt,f)
                    for e in f:
                        if e.startswith('minecraft:') and e.split(':')[1] in ('mob_spawner','chest','barrel'): continue
                        o['spawners'][e]=o['spawners'].get(e,0)+1
            for e in d.get('entities',[]) or []:
                nbt=e.get('nbt',{}) if isinstance(e,dict) else {}
                eid=nbt.get('id','?') if isinstance(nbt,dict) else '?'
                o['entites'][eid]=o['entites'].get(eid,0)+1
json.dump(out,open(sys.argv[2],'w'),indent=1,ensure_ascii=False)
for m in sorted(out): print(m, json.dumps(out[m],ensure_ascii=False)[:600])
