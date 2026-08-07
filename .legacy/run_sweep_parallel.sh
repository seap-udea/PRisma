#!/usr/bin/env bash
# =============================================================================
# run_sweep_parallel.sh — dynesty sweep without papermill (fork pool OK)
# =============================================================================
# Usage:
#   bash run_sweep_parallel.sh [--config CONFIG] [--model MODEL] [--n-procs N] [--jobs J] [--dry-run] [--force] [--case CASE]
#
# Examples:
#   bash run_sweep_parallel.sh --dry-run
#   bash run_sweep_parallel.sh --config run_sweep_single --model exorings --n-procs 6
#   bash run_sweep_parallel.sh --config run_sweep_single --model geotrans --n-procs 6
#   bash run_sweep_parallel.sh --config run_sweep_full --model geotrans --n-procs 6
#   bash run_sweep_parallel.sh --jobs 2 --n-procs 6
#
# Pause / resume:
#   bash stop_sweep_parallel.sh                             # stop current sweep
#   nohup bash run_sweep_parallel.sh --n-procs 6 \
#       > sweep_parallel_96.log 2>&1 &                      # resume (skips .npz)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUNNER="${SCRIPT_DIR}/run_sweep_parallel.py"

if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
    PYTHON="${REPO_ROOT}/.venv/bin/python"
else
    PYTHON="python3"
fi

echo ""
echo "================================================================"
echo "  Photo-Ring PARALLEL sweep — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Python: ${PYTHON}"
echo "================================================================"
echo ""

cd "${SCRIPT_DIR}"
exec "${PYTHON}" "${RUNNER}" "$@"
