"""Sampler-friendly wrapper around the ``geotrans2`` numerically-integrated
ring-transit model.

``geotrans2_lite`` (a lightweight refactor of the original ``GeoTrans`` code) computes
the transit of a ringed planet by *numerically integrating* the projected ring+planet
area — a more rigorous but slower alternative to the closed-form ``exorings`` model.

This module exposes a single function, :func:`geotrans2_model`, with **exactly the same
signature and return contract** as :func:`exorings.forward.forward_observables`, so the
inference pipeline can swap forward models transparently (``FORWARD_MODEL='geotrans'``).

It returns a plain ``dict`` of transit observables, or ``None`` when the geometry is
unphysical / the contact times cannot be computed — the contract nested sampling and
MCMC need to reject a proposal (map it to ``-inf`` log-likelihood).

Ported verbatim from the inline ``geotrans2_model`` that used to live in the pipeline
notebooks; only the module import was made explicit (no ``importlib`` path hack).
"""

from __future__ import annotations

import numpy as _np

from . import geotrans2_lite as gt2


def geotrans2_model(rhotrue_gcc, P_days, b, p, fi, fe, tau, theta_deg, ir_deg):
    """Compute transit observables for a ringed planet using ``geotrans2-lite``.

    Parameters
    ----------
    rhotrue_gcc : float
        Stellar density [g/cm^3].
    P_days : float
        Orbital period [days].
    b : float
        Impact parameter [R*].
    p : float
        Planet radius ratio Rp/R*.
    fi, fe : float
        Inner / outer ring radii [Rp].
    tau : float
        Normal opacity.
    theta_deg : float
        Ring roll angle [deg]; maps to ``S.phir`` in geotrans2.
    ir_deg : float
        Ring inclination [deg]; maps to ``S.ir`` in geotrans2.

    Returns
    -------
    dict or None
        ``dict`` with keys ``delta, T14, T23, rhoobs, bobs, aobs, pobs, logPR``.
        ``None`` if the geometry is unphysical or contact times cannot be computed.
    """
    # ── Build geotrans2 system configuration ──────────────────────────────
    cfg = dict(
        rhotrue=float(rhotrue_gcc),   # g/cm^3  -> gt2 converts to kg/m^3 internally
        P=float(P_days),              # days
        b=float(b),                   # R*
        p=float(p),                   # Rp/R*
        fp=0.0,                       # no oblateness
        fi=float(fi),                 # Rp units
        fe=float(fe),                 # Rp units
        tau=float(tau),
        ir=float(ir_deg) * gt2.DEG,       # rad
        phir=float(theta_deg) * gt2.DEG,  # rad  (theta -> roll angle)
        ep=0.0,                       # circular orbit
        wp=0.0,
    )

    # ── Instantiate RingedSystem ──────────────────────────────────────────
    try:
        S = gt2.RingedSystem(cfg)
    except SystemExit:
        # gt2 calls exit() for unphysical configs (b > aRs, etc.)
        return None
    except Exception:
        return None

    # ── Sanity: effective inclination must allow a visible ring ───────────
    # (ieff ~ 90 deg -> edge-on ring; cos(ieff) ~ 0 -> block factor undefined)
    if _np.cos(S.ieff) < 1e-6:
        return None

    # ── Observed stellar density (Seager & Mallen-Ornelas 2003, Kipping 2010) ──
    rhoobs, aobs, bobs = S.calculate_rho_obs()

    # ── Contact times -> T14, T23 ─────────────────────────────────────────
    T14, T23 = S.tT, S.tF

    # ── Photo-Ring log ratio ──────────────────────────────────────────────
    logPR = _np.log10(rhoobs / 1e3 / rhotrue_gcc)

    # ── Transit depth (delta = Ar / R*^2 = ringed area in R* units) ───────
    Ar = S.Ar                       # area in R*^2 units
    delta = Ar / _np.pi             # = (Rp_eff/R*)^2 -- same convention as exorings
    if delta <= 0:
        return None
    pobs = _np.sqrt(delta)

    return dict(
        delta=delta,
        T14=T14,
        T23=T23,
        rhoobs=rhoobs / 1e3,
        bobs=bobs,
        aobs=aobs,
        pobs=pobs,
        logPR=logPR,
    )
