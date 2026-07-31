# exorings — ring-transit forward model

The forward model used throughout [`../`](../): given a planet's true stellar density, orbital
period, impact parameter, radius ratio, and ring geometry, compute the transit observables
(depth, contact durations, apparent stellar density) a ringed planet would produce.

Lives under [`pipeline/`](../) next to `photoring` and `geotrans`.

## Python API

Two entry points, one physics:

**1. The pipeline contract — [`forward.py`](forward.py).** `forward_observables(...)` returns a
plain dict of transit observables, or `None` for unphysical geometries — the contract the samplers
need.

```python
from exorings.forward import forward_observables

obs = forward_observables(rhotrue_gcc=1.406, P_days=365.0, b=0.19, p=0.08,
                          fi=1.5, fe=2.35, tau=1.0, theta_deg=30.0, ir_deg=80.0)
# -> dict(delta, T14, T23, rhoobs, bobs, aobs, pobs, beta, a, logPR)  or  None
```

The `bobs_method` argument selects the impact-parameter inversion (`'kipping'`, default, or
`'mallen'`); all other outputs are independent of it.

**2. The reference OO API — [`basic.py`](basic.py).** A frozen-dataclass parameter object
(`ExoringsBasicParams`), a pure function (`compute_exorings_basic`) and a thin OO wrapper
(`ExoringsBasic`) returning a rich `ExoringsBasicResult` and *raising* on non-transiting geometries.

```python
from exorings import ExoringsBasic, ExoringsBasicParams

result = ExoringsBasic(ExoringsBasicParams(rhotrue=1.40598, P=365.2446, b=0.1875,
                                           p=0.08, fi=1.5, fe=2.35, tau=1.0,
                                           theta=30.0, ir=80.0)).compute()
print(result.delta, result.T14, result.rhoobs)
```

Both guard the `cos(ir) → 0` singularity at exactly edge-on ring inclination (`ir = 90°`). For the
underlying physics, equation by equation: [`theory.md`](theory.md).

## Sibling package

Numerical cross-check / alternate forward model: [`../geotrans/`](../geotrans/).

Standalone Python-2-era scripts: [`.legacy/exorings/`](../../.legacy/exorings/).

## Reference

> Zuluaga, J.I., Kipping, D., Sucerquia, M., Alvarado, J. A. "A novel method for identifying
> exoplanetary rings", ApJL 803, L14 (2015).

# Exorings Basic — Theory Guide and Physics Walkthrough

> Technical documentation for navigating the physical model behind `basic.py` /
> `forward.py`, connecting each equation to its code implementation.

---

# Table of contents

1. Physical goal of the module
2. Input parameters
3. Orbital geometry
4. Projected ring geometry
5. Transit condition
6. Radiative transfer / opacity
7. Inner effective radius
8. Outer effective radius
9. Total blocked area
10. Transit depth
11. Observed planetary radius
12. Contact positions
13. Transit duration
14. Inferred observed parameters
15. Photo-Ring effect
16. Full physical flow of the algorithm

---

# 1) Physical goal of the module

This module models the photometric transit of a **ringed planet** across a star.

The purpose is to quantify how rings modify:

- transit depth,
- duration,
- observed radius,
- inferred impact parameter,
- inferred stellar density.

In compact form:

$$
\text{Planet}
+
\text{Rings}
+
\text{Geometric projection}
+
\text{Opacity}
\longrightarrow
\text{Transit observables}
$$

The primary observable is:

$$
\delta = \frac{A_{\rm blocked}}{A_*}
$$

where:

- $A_{\rm blocked}$ = effective occulted area
- $A_*$ = stellar-disk area

---

# 2) Input parameters

## Physical variables

| Parameter | Meaning | Unit |
|---|---|---|
| `rhotrue` | true stellar density | g/cm³ |
| `P` | orbital period | days |
| `b` | impact parameter | $R_*$ |
| `p` | relative planetary radius | $R_p/R_*$ |
| `fi` | inner ring radius | $R_i/R_p$ |
| `fe` | outer ring radius | $R_e/R_p$ |
| `tau` | normal optical depth | dimensionless |
| `theta` | projected tilt | degrees |
| `ir` | apparent ring inclination | degrees |

Implementation:

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

# 3) Orbital geometry

## 3.1 Scaled semi-major axis

Using Kepler's law expressed through stellar density:

$$
\frac{a}{R_*}
=
\left(
\frac{G\rho_*}{3\pi}P^2
\right)^{1/3}
$$

with:

$$
\rho_* = 1000\cdot \rho_{\rm true}
$$

Implementation:

```python
a=(GCONST*(par.rhotrue*1E3)/(3*np.pi)*(par.P*DAY)**2)**(1./3)
```

---

## 3.2 Orbital inclination

$$
b=
\frac{a}{R_*}\cos i_{\rm orb}
$$

hence:

$$
\cos i_{\rm orb}=\frac{b}{a}
$$

and:

