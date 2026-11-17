"""
Shared helpers for the test suite.

Most course examples are scripts, not libraries: their code runs as soon as the file
is loaded. These fixtures run them safely:
- inside a temporary folder that holds a COPY of the script's data/ folder,
  so tests never overwrite files in the repo
- with input() replaced by canned answers
- with network calls replaced by fakes (see FakeResponse), so tests are fast,
  offline and repeatable

Run all tests from the repo root with:  python -m pytest
"""
import importlib.util
import io
import runpy
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


class FakeResponse:
    """Stands in for requests.Response, so tests never touch the network."""

    def __init__(self, text="", status_code=200, json_data=None, content=b""):
        self.text = text
        self.status_code = status_code
        self.reason = "OK" if status_code < 400 else "Error"
        self._json = json_data
        self.raw = io.BytesIO(content)  # For stream=True downloads

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            import requests
            raise requests.HTTPError(f"{self.status_code} {self.reason}", response=self)


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """A temporary working folder. tmp_path/work is used so "../" paths stay inside tmp_path."""
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    return work


def _prepare(script: Path, work: Path, files: dict[str, str] | None, remove: list[str] | None):
    """Copy the script's data/ folder into the work folder, then apply test-specific changes."""
    data = script.parent / "data"
    if data.is_dir():
        shutil.copytree(data, work / "data")
    else:
        (work / "data").mkdir()
    for name, content in (files or {}).items():
        path = work / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    for name in remove or []:
        path = work / name
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


@pytest.fixture
def run_script(workdir, monkeypatch):
    """Run a script as if from the command line (`python script.py`) and return its variables.

    run_script("examples/example_1_review.py", inputs=["25"], files={...}, remove=[...])
    """
    def _run(relative_path, inputs=(), files=None, remove=None):
        script = ROOT / relative_path
        _prepare(script, workdir, files, remove)
        answers = iter(inputs)
        monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
        return runpy.run_path(str(script), run_name="__main__")
    return _run


@pytest.fixture
def load_module(workdir, monkeypatch):
    """Import a file as a module, WITHOUT running its `if __name__ == "__main__":` block.

    Returns the module, so tests can call its functions: load_module("...").encrypt("abc", 1)
    """
    def _load(relative_path, files=None, remove=None):
        script = ROOT / relative_path
        _prepare(script, workdir, files, remove)
        name = "course_" + "_".join(script.relative_to(ROOT).with_suffix("").parts)
        spec = importlib.util.spec_from_file_location(name, script)
        module = importlib.util.module_from_spec(spec)
        monkeypatch.setitem(sys.modules, name, module)  # Removed again after the test
        spec.loader.exec_module(module)
        return module
    return _load
