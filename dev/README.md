# PRisma Dev Directory

This directory contains parallel execution scripts to perform performance tests and configuration sweeps without affecting the original scripts in the `pipeline/` directory.

Two sweep configurations are included:
1. **`run_sweep_single.py`**: Configuration with **a single case** (Kepler-51 d). Useful for quick performance tests.
2. **`run_sweep_full.py`**: The full sweep (both planets, all free variable scenarios, etc.), resulting in 96 retrievals per model.

## How to Run the Performance Tests (Comparison)

If you only want to measure and compare the times between both models for the base configuration we defined, you can execute the `single` configuration independently by dynamically injecting the `--model` flag:

```bash
# Enter the dev directory
cd dev

# 1. Run the quick exorings retrieval with 6 processors (runs in the foreground)
bash run_sweep_parallel.sh --config run_sweep_single --model exorings --n-procs 6

# 2. Run the quick geotrans retrieval with 6 processors (runs in the foreground)
bash run_sweep_parallel.sh --config run_sweep_single --model geotrans --n-procs 6
```

*(Tip: If you have already run these before and want to overwrite the existing `.npz` files, append `--force` to the commands above)*

Once both finish, the `.npz` files will be saved in `dev/kepler_51/results/`. To visualize the comparison, open and execute all cells in the notebook:
- **`PRisma-ExoringsVsGeotransRetrieval.ipynb`** (This will print the comparative times and plot the Corner Plots and PPCs).

## How to Run the Full Sweep

To run the exhaustive 96 retrievals for the `geotrans` model for your system:

```bash
cd dev
nohup bash run_sweep_parallel.sh --config run_sweep_full --model geotrans --n-procs 6 > full_sweep.log 2>&1 &
```

*(Tip: Monitor the progress of the full sweep with `tail -f full_sweep.log`)*

This will safely save all results in `dev/kepler_51/results/` without messing up the paper data in your main pipeline.
