#!/usr/bin/env python
"""
Backend API测试脚本
测试所有API端点的功能
"""
import requests
import json
import os
import sys
from pathlib import Path

# 配置
BASE_URL = "http://localhost:8000"
TEST_AUDIO = "test_audio.wav"

def print_section(title):
    """打印测试章节标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """测试健康检查"""
    print_section("测试健康检查")
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ 健康检查通过")

def test_root():
    """测试根路径"""
    print_section("测试根路径")
    response = requests.get(f"{BASE_URL}/")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    assert response.status_code == 200
    print("✅ 根路径测试通过")

def test_upload():
    """测试文件上传"""
    print_section("测试文件上传")
    
    if not os.path.exists(TEST_AUDIO):
        print(f"❌ 测试文件不存在: {TEST_AUDIO}")
        return None
    
    with open(TEST_AUDIO, 'rb') as f:
        files = {'file': (TEST_AUDIO, f, 'audio/wav')}
        response = requests.post(f"{BASE_URL}/api/v1/upload", files=files)
    
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    assert data["success"] == True
    file_id = data["data"]["file_id"]
    print(f"✅ 文件上传成功，文件ID: {file_id}")
    return file_id

def test_analyze(file_id):
    """测试音频分析"""
    print_section("测试音频分析")
    
    payload = {"file_id": file_id}
    response = requests.post(
        f"{BASE_URL}/api/v1/analyze",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    assert data["success"] == True
    assert "duration" in data["data"]
    assert "tempo" in data["data"]
    assert "emotion_scores" in data["data"]
    print("✅ 音频分析成功")

def test_generate_expression(file_id):
    """测试表情生成"""
    print_section("测试表情生成")
    
    payload = {
        "file_id": file_id,
        "time_resolution": 0.1,
        "enable_smoothing": True
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/generate",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    assert data["success"] == True
    expression_id = data["data"]["expression_id"]
    print(f"✅ 表情生成成功，表情ID: {expression_id}")
    return expression_id

def test_get_expression(expression_id):
    """测试获取表情数据"""
    print_section("测试获取表情数据")
    
    response = requests.get(f"{BASE_URL}/api/v1/expression/{expression_id}")
    
    print(f"状态码: {response.status_code}")
    data = response.json()
    
    # 只打印部分数据，避免输出过长
    summary = {
        "success": data["success"],
        "message": data["message"],
        "duration": data["data"]["duration"],
        "tempo": data["data"]["tempo"],
        "emotion_scores": data["data"]["emotion_scores"],
        "expression_count": len(data["data"]["expressions"])
    }
    print(f"响应摘要: {json.dumps(summary, indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    assert data["success"] == True
    assert "expressions" in data["data"]
    print("✅ 获取表情数据成功")

def test_delete_file(file_id):
    """测试文件删除"""
    print_section("测试文件删除")
    
    response = requests.delete(f"{BASE_URL}/api/v1/upload/{file_id}")
    
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    assert data["success"] == True
    print("✅ 文件删除成功")

def main():
    """主测试流程"""
    print("\n" + "="*60)
    print("  Backend API 综合测试")
    print("="*60)
    
    try:
        # 1. 健康检查
        test_health()
        
        # 2. 根路径测试
        test_root()
        
        # 3. 文件上传
        file_id = test_upload()
        if not file_id:
            print("\n❌ 文件上传失败，跳过后续测试")
            return
        
        # 4. 音频分析
        test_analyze(file_id)
        
        # 5. 表情生成
        expression_id = test_generate_expression(file_id)
        
        # 6. 获取表情数据
        test_get_expression(expression_id)
        
        # 7. 文件删除
        test_delete_file(file_id)
        
        print("\n" + "="*60)
        print("  🎉 所有测试通过！")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {str(e)}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务器，请确保后端服务已启动")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
