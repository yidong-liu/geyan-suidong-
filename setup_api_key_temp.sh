#!/bin/bash
echo "=================================================="
echo "  设置 API Key"
echo "=================================================="
echo ""
echo "请选择要使用的 AI 服务:"
echo "  1) OpenAI (需要付费 API Key)"
echo "  2) Google Gemini (推荐 - 有免费额度)"
echo ""
read -p "请输入选项 (1 或 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    read -p "请输入 OpenAI API Key: " api_key
    read -p "请输入 OpenAI Base URL (留空使用默认): " base_url
    
    if [ -z "$base_url" ]; then
        base_url="https://api.openai.com/v1"
    fi
    
    # 更新 .env 文件
    sed -i "s|AI_USE_GEMINI=.*|AI_USE_GEMINI=false|g" .env
    sed -i "s|OPENAI_API_KEY=.*|OPENAI_API_KEY=$api_key|g" .env 2>/dev/null || echo "OPENAI_API_KEY=$api_key" >> .env
    sed -i "s|OPENAI_API_BASE=.*|OPENAI_API_BASE=$base_url|g" .env 2>/dev/null || echo "OPENAI_API_BASE=$base_url" >> .env
    
    export AI_USE_GEMINI=false
    export OPENAI_API_KEY=$api_key
    export OPENAI_API_BASE=$base_url
    
    echo ""
    echo "✅ OpenAI API Key 已设置"
    
elif [ "$choice" = "2" ]; then
    echo ""
    read -p "请输入 Google Gemini API Key: " api_key
    
    sed -i "s|GOOGLE_API_KEY=.*|GOOGLE_API_KEY=$api_key|g" .env
    sed -i "s|AI_USE_GEMINI=.*|AI_USE_GEMINI=true|g" .env
    
    export AI_USE_GEMINI=true
    export GOOGLE_API_KEY=$api_key
    
    echo ""
    echo "✅ Google Gemini API Key 已设置"
else
    echo "❌ 无效的选项"
    exit 1
fi

echo ""
echo "=================================================="
