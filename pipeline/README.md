# PRisma Pipeline Guide

This document contains the operational details for running PRisma analyses, generating figures, understanding PPC ranking (`z1`), filename ordering, and building gallery previews.

## Scope

The `pipeline/` folder contains:

- Retrieval runners: `run_sweep.py`, `run_sweep_parallel.py`, `run_sweep_parallel.sh`
- Analysis packages: `photoring/`, `exorings/`, `geotrans/`
- Figure generator: `generate_figures.py`
- Case data/results: `kepler_51/inputs/`, `kepler_51/results/`

## Environment setup

From the repository root:

```bash
git clone https://github.com/seap-udea/PRisma.git
cd PRisma

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional Jupyter kernel:

```bash
python -m ipykernel install --user --name prisma --display-name "Python (PRisma)"
```

## Running the retrieval analysis

### Inputs

Kepler-51 inputs are in `pipeline/kepler_51/inputs/`:

- `ttv/<planet>/...post_equal_weights.dat`
- `observables/kepler_51_<planet>_observables.dat`
- `rho_true_data/rho_true_samples.dat`

Run products are written under `pipeline/kepler_51/results/exorings/` as:

- `<run_tag>.npz`
- `<run_tag>_meta.json`

### Preview the full campaign

From `pipeline/`:

```bash
bash run_sweep_parallel.sh --dry-run --n-procs 6
```

Reference-only preview (the two manuscript runs):

```bash
bash run_sweep_parallel.sh --dry-run --validate-refs --n-procs 6
```

### Launch

```bash
nohup bash run_sweep_parallel.sh --n-procs 6 > sweep_parallel_96.log 2>&1 &
tail -f sweep_parallel_96.log
```

Useful flags:

- `--n-procs N`: dynesty worker processes per configuration
- `--jobs J`: concurrent configurations
- `--validate-refs`: only manuscript reference tags
- `--skip-ppc`: skip posterior predictive draws
- `--case NAME`: case folder under `pipeline/` (default `kepler_51`)

### Stop and resume

Stop:

```bash
bash stop_sweep_parallel.sh
bash stop_sweep_parallel.sh --status
```

Resume: rerun the same launch command. Completed tags are skipped.

## Figure generation from saved runs

Script: `pipeline/generate_figures.py`

### Typical usage

From `pipeline/`:

```bash
python generate_figures.py kepler_51/results/exorings/*.npz
```

Generate only PPC figures:

```bash
python generate_figures.py kepler_51/results/exorings/*.npz --only ppc
```

Preview names without drawing:

```bash
python generate_figures.py kepler_51/results/exorings/*.npz --dry-run
```

Enable TeX labels:

```bash
python generate_figures.py kepler_51/results/exorings/*.npz --latex
```

Output directory:

- `pipeline/<case>/results/figures/`

Generated names:

- `{case}_{planet}_{ORDKEY}-{run_tag}_corner.png`
- `{case}_{planet}_{ORDKEY}-{run_tag}_corner_reduced.png`
- `{case}_{planet}_{ORDKEY}-{run_tag}_ppc.png`

## PPC score (`z1`) and ordering

For each observable in the PPC set
`{delta, T14, T23, rho_obs, b_obs}`:

1. Compute normalized mismatch:

$$
 w_{1,i} = \frac{W1_i}{|\langle x_{obs,i} \rangle|}
$$

2. Average across available observables:

$$
\langle w_1 \rangle = \text{mean}_i(w_{1,i})
$$

3. Define score:

$$
 z_1 = -\log_{10}(\langle w_1 \rangle)
$$

Interpretation: larger `z1` means better PPC agreement.

### `ORDKEY` structure

`ORDKEY` format:

- `ordXXXXX-z1_YY.YY`

Where:

- `z1_YY.YY` is the readable score (2 decimals)
- `ordXXXXX` is an inverted sortable bucket:

$$
\text{ord} = \text{clip}(\text{round}((100-z_1)\times 1000), 0, 99999)
$$

Because `ord` decreases when `z1` increases, alphabetical sorting puts better runs first.

If `z1` cannot be computed (for example missing PPC array), the script uses:

- `ord99999-z1_nan`

so those files go to the end.

## Why case+planet is in the prefix

The filename prefix starts with `{case}_{planet}_...` so files naturally group by planet in file browsers. Within each planet group, `ORDKEY` keeps best PPC files first.

## Manuscript figures and tables

To regenerate manuscript artifacts from `papers/kepler51/`:

```bash
cd ../papers/kepler51
make notebooks
make
```

- `make notebooks` syncs reference runs and executes all `PRisma-*.ipynb`
- outputs figures under `papers/kepler51/figures/`
- regenerates `tab_ring_summary.tex` and `tab_ppc_all.tex`

## Gallery generation

There are two related concepts:

1. Analysis figure outputs:
- `pipeline/kepler_51/results/figures/`

2. Web gallery previews (`.webp` thumbnails):
- generated into `pipeline/kepler_51/results/figures/.gallery/`

Preview generation uses:

- config: `.seap-udea-gallery.json` (repo root)
- script: `bin/seap-udea-gallery.sh`

Run from repo root:

```bash
bash bin/seap-udea-gallery.sh
```

Optional tuning:

```bash
MAX_WIDTH=640 QUALITY=78 bash bin/seap-udea-gallery.sh
```

Notes:

- The script reads `path` from `.seap-udea-gallery.json`.
- It builds lightweight `.webp` previews in `.gallery/` next to source images.
- If naming conventions change, update `start_with` in `.seap-udea-gallery.json` to an existing file in `pipeline/kepler_51/results/figures/`.

## End-to-end example

From `pipeline/`:

```bash
# 1) Run retrievals (or skip if results already exist)
bash run_sweep_parallel.sh --n-procs 6

# 2) Build ranked figures from saved runs
python generate_figures.py kepler_51/results/exorings/*.npz
```

From repo root:

```bash
# 3) Build gallery previews
bash bin/seap-udea-gallery.sh
```
