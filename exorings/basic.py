"""Object-oriented API for the legacy `exorings-basic.py` calculations.

This module mirrors the analytical/approximate formulas implemented in
`exorings-basic.py`, but exposes them as reusable classes/functions so they can
be imported from notebooks and other scripts.

The goal is *standardized computation* (no copy/paste of formulas), while
keeping the legacy script as a reference implementation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any, Mapping

import numpy as np

try:
    # When imported as a package module: `import exorings.basic`
    from .exorings import DEG, RAD, DAY, HOUR, GCONST
except ImportError:  # pragma: no cover
    # When running from inside the folder (where `exorings.py` is importable)
    from exorings import DEG, RAD, DAY, HOUR, GCONST  # type: ignore


class ExoringsError(RuntimeError):
    """Base exception for exorings computations."""


class NoTransitError(ExoringsError):
    """Raised when the input geometry does not yield a (non-grazing) transit."""

    def __init__(self, b: float, bmax: float):
        message = (
            "No transit (or a grazing transit) occurrs with this impact parameter, "
            f"b = {b:.2f}.\n"
            f"Maximum impact parameter: bmax ~ {bmax:.3f}"
        )
        super().__init__(message)
        self.b = float(b)
        self.bmax = float(bmax)


@dataclass(frozen=True)
class ExoringsBasicParams:
    """Input parameters for the `exorings-basic` analytical model."""

    # Transit parameters
    rhotrue: float = 1.40598  # g/cm^3
    P: float = 365.2446  # days
    b: float = 0.1875  # R*

    # Planet and rings
    p: float = 0.08  # Rp/R*
    fi: float = 1.5  # Ri/Rp
    fe: float = 2.35  # Re/Rp
    tau: float = 1.0
    theta: float = 30.0  # degrees
    ir: float = 80.0  # degrees

    @classmethod
    def from_any(cls, obj: Any) -> "ExoringsBasicParams":
        """Build params from a dataclass, mapping, or `dict2obj`-style object."""

        if isinstance(obj, cls):
            return obj

        allowed = {f.name for f in fields(cls)}

        if isinstance(obj, Mapping):
            kwargs = {k: obj[k] for k in allowed if k in obj}
            return cls(**kwargs)

        if hasattr(obj, "__dict__"):
            d = obj.__dict__
            kwargs = {k: d[k] for k in allowed if k in d}
            return cls(**kwargs)

        raise TypeError(
            "Unsupported params type. Expected ExoringsBasicParams, a mapping, "
            "or an object with __dict__."
        )


@dataclass(frozen=True)
class ExoringsBasicResult:
    """All derived quantities computed by the `exorings-basic` model."""

    params: ExoringsBasicParams

    # Orbital properties
    a: float  # a/R*
    iorb: float  # degrees

    # External ring projected axes
    A: float  # semimajor axis (in R*)
    B: float  # semiminor axis (in R*)

    # Transit condition helper
    hp: float

    # Depth / area
    beta: float
    ri2: float
    re2: float
    ARp: float
    delta: float
    pobs: float

    # Contact positions
    xp1: float
    xp2: float
    xp3: float
    xp4: float

    xR1: float
    xR2: float
    xR3: float
    xR4: float

    x1: float
    x2: float
    x3: float
    x4: float

    # Transit times (hours)
    T14p: float
    T23p: float
    T14: float
    T23: float

    # Derived observed properties
    aobs: float
    bobs: float
    rhoobs: float
    PR: float
    logPR: float

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict (dataclasses + numpy floats)."""

        d = asdict(self)
        # Convert any numpy scalars to plain Python floats
        for k, v in list(d.items()):
            if isinstance(v, (np.floating, np.integer)):
                d[k] = v.item()
        return d


