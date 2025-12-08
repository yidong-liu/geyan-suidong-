@echo off
echo 启动格焉随动 Live2D系统...
echo.

echo 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境
    pause
    exit /b 1
)

echo.
echo 检查依赖包...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo 安装依赖包...
    pip install -r requirements.txt
)

echo.
echo 启动后端API服务 (端口 8000)...
start cmd /k "cd /d %~dp0 && python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload"

echo 等待后端启动...
timeout /t 3

echo.
echo 启动前端Web界面 (端口 8503)...
start cmd /k "cd /d %~dp0 && streamlit run app.py --server.port 8503 --server.headless false"

echo.
echo 系统启动完成！
echo 前端访问地址: http://localhost:8503
echo 后端API文档: http://localhost:8000/docs
echo.
echo 按任意键退出启动器...
pause >nul