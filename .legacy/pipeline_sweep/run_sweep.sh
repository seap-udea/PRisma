#!/usr/bin/env bash
# =============================================================================
# run_sweep.sh — Photo-Ring pipeline · sweep launcher
# =============================================================================
# Usage:
#   bash run_sweep.sh [emcee|dynesty|both] [--case CASE] [--dry-run]
#
# Examples:
#   bash run_sweep.sh                       # dynesty, 32 configs, case kepler_51
#   bash run_sweep.sh dynesty               # nested sampling only (same as default)
#   bash run_sweep.sh dynesty --dry-run     # preview the 32 run tags
#   bash run_sweep.sh both --case my_planet # dynesty + emcee on another case
#
# Results are written only under pipeline/<case>/results/ (gitignored).
# papers/<case>/reference_runs/ is never touched by this launcher.
# =============================================================================

set -euo pipefail

SAMPLER="${1:-dynesty}"
if [[ "${SAMPLER}" == emcee || "${SAMPLER}" == dynesty || "${SAMPLER}" == both ]]; then
    shift || true
else
    # No sampler positional; treat all args as flags and keep the default.
    SAMPLER="dynesty"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SWEEP_PY="${SCRIPT_DIR}/run_sweep.py"

# Prefer the repo virtualenv so papermill / dynesty / the jupyter kernel match.
if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
    PYTHON="${REPO_ROOT}/.venv/bin/python"
else
    PYTHON="python3"
fi

if ! "${PYTHON}" -c "import papermill" &>/dev/null; then
    echo "[setup] Installing papermill into ${PYTHON}..."
    "${PYTHON}" -m pip install papermill --quiet
fi

if [[ ! -f "${SWEEP_PY}" ]]; then
    echo "[ERROR] run_sweep.py not found in ${SCRIPT_DIR}"
    exit 1
fi

echo ""
echo "================================================================"
echo "  Photo-Ring sweep — $(date '+%Y-%m-%d %H:%M:%S')  |  sampler: ${SAMPLER}"
echo "  Python: ${PYTHON}"
echo "================================================================"
echo ""

cd "${SCRIPT_DIR}"
exec "${PYTHON}" "${SWEEP_PY}" --sampler "${SAMPLER}" "$@"