def compute_exorings_basic(params: ExoringsBasicParams | Mapping[str, Any] | Any) -> ExoringsBasicResult:
    """Compute all `exorings-basic` quantities.

    Parameters
    ----------
    params:
        Accepts an `ExoringsBasicParams` instance, a mapping (dict-like), or an
        object with attributes (e.g. `dict2obj` from the legacy CLI parser).

    Returns
    -------
    ExoringsBasicResult
    """

    par = ExoringsBasicParams.from_any(params)

    # ==============================
    # ORBITAL PROPERTIES
    # ==============================
    a = (GCONST * (par.rhotrue * 1e3) / (3 * np.pi) * (par.P * DAY) ** 2) ** (1.0 / 3.0)

    cosiorb = par.b / a
    siniorb = (1 - cosiorb**2) ** 0.5
    iorb = float(np.arccos(cosiorb) * RAD)

    # ==============================
    # EXTERNAL RING PROPERTIES
    # ==============================
    A = par.fe * par.p
    B = A * np.cos(par.ir * DEG)

    # ==============================
    # CHECK TRANSIT CONDITION
    # ==============================
    hp = max(par.p, A * np.sin(par.theta * DEG), B * np.cos(par.theta * DEG))

    if par.b > 1.0 - hp:
        bmax = 1.0 - hp
        raise NoTransitError(b=float(par.b), bmax=float(bmax))

    # ==============================
    # TRANSIT DEPTH
    # ==============================
    cosir = np.cos(par.ir * DEG)
    sinir = np.sin(par.ir * DEG)

    # Guard for the edge-on limit (cosir -> 0)
    if abs(float(cosir)) < 1e-15:
        cosir_safe = np.copysign(1e-15, float(cosir) if float(cosir) != 0.0 else 1.0)
    else:
        cosir_safe = cosir

    beta = 1 - np.exp(-par.tau / cosir_safe)

    # Internal ring effective radius^2
    if par.fi * cosir > 1:
        ri2 = par.fi**2 * cosir - 1
    else:
        yi = np.sqrt(par.fi**2 - 1) / (par.fi * sinir)
        ri2 = (
            par.fi**2 * cosir * 2 / np.pi * np.arcsin(yi)
            - 2 / np.pi * np.arcsin(yi * par.fi * cosir)
        )
    ri2 = beta * ri2

    # External ring effective radius^2
    if par.fe * cosir > 1:
        re2 = par.fe**2 * cosir - 1
    else:
        ye = np.sqrt(par.fe**2 - 1) / (par.fe * sinir)
        re2 = (
            par.fe**2 * cosir * 2 / np.pi * np.arcsin(ye)
            - 2 / np.pi * np.arcsin(ye * par.fe * cosir)
        )
    re2 = beta * re2

    ARp = np.pi * par.p**2 + np.pi * (re2 - ri2) * par.p**2
    delta = ARp / np.pi
    pobs = np.sqrt(delta)

    # ==============================
    # CONTACT POSITIONS
    # ==============================
    xp14 = np.sqrt((1 + par.p) ** 2 - par.b**2)
    xp1 = -xp14
    xp4 = +xp14

    xp23 = np.sqrt((1 - par.p) ** 2 - par.b**2)
    xp2 = -xp23
    xp3 = +xp23

    # External ring contacts (approximate solution)
    xR13 = 1 - A**2 * (np.sin(par.theta * DEG) - par.b / A) ** 2 * (1 - B**2 / A)
    xR24 = 1 - A**2 * (np.sin(par.theta * DEG) + par.b / A) ** 2 * (1 - B**2 / A)

    xR1 = -np.sqrt(xR13) - A * np.cos(par.theta * DEG)
    xR2 = -np.sqrt(xR24) + A * np.cos(par.theta * DEG)
    xR3 = +np.sqrt(xR13) - A * np.cos(par.theta * DEG)
    xR4 = +np.sqrt(xR24) + A * np.cos(par.theta * DEG)

    # Choose final contact positions
    x1 = min(xp1, xR1)
    x2 = max(xp2, xR2)
    x3 = min(xp3, xR3)
    x4 = max(xp4, xR4)

    # ==============================
    # TRANSIT TIMES
    # ==============================
    T14p = (par.P * DAY) * np.arcsin((xp4 - xp1) / (a * siniorb)) / (2 * np.pi) / HOUR
    T23p = (par.P * DAY) * np.arcsin((xp3 - xp2) / (a * siniorb)) / (2 * np.pi) / HOUR

    T14 = (par.P * DAY) * np.arcsin((x4 - x1) / (a * siniorb)) / (2 * np.pi) / HOUR
    T23 = (par.P * DAY) * np.arcsin((x3 - x2) / (a * siniorb)) / (2 * np.pi) / HOUR

    # ==============================
    # DERIVED TRANSIT PROPERTIES
    # ==============================
    aobs = 2 * (par.P * DAY / HOUR) / np.pi * delta**0.25 / (T14**2 - T23**2) ** 0.5

    bobs = (
        (T14**2 * (1 - np.sqrt(delta)) - T23**2 * (1 + np.sqrt(delta))) / (T14**2 - T23**2)
    ) ** 0.5

    rhoobs = (3 * np.pi / GCONST) * aobs**3 / (par.P * DAY) ** 2 / 1e3

    PR = rhoobs / par.rhotrue
    logPR = np.log10(PR)

    return ExoringsBasicResult(
        params=par,
        a=float(a),
        iorb=float(iorb),
        A=float(A),
        B=float(B),
        hp=float(hp),
        beta=float(beta),
        ri2=float(ri2),
        re2=float(re2),
        ARp=float(ARp),
        delta=float(delta),
        pobs=float(pobs),
        xp1=float(xp1),
        xp2=float(xp2),
        xp3=float(xp3),
        xp4=float(xp4),
        xR1=float(xR1),
        xR2=float(xR2),
        xR3=float(xR3),
        xR4=float(xR4),
        x1=float(x1),
        x2=float(x2),
        x3=float(x3),
        x4=float(x4),
        T14p=float(T14p),
        T23p=float(T23p),
        T14=float(T14),
        T23=float(T23),
        aobs=float(aobs),
        bobs=float(bobs),
        rhoobs=float(rhoobs),
        PR=float(PR),
        logPR=float(logPR),
    )


