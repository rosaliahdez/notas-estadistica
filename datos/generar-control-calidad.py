# -*- coding: utf-8 -*-
"""Simula el control de calidad en el aula: 20 Pinguinos Marinela mini.
   Cada pieza se mide DOS veces, por dos observadores distintos, con el orden
   contrabalanceado. Archivo de respaldo mientras el grupo captura los datos reales.

   Lo que se le sembro a los datos, y que el analisis deberia recuperar:
     - el proceso llena por ARRIBA del contenido declarado (25 g): media real 26.1 g
     - la pieza pierde masa al ser manipulada (se desprende chocolate): -0.12 g
     - el observador B lee el diametro 0.5 mm mas grande (sesgo humano con la regla)
     - el observador NO afecta la masa: la bascula digital no sabe quien la mira
     - el lote 2 pesa 0.35 g mas que el lote 1, diferencia real pero DEMASIADO
       pequena para detectarla con 10 piezas por lote (sirve para motivar potencia)
"""
import random, math, statistics as st, csv, os
random.seed(2026)

DECLARADO   = 25.0    # g por pieza, segun el empaque (verificar en el que se compre)
N           = 20
SOBRELLENADO= 1.1     # g por arriba de lo declarado
DIF_LOTE    = 0.35    # g de mas en el lote 2
DESPRENDE   = 0.12    # g que pierde al manipularla
SESGO_B     = 0.5     # mm que lee de mas el observador B con la regla

piezas=[]
for i in range(1, N+1):
    lote = 1 if i <= N//2 else 2
    masa = DECLARADO + SOBRELLENADO + (DIF_LOTE if lote==2 else 0) + random.gauss(0,0.85)
    piezas.append(dict(id=i, lote=lote, masa=masa, diam=48 + random.gauss(0,1.6)))

# dos bloques de 10: en el primero mide A y luego B; en el segundo, al reves
filas=[]
for k,p in enumerate(piezas):
    primero, segundo = ("A","B") if (k % 2 == 0) else ("B","A")
    for orden,obs in enumerate([primero,segundo], start=1):
        masa = p["masa"] - (DESPRENDE if orden==2 else 0) + random.gauss(0,0.05)
        diam = p["diam"] + (SESGO_B if obs=="B" else 0) + random.gauss(0,0.6)
        filas.append(dict(id=p["id"], lote=p["lote"], observador=obs, orden=orden,
                          masa_g=round(masa,1), diametro_mm=round(diam)))

def borra(idd,orden,campo):
    for f in filas:
        if f["id"]==idd and f["orden"]==orden: f[campo]=""
borra(7,2,"diametro_mm")    # se deshizo al manipularla
borra(14,1,"masa_g")        # se registro mal y no se pudo repetir

# ==================== verificaciones ====================
num=lambda v: v not in ("",None)
def t1(vals, mu0):
    m=st.mean(vals); s=st.stdev(vals); n=len(vals)
    return m,s,(m-mu0)/(s/math.sqrt(n)),n
def tpar(campo, clave, a, b):
    d=[]
    for i in range(1,N+1):
        g={f[clave]:f for f in filas if f["id"]==i}
        if a in g and b in g and num(g[a][campo]) and num(g[b][campo]):
            d.append(g[b][campo]-g[a][campo])
    m=st.mean(d); s=st.stdev(d)
    return m,s,m/(s/math.sqrt(len(d))),len(d)

pri=[f["masa_g"] for f in filas if f["orden"]==1 and num(f["masa_g"])]
m,s,t,n=t1(pri, DECLARADO)
CRIT = {9:2.26, 17:2.11, 18:2.10, 19:2.09}
def veredicto(tv, gl):
    c = CRIT.get(gl, 2.10)
    return f"SE DETECTA (|t|={abs(tv):.2f} > {c})" if abs(tv) > c else f"NO se detecta (|t|={abs(tv):.2f} < {c})"
print(f"1) masa contra lo declarado ({DECLARADO} g): media={m:.2f}  sd={s:.2f}  t={t:+.2f}  n={n}")
print("   sobrellenado ->", veredicto(t, n-1))
m,s,t,n=tpar("masa_g","orden",1,2)
print(f"2) masa, 2a - 1a medicion: {m:+.3f} g  t={t:+.2f}  n={n}   ->", veredicto(t,n-1), "(se desprende chocolate)")
m,s,t,n=tpar("masa_g","observador","A","B")
print(f"3) masa, B - A:            {m:+.3f} g  t={t:+.2f}  n={n}   ->", veredicto(t,n-1), "(la bascula no sabe quien la lee)")
m,s,t,n=tpar("diametro_mm","observador","A","B")
print(f"4) diametro, B - A:        {m:+.2f} mm  t={t:+.2f}  n={n}   ->", veredicto(t,n-1), "(sesgo humano con la regla)")
a=[f["masa_g"] for f in filas if f["orden"]==1 and f["lote"]==1 and num(f["masa_g"])]
b=[f["masa_g"] for f in filas if f["orden"]==1 and f["lote"]==2 and num(f["masa_g"])]
sp=math.sqrt(((len(a)-1)*st.variance(a)+(len(b)-1)*st.variance(b))/(len(a)+len(b)-2))
t5=(st.mean(b)-st.mean(a))/(sp*math.sqrt(1/len(a)+1/len(b)))
print(f"5) lote 2 - lote 1: {st.mean(b)-st.mean(a):+.2f} g  t={t5:+.2f}  n={len(a)}+{len(b)}")
print("   ->", veredicto(t5, len(a)+len(b)-2), f"; la diferencia sembrada ({DIF_LOTE} g) es real pero la muestra es chica")
n_nec=2*((1.96+0.84)*sp/DIF_LOTE)**2
print(f"   -> harian falta ~{math.ceil(n_nec)} piezas por lote para detectarla con potencia 0.80")
print(f"\ncoef. de variacion de la masa: {100*st.stdev(pri)/st.mean(pri):.1f}%")

aqui=os.path.dirname(os.path.abspath(__file__))
cols=["id","lote","observador","orden","masa_g","diametro_mm"]
with open(os.path.join(aqui,"pinguinos-marinela-diseno-ejemplo.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,cols); w.writeheader()
    for r in sorted(filas,key=lambda r:(r["id"],r["orden"])): w.writerow({c:r[c] for c in cols})
cols2=["id","lote","masa_g","diametro_mm"]
with open(os.path.join(aqui,"pinguinos-marinela-ejemplo.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,cols2); w.writeheader()
    for r in sorted([x for x in filas if x["orden"]==1],key=lambda r:r["id"]):
        w.writerow({c:r[c] for c in cols2})
print("\nEscritos los dos CSV.")
