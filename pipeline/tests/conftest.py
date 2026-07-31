"""Put the repo root and pipeline/ on sys.path so tests can import the packages."""
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve()
_PIPELINE = _HERE.parents[1]          # pipeline/  (photoring/, exorings/, geotrans/)
_REPO = _PIPELINE.parent
for _p in (str(_PIPELINE), str(_REPO)):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: full nested-sampling regression (~1 min)"
    )
