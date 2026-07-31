# Legacy papermill sweep launcher

`run_sweep.sh` drove `02_inference_*.ipynb` via papermill. Those notebooks live under `.legacy/`
and the path deadlocks under `use_pool=True` on macOS.

**Use instead:** `pipeline/run_sweep_parallel.sh` (imports `run_sweep.py` only for the shared
combinatorial grid / `PLANET_PARAMS`). Keep `pipeline/run_sweep.py` — it is not legacy.
