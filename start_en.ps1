# Geyan Suidong Startup Script
Write-Host "Starting Geyan Suidong Live2D System..." -ForegroundColor Cyan
Write-Host ""

# Set working directory
$workdir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $workdir
Write-Host "Working Directory: $workdir" -ForegroundColor Blue

# Check Python
Write-Host "Checking Python environment..." -ForegroundColor Yellow
$pythonExe = "E:/workspace/geyan-suidong-/.conda/python.exe"
if (Test-Path $pythonExe) {
    $pythonCheck = & $pythonExe --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python environment: $pythonCheck" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Python execution failed" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "ERROR: Python not found at $pythonExe" -ForegroundColor Red
    Write-Host "Please run conda environment setup first" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check and install dependencies
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$streamlitCheck = & $pythonExe -m pip show streamlit 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    & $pythonExe -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host "Dependencies check completed" -ForegroundColor Green

# Start backend
Write-Host ""
Write-Host "Starting backend API service (port 8000)..." -ForegroundColor Yellow
$backendProcess = Start-Process -FilePath $pythonExe -ArgumentList "-m", "uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -PassThru -WindowStyle Normal
if ($backendProcess) {
    Write-Host "Backend process started successfully (PID: $($backendProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "ERROR: Backend startup failed" -ForegroundColor Red
}

# Wait for backend
Write-Host "Waiting for backend service..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start frontend
Write-Host ""
Write-Host "Starting frontend web interface (port 8503)..." -ForegroundColor Yellow
$frontendProcess = Start-Process -FilePath $pythonExe -ArgumentList "-m", "streamlit", "run", "app.py", "--server.port", "8503" -PassThru -WindowStyle Normal
if ($frontendProcess) {
    Write-Host "Frontend process started successfully (PID: $($frontendProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "ERROR: Frontend startup failed" -ForegroundColor Red
}

# Display access info
Write-Host ""
Write-Host "System startup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend URL: http://localhost:8503" -ForegroundColor Cyan
Write-Host "Backend API docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Backend health check: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""

# Wait and check services
Write-Host "Waiting for services to fully start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Checking service status..." -ForegroundColor Yellow

# Check backend
$backendHealthy = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "Backend API: Running normally" -ForegroundColor Green
        $backendHealthy = $true
    }
} catch {
    Write-Host "Backend API: Starting or error" -ForegroundColor Yellow
}

# Check frontend
$frontendHealthy = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8503" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "Frontend Web: Running normally" -ForegroundColor Green
        $frontendHealthy = $true
    }
} catch {
    Write-Host "Frontend Web: Starting or error" -ForegroundColor Yellow
}

# Show control options
Write-Host ""
Write-Host "Control Options:" -ForegroundColor Cyan
Write-Host "  - Press [Enter] to exit and stop all services"
Write-Host "  - Type 'open' to open frontend page"
Write-Host "  - Type 'status' to view service status"
Write-Host "  - Type 'logs' to view log directory"
Write-Host ""

# Save process IDs for cleanup
$script:ProcessesToKill = @()
if ($backendProcess) { $script:ProcessesToKill += $backendProcess.Id }
if ($frontendProcess) { $script:ProcessesToKill += $frontendProcess.Id }

# Wait for user input
do {
    $input = Read-Host "Enter command (Press Enter to exit)"
    
    switch ($input.ToLower()) {
        "open" {
            Write-Host "Opening frontend page..." -ForegroundColor Cyan
            Start-Process "http://localhost:8503"
        }
        "status" {
            Write-Host ""
            Write-Host "Current service status:" -ForegroundColor Yellow
            if ($backendProcess -and !$backendProcess.HasExited) {
                Write-Host "Backend process (PID $($backendProcess.Id)): Running" -ForegroundColor Green
            } else {
                Write-Host "Backend process: Stopped" -ForegroundColor Red
            }
            
            if ($frontendProcess -and !$frontendProcess.HasExited) {
                Write-Host "Frontend process (PID $($frontendProcess.Id)): Running" -ForegroundColor Green
            } else {
                Write-Host "Frontend process: Stopped" -ForegroundColor Red
            }
            Write-Host ""
        }
        "logs" {
            Write-Host "Log locations:" -ForegroundColor Yellow
            Write-Host "- Backend logs: Check backend console window"
            Write-Host "- Frontend logs: Check frontend console window"
            Write-Host "- Application logs: $workdir\logs\" -ForegroundColor Cyan
        }
        "" {
            break
        }
        default {
            Write-Host "Unknown command: $input" -ForegroundColor Yellow
        }
    }
} while ($true)

# Cleanup resources
Write-Host ""
Write-Host "Stopping all services..." -ForegroundColor Red

# Stop processes
foreach ($pid in $script:ProcessesToKill) {
    try {
        $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "Stopping process PID $pid ..." -ForegroundColor Yellow
            $process.Kill()
            $process.WaitForExit(5000)  # Wait max 5 seconds
        }
    } catch {
        Write-Host "Warning: Cannot stop process PID $pid" -ForegroundColor Yellow
    }
}

# Additional cleanup (force)
Write-Host "Performing cleanup..." -ForegroundColor Yellow
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*" -or $_.CommandLine -like "*streamlit*"
} | ForEach-Object {
    try {
        Write-Host "Force stopping: $($_.ProcessName) (PID $($_.Id))" -ForegroundColor Yellow
        $_.Kill()
    } catch {
        # Ignore errors
    }
}

Write-Host ""
Write-Host "System completely stopped" -ForegroundColor Green
Write-Host "Thank you for using Geyan Suidong!" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"