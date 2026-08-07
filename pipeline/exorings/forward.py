"""Sampler-friendly forward model for the ``exorings`` (Zuluaga+2015) ring transit.

This is the **closed-form / analytical** forward model used by default throughout the
inference pipeline. It replaces the ``exorings_model`` function that used to be defined
*inline* (and, worse, duplicated with subtle divergences) inside every inference
notebook.

Relationship to :mod:`exorings.basic`
-------------------------------------
:mod:`exorings.basic` (``compute_exorings_basic`` / ``ExoringsBasic``) is the reference,
strongly-typed OO API: it returns a rich :class:`~exorings.basic.ExoringsBasicResult`
dataclass and *raises* :class:`~exorings.basic.NoTransitError` on non-transiting
geometries. That contract is ideal for a single, interactive computation but awkward
for a likelihood evaluated millions of times.

:func:`forward_observables` here is the **sampler contract**: it returns a plain ``dict``
of the observables the KDE likelihood needs, or ``None`` when the geometry is unphysical
(so the sampler can map it to ``-inf``). The physics is identical to
``compute_exorings_basic``; the two differ only in packaging and in the ``bobs``
convention (see ``bobs_method`` below).

``bobs_method``
---------------
The transit-inferred impact parameter ``bobs`` can be obtained two ways, which
historically differed between the two inference notebooks:

- ``'kipping'`` — Kipping (2010) inversion (used by the ``dynesty`` notebook). **Default.**
- ``'mallen'`` — Mallen-Ornelas (2003) inversion (used by the ``emcee`` notebook).

They agree closely; the choice only matters when ``b_obs`` enters the likelihood or the
posterior-predictive check. The default (``'kipping'``) matches the primary (dynesty)
pipeline; pass ``bobs_method='mallen'`` to reproduce the historical emcee behaviour
exactly. Every other returned quantity is independent of this flag.
"""

from __future__ import annotations

import numpy as np

try:
    from .exorings import DEG, DAY, HOUR, GCONST
except Exception:  # pragma: no cover - fallback if constants module unavailable
    DEG = np.pi / 180
    DAY = 86400.0
    HOUR = 3600.0
    GCONST = 6.67428e-11

def forward_observables(rhotrue_gcc, P_days, b, p, fi, fe, alpha, theta_deg, ir_deg, bobs_method="kipping"):
    """Compute transit observables for a ringed planet with improved analytical
    formula (Numpaque, Zuluaga et al. 2026).

    Parameters
    ----------
    rhotrue_gcc : float
        Stellar density [g/cm^3] (true density; rho_obs is an *output*).
    P_days : float
        Orbital period [days].
    b : float
        Impact parameter [R*].
    p : float
        Planet radius ratio Rp/R*.
    fi, fe : float
        Inner / outer ring radii [Rp].
    alpha : float
        Opacity attenuation factor alpha = exp(-tau), in the range (0, 1].
        alpha=1 means a transparent ring (tau=0); alpha->0 means an opaque ring (tau->inf).
        Internally converted to tau = -log(alpha) before computing the blocking factor.
    theta_deg : float
        Projected tilt [deg]; 90 = perpendicular to orbit.
    ir_deg : float
        Projected inclination [deg]; 90 = edge-on.
    bobs_method : {'kipping', 'mallen'}, optional
        Inversion used for ``bobs`` (see module docstring). Default ``'kipping'``.

    Returns
    -------
    dict or None
        ``dict`` with keys ``delta, T14, T23, rhoobs, bobs, aobs, pobs, beta, a, logPR``.
        ``None`` if the geometry is unphysical.
    """
    # --- reparametrization: alpha = exp(-tau)  =>  tau = -log(alpha) ---
    # The blocking factor becomes: beta = 1 - exp(-tau/cosir) = 1 - alpha^(1/cosir)
    if alpha <= 0.0 or alpha > 1.0:
        return None
    tau = -np.log(alpha)
    # -------------------------------------------------------------------
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
    beta = 1 - np.exp(-tau / cosir)  # equivalent to 1 - alpha**(1/cosir)

    def _ring_r2(f):
        if f * cosir > 1:
            return f**2 * cosir - 1
        y = np.sqrt(max(f**2 - 1, 0)) / (f * sinir)
        return (f**2 * cosir * 2 / np.pi * np.arcsin(min(y, 1))
                - 2 / np.pi * np.arcsin(min(y * f * cosir, 1)))

    ri2 = beta * _ring_r2(fi)
    re2 = beta * _ring_r2(fe)
    delta = p**2 + (re2 - ri2) * p**2    # = ARp/pi
    pobs = np.sqrt(delta)

    # ==================================================
    # Contact positions (Support Function Approach)
    # ==================================================
    xp14 = np.sqrt(max((1 + p)**2 - b**2, 0))
    xp23 = np.sqrt(max((1 - p)**2 - b**2, 0))
    
    sinTh = np.sin(theta_deg * DEG)
    cosTh = np.cos(theta_deg * DEG)
    x0 = np.sqrt(max(1.0 - b**2, 0))
    
    hR = np.sqrt(A**2 * (x0 * cosTh + b * sinTh)**2 + B**2 * (b * cosTh - x0 * sinTh)**2)
    hL = np.sqrt(A**2 * (-x0 * cosTh + b * sinTh)**2 + B**2 * (b * cosTh + x0 * sinTh)**2)
    
    xR1 = -np.sqrt(max((1 + hL)**2 - b**2, 0))
    xR2 = -np.sqrt(max((1 - hL)**2 - b**2, 0))
    xR3 = +np.sqrt(max((1 - hR)**2 - b**2, 0))
    xR4 = +np.sqrt(max((1 + hR)**2 - b**2, 0))
    
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

    if bobs_method == "mallen":
        # Mallen-Ornelas (2003)
        bobs = np.sqrt(max(
            (T14**2 * (1 - np.sqrt(delta)) - T23**2 * (1 + np.sqrt(delta))) / denom2, 0))
    else:
        # Kipping (2010)
        sfF = (np.sin(T23 * np.pi / P_s / HOUR))**2
        sfT = (np.sin(T14 * np.pi / P_s / HOUR))**2
        bobs = (((1 - pobs)**2 - (sfF / sfT) * (1 + pobs)**2) / (1 - sfF / sfT))**0.5

    return dict(delta=delta, T14=T14, T23=T23, rhoobs=rhoobs, bobs=bobs,
                aobs=aobs, pobs=pobs, beta=beta, a=a,
                logPR=np.log10(rhoobs / rhotrue_gcc))