$$
\sin i_{\rm orb}
=
\sqrt{1-\cos^2 i_{\rm orb}}
$$

Implementation:

```python
cosiorb=par.b/a
siniorb=(1-cosiorb**2)**0.5
```

---

# 4) Projected ring geometry

A circular ring appears as an ellipse in projection.

## Semi-major axis

$$
A=f_e\,p
$$

Implementation:

```python
A=par.fe*par.p
```

## Semi-minor axis

$$
B=A\cos i_r
$$

Implementation:

```python
B=A*np.cos(par.ir*DEG)
```

---

# 5) Transit condition

Maximum projected height:

$$
h_p=
\max\left(
p,\;
A\sin\theta,\;
B\cos\theta
\right)
$$

Condition:

$$
b<1-h_p
$$

Implementation:

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

# 6) Radiative transfer — blocking factor

$$
\beta=
1-
\exp\left(
-\frac{\tau}{\cos i_r}
\right)
$$

Limits:

Transparent:

$$
\tau\to0
\Rightarrow
\beta\to0
$$

Opaque:

$$
\tau\to\infty
\Rightarrow
\beta\to1
$$

Implementation:

```python
beta=1-np.exp(-par.tau/cosir)
```

---

# 7) Inner effective radius

Simple case:

$$
f_i\cos i_r>1
$$

then:

$$
r_i^2=f_i^2\cos i_r-1
$$

Implementation:

```python
if par.fi*cosir>1:
    ri2=par.fi**2*cosir-1
```

Geometric case:

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

corrected by opacity:

$$
r_i^2\leftarrow \beta r_i^2
$$

Implementation:

```python
yi=np.sqrt(par.fi**2-1)/(par.fi*sinir)

ri2=
    par.fi**2*cosir*2/np.pi*np.arcsin(yi)
    -
    2/np.pi*np.arcsin(yi*par.fi*cosir)

ri2=beta*ri2
```

---

# 8) Outer effective radius

Same physics with:

$$
f_i \rightarrow f_e
$$

yielding:

$$
r_e^2
$$

and:

$$
r_e^2\leftarrow\beta r_e^2
$$

Implementation:

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

# 9) Total blocked area

Planet area:

$$
A_p=\pi p^2
$$

Ring area:

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

Implementation:

```python
ARp=np.pi*par.p**2 + np.pi*(re2-ri2)*par.p**2
```

---

# 10) Transit depth

$$
\delta=
\frac{A_{Rp}}{\pi}
$$

Implementation:

```python
delta=ARp/np.pi
```

---

# 11) Observed radius

$$
p_{\rm obs}=\sqrt{\delta}
$$

Implementation:

```python
pobs=np.sqrt(delta)
```

Bias:

$$
\frac{p_{\rm obs}}{p}>1
$$

---

# 12) Contact positions

First / fourth contact:

$$
x_{14}
=
\sqrt{(1+p)^2-b^2}
$$

Second / third contact:

$$
x_{23}
=
\sqrt{(1-p)^2-b^2}
$$

Implementation:

```python
xp14=np.sqrt((1+par.p)**2-par.b**2)
xp23=np.sqrt((1-par.p)**2-par.b**2)
```

---

# 13) Transit duration

$$
T=
\frac{P}{2\pi}
\arcsin\left(
\frac{\Delta x}{a\sin i}
\right)
$$

Implementation:

```python
T14p=...
T23p=...

T14=...
T23=...
```

---

# 14) Inferred observed parameters

## Observed semi-major axis

$$
a_{\rm obs}
=
\frac{2(P/H)}{\pi}
\frac{\delta^{1/4}}
{\sqrt{T_{14}^2-T_{23}^2}}
$$

Implementation:

```python
aobs=...
```

## Observed impact parameter

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

Implementation:

```python
bobs=...
```

## Observed stellar density

$$
\rho_{\rm obs}
=
\frac{3\pi}{G}
\frac{a_{\rm obs}^3}{P^2}
$$

Implementation:

```python
rhoobs=(3*np.pi/GCONST)*aobs**3/(par.P*DAY)**2/1E3
```

---

# 15) Photo-Ring effect

$$
PR=
\frac{\rho_{\rm obs}}
{\rho_{\rm true}}
$$

and:

$$
\log_{10}(PR)
$$

Implementation:

```python
PR=rhoobs/par.rhotrue
logPR=np.log10(PR)
```

Interpretation:

- $PR>1$ → the star appears denser
- $PR<1$ → the star appears less dense

---

# 16) Full physical flow

$$
\text{Physical inputs}
$$

↓

$$
\text{Orbital geometry}
$$

↓

$$
\text{Ring projection}
$$

↓

$$
\text{Radiative blocking}
$$

↓

$$
\text{Effective area}
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

## Summary

$$
\boxed{
\text{Geometry}
+
\text{Radiative transfer}
+
\text{Kinematics}
}
\Longrightarrow
\boxed{
\text{Observational bias}
}
$$
