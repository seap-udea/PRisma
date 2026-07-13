"""Equivalence tests: the packaged forward model reproduces the (former) inline code.

The pipeline notebooks used to define the ``exorings`` ring-transit model inline (and had
drifted between the emcee and dynesty notebooks). It now lives once in
:func:`exorings.forward.forward_observables`. These tests pin that refactor: the packaged
function must reproduce, bit-for-bit, the original inline formulas — both the ``kipping`` bobs
convention (the dynesty notebook) and the ``mallen`` one (the emcee notebook) — including
returning ``None`` on the exact same unphysical geometries.
"""

import numpy as np

from exorings.forward import forward_observables

DEG = np.pi / 180
DAY = 86400.0
HOUR = 3600.0
GCONST = 6.67428e-11


# ── reference: the original inline exorings_model (dynesty notebook, kipping bobs) ──
def _inline_kipping(rhotrue_gcc, P_days, b, p, fi, fe, tau, theta_deg, ir_deg):
    rhotrue_SI = rhotrue_gcc * 1e3
    P_s = P_days * DAY
    a = (GCONST * rhotrue_SI / (3 * np.pi) * P_s**2) ** (1 / 3)
    cosiorb = b / a
    if abs(cosiorb) >= 1:
        return None
    siniorb = np.sqrt(1 - cosiorb**2)
    A = fe * p
    B = A * np.cos(ir_deg * DEG)
    hp = max(p, A * np.sin(theta_deg * DEG), B * np.cos(theta_deg * DEG))
    if b > 1.0 - hp:
        return None
    cosir = np.cos(ir_deg * DEG)
    sinir = np.sin(ir_deg * DEG)
    beta = 1 - np.exp(-tau / cosir)

    def _r2(f):
        if f * cosir > 1:
            return f**2 * cosir - 1
        y = np.sqrt(max(f**2 - 1, 0)) / (f * sinir)
        return (f**2 * cosir * 2 / np.pi * np.arcsin(min(y, 1))
                - 2 / np.pi * np.arcsin(min(y * f * cosir, 1)))

    ri2 = beta * _r2(fi)
    re2 = beta * _r2(fe)
    delta = p**2 + (re2 - ri2) * p**2
    pobs = np.sqrt(delta)
    xp14 = np.sqrt(max((1 + p)**2 - b**2, 0))
    xp23 = np.sqrt(max((1 - p)**2 - b**2, 0))
    sinTh = np.sin(theta_deg * DEG)
    cosTh = np.cos(theta_deg * DEG)
    xR13 = 1 - A**2 * (sinTh - b / A)**2 * (1 - B**2 / A)
    xR24 = 1 - A**2 * (sinTh + b / A)**2 * (1 - B**2 / A)
    xR1 = -np.sqrt(max(xR13, 0)) - A * cosTh
    xR2 = -np.sqrt(max(xR24, 0)) + A * cosTh
    xR3 = +np.sqrt(max(xR13, 0)) - A * cosTh
    xR4 = +np.sqrt(max(xR24, 0)) + A * cosTh
    x1, x2, x3, x4 = min(-xp14, xR1), max(-xp23, xR2), min(xp23, xR3), max(xp14, xR4)
    arg14 = (x4 - x1) / (a * siniorb)
    arg23 = (x3 - x2) / (a * siniorb)
    if abs(arg14) > 1 or abs(arg23) > 1:
        return None
    T14 = P_s * np.arcsin(arg14) / (2 * np.pi) / HOUR
    T23 = P_s * np.arcsin(np.clip(arg23, -1, 1)) / (2 * np.pi) / HOUR
    denom2 = T14**2 - T23**2
    if denom2 <= 0:
        return None
    aobs = 2 * (P_s / HOUR) / np.pi * delta**0.25 / np.sqrt(denom2)
    rhoobs = (3 * np.pi / GCONST) * aobs**3 / P_s**2 / 1e3
    sfF = (np.sin(T23 * np.pi / P_s / HOUR))**2
    sfT = (np.sin(T14 * np.pi / P_s / HOUR))**2
    bobs = (((1 - pobs)**2 - (sfF / sfT) * (1 + pobs)**2) / (1 - sfF / sfT))**0.5
    return dict(delta=delta, T14=T14, T23=T23, rhoobs=rhoobs, bobs=bobs,
                aobs=aobs, pobs=pobs, beta=beta, a=a, logPR=np.log10(rhoobs / rhotrue_gcc))


def _inline_mallen_bobs(delta, T14, T23):
    denom2 = T14**2 - T23**2
    return np.sqrt(max((T14**2 * (1 - np.sqrt(delta)) - T23**2 * (1 + np.sqrt(delta))) / denom2, 0))


def _param_grid(n=6000, seed=0):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        yield dict(
            rhotrue_gcc=rng.uniform(0.3, 3.0), P_days=rng.uniform(10, 400),
            b=rng.uniform(0, 0.99), p=rng.uniform(0.02, 0.15),
            fi=1.0, fe=rng.uniform(1.01, 10.0), tau=rng.uniform(0.1, 10),
            theta_deg=rng.uniform(0, 90), ir_deg=rng.uniform(0.5, 89.5),
        )


def test_forward_matches_inline_kipping():
    """forward_observables(bobs_method='kipping') == inline dynesty model, bit-for-bit."""
    checked = valid = 0
    for kw in _param_grid():
        ref = _inline_kipping(**kw)
        got = forward_observables(bobs_method="kipping", **kw)
        assert (ref is None) == (got is None), f"None disagreement at {kw}"
        checked += 1
        if ref is None:
            continue
        valid += 1
        for key in ref:
            a, b = float(ref[key]), float(got[key])
            if np.isnan(a) or np.isnan(b):
                assert np.isnan(a) and np.isnan(b), f"{key} nan disagreement at {kw}"
            else:
                assert a == b, f"{key} differs at {kw}: {a} vs {b}"
    assert checked > 1000 and valid > 100


def test_forward_matches_inline_mallen():
    """forward_observables(bobs_method='mallen') reproduces the emcee bobs convention."""
    for kw in _param_grid(n=3000, seed=1):
        ref = _inline_kipping(**kw)
        got = forward_observables(bobs_method="mallen", **kw)
        assert (ref is None) == (got is None)
        if ref is None:
            continue
        # every field except bobs matches the shared physics
        for key in ("delta", "T14", "T23", "rhoobs", "aobs", "pobs", "beta", "a", "logPR"):
            assert float(ref[key]) == float(got[key])
        # bobs matches the Mallen-Ornelas inversion
        expect = _inline_mallen_bobs(ref["delta"], ref["T14"], ref["T23"])
        assert float(got["bobs"]) == float(expect)


def test_geotrans_model_runs():
    """The geotrans wrapper returns the observable contract for a physical geometry."""
    from geotrans.model import geotrans2_model
    r = geotrans2_model(rhotrue_gcc=1.406, P_days=365.0, b=0.19, p=0.08,
                        fi=1.5, fe=2.35, tau=1.0, theta_deg=30.0, ir_deg=80.0)
    assert r is not None
    for key in ("delta", "T14", "T23", "rhoobs", "bobs", "aobs", "pobs", "logPR"):
        assert key in r and np.isfinite(r[key])
