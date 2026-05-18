$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ProjectRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtual environment not found. Run: python -m venv .venv; .\.venv\Scripts\python -m pip install -r requirements.txt; .\.venv\Scripts\python -m pip install 'PyQt6>=6.7'"
}

Set-Location $ProjectRoot
& $VenvPython -m maptoposter_gui.app
