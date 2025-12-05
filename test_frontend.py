#!/usr/bin/env python
"""
Frontend功能测试脚本
测试前端与后端的集成
"""
import requests
import time
import sys
from pathlib import Path

# 配置
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8501"
TEST_AUDIO = "test_audio.wav"

def print_section(title):
    """打印测试章节标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_backend_health():
    """测试Backend健康状态"""
    print_section("测试Backend服务")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend服务正常运行")
            print(f"   状态: {response.json()}")
            return True
        else:
            print(f"❌ Backend服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend服务连接失败: {str(e)}")
        return False

def test_frontend_health():
    """测试Frontend健康状态"""
    print_section("测试Frontend服务")
    try:
        response = requests.get(f"{FRONTEND_URL}/_stcore/health", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend服务正常运行")
            print(f"   访问地址: {FRONTEND_URL}")
            return True
        else:
            print(f"❌ Frontend服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend服务连接失败: {str(e)}")
        return False

def test_api_integration():
    """测试API集成"""
    print_section("测试API集成")
    
    try:
        # 使用API客户端测试
        sys.path.append(str(Path(__file__).parent))
        from frontend.utils.api_client import APIClient
        
        api_client = APIClient()
        
        # 测试健康检查
        health = api_client.health_check()
        if health.get('status') == 'healthy':
            print("✅ API客户端连接成功")
        else:
            print("❌ API客户端连接失败")
            return False
        
        # 测试文件上传（使用测试文件）
        if Path(TEST_AUDIO).exists():
            print("\n📤 测试文件上传...")
            
            class MockFile:
                def __init__(self, path):
                    self.name = Path(path).name
                    self.type = "audio/wav"
                    with open(path, 'rb') as f:
                        self._content = f.read()
                
                def getvalue(self):
                    return self._content
            
            mock_file = MockFile(TEST_AUDIO)
            
            try:
                upload_result = api_client.upload_file(mock_file)
                if upload_result.get('success'):
                    print("✅ 文件上传成功")
                    file_id = upload_result['data']['file_id']
                    
                    # 测试音频分析
                    print("\n🎵 测试音频分析...")
                    analyze_result = api_client.analyze_audio(file_id)
                    if analyze_result.get('success'):
                        print("✅ 音频分析成功")
                        print(f"   时长: {analyze_result['data']['duration']:.2f}秒")
                    
                    # 测试表情生成
                    print("\n🎭 测试表情生成...")
                    expression_result = api_client.generate_expression(
                        file_id=file_id,
                        time_resolution=0.1
                    )
                    if expression_result.get('success'):
                        print("✅ 表情生成成功")
                        print(f"   关键帧数: {expression_result['data']['keyframe_count']}")
                        
                        # 测试获取表情
                        expression_id = expression_result['data']['expression_id']
                        print("\n📊 测试获取表情数据...")
                        get_result = api_client.get_expression(expression_id)
                        if get_result.get('success'):
                            print("✅ 获取表情数据成功")
                            print(f"   表情数量: {len(get_result['data']['expressions'])}")
                        
                        return True
                else:
                    print(f"❌ 文件上传失败: {upload_result}")
                    return False
            except Exception as e:
                print(f"❌ API调用失败: {str(e)}")
                return False
        else:
            print(f"⚠️  测试文件不存在: {TEST_AUDIO}")
            print("   跳过API集成测试")
            return True
    
    except ImportError as e:
        print(f"❌ 导入API客户端失败: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ API集成测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_frontend_pages():
    """测试前端页面"""
    print_section("测试前端页面")
    
    pages = {
        "主页": f"{FRONTEND_URL}",
    }
    
    all_passed = True
    for name, url in pages.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: 可访问")
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ {name}: 连接失败 - {str(e)}")
            all_passed = False
    
    return all_passed

def main():
    """主测试流程"""
    print("\n" + "="*60)
    print("  Frontend + Backend 集成测试")
    print("="*60)
    
    results = {
        "Backend服务": False,
        "Frontend服务": False,
        "API集成": False,
        "前端页面": False
    }
    
    try:
        # 1. Backend健康检查
        results["Backend服务"] = test_backend_health()
        
        # 2. Frontend健康检查
        results["Frontend服务"] = test_frontend_health()
        
        # 3. API集成测试
        if results["Backend服务"]:
            results["API集成"] = test_api_integration()
        else:
            print("\n⚠️  Backend服务未运行，跳过API集成测试")
        
        # 4. 前端页面测试
        if results["Frontend服务"]:
            results["前端页面"] = test_frontend_pages()
        else:
            print("\n⚠️  Frontend服务未运行，跳过页面测试")
        
        # 总结
        print("\n" + "="*60)
        print("  测试结果总结")
        print("="*60)
        
        for test_name, passed in results.items():
            status = "✅ 通过" if passed else "❌ 失败"
            print(f"  {test_name}: {status}")
        
        all_passed = all(results.values())
        
        if all_passed:
            print("\n" + "="*60)
            print("  🎉 所有测试通过！")
            print("="*60)
            print("\n💡 提示:")
            print(f"  - Frontend访问地址: {FRONTEND_URL}")
            print(f"  - Backend API文档: {BACKEND_URL}/docs")
        else:
            print("\n⚠️  部分测试未通过，请检查服务状态")
            if not results["Backend服务"]:
                print("   启动Backend: ./start_backend.sh")
            if not results["Frontend服务"]:
                print("   启动Frontend: ./start_frontend.sh")
        
        return 0 if all_passed else 1
        
    except Exception as e:
        print(f"\n❌ 测试过程发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
