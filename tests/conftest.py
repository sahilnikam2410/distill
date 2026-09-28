import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "plugins" / "distill" / "skills" / "distill"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def meter(monkeypatch):
    """token_meter forced onto its dependency-free heuristic, for stable counts."""
    monkeypatch.setitem(sys.modules, "tiktoken", None)
    return _load("token_meter", SKILL_DIR / "scripts" / "token_meter.py")


@pytest.fixture
def build_skill():
    return _load("build_skill", ROOT / "scripts" / "build_skill.py")
