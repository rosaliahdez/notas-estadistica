# -*- coding: utf-8 -*-
"""Genera y verifica las bases de datos simuladas para el curso de Estadística.
Solo requiere numpy y pandas. Semilla fija = 2026 para reproducibilidad."""
import numpy as np, pandas as pd, math, os

OUT = "/sessions/affectionate-lucid-ritchie/mnt/outputs/datos_simulados"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(2026)

# ---------- p-values sin scipy (Numerical Recipes) ----------
def gammln(x): return math.lgamma(x)
def gammp(a, x):
    if x < 0 or a <= 0: raise ValueError
    if x < a + 1:  # serie
        ap, s, d = a, 1.0/a, 1.0/a
        for _ in range(500):
            ap += 1; d *= x/ap; s += d
            if abs(d) < abs(s)*1e-12: break
        return s*math.exp(-x + a*math.log(x) - gammln(a))
    else:          # fracción continua -> Q, regresar 1-Q
        b, c = x+1-a, 1e300; d = 1.0/b; h = d
        for i in range(1, 500):
            an = -i*(i-a); b += 2
            d = an*d + b;  d = 1e-300 if abs(d) < 1e-300 else d
            c = b + an/c;  c = 1e-300 if abs(c) < 1e-300 else c
            d = 1.0/d; delt = d*c; h *= delt
            if abs(delt-1) < 1e-12: break
        Q = math.exp(-x + a*math.log(x) - gammln(a))*h
        return 1.0 - Q
def betacf(a, b, x):
    qab, qap, qam = a+b, a+1, a-1
    c = 1.0; d = 1 - qab*x/qap
    d = 1e-300 if abs(d) < 1e-300 else d; d = 1.0/d; h = d
    for m in range(1, 300):
        m2 = 2*m
        aa = m*(b-m)*x/((qam+m2)*(a+m2))
        d = 1+aa*d; d = 1e-300 if abs(d) < 1e-300 else d
        c = 1+aa/c; c = 1e-300 if abs(c) < 1e-300 else c
        d = 1.0/d; h *= d*c
        aa = -(a+m)*(qab+m)*x/((a+m2)*(qap+m2))
        d = 1+aa*d; d = 1e-300 if abs(d) < 1e-300 else d
        c = 1+aa/c; c = 1e-300 if abs(c) < 1e-300 else c
        d = 1.0/d; delt = d*c; h *= delt
        if abs(delt-1) < 1e-12: break
    return h
