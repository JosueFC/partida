# Partida

Open-source, bilingual (English/Spanish) HS/HTS tariff-code classifier that runs in the browser.

Given a product description it will suggest HS codes (6-digit first, 10-digit HTS as a stretch) with a
calibrated confidence, a conformal prediction set, cited CBP rulings, and a "send to a broker"
abstention when it is not sure.

Status: scaffold only. See `docs/adr/` for design decisions.

## Development setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Checks

```powershell
ruff check .
ruff format --check .
mypy
pytest
```
