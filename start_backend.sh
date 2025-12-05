#!/bin/bash
# Backend服务启动脚本

echo "========================================="
echo "  歌颜随动 - Backend API 服务启动"
echo "========================================="
echo ""

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到Python环境"
    exit 1
fi

echo "✅ Python版本: $(python --version)"

# 检查是否安装了依赖
if ! python -c "import fastapi" 2>/dev/null; then
    echo "⚠️  检测到依赖未安装，正在安装..."
    pip install -q -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
fi

# 创建必要的目录
mkdir -p data/uploads
mkdir -p data/expressions
mkdir -p logs
echo "✅ 数据目录已创建"

# 检查端口是否被占用
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  端口8000已被占用，正在尝试关闭..."
    PID=$(lsof -ti:8000)
    if [ ! -z "$PID" ]; then
        kill $PID
        sleep 2
    fi
fi

echo ""
echo "🚀 启动Backend API服务..."
echo "   - 服务地址: http://localhost:8000"
echo "   - API文档: http://localhost:8000/docs"
echo "   - 健康检查: http://localhost:8000/health"
echo ""

# 启动服务
python -m backend.api.main
