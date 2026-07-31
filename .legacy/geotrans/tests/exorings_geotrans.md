# Technical Research Report: Consistencia física entre `exorings` y GeoTrans

**Fuentes analizadas**
- `exorings-basic`: [exorings/exorings-basic.py](../../../exorings/exorings-basic.py)
- GeoTrans: [Zuluaga_PhotoRing/GeoTrans/geotrans2.py](../../../Zuluaga_PhotoRing/GeoTrans/geotrans2.py)

---

## 1. Objetivo y alcance

Este reporte evalúa la **consistencia física** (misma geometría/procesos) entre:

1) el cálculo “rápido” de propiedades de un tránsito con anillos en `exorings-basic`, y
2) las rutinas analíticas y geométricas en GeoTrans.

**Alcance**: se compara lo que ambos códigos comparten explícitamente:
- geometría proyectada de un planeta con anillos,
- opacidad normal convertida a factor de bloqueo line-of-sight,
- profundidad geométrica $\delta$ (sin oscurecimiento al limbo),
- inversión de densidad observada a partir de $(\delta, T_{14}, T_{23}, P)$.

**Fuera de alcance**: limb darkening, oblaticidad, excentricidad, y estimación de tiempos de contacto por métodos numéricos (aunque se discuten diferencias esperables).

---

## 2. Mapeo de parámetros y convenciones

### 2.1 Unidades y tipos

| Concepto | `exorings-basic` | GeoTrans |
|---|---:|---:|
| Radio estelar | $R_\star=1$ (adimensional) | Star = círculo unitario en geometría; propiedades físicas en SI |
| $p$ | `p = Rp/R*` | `S.Rp = Rplanet/Rstar` (ver `derivedSystemProperties`) |
| $f_i, f_e$ | `fi, fe` (en unidades de $R_p$) | `S.fi, S.fe` (en unidades de $R_p$) |
| Radio de anillo en $R_\star$ | `A=fe*p`, `B=A*cos(ir)` | `S.Ri=S.fi*S.Rp`, `S.Re=S.fe*S.Rp` |
| Opacidad | `tau` (normal) | `S.tau` |
| Ángulos | grados (`DEG`) | radianes (`DEG=pi/180`) |
| Periodo | días | `S.Porb` en segundos; rutinas auxiliares a veces esperan horas |

### 2.2 Convención angular (clave para comparar)

- En `exorings-basic`, `ir` y `theta` son **parámetros proyectados en el plano del cielo**.
- En GeoTrans, los parámetros “en el marco orbital” (`S.ir`, `S.phir`) se convierten a **ángulos efectivos proyectados**:
  - inclinación efectiva `S.ieff`
  - rotación/roll en el cielo `S.teff`

