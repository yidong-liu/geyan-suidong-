#!/bin/bash
# 完整系统启动脚本 - 同时启动Backend和Frontend

echo "========================================="
echo "  歌颜随动 - 完整系统启动"
echo "========================================="
echo ""

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到Python环境"
    exit 1
fi

echo "✅ Python环境: $(python --version)"

# 创建必要的目录
mkdir -p data/uploads data/expressions logs
echo "✅ 数据目录已创建"

# 检查并安装依赖
echo ""
echo "📦 检查依赖..."
if ! python -c "import fastapi, streamlit" 2>/dev/null; then
    echo "⚠️  安装缺失的依赖..."
    pip install -q -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已安装"
fi

# 启动Backend
echo ""
echo "🚀 启动Backend服务..."
python -m backend.api.main > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# 等待Backend启动
echo "   等待Backend启动..."
for i in {1..10}; do
    sleep 1
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "   ✅ Backend启动成功 (http://localhost:8000)"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "   ❌ Backend启动超时"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
done

# 启动Frontend
echo ""
echo "🚀 启动Frontend服务..."
python -m streamlit run app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    > logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

# 等待Frontend启动
echo "   等待Frontend启动..."
for i in {1..10}; do
    sleep 1
    if curl -s http://localhost:8501/_stcore/health > /dev/null 2>&1; then
        echo "   ✅ Frontend启动成功 (http://localhost:8501)"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "   ❌ Frontend启动超时"
        kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
        exit 1
    fi
done

# 保存PID到文件
echo $BACKEND_PID > logs/backend.pid
echo $FRONTEND_PID > logs/frontend.pid

echo ""
echo "================================================"
echo "  🎉 系统启动完成！"
echo "================================================"
echo ""
echo "📡 服务信息:"
echo "  - Frontend Web界面: http://localhost:8501"
echo "  - Backend API文档:  http://localhost:8000/docs"
echo "  - Backend健康检查:  http://localhost:8000/health"
echo ""
echo "📝 日志文件:"
echo "  - Backend日志: logs/backend.log"
echo "  - Frontend日志: logs/frontend.log"
echo ""
echo "⏹️  停止服务:"
echo "  - 停止所有: ./stop_all.sh"
echo "  - 或使用: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "💡 提示: Frontend会自动连接到Backend API"
echo ""
