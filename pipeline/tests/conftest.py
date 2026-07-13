"""Put the repo root and pipeline/ on sys.path so tests can import the packages."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_PIPELINE = _HERE.parents[1]          # pipeline/
_REPO = _PIPELINE.parent              # repo root (exorings/, geotrans/)
for _p in (str(_REPO), str(_PIPELINE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
