import zipfile,json,os,sys,re,glob
mods=sys.argv[1]; out=sys.argv[2]
idx={'items':{}, 'entities':{}, 'biomes':{}, 'structures':{}, 'advancements':{}, 'dimensions':{}, 'tags_items':{}, 'tags_blocks':{}, 'tags_entities':{}, 'lang':{}, 'recipes':{}, 'mods':{}, 'fr':{}, 'tag_membres':{}, 'spawns':{}, 'biome_dim':{}}
for jar in sorted(glob.glob(os.path.join(mods,'*.jar'))):
    try: z=zipfile.ZipFile(jar)
    except Exception as e: print('ERR',jar,e); continue
    names=z.namelist()
    modid=None
    if 'META-INF/mods.toml' in names:
        t=z.read('META-INF/mods.toml').decode('utf-8','replace')
        m=re.search(r'modId\s*=\s*"([^"]+)"',t); modid=m.group(1) if m else None
        v=re.search(r'version\s*=\s*"([^"]+)"',t)
        idx['mods'][modid or os.path.basename(jar)]={'jar':os.path.basename(jar),'version':v.group(1) if v else None}
    for n in names:
        p=n.split('/')
        if n.startswith('assets/') and len(p)>=4 and p[2]=='lang' and p[3]=='fr_fr.json':
            try: d=json.loads(z.read(n).decode('utf-8','replace'))
            except Exception: continue
            for k,val in d.items():
                mm=re.match(r'^(item|block|entity|biome)\.([a-z0-9_.-]+)\.([a-z0-9_./-]+)$',k)
                if mm and isinstance(val,str): idx['fr'][f'{mm.group(2)}:{mm.group(3)}']=val
        if n.startswith('assets/') and len(p)>=4 and p[2]=='lang' and p[3]=='en_us.json':
            try:
                d=json.loads(z.read(n).decode('utf-8','replace'))
            except Exception: continue
            for k,val in d.items():
                if not isinstance(val,str): continue
                mm=re.match(r'^(item|block|entity|biome|advancements?|structure|dimension)\.([a-z0-9_.-]+)\.([a-z0-9_./-]+?)(\.title)?$',k)
                if mm:
                    kind,mod,rest,title=mm.groups()
                    if kind in('item','block'):
                        idx['items'][f'{mod}:{rest}']=val
                    elif kind=='entity': idx['entities'][f'{mod}:{rest}']=val
                    elif kind=='biome': idx['biomes'][f'{mod}:{rest}']=val
                    elif kind.startswith('advancement') and (title or k.endswith('.title')): idx['advancements'][f'{mod}:{rest}']=val
                    elif kind=='structure': idx['structures'][f'{mod}:{rest}']=val
                    elif kind=='dimension': idx['dimensions'][f'{mod}:{rest}']=val
            idx['lang'][p[1]]=idx['lang'].get(p[1],0)+len(d)
        elif n.startswith('data/') and len(p)>=4 and n.endswith('.json'):
            mod=p[1]; kind=p[2]
            key=f"{mod}:{'/'.join(p[3:])[:-5]}"
            if kind=='advancements': idx['advancements'].setdefault(key,None)
            elif kind=='worldgen' and len(p)>=5 and p[3]=='structure': idx['structures'].setdefault(f"{mod}:{'/'.join(p[4:])[:-5]}",None)
            elif kind=='worldgen' and len(p)>=5 and p[3]=='biome': idx['biomes'].setdefault(f"{mod}:{'/'.join(p[4:])[:-5]}",None)
            elif kind=='dimension' : idx['dimensions'].setdefault(key,None)
            elif kind=='recipes': idx['recipes'][key]=1
            elif kind=='tags' and len(p)>=5:
                tk={'items':'tags_items','blocks':'tags_blocks','entity_types':'tags_entities'}.get(p[3])
                if tk:
                    tname=f"{mod}:{'/'.join(p[4:])[:-5]}"
                    idx[tk].setdefault(tname,[]).append(os.path.basename(jar))
                    if p[3]=='items':
                        try: vals=json.loads(z.read(n).decode('utf-8','replace')).get('values',[])
                        except Exception: vals=[]
                        idx['tag_membres'].setdefault(tname,[]).extend(v if isinstance(v,str) else v.get('id','') for v in vals)
            if kind=='worldgen' and len(p)>=5 and p[3]=='biome':
                bid=f"{mod}:{'/'.join(p[4:])[:-5]}"
                try: bj=json.loads(z.read(n).decode('utf-8','replace'))
                except Exception: bj={}
                for cat,lst in (bj.get('spawners') or {}).items():
                    for sp in lst or []:
                        e=sp.get('type')
                        if e:
                            r=idx['spawns'].setdefault(e,{'cat':[],'biomes':[]})
                            if cat not in r['cat']: r['cat'].append(cat)
                            if bid not in r['biomes']: r['biomes'].append(bid)
            if kind=='forge' and len(p)>=4 and p[3]=='biome_modifier':
                try: bm=json.loads(z.read(n).decode('utf-8','replace'))
                except Exception: bm={}
                if str(bm.get('type','')).endswith('add_spawns'):
                    sps=bm.get('spawners'); sps=sps if isinstance(sps,list) else [sps]
                    bs=bm.get('biomes'); bs=bs if isinstance(bs,list) else [bs]
                    for sp in sps:
                        e=(sp or {}).get('type')
                        if e:
                            r=idx['spawns'].setdefault(e,{'cat':[],'biomes':[]})
                            for b in bs:
                                if b and b not in r['biomes']: r['biomes'].append(b)
            if kind=='dimension' and n.endswith('.json'):
                try: dj=json.loads(z.read(n).decode('utf-8','replace'))
                except Exception: dj={}
                def biomes_de(o):
                    if isinstance(o,dict):
                        if 'biome' in o and isinstance(o['biome'],str): yield o['biome']
                        for v in o.values(): yield from biomes_de(v)
                    elif isinstance(o,list):
                        for v in o: yield from biomes_de(v)
                for b in biomes_de(dj.get('generator',{})): idx['biome_dim'][b]=key
json.dump(idx,open(out,'w'),ensure_ascii=False)
print({k:len(v) for k,v in idx.items()})
