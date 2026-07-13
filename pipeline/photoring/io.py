"""Loading case inputs and persisting run outputs.

Centralises every read/write the pipeline does so the notebooks never touch a raw path:

- :func:`load_observables` / :func:`load_case_data` — read a case's derived observables,
  ``rho_true`` samples and inverse-CDF grid, and pack them for :class:`~photoring.model.PhotoRingModel`.
- :func:`save_run` / :func:`discover_runs` / :func:`load_run` — persist and reload posterior
  chains (``.npz``) and metadata (``_meta.json``).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

# Column order of the derived-observables files (output of step 1).
#   p, delta, aR, rho_obs[kg/m^3], P[days], b, i_orb, T14[h], T23[h]
OBS_FILE_COLUMNS = ("p", "delta", "aR", "rho_obs_kgm3", "P_days", "b", "i_orb", "T14", "T23")


def load_observables(path):
    """Load a derived-observables ``.dat`` file into a TTV dict (densities in g/cm^3).

    Returns
    -------
    dict
        Keys ``delta, T14, T23, rho_obs_gcc, b, p, P_days`` (arrays), matching what
        :class:`~photoring.model.PhotoRingModel` and the plotting code expect.
    """
    obs = np.loadtxt(path)
    p_s, delta_s, aR_s, rho_kgm3_s, P_days_s, b_s, iorb_s, T14_s, T23_s = obs.T
    return dict(
        delta=delta_s, T14=T14_s, T23=T23_s,
        rho_obs_gcc=rho_kgm3_s / 1000.0,
        b=b_s, p=p_s, P_days=P_days_s,
        aR=aR_s, i_orb=iorb_s,
    )


def load_case_data(paths, planet):
    """Load everything :class:`~photoring.model.PhotoRingModel` needs for one planet.

    Parameters
    ----------
    paths : photoring.config.CasePaths
        Resolved case paths.
    planet : str
        Planet key (e.g. ``'b'`` or ``'d'``).

    Returns
    -------
    dict
        ``ttv`` (dict), ``rho_true_gcc_samples`` (ndarray), ``rho_grid``/``rho_cdf``
        (ndarray or ``None``), ``P_fixed`` (float).
    """
    obs_file = paths.observables_file(planet)
    if not obs_file.exists():
        raise FileNotFoundError(
            f"Observables file not found: {obs_file}\n"
            f"Run notebook 01 first, or place a derived-observables .dat there.")
    ttv = load_observables(obs_file)

    rho_true = np.loadtxt(paths.rho_true_samples) / 1000.0  # kg/m^3 -> g/cm^3

    rho_grid = rho_cdf = None
    if paths.rho_cdf_file.exists():
        loaded = np.loadtxt(paths.rho_cdf_file, skiprows=1)
        rho_grid, rho_cdf = loaded[:, 0], loaded[:, 1]

    return dict(
        ttv=ttv,
        rho_true_gcc_samples=rho_true,
        rho_grid=rho_grid,
        rho_cdf=rho_cdf,
        P_fixed=float(np.median(ttv["P_days"])),
    )


def make_run(model, result, run_tag, planet, ppc=None):
    """Assemble an in-memory ``run`` dict (same shape as :func:`load_run`).

    Lets the inference notebooks feed the publication plotting functions the *same*
    record the results notebook builds from saved files.
    """
    return dict(
        tag=run_tag,
        chain=result["chain"],
        ppc=ppc,
        samples=result.get("dres").samples if result.get("dres") is not None else None,
        logwt=result.get("dres").logwt if result.get("dres") is not None else None,
        logl=result.get("dres").logl if result.get("dres") is not None else None,
        dres=result.get("dres"),
        meta=dict(planet=planet, param_names=model.PARAM_NAMES,
                  kde_observables=model.observables,
                  B_FIXED=model.B_FIXED, B_SIGMA=model.B_SIGMA,
                  FI_FIXED=model.FI_FIXED, FE_MAX=model.FE_MAX,
                  p_mean_ref=model.p_mean_ref),
        param_names=model.PARAM_NAMES,
        planet=planet,
        logz=result.get("logz", float("nan")),
        logz_err=result.get("logz_err", float("nan")),
        n_iter=result.get("n_iter", 0),
        runtime_s=result.get("runtime_s", 0),
        kde_obs=model.observables,
    )


def save_run(results_dir, run_tag, arrays, meta, overwrite=False):
    """Save a run's chain arrays (``.npz``) and metadata (``_meta.json``).

    Parameters
    ----------
    results_dir : str or Path
        Destination directory (e.g. ``paths.results_dir('exorings')``).
    run_tag : str
        Base filename (encodes the run configuration).
    arrays : dict
        Arrays to store in the ``.npz`` (e.g. ``chain``, ``ppc``, ``samples`` …).
    meta : dict
        JSON-serialisable metadata.
    overwrite : bool
        If ``False`` (default) and the ``.npz`` exists, do not overwrite (returns ``None``).

    Returns
    -------
    tuple(Path, Path) or None
        ``(npz_path, json_path)`` if written, else ``None``.
    """
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    npz_path = results_dir / f"{run_tag}.npz"
    json_path = results_dir / f"{run_tag}_meta.json"

    if npz_path.exists() and not overwrite:
        print(f"WARNING: {npz_path} already exists — NOT overwriting.")
        print("  Change the run configuration (RUN_TAG) to save a new run.")
        return None

    np.savez_compressed(npz_path, **arrays)
    with open(json_path, "w") as f:
        json.dump(meta, f, indent=2)
    return npz_path, json_path


def load_run(npz_path):
    """Load a single run from its ``.npz`` and ``_meta.json`` files into a dict."""
    npz_path = Path(npz_path)
    npz = np.load(npz_path, allow_pickle=False)
    tag = npz_path.stem
    json_path = npz_path.with_name(tag + "_meta.json")
    meta = json.loads(json_path.read_text()) if json_path.exists() else {}

    dres = None
    try:
        from dynesty.results import Results as DyResults
        dres = DyResults([
            ("samples", npz["samples"]),
            ("logwt", npz["logwt"]),
            ("logl", npz["logl"]),
        ])
        if "logz" in meta:
            dres["logz"] = np.full(len(npz["samples"]), meta["logz"])
            dres["logzerr"] = np.full(len(npz["samples"]), meta.get("logz_err", 0.0))
        else:
            dres["logz"] = np.zeros(len(npz["samples"]))
            dres["logzerr"] = np.zeros(len(npz["samples"]))
    except Exception:
        dres = None

    return dict(
        tag=tag,
        chain=npz["chain"],
        ppc=npz["ppc"] if "ppc" in npz else None,
        samples=npz["samples"] if "samples" in npz else None,
        logwt=npz["logwt"] if "logwt" in npz else None,
        logl=npz["logl"] if "logl" in npz else None,
        dres=dres,
        meta=meta,
        param_names=meta.get("param_names", []),
        planet=meta.get("planet", "?"),
        logz=meta.get("logz", float("nan")),
        logz_err=meta.get("logz_err", float("nan")),
        n_iter=meta.get("n_iter", 0),
        runtime_s=meta.get("runtime_s", 0),
        kde_obs=meta.get("kde_observables", []),
    )


def discover_runs(results_dir, run_tags=None):
    """Load all runs (or a specific list of ``run_tags``) from a results directory.

    Returns
    -------
    dict
        ``{tag: run_dict}`` as produced by :func:`load_run`.
    """
    results_dir = Path(results_dir)
    if run_tags:
        npz_files = [results_dir / f"{t}.npz" for t in run_tags]
    else:
        npz_files = sorted(results_dir.glob("*.npz"))
    runs = {}
    for p in npz_files:
        try:
            r = load_run(p)
            runs[r["tag"]] = r
        except Exception as e:
            print(f"  SKIP {p.name}: {e}")
    return runs