class ExoringsBasic:
    """OO wrapper around `compute_exorings_basic`."""

    def __init__(self, params: ExoringsBasicParams | Mapping[str, Any] | Any = ExoringsBasicParams()):
        self.params = ExoringsBasicParams.from_any(params)

    def compute(self) -> ExoringsBasicResult:
        return compute_exorings_basic(self.params)


def render_exorings_basic_report(result: ExoringsBasicResult) -> str:
    """Render a human-readable report similar to `exorings-basic.py`."""

    par = result.params

    lines: list[str] = []
    L = "*" * 60

    lines.append(L)
    lines.append("INPUT PARAMETERS")
    lines.append(L)

    lines.append("Stellar properties:")
    lines.append(f"\tStellar Density: rho_true = {par.rhotrue:.2f} g/cm^3.")

    lines.append("Planetary properties:")
    lines.append(f"\tPlanetary radius: p = Rp/R* = {par.p:.4f}.")

    lines.append("Orbital properties:")
    lines.append(f"\tOrbital period: P = {par.P:.4f} days.")
    lines.append(f"\tImpact parameter: b/R*= {par.b:.4f}")

    lines.append("Ring properties:")
    lines.append(f"\tInternal Ring Radius: Ri/Rp = {par.fi:.3f} Rp.")
    lines.append(f"\tExternal Ring Radius: Re/Rp = {par.fe:.3f} Rp.")
    lines.append(f"\tNormal opacity: tau = {par.tau:.3f}.")
    lines.append(f"\tProjected inclination (90 deg for edge on): ir = {par.ir:.2f} deg.")
    lines.append(f"\tProjected tilt: theta = {par.theta:.2f} deg.")
    lines.append(f"\tBlocking factor: beta = {result.beta:e}.")

    lines.append(L)
    lines.append("DERIVED PROPERTIES")
    lines.append(L)

    lines.append("Orbital properties:")
    lines.append(f"\tSemimajor axis: a/R*= {result.a:.4f}")
    lines.append(f"\tOrbital Inclination: iorb = {result.iorb:.3f} deg")

    lines.append("Ring derived properties:")
    lines.append(f"\tProjected exrenal ring axes: A/R* = {result.A:.4f}, B/R* = {result.B:.4f}")
    lines.append(f"\tEffective ring interior radius: r_i/R* = {np.sqrt(result.ri2):e}")
    lines.append(f"\tEffective ring exterior radius: r_e/R* = {np.sqrt(result.re2):e}")
    lines.append(f"\tProjected ring Area: A_Rp/R*^2 = {result.ARp:e}")

    lines.append(L)
    lines.append("TRANSIT PROPERTIES")
    lines.append(L)

    lines.append(f"Transit Depth: delta = {result.delta * 1e6:.2f} ppm")
    lines.append(f"Observed Planetary Radius: pobs = sqrt(delta) = {result.pobs:.6f}")
    lines.append(f"Scaled planetary radius: p = Rp/R* = {par.p:.6f}")
    lines.append(f"Planetary radius ratio: pobs/p = {result.pobs / par.p:.2f}")

    lines.append("Planet contact positions:")
    lines.append(f"\tx1 = {result.xp1:.3f}, x2 = {result.xp2:.3f}")
    lines.append(f"\tx3 = {result.xp3:.3f}, x4 = {result.xp4:.3f}")

    lines.append("Ring contact positions:")
    lines.append(f"\tx1 = {result.xR1:.3f}, x2 = {result.xR2:.3f}")
    lines.append(f"\tx3 = {result.xR3:.3f}, x4 = {result.xR4:.3f}")

    lines.append("Final Contact positions:")
    lines.append(f"\tx1 = {result.x1:.3f}, x2 = {result.x2:.3f}")
    lines.append(f"\tx3 = {result.x3:.3f}, x4 = {result.x4:.3f}")

    lines.append(
        f"Transit duration (non-ringed): T14 = {result.T14p:.4f} h, T23 = {result.T23p:.4f}"
    )
    lines.append(f"Transit duration (ringed): T14 = {result.T14:.4f} h, T23 = {result.T23:.4f}")
    lines.append(f"Observed scaled semimajor axis: (a/Rs)_obs = {result.aobs:.2f}")
    lines.append(f"Observed impact parameter: b_obs/R* = {result.bobs:.4f}")
    lines.append(f"Observed stellar density: rho_obs = {result.rhoobs:.2f} g/cm^3")
    lines.append(f"Photo-ring effect: PR = {result.PR:.4f}, log10(PR) = {result.logPR:.2f}")

    return "\n".join(lines)
