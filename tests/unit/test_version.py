"""Smoke tests proving the toolchain and the editable install work."""

from __future__ import annotations

import re
from importlib.metadata import version

import partida

SEMVER = re.compile(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?")


def test_version_is_semver_string() -> None:
    assert isinstance(partida.__version__, str)
    assert SEMVER.fullmatch(partida.__version__) is not None


def test_version_matches_installed_metadata() -> None:
    assert version("partida") == partida.__version__
