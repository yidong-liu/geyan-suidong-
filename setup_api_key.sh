#!/bin/bash
# API 配置助手脚本
# 帮助快速配置 OpenAI/Gemini API

set -e

echo "======================================"
echo "  歌颜随动 - API 配置助手"
echo "======================================"
echo ""

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，从示例创建..."
    cp .env.example .env
    echo "✓ .env 文件已创建"
fi

echo "请选择要配置的 AI 服务:"
echo ""
echo "1) Google Gemini (推荐，免费额度较高)"
echo "2) OpenAI (需付费 API key)"
echo "3) OpenAI 代理服务 (使用第三方代理)"
echo "4) 查看当前配置"
echo "5) 测试 API 连接"
echo "0) 退出"
echo ""
read -p "请输入选项 (0-5): " choice

case $choice in
    1)
        echo ""
        echo "配置 Google Gemini API"
        echo "----------------------"
        echo "1. 访问: https://makersuite.google.com/app/apikey"
        echo "2. 创建 API Key"
        echo ""
        read -p "请输入 Google API Key: " GOOGLE_KEY
        
        if [ -z "$GOOGLE_KEY" ]; then
            echo "✗ API Key 不能为空"
            exit 1
        fi
        
        # 更新 .env
        if grep -q "GOOGLE_API_KEY=" .env; then
            sed -i "s|GOOGLE_API_KEY=.*|GOOGLE_API_KEY=$GOOGLE_KEY|" .env
        else
            echo "GOOGLE_API_KEY=$GOOGLE_KEY" >> .env
        fi
        
        if grep -q "AI_USE_GEMINI=" .env; then
            sed -i "s|AI_USE_GEMINI=.*|AI_USE_GEMINI=true|" .env
        else
            echo "AI_USE_GEMINI=true" >> .env
        fi
        
        if grep -q "AI_MODEL_NAME=" .env; then
            sed -i "s|AI_MODEL_NAME=.*|AI_MODEL_NAME=gemini-1.5-flash|" .env
        else
            echo "AI_MODEL_NAME=gemini-1.5-flash" >> .env
        fi
        
        echo "✓ Google Gemini 配置完成"
        ;;
        
    2)
        echo ""
        echo "配置 OpenAI API"
        echo "---------------"
        echo "1. 访问: https://platform.openai.com/api-keys"
        echo "2. 创建 API Key"
        echo ""
        read -p "请输入 OpenAI API Key: " OPENAI_KEY
        
        if [ -z "$OPENAI_KEY" ]; then
            echo "✗ API Key 不能为空"
            exit 1
        fi
        
        # 更新 .env
        if grep -q "OPENAI_API_KEY=" .env; then
            sed -i "s|OPENAI_API_KEY=.*|OPENAI_API_KEY=$OPENAI_KEY|" .env
        else
            echo "OPENAI_API_KEY=$OPENAI_KEY" >> .env
        fi
        
        if grep -q "OPENAI_API_BASE=" .env; then
            sed -i "s|OPENAI_API_BASE=.*|OPENAI_API_BASE=https://api.openai.com/v1|" .env
        else
            echo "OPENAI_API_BASE=https://api.openai.com/v1" >> .env
        fi
        
        if grep -q "AI_USE_GEMINI=" .env; then
            sed -i "s|AI_USE_GEMINI=.*|AI_USE_GEMINI=false|" .env
        else
            echo "AI_USE_GEMINI=false" >> .env
        fi
        
        echo "✓ OpenAI 配置完成"
        ;;
        
    3)
        echo ""
        echo "配置 OpenAI 代理服务"
        echo "--------------------"
        read -p "请输入代理 API Key: " PROXY_KEY
        read -p "请输入代理 Base URL (默认: https://apiproxy.top/v1): " PROXY_URL
        PROXY_URL=${PROXY_URL:-https://apiproxy.top/v1}
        
        if [ -z "$PROXY_KEY" ]; then
            echo "✗ API Key 不能为空"
            exit 1
        fi
        
        # 更新 .env
        if grep -q "OPENAI_API_KEY=" .env; then
            sed -i "s|OPENAI_API_KEY=.*|OPENAI_API_KEY=$PROXY_KEY|" .env
        else
            echo "OPENAI_API_KEY=$PROXY_KEY" >> .env
        fi
        
        if grep -q "OPENAI_API_BASE=" .env; then
            sed -i "s|OPENAI_API_BASE=.*|OPENAI_API_BASE=$PROXY_URL|" .env
        else
            echo "OPENAI_API_BASE=$PROXY_URL" >> .env
        fi
        
        if grep -q "AI_USE_GEMINI=" .env; then
            sed -i "s|AI_USE_GEMINI=.*|AI_USE_GEMINI=false|" .env
        else
            echo "AI_USE_GEMINI=false" >> .env
        fi
        
        echo "✓ 代理服务配置完成"
        ;;
        
    4)
        echo ""
        echo "当前配置:"
        echo "--------"
        source .env 2>/dev/null || true
        
        if [ -n "$GOOGLE_API_KEY" ]; then
            echo "✓ GOOGLE_API_KEY: ${GOOGLE_API_KEY:0:10}..."
        else
            echo "✗ GOOGLE_API_KEY: 未设置"
        fi
        
        if [ -n "$OPENAI_API_KEY" ]; then
            echo "✓ OPENAI_API_KEY: ${OPENAI_API_KEY:0:10}..."
        else
            echo "✗ OPENAI_API_KEY: 未设置"
        fi
        
        echo "  OPENAI_API_BASE: ${OPENAI_API_BASE:-未设置}"
        echo "  AI_USE_GEMINI: ${AI_USE_GEMINI:-true}"
        echo "  AI_MODEL_NAME: ${AI_MODEL_NAME:-gemini-1.5-flash}"
        ;;
        
    5)
        echo ""
        echo "测试 API 连接..."
        echo "----------------"
        python3 test_api_error_handling.py
        ;;
        
    0)
        echo "退出"
        exit 0
        ;;
        
    *)
        echo "✗ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "配置已保存到 .env 文件"
echo "======================================"
echo ""
echo "后续步骤:"
echo "1. 重启后端服务: ./restart_backend.sh"
echo "2. 运行测试: python3 test_api_error_handling.py"
echo "3. 打开测试页面: http://localhost:8000/test_api_errors.html"
echo ""
