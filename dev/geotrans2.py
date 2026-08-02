"""geotrans2.py
================

Standalone, **test-only** companion to the pipeline's ``geotrans`` package
(``pipeline/geotrans/geotrans.py`` / ``pipeline/geotrans/model.py``). Nothing in
``pipeline/geotrans/`` is modified here -- this module only *imports* it and adds two
corrections on top, so the two packages can be compared side by side:

1. **Apparent -> intrinsic ring-angle conversion.** ``exorings.forward.forward_observables``'s
   ``ir_deg``/``theta_deg`` are the *apparent* (sky-projected) ring inclination/tilt, while
   ``geotrans``'s own free parameters ``ir``/``phir`` are *intrinsic* (defined relative to
   the orbital plane). The shipped ``pipeline/geotrans/model.py::geotrans2_model`` passes
   ``ir_deg``/``theta_deg`` straight through as ``ir``/``phir`` with no conversion, which is
   only correct for an edge-on orbit (``iorb = 90 deg``). This module numerically inverts
   the rotation-composition map that relates them (``apparent_from_intrinsic`` /
   ``apparent_to_intrinsic``), cross-checked against the original, pre-refactor
   ``geotrans_legacy.py`` in ``PRisma-GeotransVerification.ipynb`` (Section 3a).

2. **``rhoObserved_Seager``'s ``b_obs`` (impact parameter) formula bug.** The shipped
   function is called with ``p = ringedPlanetArea(S)/pi``, i.e. the transit depth
   ``delta = (Rp_obs/R*)^2`` -- despite its docstring calling ``p`` a radius ratio. Its
   ``b_obs`` formula then uses this ``delta`` directly in ``(1 -+ p)`` terms, where the
   Seager & Mallen-Ornelas (2003) formula requires the *radius ratio*
   ``p_obs = sqrt(delta)`` in **squared** ``(1 -+ p_obs)**2`` terms. This is confirmed by
   this same module's own ``rhoObserved_Kipping``, which correctly computes
   ``Rp = sqrt(p)`` before using it in the analogous squared terms. ``rhoObserved_Seager_fixed``
   below applies that same correction (only to ``b``; ``a``/``rho_obs`` only depend on
   ``p**0.25 = delta**0.25``, which was already correct).

See ``PRisma-GeotransVerification.ipynb`` for the full derivation/validation of both fixes.
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np
from scipy.optimize import fsolve

# ── Make the pipeline packages importable, without touching the pipeline itself ──
_HERE = pathlib.Path(__file__).resolve().parent
_cands = [_HERE, *_HERE.parents]
_REPO = next((c for c in _cands if (c / "pipeline" / "geotrans").is_dir()), _HERE.parent)
for _p in (str(_REPO / "pipeline"), str(_REPO)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import geotrans.geotrans as gt2  # the pipeline package -- read-only, not modified here


# ---------------------------------------------------------------------------------------
# 1. Apparent (exorings convention) <-> intrinsic (geotrans convention) ring angles
# ---------------------------------------------------------------------------------------

def apparent_from_intrinsic(ir, phir, iorb):
    """Forward map: intrinsic ring angles ``(ir, phir)`` (radians, relative to the orbital
    plane) plus the orbital inclination ``iorb`` (radians) -> apparent, sky-projected ring
    inclination/tilt ``(ieff, teff)`` (radians). Identical rotation composition to
    ``geotrans.py``/``geotrans_legacy.py``'s ``updatePlanetRings`` (``Mi . Mpr . Mir`` acting
    on the ring's normal vector).
    """
    Mi = gt2.rotMat([1, 0, 0], -iorb)
    Mpr = gt2.rotMat([0, 0, 1], phir)
    Mir = gt2.rotMat([1, 0, 0], -ir)
    Mrs = np.dot(Mi, np.dot(Mpr, Mir))
    rz = np.dot(Mrs, [0.0, 0.0, 1.0])
    ieff = np.arccos(abs(rz[2]))
    teff = -np.sign(rz[0]) * gt2.ARCTAN(abs(rz[0]), abs(rz[1]))
    return ieff, teff


def apparent_to_intrinsic(ir_deg, theta_deg, iorb):
    """Numerically invert ``apparent_from_intrinsic``: given the *apparent* ring angles
    (as used by ``exorings.forward.forward_observables``, in degrees) and the orbital
    inclination ``iorb`` (radians), solve for geotrans's *intrinsic* ``(ir, phir)`` (radians).

    Returns
    -------
    (ir_rad, phir_rad) or None
        ``None`` if the nonlinear solve does not converge.
    """
    ieff_t, teff_t = np.deg2rad(ir_deg), np.deg2rad(theta_deg)

    def residual(x):
        ieff, teff = apparent_from_intrinsic(x[0], x[1], iorb)
        return [ieff - ieff_t, teff - teff_t]

    sol, info, ier, msg = fsolve(residual, x0=[ieff_t, teff_t], full_output=True)
    return (sol[0], sol[1]) if ier == 1 else None


# ---------------------------------------------------------------------------------------
# 2. Corrected b_obs formula for the Seager & Mallen-Ornelas (2003) method
# ---------------------------------------------------------------------------------------

def rhoObserved_Seager_fixed(p, tT, tF, P):
    """Corrected version of ``geotrans.geotrans.rhoObserved_Seager``.

    Parameters (identical contract to the original):
    p : Transit depth, ``delta = (Rp_obs/R*)^2`` (an area ratio -- always called with
        ``ringedPlanetArea(S)/pi``, despite the original's docstring calling it a radius
        ratio).
    tT, tF : Total / full transit duration (hours).
    P : Orbital period (hours).

    Bug fixed: the original mixes up ``delta`` and ``p_obs = sqrt(delta)`` in the ``b_obs``
    (impact parameter) term, using linear ``(1 -+ p)`` (i.e. ``(1 -+ delta)``) instead of the
    squared ``(1 -+ p_obs)**2`` terms that the Seager & Mallen-Ornelas (2003) formula (and
    this same package's own ``rhoObserved_Kipping``, which correctly computes
    ``Rp = sqrt(p)`` first) require. ``a``/``rho`` only depend on ``p**0.25 = delta**0.25``,
    which was already correct, and are unchanged here.
    """
    pobs = np.sqrt(p)
    a = 2 * (P * gt2.HOUR) / np.pi * p ** 0.25 / ((tT * gt2.HOUR) ** 2 - (tF * gt2.HOUR) ** 2) ** 0.5
    b = np.sqrt(max((tT ** 2 * (1 - pobs) ** 2 - tF ** 2 * (1 + pobs) ** 2) / (tT ** 2 - tF ** 2), 0.0))
    rho = 3 * np.pi * a ** 3 / (gt2.GCONST * (P * gt2.HOUR) ** 2)
    return rho, a, b


def calculate_rho_obs_fixed(S, method="Seager"):
    """Corrected drop-in for ``geotrans.geotrans.RingedSystem.calculate_rho_obs``: identical
    logic, except the ``'Seager'`` branch calls ``rhoObserved_Seager_fixed`` instead of the
    shipped (buggy) ``rhoObserved_Seager``. ``'Kipping'`` is unchanged (it was already
    correct) and is exposed here only for convenience/comparison.
    """
    tcsp = gt2.contactTimes(S)
    S.tT = (tcsp[-1] - tcsp[1]) / gt2.HOUR
    S.tF = (tcsp[-2] - tcsp[2]) / gt2.HOUR

    p = gt2.ringedPlanetArea(S) / np.pi
    if method == "Kipping":
        rho_obs, a, b = gt2.rhoObserved_Kipping(p, S.tT, S.tF, S.Porb / gt2.HOUR)
    elif method == "Seager":
        rho_obs, a, b = rhoObserved_Seager_fixed(p, S.tT, S.tF, S.Porb / gt2.HOUR)
    else:
        raise ValueError("Invalid method for rho_obs calculation. Use 'Seager' or 'Kipping'.")
    S.rho_obs = rho_obs
    return rho_obs, a, b


# ---------------------------------------------------------------------------------------
# 3. Test wrapper: same contract as pipeline/geotrans/model.py's geotrans2_model, with
#    both fixes applied -- for side-by-side testing against the shipped wrapper.
# ---------------------------------------------------------------------------------------

def geotrans2_model(rhotrue_gcc, P_days, b, p, fi, fe, tau, theta_deg, ir_deg, method="Seager"):
    """Compute transit observables for a ringed planet using ``geotrans``, with the
    apparent-to-intrinsic ring-angle conversion and the corrected Seager ``b_obs`` formula
    applied. Same signature/return contract as
    ``pipeline/geotrans/model.py::geotrans2_model`` (plus an extra ``method`` kwarg).

    Returns
    -------
    dict or None
        ``dict`` with keys ``delta, T14, T23, rhoobs, bobs, aobs, pobs, logPR``.
        ``None`` if the geometry is unphysical or contact times cannot be computed.
    """
    # ── Orbital inclination (needed to invert the apparent ring angles) ───────────
    aRs = (gt2.GCONST * (rhotrue_gcc * 1e3) / (3 * np.pi) * (P_days * gt2.DAY) ** 2) ** (1 / 3)
    cosiorb = b / aRs
    if abs(cosiorb) > 1:
        return None
    iorb = np.arccos(cosiorb)

    sol = apparent_to_intrinsic(ir_deg, theta_deg, iorb)
    if sol is None:
        return None
    ir_rad, phir_rad = sol

    # ── Build geotrans2 system configuration (intrinsic ir/phir, not apparent) ────
    cfg = dict(
        rhotrue=float(rhotrue_gcc),
        P=float(P_days),
        b=float(b),
        p=float(p),
        fp=0.0,
        fi=float(fi),
        fe=float(fe),
        tau=float(tau),
        ir=float(ir_rad),
        phir=float(phir_rad),
        ep=0.0,
        wp=0.0,
    )

    try:
        S = gt2.RingedSystem(cfg)
    except SystemExit:
        return None
    except Exception:
        return None

    if np.cos(S.ieff) < 1e-6:
        return None

    rhoobs, aobs, bobs = calculate_rho_obs_fixed(S, method=method)
    delta = S.Ar / np.pi
    if delta <= 0:
        return None

    return dict(
        delta=delta,
        T14=S.tT,
        T23=S.tF,
        rhoobs=rhoobs / 1e3,
        bobs=bobs,
        aobs=aobs,
        pobs=np.sqrt(delta),
        logPR=np.log10(rhoobs / 1e3 / rhotrue_gcc),
    )
