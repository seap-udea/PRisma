#!/usr/bin/env bash
# =============================================================================
# stop_sweep_parallel.sh — pause the parallel dynesty sweep
# =============================================================================
# Sends SIGTERM to the run_sweep_parallel_configurable.py process tree. Completed runs are
# already saved as <tag>.npz under pipeline/<case>/results/ and will be
# SKIPPED when you resume. The run that was in progress (no .npz yet) will
# restart from scratch — that is expected.
#
# Usage:
#   bash stop_sweep_parallel.sh           # stop
#   bash stop_sweep_parallel.sh --status  # show running PIDs only
#
# Resume later (same flags you used to start):
#   nohup bash run_sweep_parallel_configurable.sh --n-procs 6 > sweep_parallel_96.log 2>&1 &
# =============================================================================

set -euo pipefail

STATUS_ONLY=0
if [[ "${1:-}" == "--status" ]]; then
    STATUS_ONLY=1
fi

# Match the Python runner, not this shell script / editors.
PIDS="$(pgrep -f 'run_sweep_parallel_configurable\.py' || true)"

if [[ -z "${PIDS}" ]]; then
    echo "No run_sweep_parallel_configurable.py process found."
    exit 0
fi

echo "Found run_sweep_parallel_configurable.py PID(s):"
ps -o pid,ppid,etime,command -p $(echo "${PIDS}" | tr '\n' ',' | sed 's/,$//') 2>/dev/null || true
echo ""

if [[ "${STATUS_ONLY}" -eq 1 ]]; then
    exit 0
fi

echo "Stopping (SIGTERM)…"
# Kill each matching PID; children of the pool usually exit with the parent.
while read -r pid; do
    [[ -z "${pid}" ]] && continue
    kill -TERM "${pid}" 2>/dev/null || true
done <<< "${PIDS}"

sleep 2

LEFT="$(pgrep -f 'run_sweep_parallel_configurable\.py' || true)"
if [[ -n "${LEFT}" ]]; then
    echo "Still alive — sending SIGKILL to: ${LEFT}"
    while read -r pid; do
        [[ -z "${pid}" ]] && continue
        kill -KILL "${pid}" 2>/dev/null || true
    done <<< "${LEFT}"
fi

echo "Stopped. Resume with the same launch command; finished .npz runs are skipped."
