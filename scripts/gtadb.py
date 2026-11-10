import json,re,sys,datetime,os
SRC=sys.argv[1]; OUT=sys.argv[2]
d=json.load(open(SRC))
T=[('h',{'hotel'}),('r',{'residential'}),('c',{'retail','restaurant','office','supermarket','mixed'}),('o',{'leisure','landmark','events'}),
   ('t',{'transportation'}),('n',{'natural','agriculture'}),('i',{'industrial','utilities','construction'}),('p',{'public','government'})]
def short_rl(s):
    s=re.sub(r'(?<=.)\?$','',s.strip())
    if not s or s=='?': return ''
    parts=[p.strip() for p in s.split(',')]
    if parts[-1] in ('USA','United States'): parts=parts[:-1]
    if parts and re.match(r'^[A-Z]{2}( \d{5})?$',parts[-1]): parts=parts[:-1]
    if len(parts)>=3: return parts[0]+' · '+parts[-1]
    return ' · '.join(parts)
rows=[]
for k,v in d.items():
    c=v[1]
    if not c or len(c)!=2: continue
    X=round((c[0]+16384)/32,2); Y=round((16384-c[1])/32,2)
    parts=v[0].split(', ')
    name='' if parts[0].strip() in ('?','') else parts[0].strip()
    area=', '.join(parts[1:])
    tags=set(t.lower() for t in v[6])
    typ='x'
    for code,S in T:
        if tags & S: typ=code; break
    fl=(1 if 'enterable' in tags else 0)|(2 if 'unconfirmed' in tags else 0)|(4 if 'closed' in tags else 0)|(8 if 'demolished' in tags else 0)
    rows.append([int(k[1:]),name,area,X,Y,short_rl(v[3]),typ,fl])
rows.sort(key=lambda r:r[0])
# intern areas
areas=sorted({r[2] for r in rows}); ai={a:i for i,a in enumerate(areas)}
for r in rows: r[2]=ai[r[2]]
out={"fuente":"GTA VI Landmarks Data (CC BY 4.0) — https://map.gtadb.org","licencia":"https://creativecommons.org/licenses/by/4.0/deed.es",
     "cambios":"Coordenadas convertidas a unidades del mapa, campos simplificados y sin fotos.","fecha":datetime.date.today().isoformat(),
     "areas":areas,"l":rows}
json.dump(out,open(OUT,'w'),ensure_ascii=False,separators=(',',':'))
print(len(rows),'puntos', len(areas),'áreas', round(os.path.getsize(OUT)/1024),'KB')
