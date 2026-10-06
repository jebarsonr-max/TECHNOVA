# TECHNOVA - Localhost Startup Script (PowerShell)
# Usage: .\start.ps1

$PROJECT_ROOT = $PSScriptRoot
$VENV_PYTHON  = Join-Path $PROJECT_ROOT "venv\Scripts\python.exe"
$NODE_DIR     = "C:\Users\Acer\AppData\Local\node_portable\node-v20.18.0-win-x64"

# Add portable Node to PATH for this session
$env:PATH = "$NODE_DIR;" + $env:PATH
$env:PYTHONIOENCODING = "utf-8"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  TECHNOVA - Proof-Carrying Data Analyst" -ForegroundColor Cyan
Write-Host "  Starting localhost development environment..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ── Start Backend ─────────────────────────────────────────────
Write-Host "[1/2] Starting FastAPI backend on http://localhost:8000 ..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    param($root, $python)
    Set-Location $root
    $env:PYTHONIOENCODING = "utf-8"
    & $python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
} -ArgumentList $PROJECT_ROOT, $VENV_PYTHON

# Wait for backend to be ready
Write-Host "   Waiting for backend to start..." -ForegroundColor Gray
$maxWait = 30
$waited  = 0
do {
    Start-Sleep -Seconds 1
    $waited++
    try {
        $resp = Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        Write-Host "   Backend READY (HTTP $($resp.StatusCode))" -ForegroundColor Green
        break
    } catch { }
} while ($waited -lt $maxWait)

if ($waited -ge $maxWait) {
    Write-Host "   WARNING: Backend did not respond within $maxWait seconds." -ForegroundColor Red
}

# ── Start Frontend ────────────────────────────────────────────
Write-Host ""
Write-Host "[2/2] Starting Vite frontend on http://localhost:5173 ..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    param($frontendDir, $nodePath)
    $env:PATH = "$nodePath;" + $env:PATH
    Set-Location $frontendDir
    npm run dev
} -ArgumentList (Join-Path $PROJECT_ROOT "frontend"), $NODE_DIR

Start-Sleep -Seconds 4

# ── Summary ───────────────────────────────────────────────────
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  TECHNOVA is running!" -ForegroundColor Green
Write-Host ""
Write-Host "  Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "  Press Ctrl+C to stop all services." -ForegroundColor Gray
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

try {
    # Keep running until Ctrl+C
    while ($true) {
        Start-Sleep -Seconds 5
        $be = Get-Job $backendJob.Id  -ErrorAction SilentlyContinue
        $fe = Get-Job $frontendJob.Id -ErrorAction SilentlyContinue
        if ($be.State -eq "Failed") { Write-Host "[!] Backend job failed. Check logs." -ForegroundColor Red }
        if ($fe.State -eq "Failed") { Write-Host "[!] Frontend job failed. Check logs." -ForegroundColor Red }
    }
} finally {
    Write-Host ""
    Write-Host "Stopping services..." -ForegroundColor Yellow
    Stop-Job  $backendJob.Id  -ErrorAction SilentlyContinue
    Stop-Job  $frontendJob.Id -ErrorAction SilentlyContinue
    Remove-Job $backendJob.Id  -ErrorAction SilentlyContinue
    Remove-Job $frontendJob.Id -ErrorAction SilentlyContinue
    Write-Host "All services stopped." -ForegroundColor Green
}
