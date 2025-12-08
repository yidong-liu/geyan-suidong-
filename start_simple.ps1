# 格焉随动简化启动脚本
Write-Host "🎭 启动格焉随动 Live2D系统..." -ForegroundColor Cyan
Write-Host ""

# 设置工作目录
$workdir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $workdir
Write-Host "📁 工作目录: $workdir" -ForegroundColor Blue

# 检查Python
Write-Host "🔍 检查Python环境..." -ForegroundColor Yellow
$pythonCheck = & python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 错误: 未找到Python环境" -ForegroundColor Red
    Write-Host "请确保Python已安装并添加到PATH环境变量" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}
Write-Host "✅ Python环境: $pythonCheck" -ForegroundColor Green

# 检查并安装依赖
Write-Host ""
Write-Host "📦 检查依赖包..." -ForegroundColor Yellow
$streamlitCheck = & pip show streamlit 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "📥 安装依赖包..." -ForegroundColor Yellow
    & pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 依赖包安装失败" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
}
Write-Host "✅ 依赖包检查完成" -ForegroundColor Green

# 启动后端
Write-Host ""
Write-Host "🚀 启动后端API服务 (端口 8000)..." -ForegroundColor Yellow
$backendProcess = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -PassThru -WindowStyle Normal
if ($backendProcess) {
    Write-Host "✅ 后端进程启动成功 (PID: $($backendProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "❌ 后端启动失败" -ForegroundColor Red
}

# 等待后端启动
Write-Host "⏳ 等待后端服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 启动前端
Write-Host ""
Write-Host "🌐 启动前端Web界面 (端口 8503)..." -ForegroundColor Yellow
$frontendProcess = Start-Process -FilePath "python" -ArgumentList "-m", "streamlit", "run", "app.py", "--server.port", "8503" -PassThru -WindowStyle Normal
if ($frontendProcess) {
    Write-Host "✅ 前端进程启动成功 (PID: $($frontendProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "❌ 前端启动失败" -ForegroundColor Red
}

# 显示访问信息
Write-Host ""
Write-Host "🎉 系统启动完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📱 前端访问地址: http://localhost:8503" -ForegroundColor Cyan
Write-Host "📖 后端API文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🩺 后端健康检查: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""

# 等待几秒后检查服务状态
Write-Host "⏳ 等待服务完全启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "📊 检查服务状态..." -ForegroundColor Yellow

# 检查后端
$backendHealthy = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ 后端API: 正常运行" -ForegroundColor Green
        $backendHealthy = $true
    }
} catch {
    Write-Host "⚠️ 后端API: 启动中或异常" -ForegroundColor Yellow
}

# 检查前端
$frontendHealthy = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8503" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ 前端Web: 正常运行" -ForegroundColor Green
        $frontendHealthy = $true
    }
} catch {
    Write-Host "⚠️ 前端Web: 启动中或异常" -ForegroundColor Yellow
}

# 显示控制选项
Write-Host ""
Write-Host "🎮 控制选项:" -ForegroundColor Cyan
Write-Host "  - 直接按 [Enter] 退出并停止所有服务"
Write-Host "  - 输入 'open' 打开前端页面"
Write-Host "  - 输入 'status' 查看服务状态"
Write-Host "  - 输入 'logs' 查看日志目录"
Write-Host ""

# 保存进程ID以便后续清理
$script:ProcessesToKill = @()
if ($backendProcess) { $script:ProcessesToKill += $backendProcess.Id }
if ($frontendProcess) { $script:ProcessesToKill += $frontendProcess.Id }

# 等待用户输入
do {
    $input = Read-Host "请输入命令 (直接按Enter退出)"
    
    switch ($input.ToLower()) {
        "open" {
            Write-Host "🌐 打开前端页面..." -ForegroundColor Cyan
            Start-Process "http://localhost:8503"
        }
        "status" {
            Write-Host ""
            Write-Host "📊 当前服务状态:" -ForegroundColor Yellow
            if ($backendProcess -and !$backendProcess.HasExited) {
                Write-Host "后端进程 (PID $($backendProcess.Id)): 运行中" -ForegroundColor Green
            } else {
                Write-Host "后端进程: 已停止" -ForegroundColor Red
            }
            
            if ($frontendProcess -and !$frontendProcess.HasExited) {
                Write-Host "前端进程 (PID $($frontendProcess.Id)): 运行中" -ForegroundColor Green
            } else {
                Write-Host "前端进程: 已停止" -ForegroundColor Red
            }
            Write-Host ""
        }
        "logs" {
            Write-Host "📋 日志位置:" -ForegroundColor Yellow
            Write-Host "- 后端日志: 查看后端控制台窗口"
            Write-Host "- 前端日志: 查看前端控制台窗口"
            Write-Host "- 应用日志: $workdir\logs\" -ForegroundColor Cyan
        }
        "" {
            break
        }
        default {
            Write-Host "❓ 未知命令: $input" -ForegroundColor Yellow
        }
    }
} while ($true)

# 清理资源
Write-Host ""
Write-Host "🛑 正在停止所有服务..." -ForegroundColor Red

# 停止进程
foreach ($pid in $script:ProcessesToKill) {
    try {
        $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "停止进程 PID $pid ..." -ForegroundColor Yellow
            $process.Kill()
            $process.WaitForExit(5000)  # 等待最多5秒
        }
    } catch {
        Write-Host "警告: 无法停止进程 PID $pid" -ForegroundColor Yellow
    }
}

# 额外清理 (强制)
Write-Host "🧹 执行清理..." -ForegroundColor Yellow
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*" -or $_.CommandLine -like "*streamlit*"
} | ForEach-Object {
    try {
        Write-Host "强制停止: $($_.ProcessName) (PID $($_.Id))" -ForegroundColor Yellow
        $_.Kill()
    } catch {
        # 忽略错误
    }
}

Write-Host ""
Write-Host "✅ 系统已完全停止" -ForegroundColor Green
Write-Host "感谢使用格焉随动！🎭" -ForegroundColor Cyan
Write-Host ""
Read-Host "按回车键退出"