def betai(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    bt = math.exp(gammln(a+b)-gammln(a)-gammln(b)+a*math.log(x)+b*math.log(1-x))
    return bt*betacf(a, b, x)/a if x < (a+1)/(a+b+2) else 1-bt*betacf(b, a, 1-x)/b
def p_t_two(t, v):    # dos colas
    return betai(v/2, 0.5, v/(v+t*t))
def p_F_upper(f, d1, d2):
    return betai(d2/2, d1/2, d2/(d2+d1*f))
def p_chi2_upper(x, k):
    return 1 - gammp(k/2, x/2)
def p_z_two(z):
    return math.erfc(abs(z)/math.sqrt(2))

# ---------- pruebas ----------
def anova(values, groups):
    labs = pd.unique(groups); grand = values.mean(); k = len(labs); N = len(values)
    ssb = sum(len(values[groups==g])*(values[groups==g].mean()-grand)**2 for g in labs)
    ssw = sum(((values[groups==g]-values[groups==g].mean())**2).sum() for g in labs)
    d1, d2 = k-1, N-k; F = (ssb/d1)/(ssw/d2)
    return F, d1, d2, p_F_upper(F, d1, d2)
def welch_t(a, b):
    m1,m2,v1,v2,n1,n2 = a.mean(),b.mean(),a.var(ddof=1),b.var(ddof=1),len(a),len(b)
    t = (m1-m2)/math.sqrt(v1/n1+v2/n2)
    df = (v1/n1+v2/n2)**2/((v1/n1)**2/(n1-1)+(v2/n2)**2/(n2-1))
    return t, df, p_t_two(t, df)
def chi2_ct(tab):
    tab = tab.astype(float); rt = tab.sum(1, keepdims=True); ct = tab.sum(0, keepdims=True); N = tab.sum()
    E = rt@ct/N; X2 = ((tab-E)**2/E).sum(); df = (tab.shape[0]-1)*(tab.shape[1]-1)
    return X2, df, p_chi2_upper(X2, df)
def lin_reg(x, y):
    n = len(x); xb, yb = x.mean(), y.mean()
    Sxx = ((x-xb)**2).sum(); Sxy = ((x-xb)*(y-yb)).sum()
    b = Sxy/Sxx; a = yb-b*xb; yhat = a+b*x; sse = ((y-yhat)**2).sum()
    s2 = sse/(n-2); seb = math.sqrt(s2/Sxx); t = b/seb
    r = Sxy/math.sqrt(Sxx*((y-yb)**2).sum())
    return a, b, r, t, n-2, p_t_two(t, n-2)

report = []
def say(s): report.append(s); print(s)

# ============ 1. GALLETAS (ANOVA de un factor) ============
marcas = ["Oreo", "Chokis", "Lors", "GreatValue"]
base = {"Oreo":7.3, "Chokis":6.6, "Lors":5.8, "GreatValue":5.4}
nj = 25
rows = []
for j in range(1, nj+1):
    juez_eff = rng.normal(0, 0.6)
    orden = rng.permutation(marcas)               # orden de cata balanceado por juez
    for pos, m in enumerate(orden, start=1):
        fatiga = -0.12*(pos-1)                     # cansancio de paladar
        val = base[m] + juez_eff + fatiga + rng.normal(0, 1.0)
        val = int(np.clip(round(val), 1, 9))
        rows.append((j, pos, m, val))
gall = pd.DataFrame(rows, columns=["juez","orden","marca","agrado"])
gall.to_csv(f"{OUT}/galletas.csv", index=False)
F,d1,d2,p = anova(gall["agrado"].values, gall["marca"].values)
say(f"[galletas] ANOVA marca: F({d1},{d2})={F:.2f}, p={p:.2e}  medias="
    + ", ".join(f"{m}:{gall[gall.marca==m].agrado.mean():.2f}" for m in marcas))

# ============ 2. LAGARTIJAS (dos muestras) ============
n_u, n_c = 32, 30
def lz(n, hab, temp, mt, masa, ms, lhc, ml, fc, mf):
    return pd.DataFrame({
        "id":[f"{hab[:1].upper()}{i:02d}" for i in range(1,n+1)], "habitat":hab,
        "temp_corporal": np.round(rng.normal(temp, mt, n),1),
        "masa_g":        np.round(rng.normal(masa, ms, n),1),
        "lhc_mm":        np.round(rng.normal(lhc, ml, n),1),
        "frec_cardiaca": np.round(rng.normal(fc, mf, n)).astype(int)})
lag = pd.concat([
    lz(n_u,"urbana", 35.3,1.4, 14.5,3.0, 62,5.0, 88,10),   # urbana: mas calida y variable
    lz(n_c,"campo",  33.9,1.2, 12.8,2.6, 62,5.0, 80, 9)],
    ignore_index=True)
lag.to_csv(f"{OUT}/lagartijas.csv", index=False)
u = lag[lag.habitat=="urbana"]; c = lag[lag.habitat=="campo"]
for var in ["temp_corporal","lhc_mm","masa_g"]:
    t,df,p = welch_t(u[var].values, c[var].values)
    say(f"[lagartijas] t Welch {var}: t={t:.2f}, gl={df:.1f}, p={p:.4f} "
        f"(urb {u[var].mean():.2f} vs campo {c[var].mean():.2f})")

# ============ 3. RICKETTSIOSIS (proporciones y ji-cuadrada) ============
def expit(x): return 1/(1+np.exp(-x))
zonas = np.array(["urbana_marginada"]*180 + ["urbana"]*140 + ["rural"]*100)
rng.shuffle(zonas)
p_perro = {"urbana_marginada":0.75,"urbana":0.50,"rural":0.80}
contacto = np.array([rng.random() < p_perro[z] for z in zonas])
p_gar = np.where(contacto, 0.55, 0.20)
garrapatas = rng.random(len(zonas)) < p_gar
lin = -2.6 + 1.1*contacto + 1.0*garrapatas + 0.5*(zonas=="urbana_marginada")
positivo = rng.random(len(zonas)) < expit(lin)
rick = pd.DataFrame({"id":[f"P{i:03d}" for i in range(1,len(zonas)+1)], "zona":zonas,
    "contacto_perro":np.where(contacto,"si","no"),
    "garrapatas":np.where(garrapatas,"si","no"),
    "resultado":np.where(positivo,"positivo","negativo")})
rick.to_csv(f"{OUT}/rickettsiosis.csv", index=False)
ct = pd.crosstab(rick.contacto_perro, rick.resultado)
X2,df,p = chi2_ct(ct.values)
say(f"[rickettsiosis] ji-cuadrada contacto_perro x resultado: X2={X2:.2f}, gl={df}, p={p:.2e}")
pp = rick.groupby("contacto_perro").resultado.apply(lambda s:(s=='positivo').mean())
say(f"           positividad: contacto si={pp['si']:.2%}, no={pp['no']:.2%}; global={(rick.resultado=='positivo').mean():.2%}")

# ============ 4a. ALGORITMOS - REGRESION (tiempo ~ tamaño) ============
sizes = np.repeat(np.arange(1000, 10001, 1000), 5)     # 10 tamaños x 5 réplicas
rows = []
for ent,(a,b,sd) in {"Mac":(1.5,0.00170,1.5),"Windows":(2.2,0.00195,1.7)}.items():
    for n in sizes:
        t = a + b*n + 1e-8*n*n + rng.normal(0, sd)      # leve curvatura para residuales
        rows.append((ent, int(n), round(max(t,0.1),2)))
alg = pd.DataFrame(rows, columns=["entorno","n","tiempo_ms"])
alg.to_csv(f"{OUT}/algoritmos_regresion.csv", index=False)
mac = alg[alg.entorno=="Mac"]
a,b,r,t,df,p = lin_reg(mac.n.values.astype(float), mac.tiempo_ms.values)
say(f"[algoritmos] regresion (Mac) tiempo~n: b={b:.5f} ms/elem, r={r:.3f}, t={t:.1f}, gl={df}, p={p:.2e}")

# ============ 4b. ALGORITMOS - A/B (dos muestras, n fijo=5000) ============
rows = []
for ent,(a,b,sd) in {"Mac":(1.5,0.00170,1.5),"Windows":(2.2,0.00195,1.7)}.items():
    for k in range(1, 31):                              # 30 corridas por entorno
        t = a + b*5000 + 1e-8*5000*5000 + rng.normal(0, sd)
        rows.append((ent, k, round(max(t,0.1),2)))
ab = pd.DataFrame(rows, columns=["entorno","corrida","tiempo_ms"])
ab.to_csv(f"{OUT}/algoritmos_ab.csv", index=False)
at,adf,ap = welch_t(ab[ab.entorno=='Windows'].tiempo_ms.values, ab[ab.entorno=='Mac'].tiempo_ms.values)
say(f"[algoritmos] A/B n=5000 (Win {ab[ab.entorno=='Windows'].tiempo_ms.mean():.2f} vs "
    f"Mac {ab[ab.entorno=='Mac'].tiempo_ms.mean():.2f}): t={at:.2f}, gl={adf:.1f}, p={ap:.4f}")

# ============ 5. HONGOS / SUSTRATO (ANOVA + ji-cuadrada) ============
sus = {"paja_trigo":(88,8,21,0.04), "pulpa_cafe":(80,8,24,0.24),
       "olote_maiz":(66,8,27,0.12), "aserrin":(52,12,30,0.48)}  # EB media, sd, dias, p_contam
rows = []
for s,(eb,sd,dias,pc) in sus.items():
    for i in range(25):
        rows.append((f"{s[:3]}{i+1:02d}", s,
                     round(max(rng.normal(eb,sd),1),1),
                     int(round(rng.normal(dias,2.5))),
                     "si" if rng.random()<pc else "no"))
hon = pd.DataFrame(rows, columns=["id","sustrato","eficiencia_biologica","dias_cosecha","contaminado"])
hon.to_csv(f"{OUT}/hongos_sustrato.csv", index=False)
F,d1,d2,p = anova(hon.eficiencia_biologica.values, hon.sustrato.values)
say(f"[hongos] ANOVA EB~sustrato: F({d1},{d2})={F:.2f}, p={p:.2e}  medias="
    + ", ".join(f"{s}:{hon[hon.sustrato==s].eficiencia_biologica.mean():.1f}" for s in sus))
ct2 = pd.crosstab(hon.sustrato, hon.contaminado)
X2,df,p = chi2_ct(ct2.values)
say(f"[hongos] ji-cuadrada sustrato x contaminado: X2={X2:.2f}, gl={df}, p={p:.3f}")

# resumen de archivos
print("\n--- archivos ---")
for f in sorted(os.listdir(OUT)):
    d = pd.read_csv(f"{OUT}/{f}"); print(f"{f}: {d.shape[0]} filas x {d.shape[1]} col -> {list(d.columns)}")
open(f"{OUT}/_verificacion.txt","w").write("\n".join(report))
