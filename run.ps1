$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "=== THPTQG Trends - Chay pipeline ===" -ForegroundColor Cyan
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "Tao virtualenv lan dau..." -ForegroundColor Yellow
    python -m venv .venv
    & .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
} else {
    & .\.venv\Scripts\Activate.ps1
}
python scripts/run_all.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "`nXong! Mo README.md va outputs/figures/" -ForegroundColor Green