Esto ocurre en `updatePlanetRings` ([geotrans2.py#L1978](../../../Zuluaga_PhotoRing/GeoTrans/geotrans2.py#L1978)), donde se construye la matriz de rotación y se define:

- `S.ieff = arccos(|rz·z|)`
- `S.teff = ...`  (orientación del eje mayor proyectado)

**Conclusión práctica**: para comparar contra `exorings-basic`, use
- `ir_exorings (deg)  ↔  ieff_GeoTrans (rad)`
- `theta_exorings (deg) ↔ teff_GeoTrans (rad)`

---

## 3. Profundidad del tránsito y área proyectada (consistencia exacta)

### 3.1 Resultado en `exorings-basic`

La profundidad geométrica se construye como área bloqueada sobre el disco estelar unitario:

- Área del “planeta + anillos” (proyección y auto-ocultación por el planeta):
  - [exorings-basic.py#L138](../../../exorings/exorings-basic.py#L138)
- Profundidad:
  - [exorings-basic.py#L143](../../../exorings/exorings-basic.py#L143)

En forma compacta:

$$
\delta\;=\;\frac{A_{\rm ringed}}{\pi}\;=\;p^2\,\Big[1 + \beta\,(T(f_e,i)-T(f_i,i))\Big]
$$

(donde $p=R_p/R_\star$, $f_{i,e}=R_{i,e}/R_p$).

### 3.2 Resultado en GeoTrans

GeoTrans implementa exactamente la misma expresión mediante:

- `transitFunction(f,i)` ([geotrans2.py#L2480](../../../Zuluaga_PhotoRing/GeoTrans/geotrans2.py#L2480))
- `analyticalTransitArea(Rp,beta,fi,fe,i)` ([geotrans2.py#L2495](../../../Zuluaga_PhotoRing/GeoTrans/geotrans2.py#L2495))
  - ecuación principal en [geotrans2.py#L2499](../../../Zuluaga_PhotoRing/GeoTrans/geotrans2.py#L2499)

$$
A_{\rm ringed}=\pi R_p^2\,\Big[1 + \beta\,T(f_e,i) - \beta\,T(f_i,i)\Big]
\quad\Rightarrow\quad
\delta = A_{\rm ringed}/\pi
$$

### 3.3 Interpretación de los dos regímenes de `T(f,i)`

`transitFunction` (y las ramas equivalentes de `exorings-basic`) refleja un punto geométrico: dependiendo de $f\cos i$ la proyección del anillo puede quedar **totalmente por fuera** del planeta en el eje menor, o ser **parcialmente ocultada** por el disco planetario. Por eso:

- si $f\cos i>1$: forma cerrada simple ($\propto f^2\cos i-1$)
- si $f\cos i\le 1$: aparece una combinación de $\arcsin$ por la intersección elipse-círculo

**Conclusión**: para la profundidad (área) hay **consistencia analítica exacta** entre ambos códigos.

---

## 4. Opacidad y factor de bloqueo `β`

En `exorings-basic`:
- `beta = 1 - exp(-tau/cosir)` ([exorings-basic.py#L111](../../../exorings/exorings-basic.py#L111))

En GeoTrans:
- `blockFactor(tau,i)` ([geotrans2.py#L2536](../../../Zuluaga_PhotoRing/GeoTrans/geotrans2.py#L2536))
- y, a nivel sistema, `S.block=1-exp(-S.tau/cos(S.ieff))` ([geotrans2.py#L2017](../../../Zuluaga_PhotoRing/GeoTrans/geotrans2.py#L2017))

**Diferencia importante (numérica, no física)**
- GeoTrans protege el caso $\cos i\to 0$ (`abs(ci)<1E-15`) devolviendo `block=1.0`.
- `exorings-basic` no tiene guardia: exactamente en `ir=90°` puede aparecer división por cero.

Físicamente, el límite es benigno porque cuando $i\to 90°$ la proyección del anillo tiende a una línea y $T(f,i)\to 0$, por lo que el aporte del anillo a $\delta$ desaparece.

---

## 5. Densidad observada y efecto Photo-Ring

### 5.1 En `exorings-basic`

Tras obtener $(\delta, T_{14}, T_{23})$ para el sistema “ringed”, `exorings-basic` construye parámetros observados como si el objeto fuese un planeta sin anillos con radio observado $p_{\rm obs}=\sqrt{\delta}$.

- `aobs` (inversión tipo Seager & Mallen-Ornelas): [exorings-basic.py#L191](../../../exorings/exorings-basic.py#L191)
- `rhoobs` y PR: líneas siguientes.

### 5.2 En GeoTrans (Seager vs Kipping)

GeoTrans ofrece dos funciones explícitas:
- `rhoObserved_Seager` ([geotrans2.py#L2662](../../../Zuluaga_PhotoRing/GeoTrans/geotrans2.py#L2662))
- `rhoObserved_Kipping` ([geotrans2.py#L2676](../../../Zuluaga_PhotoRing/GeoTrans/geotrans2.py#L2676))

Notas:
- Aunque el docstring en GeoTrans usa `p`, en la implementación se usa `p**0.25` y `sqrt(p)`, por lo que **`p` es la profundidad** $\delta$ (consistente con `exorings-basic`).
- `exorings-basic` coincide con la versión Seager (aproximada). La versión Kipping usa $\sin(\pi T/P)$ y es más precisa cuando $T/P$ no es muy pequeño.

---

## 6. Tiempos de contacto y duraciones (donde pueden diferir)

### 6.1 `exorings-basic`: contactos aproximados para el anillo

- Los contactos del planeta son exactos para un disco: [exorings-basic.py#L153-L158](../../../exorings/exorings-basic.py#L153-L158)
- Los contactos del anillo se aproximan con una solución cerrada: [exorings-basic.py#L160](../../../exorings/exorings-basic.py#L160) y siguientes.

Esto es rápido y útil para exploración, pero puede fallar o sesgar duraciones en:
- configuraciones cercanas al grazing,
- anillos muy grandes,
- ángulos donde la aproximación deja $xR13<0$ o $xR24<0$ (no real),
- casos donde la geometría real de contacto depende de intersecciones múltiples.

### 6.2 GeoTrans: contactos por geometría/intersección

GeoTrans tiene infraestructura para contactos por intersección y root-finding (por ejemplo `contactTime(s)`), consistente con la geometría completa (elipse-círculo, inclusión/exclusión, etc.). Esto hace que, aun con la misma $\delta$ analítica, los **$T_{14},T_{23}$** puedan diferir respecto a `exorings-basic`.

---

## 7. Chequeo numérico reproducible (caso por defecto)

Usando los valores por defecto de `exorings-basic`:

- $\rho_{\rm true}=1.40598\;\mathrm{g/cm^3}$
- $P=365.2446\;\mathrm{d}$
- $b=0.1875$
- $p=0.08$
- $f_i=1.5$, $f_e=2.35$
- $\tau=1$
- $i_r=80^\circ$, $\theta=30^\circ$

### 7.1 Resultados

- **Bloqueo**: $\beta = 0.9968450117$
- **Profundidad**: $\delta = 8.8211846\times 10^{-3}$ (8821.18 ppm)
- **Radio observado**: $p_{\rm obs}=\sqrt{\delta}=0.09392116$

Comparación de profundidad/área:
- `exorings-basic` (por `re2,ri2`) y GeoTrans (`analyticalTransitArea`) coinciden a precisión de máquina: $|\delta_{\rm ex}-\delta_{\rm GT}|=0$.

Duraciones (según la aproximación de contactos en `exorings-basic`):
- $T_{14,p}=13.8143\,$h, $T_{23,p}=11.6983\,$h (sin anillos)
- $T_{14}=14.8135\,$h, $T_{23}=10.5841\,$h (con anillos)

Comparación contra GeoTrans `contactTimes` (contactos geométricos, misma geometría proyectada $i_r=80^\circ$, $\theta=30^\circ$):
- $T_{14}=14.8294\,$h, $T_{23}=10.5736\,$h
- Diferencias (GeoTrans − exorings): $\Delta T_{14}=+57\,$s, $\Delta T_{23}=-38\,$s

Densidad observada:
- $\rho_{\rm obs}$ (Seager; `exorings-basic`) = $0.6371366\;\mathrm{g/cm^3}$
- GeoTrans `rhoObserved_Seager` da el mismo valor (diferencia $\sim 2\times 10^{-16}$).
- GeoTrans `rhoObserved_Kipping` = $0.6371652\;\mathrm{g/cm^3}$ (ligeramente distinto).

Efecto Photo-Ring:
- $\mathrm{PR}=\rho_{\rm obs}/\rho_{\rm true}=0.453162$
- $\log_{10}(\mathrm{PR})=-0.34375$

---

## 8. Conclusiones y recomendaciones

1) **Profundidad/área y factor de bloqueo**: `exorings-basic` y GeoTrans son **físicamente consistentes** (misma ecuación), siempre que se compare con los ángulos proyectados efectivos (`ieff`).

2) **Densidad observada**: `exorings-basic` implementa la inversión aproximada de Seager; GeoTrans ofrece Seager (equivalente) y Kipping (más precisa). Para inferencia fina sobre $\rho_{\rm obs}$, conviene preferir Kipping.

3) **Duraciones/contactos**: aquí es donde se esperan discrepancias: `exorings-basic` usa contactos aproximados del anillo, mientras GeoTrans puede resolver contactos geométricamente. En regímenes cercanos a grazing o con anillos grandes/inclinados, GeoTrans es la referencia más robusta.

---

## Apéndice A: snippet mínimo para reproducir el chequeo (Python)

```python
import numpy as np
DEG=np.pi/180; DAY=86400.0; HOUR=3600.0; G=6.67428e-11
rhotrue=1.40598; P=365.2446; b=0.1875; p=0.08; fi=1.5; fe=2.35; tau=1.0
ir=80*DEG
beta=1-np.exp(-tau/np.cos(ir))

def T(f,i):
    if f*np.cos(i)>1: return f*f*np.cos(i)-1
    t1=2/np.pi*np.arcsin(np.sqrt(f*f-1)/(f*np.sin(i)))
    t2=2/np.pi*np.arcsin(np.cos(i)*np.sqrt(f*f-1)/np.sin(i))
    return f*f*np.cos(i)*t1-t2

delta = p*p*(1 + beta*T(fe,ir) - beta*T(fi,ir))
print(delta, delta*1e6)
```
