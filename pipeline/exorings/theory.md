# Exorings Basic — Guía Teórica y Navegación Física del Módulo

> Documentación técnica para navegar el modelo físico de `exorings-basic.py` desde la teoría, conectando cada ecuación con su implementación en código.

---

# Tabla de contenido

1. Objetivo físico del módulo  
2. Parámetros de entrada  
3. Geometría orbital  
4. Geometría proyectada de anillos  
5. Condición de tránsito  
6. Transferencia radiativa / opacidad  
7. Radio efectivo interno  
8. Radio efectivo externo  
9. Área bloqueada total  
10. Profundidad de tránsito  
11. Radio planetario observado  
12. Posiciones de contacto  
13. Duración del tránsito  
14. Parámetros observados inferidos  
15. Photo-Ring Effect  
16. Flujo físico completo del algoritmo

---

# 1) Objetivo físico del módulo

Este script modela el tránsito fotométrico de un **planeta con anillos** frente a una estrella.

El propósito es cuantificar cómo los anillos modifican:

- profundidad del tránsito,
- duración,
- radio observado,
- parámetro de impacto inferido,
- densidad estelar inferida.

En términos compactos:

$$
\text{Planeta}
+
\text{Anillos}
+
\text{Proyección geométrica}
+
\text{Opacidad}
\longrightarrow
\text{Observables de tránsito}
$$

El observable principal es:

$$
\delta = \frac{A_{\rm bloqueada}}{A_*}
$$

donde:

- $A_{\rm bloqueada}$ = área efectiva tapada
- $A_*$ = área del disco estelar

---

# 2) Parámetros de entrada

## Variables físicas

| Parámetro | Significado | Unidad |
|---|---|---|
| `rhotrue` | densidad estelar real | g/cm³ |
| `P` | período orbital | días |
| `b` | parámetro de impacto | $R_*$ |
| `p` | radio planetario relativo | $R_p/R_*$ |
| `fi` | radio interno del anillo | $R_i/R_p$ |
| `fe` | radio externo del anillo | $R_e/R_p$ |
| `tau` | opacidad normal | adimensional |
| `theta` | inclinación proyectada | grados |
| `ir` | inclinación aparente del anillo | grados |

Implementación:

```python
default=dict(
    rhotrue=1.40598,
    P=365.2446,
    b=0.1875,
    p=0.08,
    fi=1.5,
    fe=2.35,
    tau=1.0,
    theta=30.0,
    ir=80.0,
)
```

---

# 3) Geometría orbital

## 3.1 Semieje mayor escalado

Usando Kepler expresado en densidad estelar:

$$
\frac{a}{R_*}
=
\left(
\frac{G\rho_*}{3\pi}P^2
\right)^{1/3}
$$

con:

$$
\rho_* = 1000\cdot \rho_{\rm true}
$$

Implementación:

```python
a=(GCONST*(par.rhotrue*1E3)/(3*np.pi)*(par.P*DAY)**2)**(1./3)
```

---

## 3.2 Inclinación orbital

$$
b=
\frac{a}{R_*}\cos i_{\rm orb}
$$

por tanto:

$$
\cos i_{\rm orb}=\frac{b}{a}
$$

y:

$$
\sin i_{\rm orb}
=
\sqrt{1-\cos^2 i_{\rm orb}}
$$

Implementación:

```python
cosiorb=par.b/a
siniorb=(1-cosiorb**2)**0.5
```

---

# 4) Geometría proyectada de anillos

Un anillo circular proyectado se observa como una elipse.

## Semieje mayor

$$
A=f_e\,p
$$

Implementación:

```python
A=par.fe*par.p
```

## Semieje menor

$$
B=A\cos i_r
$$

Implementación:

```python
B=A*np.cos(par.ir*DEG)
```

---

# 5) Condición de tránsito

Altura máxima proyectada:

$$
h_p=
\max\left(
p,\;
A\sin\theta,\;
B\cos\theta
\right)
$$

Condición:

$$
b<1-h_p
$$

Implementación:

```python
hp=max(
    par.p,
    A*np.sin(par.theta*DEG),
    B*np.cos(par.theta*DEG)
)

if par.b>1.0-hp:
    ...
```

---

# 6) Transferencia radiativa — factor de bloqueo

$$
\beta=
1-
\exp\left(
-\frac{\tau}{\cos i_r}
\right)
$$

Límites:

Transparente:

$$
\tau\to0
\Rightarrow
\beta\to0
$$

Opaco:

$$
\tau\to\infty
\Rightarrow
\beta\to1
$$

Implementación:

```python
beta=1-np.exp(-par.tau/cosir)
```

---

# 7) Radio efectivo interno

Caso simple:

$$
f_i\cos i_r>1
$$

entonces:

$$
r_i^2=f_i^2\cos i_r-1
$$

Implementación:

```python
if par.fi*cosir>1:
    ri2=par.fi**2*cosir-1
```

Caso geométrico:

