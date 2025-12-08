# 格焉随动启动脚本
Write-Host "🎭 启动格焉随动 Live2D系统..." -ForegroundColor Cyan
Write-Host ""

# 检查Python环境
Write-Host "🔍 检查Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python环境: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python command failed"
    }
} catch {
    Write-Host "❌ 错误: 未找到Python环境" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 检查依赖包
Write-Host ""
Write-Host "📦 检查依赖包..." -ForegroundColor Yellow
try {
    $result = pip show streamlit 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 依赖包已安装" -ForegroundColor Green
    } else {
        throw "Streamlit not found"
    }
} catch {
    Write-Host "📥 安装依赖包..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# 启动后端服务
Write-Host ""
Write-Host "🚀 启动后端API服务 (端口 8000)..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
}

Write-Host "⏳ 等待后端启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# 启动前端服务
Write-Host ""
Write-Host "🌐 启动前端Web界面 (端口 8503)..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    streamlit run app.py --server.port 8503 --server.headless false
}

Write-Host ""
Write-Host "✅ 系统启动完成！" -ForegroundColor Green
Write-Host "📱 前端访问地址: http://localhost:8503" -ForegroundColor Cyan
Write-Host "📖 后端API文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

# 检查服务状态
Write-Host "📊 检查服务状态..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

try {
    $backendTest = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ 后端服务: 正常运行" -ForegroundColor Green
} catch {
    Write-Host "⚠️ 后端服务: 启动中或异常" -ForegroundColor Yellow
}

try {
    $frontendTest = Invoke-WebRequest -Uri "http://localhost:8503" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ 前端服务: 正常运行" -ForegroundColor Green
} catch {
    Write-Host "⚠️ 前端服务: 启动中或异常" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎮 控制选项:" -ForegroundColor Cyan
Write-Host "  - 按 [Enter] 退出所有服务"
Write-Host "  - 按 [B] 查看后端日志"
Write-Host "  - 按 [F] 查看前端日志"
Write-Host "  - 按 [S] 查看服务状态"
Write-Host ""

# 等待用户输入
do {
    $input = Read-Host "请输入选项"
    
    switch ($input.ToLower()) {
        "b" {
            Write-Host "📋 后端日志:" -ForegroundColor Yellow
            Receive-Job -Job $backendJob
        }
        "f" {
            Write-Host "📋 前端日志:" -ForegroundColor Yellow
            Receive-Job -Job $frontendJob
        }
        "s" {
            Write-Host "📊 服务状态:" -ForegroundColor Yellow
            Write-Host "后端Job状态: $($backendJob.State)" -ForegroundColor Cyan
            Write-Host "前端Job状态: $($frontendJob.State)" -ForegroundColor Cyan
        }
        "" {
            break
        }
    }
} while ($true)

# 清理资源
Write-Host ""
Write-Host "🛑 停止所有服务..." -ForegroundColor Red
Stop-Job -Job $backendJob, $frontendJob
Remove-Job -Job $backendJob, $frontendJob

# 强制结束进程（如果需要）
Write-Host "🧹 清理进程..." -ForegroundColor Yellow
try {
    Get-Process | Where-Object {$_.ProcessName -like "*python*" -and $_.CommandLine -like "*uvicorn*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Get-Process | Where-Object {$_.ProcessName -like "*python*" -and $_.CommandLine -like "*streamlit*"} | Stop-Process -Force -ErrorAction SilentlyContinue
} catch {
    # 忽略清理错误
}

Write-Host "✅ 系统已停止" -ForegroundColor Green
Write-Host ""
Read-Host "按回车键退出"