def forward_observables_legacy(rhotrue_gcc, P_days, b, p, fi, fe, alpha, theta_deg, ir_deg, bobs_method="kipping"):
    """Compute transit observables for a ringed planet (Zuluaga+2015) — legacy contact formula.

    Parameters
    ----------
    rhotrue_gcc : float
        Stellar density [g/cm^3] (true density; rho_obs is an *output*).
    P_days : float
        Orbital period [days].
    b : float
        Impact parameter [R*].
    p : float
        Planet radius ratio Rp/R*.
    fi, fe : float
        Inner / outer ring radii [Rp].
    alpha : float
        Opacity attenuation factor alpha = exp(-tau), in the range (0, 1].
        alpha=1 means a transparent ring (tau=0); alpha->0 means an opaque ring (tau->inf).
        Internally converted to tau = -log(alpha) before computing the blocking factor.
    theta_deg : float
        Projected tilt [deg]; 90 = perpendicular to orbit.
    ir_deg : float
        Projected inclination [deg]; 90 = edge-on.
    bobs_method : {'kipping', 'mallen'}, optional
        Inversion used for ``bobs`` (see module docstring). Default ``'kipping'``.

    Returns
    -------
    dict or None
        ``dict`` with keys ``delta, T14, T23, rhoobs, bobs, aobs, pobs, beta, a, logPR``.
        ``None`` if the geometry is unphysical.
    """
    # --- reparametrization: alpha = exp(-tau)  =>  tau = -log(alpha) ---
    # The blocking factor becomes: beta = 1 - exp(-tau/cosir) = 1 - alpha^(1/cosir)
    if alpha <= 0.0 or alpha > 1.0:
        return None
    tau = -np.log(alpha)
    # -------------------------------------------------------------------
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
    beta = 1 - np.exp(-tau / cosir)  # equivalent to 1 - alpha**(1/cosir)

    def _ring_r2(f):
        if f * cosir > 1:
            return f**2 * cosir - 1
        y = np.sqrt(max(f**2 - 1, 0)) / (f * sinir)
        return (f**2 * cosir * 2 / np.pi * np.arcsin(min(y, 1))
                - 2 / np.pi * np.arcsin(min(y * f * cosir, 1)))

    ri2 = beta * _ring_r2(fi)
    re2 = beta * _ring_r2(fe)
    delta = p**2 + (re2 - ri2) * p**2    # = ARp/pi
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

    if bobs_method == "mallen":
        # Mallen-Ornelas (2003)
        bobs = np.sqrt(max(
            (T14**2 * (1 - np.sqrt(delta)) - T23**2 * (1 + np.sqrt(delta))) / denom2, 0))
    else:
        # Kipping (2010)
        sfF = (np.sin(T23 * np.pi / P_s / HOUR))**2
        sfT = (np.sin(T14 * np.pi / P_s / HOUR))**2
        bobs = (((1 - pobs)**2 - (sfF / sfT) * (1 + pobs)**2) / (1 - sfF / sfT))**0.5

    return dict(delta=delta, T14=T14, T23=T23, rhoobs=rhoobs, bobs=bobs,
                aobs=aobs, pobs=pobs, beta=beta, a=a,
                logPR=np.log10(rhoobs / rhotrue_gcc))
