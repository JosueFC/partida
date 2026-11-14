# ADR-0001: Toolchain choices

- **Status:** Accepted
- **Date:** 2026-11-13

## Context

Partida is a solo, open-source project. It classifies product descriptions into HS/HTS tariff codes with
calibrated confidence, conformal prediction sets and abstention, and it must run in the browser. Three
constraints shape the toolchain:

1. **Cost must stay $0.** Everything runs locally or on free tiers (GitHub Actions on a public repo,
   open models, in-browser inference).
2. **Trustworthy numbers.** Calibration and conformal guarantees are only meaningful if train, calibration
   and test data are cleanly separated, so tests (especially leakage tests) are first-class.
3. **The author develops on Windows with Python 3.13.2** and is a data analyst, so the setup should be
   plain, well documented and reproducible with a handful of commands.

The planned ML stack (sentence-transformers, rank_bm25, scikit-learn, LightGBM) has compiled
dependencies whose wheel availability for the newest Python releases can lag. That has not been
verified yet.

## Decision

- **Layout:** `src/` layout (`src/partida/`), with tests in `tests/{unit,data,leakage,parity,regression,fixtures}`.
  The src layout forces tests to import the installed package, which catches packaging mistakes early.
- **Packaging:** `pyproject.toml` only, with `hatchling` as build backend. The version lives in one place,
  `src/partida/__init__.py` (`__version__`), and hatch reads it dynamically.
- **Python:** `requires-python = ">=3.11"`; CI will test 3.11 to 3.13 once it exists.
- **Dependencies:** the scaffold has **no runtime dependencies**. ML libraries are added one at a time
  in later changes, each verified to install on the author's Python before it is pinned.
  Developer tools live in a `[dev]` extra: pytest, pytest-cov, hypothesis, ruff, mypy, pre-commit.
- **Tests:** pytest with `--strict-markers --strict-config` and `--import-mode=importlib`, so test files in
  different folders may share a name. Hypothesis is used for property-based tests.
- **Lint, format, types:** ruff for both linting and formatting (line length 100); mypy in `strict` mode
  over `src` and `tests`.
- **Pre-commit:** local hooks that call the tools in the active virtual environment, so versions always
  match `[dev]` and no hook revisions need pinning separately.
- **Git hygiene:** `.gitignore` ignores `/data/` (anchored to the repo root so `src/partida/data/` and
  `tests/data/` remain tracked), virtual environments and notebook checkpoints.
- **Environment:** a plain `venv` in `.venv/` and an editable install (`pip install -e ".[dev]"`).

## Consequences

- **Easier:** one command installs everything needed to develop; one source of truth for the version;
  type errors and leakage mistakes are caught before they reach the metrics.
- **Harder:** strict mypy adds annotation work, especially around numpy, pandas and scikit-learn, which
  may need per-module relaxations later.
- **Version bumps:** because the installed metadata is generated at install time, after editing
  `__version__` you must re-run `python -m pip install -e ".[dev]"` for `importlib.metadata` to agree.
  A smoke test checks this.
- **Risk:** the newest Python may lack wheels for part of the ML stack. If so, the fallback is to run
  development on Python 3.12 (a one-line venv change) and keep `requires-python` as is.
- **Deferred:** CI (GitHub Actions), the ML dependencies, a license choice and the data pipeline are
  separate changes and will get their own ADRs where a real decision is involved.
- **Revisit** this ADR if the dev toolchain becomes a drag, for example if strict mypy slows progress
  more than it protects.
