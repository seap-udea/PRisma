"""Parameter space of the ring-geometry retrieval.

The free parameters are assembled dynamically from the model configuration. The canonical
order is always::

    fe, iR, theta, p, (alpha), (rho_true), (b)

where ``fe, iR, theta`` are always free, ``p`` is free unless ``P_FREE=False`` (then it is
pinned to the lower edge of its prior), and ``alpha``, ``rho_true``, ``b`` are appended when
their respective ``*_FREE`` flags are set.

Priors
------
======================  ==================================================================
 Parameter               Prior
======================  ==================================================================
 ``fe``                  Uniform ``(fi, FE_MAX]``
 ``iR``                  Isotropic, ``p(iR) ~ sin(iR)`` on ``(0, 90) deg``
 ``theta``               Uniform ``[0, 90] deg``
 ``p``                   Uniform ``[p_min, p_max]``
 ``alpha`` (opt.)        Uniform on ``[0, 1]``  (alpha = exp(-tau); alpha=1 transparent, alpha->0 opaque)
 ``rho_true`` (opt.)     Empirical KDE over external samples (inverse-CDF transform)
 ``b`` (opt.)            Truncated normal on ``[0, 1]`` (Masuda+2024)
======================  ==================================================================

This module holds only the *pure* parameter-space bookkeeping (:func:`build_param_space`);
the actual prior transform / log-prior are methods on
:class:`photoring.model.PhotoRingModel`, which owns the fitted distributions.
"""

from __future__ import annotations

# Display labels for each parameter (LaTeX).
PARAM_LABEL_MAP = {
    "fe":       r"$f_e\,[R_p]$",
    "ir":       r"$i_R\,[\deg]$",
    "theta":    r"$\theta\,[\deg]$",
    "p":        r"$p=R_p/R_\star$",
    "alpha":    r"$\alpha=e^{-\tau}$",
    "rho_true": r"$\rho_{\star,\mathrm{true}}\,[\mathrm{g/cm}^3]$",
    "b":        r"$b$",
}


def build_param_space(model_config):
    """Return ``(param_names, param_labels)`` for the given model configuration.

    ``model_config`` is the ``MODEL_CONFIG`` dict from the notebooks. The flags consulted
    are ``P_FREE`` (default ``True``), ``ALPHA_FREE``, ``RHO_TRUE_FREE``, ``B_FREE``.
    """
    p_free = bool(model_config.get("P_FREE", True))
    names = ["fe", "ir", "theta"]
    if p_free:
        names.append("p")
    if bool(model_config.get("ALPHA_FREE", False)):
        names.append("alpha")
    if bool(model_config.get("RHO_TRUE_FREE", False)):
        names.append("rho_true")
    if bool(model_config.get("B_FREE", False)):
        names.append("b")
    labels = [PARAM_LABEL_MAP[n] for n in names]
    return names, labels
