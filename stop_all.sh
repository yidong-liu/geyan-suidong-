#!/bin/bash
# 停止所有服务脚本

echo "========================================="
echo "  停止歌颜随动服务"
echo "========================================="
echo ""

# 从PID文件读取并停止
if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "⏹️  停止Backend服务 (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        sleep 2
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill -9 $BACKEND_PID
        fi
        echo "✅ Backend服务已停止"
    else
        echo "ℹ️  Backend服务未运行"
    fi
    rm -f logs/backend.pid
fi

if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "⏹️  停止Frontend服务 (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        sleep 2
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill -9 $FRONTEND_PID
        fi
        echo "✅ Frontend服务已停止"
    else
        echo "ℹ️  Frontend服务未运行"
    fi
    rm -f logs/frontend.pid
fi

# 查找并停止任何残留的进程
echo ""
echo "🔍 检查残留进程..."

BACKEND_PIDS=$(ps aux | grep "python -m backend.api.main" | grep -v grep | awk '{print $2}')
if [ ! -z "$BACKEND_PIDS" ]; then
    echo "发现Backend残留进程: $BACKEND_PIDS"
    for PID in $BACKEND_PIDS; do
        kill $PID 2>/dev/null
    done
fi

FRONTEND_PIDS=$(ps aux | grep "streamlit run app.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$FRONTEND_PIDS" ]; then
    echo "发现Frontend残留进程: $FRONTEND_PIDS"
    for PID in $FRONTEND_PIDS; do
        kill $PID 2>/dev/null
    done
fi

echo ""
echo "✅ 所有服务已停止"
