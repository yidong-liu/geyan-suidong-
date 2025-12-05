#!/bin/bash
# Frontend服务启动脚本

echo "========================================="
echo "  歌颜随动 - Frontend Web应用启动"
echo "========================================="
echo ""

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到Python环境"
    exit 1
fi

echo "✅ Python版本: $(python --version)"

# 检查Streamlit是否安装
if ! python -c "import streamlit" 2>/dev/null; then
    echo "⚠️  检测到Streamlit未安装，正在安装..."
    pip install -q streamlit
    if [ $? -ne 0 ]; then
        echo "❌ Streamlit安装失败"
        exit 1
    fi
    echo "✅ Streamlit安装完成"
fi

# 检查backend是否运行
echo ""
echo "🔍 检查Backend服务..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend服务正在运行"
else
    echo "⚠️  Backend服务未运行"
    echo "   建议先启动backend服务: ./start_backend.sh"
    echo "   或者在另一个终端运行: python -m backend.api.main"
    echo ""
fi

echo ""
echo "🚀 启动Frontend应用..."
echo "   - 访问地址: http://localhost:8501"
echo "   - 按 Ctrl+C 停止服务"
echo ""
echo "================================================"
echo ""

# 启动Streamlit
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
