"""The flat agents/skills layer and the docs' paths must match the repo.

These are the same checks CI runs as separate steps; running them under
pytest means a local `pytest tests/` catches the drift before a PR is opened.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(script, *args):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args],
                          capture_output=True, text=True, cwd=ROOT)


def test_flat_layer_matches_plugins():
    r = _run("consolidate-adversarial.py", "--check")
    assert r.returncode == 0, r.stdout + r.stderr


def test_doc_paths_resolve():
    r = _run("check-doc-refs.py")
    assert r.returncode == 0, r.stdout + r.stderr


def test_structure_validates():
    r = _run("validate.py", "--root", str(ROOT))
    assert r.returncode == 0, r.stdout + r.stderr
