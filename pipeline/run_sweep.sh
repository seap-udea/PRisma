#!/usr/bin/env bash
# =============================================================================
# run_sweep.sh — Photo-Ring pipeline · sweep launcher
# =============================================================================
# Usage:
#   bash run_sweep.sh [emcee|dynesty|both] [--case CASE] [--dry-run]
#
# Examples:
#   bash run_sweep.sh                       # both samplers, default case (kepler_51)
#   bash run_sweep.sh dynesty               # nested sampling only
#   bash run_sweep.sh emcee --dry-run       # preview configurations without running
#   bash run_sweep.sh both --case my_planet # sweep a different case directory
# =============================================================================

set -euo pipefail

SAMPLER="${1:-both}"
shift || true          # remaining args (--case ..., --dry-run) pass through

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SWEEP_PY="${SCRIPT_DIR}/run_sweep.py"

if ! python3 -c "import papermill" &>/dev/null; then
    echo "[setup] Installing papermill..."
    pip install papermill --quiet
fi

if [[ ! -f "${SWEEP_PY}" ]]; then
    echo "[ERROR] run_sweep.py not found in ${SCRIPT_DIR}"
    exit 1
fi

echo ""
echo "================================================================"
echo "  Photo-Ring sweep — $(date '+%Y-%m-%d %H:%M:%S')  |  sampler: ${SAMPLER}"
echo "================================================================"
echo ""

cd "${SCRIPT_DIR}"
python3 "${SWEEP_PY}" --sampler "${SAMPLER}" "$@"
