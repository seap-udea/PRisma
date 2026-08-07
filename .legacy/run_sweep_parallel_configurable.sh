#!/usr/bin/env bash
# =============================================================================
# run_sweep_parallel_configurable.sh — dynesty sweep with configurable grid
# =============================================================================
# Usage:
#   bash run_sweep_parallel_configurable.sh [--n-procs N] [--jobs J] [--dry-run] [--case CASE] [--config CONFIG_FILE] [--force]
#
# Examples:
#   bash run_sweep_parallel_configurable.sh --dry-run
#   bash run_sweep_parallel_configurable.sh --n-procs 6 --config run_config_explore-radius.py

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIPELINE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${PIPELINE_DIR}/.." && pwd)"
RUNNER="${SCRIPT_DIR}/run_sweep_parallel_configurable.py"

if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
    PYTHON="${REPO_ROOT}/.venv/bin/python"
else
    PYTHON="python3"
fi

echo ""
echo "================================================================"
echo "  Photo-Ring CONFIGURABLE PARALLEL sweep — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Python: ${PYTHON}"
echo "================================================================"
echo ""

cd "${PIPELINE_DIR}"
exec "${PYTHON}" "${RUNNER}" "$@"
