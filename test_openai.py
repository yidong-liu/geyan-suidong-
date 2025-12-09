#!/usr/bin/env python3
"""测试OpenAI连接"""
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from backend.core.ai_config import AIConfig

def test_openai_connection():
    """测试OpenAI API连接"""
    print("=" * 50)
    print("  测试 OpenAI API 连接")
    print("=" * 50)
    
    # 检查配置
    use_gemini = AIConfig.get_use_gemini()
    api_key = AIConfig.get_api_key()
    model_name = AIConfig.get_model_name()
    base_url = AIConfig.get_base_url()
    
    print(f"\n📋 当前配置:")
    print(f"  - 使用Gemini: {use_gemini}")
    print(f"  - API Key: {'✅ 已设置' if api_key else '❌ 未设置'}")
    print(f"  - 模型: {model_name}")
    print(f"  - Base URL: {base_url}")
    
    # 验证配置
    is_valid, error_msg = AIConfig.validate_config()
    if not is_valid:
        print(f"\n❌ 配置验证失败: {error_msg}")
        return False
    
    print("\n✅ 配置验证通过")
    
    # 测试实际连接
    print("\n🔄 测试API连接...")
    
    try:
        if use_gemini:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello' in one word")
            result = response.text
            print(f"✅ Gemini API 连接成功!")
            print(f"   响应: {result}")
        else:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=base_url)
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": "Say 'Hello' in one word"}],
                max_tokens=10
            )
            result = response.choices[0].message.content
            print(f"✅ OpenAI API 连接成功!")
            print(f"   响应: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ API 连接失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_openai_connection()
    sys.exit(0 if success else 1)