$$
y_i=
\frac{\sqrt{f_i^2-1}}
{f_i\sin i_r}
$$

$$
r_i^2=
f_i^2\cos i_r
\frac{2}{\pi}\arcsin(y_i)
-
\frac{2}{\pi}
\arcsin(y_i f_i\cos i_r)
$$

corregido por opacidad:

$$
r_i^2\leftarrow \beta r_i^2
$$

Implementación:

```python
yi=np.sqrt(par.fi**2-1)/(par.fi*sinir)

ri2=
    par.fi**2*cosir*2/np.pi*np.arcsin(yi)
    -
    2/np.pi*np.arcsin(yi*par.fi*cosir)

ri2=beta*ri2
```

---

# 8) Radio efectivo externo

Misma física:

$$
f_i \rightarrow f_e
$$

Se obtiene:

$$
r_e^2
$$

y:

$$
r_e^2\leftarrow\beta r_e^2
$$

Implementación:

```python
if par.fe*cosir>1:
    re2=par.fe**2*cosir-1
else:
    ye=np.sqrt(par.fe**2-1)/(par.fe*sinir)

    re2=
        par.fe**2*cosir*2/np.pi*np.arcsin(ye)
        -
        2/np.pi*np.arcsin(ye*par.fe*cosir)

re2=beta*re2
```

---

# 9) Área bloqueada total

Área planeta:

$$
A_p=\pi p^2
$$

Área anillos:

$$
A_r=
\pi(r_e^2-r_i^2)p^2
$$

Total:

$$
A_{Rp}
=
\pi p^2
+
\pi(r_e^2-r_i^2)p^2
$$

Implementación:

```python
ARp=np.pi*par.p**2 + np.pi*(re2-ri2)*par.p**2
```

---

# 10) Profundidad de tránsito

$$
\delta=
\frac{A_{Rp}}{\pi}
$$

Implementación:

```python
delta=ARp/np.pi
```

---

# 11) Radio observado

$$
p_{\rm obs}=\sqrt{\delta}
$$

Implementación:

```python
pobs=np.sqrt(delta)
```

Sesgo:

$$
\frac{p_{\rm obs}}{p}>1
$$

---

# 12) Posiciones de contacto

Primer / cuarto contacto:

$$
x_{14}
=
\sqrt{(1+p)^2-b^2}
$$

Segundo / tercer contacto:

$$
x_{23}
=
\sqrt{(1-p)^2-b^2}
$$

Implementación:

```python
xp14=np.sqrt((1+par.p)**2-par.b**2)
xp23=np.sqrt((1-par.p)**2-par.b**2)
```

---

# 13) Duración de tránsito

$$
T=
\frac{P}{2\pi}
\arcsin\left(
\frac{\Delta x}{a\sin i}
\right)
$$

Implementación:

```python
T14p=...
T23p=...

T14=...
T23=...
```

---

# 14) Parámetros observados inferidos

## Semieje mayor observado

$$
a_{\rm obs}
=
\frac{2(P/H)}{\pi}
\frac{\delta^{1/4}}
{\sqrt{T_{14}^2-T_{23}^2}}
$$

Implementación:

```python
aobs=...
```

## Parámetro de impacto observado

$$
b_{\rm obs}
=
\sqrt{
\frac{
T_{14}^2(1-\sqrt{\delta})
-
T_{23}^2(1+\sqrt{\delta})
}{
T_{14}^2-T_{23}^2
}
}
$$

Implementación:

```python
bobs=...
```

## Densidad estelar observada

$$
\rho_{\rm obs}
=
\frac{3\pi}{G}
\frac{a_{\rm obs}^3}{P^2}
$$

Implementación:

```python
rhoobs=(3*np.pi/GCONST)*aobs**3/(par.P*DAY)**2/1E3
```

---

# 15) Photo-Ring Effect

$$
PR=
\frac{\rho_{\rm obs}}
{\rho_{\rm true}}
$$

y:

$$
\log_{10}(PR)
$$

Implementación:

```python
PR=rhoobs/par.rhotrue
logPR=np.log10(PR)
```

Interpretación:

- $PR>1$ → estrella aparenta más densa
- $PR<1$ → estrella aparenta menos densa

---

# 16) Flujo físico completo

$$
\text{Input físicos}
$$

↓

$$
\text{Geometría orbital}
$$

↓

$$
\text{Proyección de anillos}
$$

↓

$$
\text{Bloqueo radiativo}
$$

↓

$$
\text{Área efectiva}
$$

↓

$$
\delta
$$

↓

$$
p_{\rm obs},\;T_{14},\;T_{23}
$$

↓

$$
a_{\rm obs},\;b_{\rm obs},\;\rho_{\rm obs}
$$

↓

$$
PR
$$

---

## Resumen

$$
\boxed{
\text{Geometría}
+
\text{Radiativa}
+
\text{Cinemática}
}
\Longrightarrow
\boxed{
\text{Sesgo observacional}
}
$$