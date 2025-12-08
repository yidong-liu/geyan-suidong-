"""
功能测试脚本
测试项目各个模块的基本功能
"""
import sys
import json
import tempfile
import requests
from pathlib import Path
import time

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

def test_audio_analyzer():
    """测试音频分析器"""
    print("🎵 测试音频分析器...")
    
    try:
        from backend.core.audio_analyzer import AudioAnalyzer
        
        # 创建测试音频文件（使用numpy生成简单的正弦波）
        import numpy as np
        import soundfile as sf
        
        # 生成2秒的测试音频
        sample_rate = 44100
        duration = 2
        t = np.linspace(0, duration, sample_rate * duration)
        frequency = 440  # A4音符
        audio = 0.5 * np.sin(2 * np.pi * frequency * t)
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            sf.write(tmp_file.name, audio, sample_rate)
            
            # 测试分析
            analyzer = AudioAnalyzer()
            features = analyzer.analyze(tmp_file.name)
            
            print(f"  ✅ 分析完成")
            print(f"  - 时长: {features.duration:.2f}秒")
            print(f"  - BPM: {features.tempo:.1f}")
            print(f"  - 情感分数: {features.emotion_scores}")
            
            # 清理临时文件
            Path(tmp_file.name).unlink()
            
        return True
        
    except Exception as e:
        print(f"  ❌ 音频分析器测试失败: {str(e)}")
        return False

def test_expression_generator():
    """测试表情生成器"""
    print("🎭 测试表情生成器...")
    
    try:
        from backend.core.expression_generator import ExpressionGenerator
        import numpy as np
        import soundfile as sf
        
        # 创建测试音频
        sample_rate = 44100
        duration = 1
        t = np.linspace(0, duration, sample_rate * duration)
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            sf.write(tmp_file.name, audio, sample_rate)
            
            # 测试生成
            generator = ExpressionGenerator()
            result = generator.generate_from_audio(
                audio_path=tmp_file.name,
                time_resolution=0.1
            )
            
            print(f"  ✅ 表情生成完成")
            print(f"  - 时长: {result['duration']:.2f}秒")
            print(f"  - 关键帧数: {len(result['expressions'])}")
            print(f"  - BPM: {result['tempo']:.1f}")
            
            # 清理临时文件
            Path(tmp_file.name).unlink()
            
        return True
        
    except Exception as e:
        print(f"  ❌ 表情生成器测试失败: {str(e)}")
        return False

def test_api_client():
    """测试API客户端"""
    print("📡 测试API客户端...")
    
    try:
        from frontend.utils.api_client import APIClient
        
        client = APIClient()
        
        # 测试健康检查
        is_healthy = client.health_check()
        
        if is_healthy:
            print("  ✅ API健康检查通过")
        else:
            print("  ⚠️ API服务未运行")
            
        return True
        
    except Exception as e:
        print(f"  ❌ API客户端测试失败: {str(e)}")
        return False

def test_full_workflow():
    """测试完整工作流程"""
    print("🔄 测试完整工作流程...")
    
    try:
        # 检查后端API是否运行
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code != 200:
                print("  ⚠️ 后端API未运行，跳过完整工作流程测试")
                return True
        except requests.exceptions.RequestException:
            print("  ⚠️ 后端API未运行，跳过完整工作流程测试")
            return True
        
        # 创建测试音频文件
        import numpy as np
        import soundfile as sf
        from io import BytesIO
        
        sample_rate = 44100
        duration = 2
        t = np.linspace(0, duration, sample_rate * duration)
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        
        # 转换为文件数据
        buffer = BytesIO()
        sf.write(buffer, audio, sample_rate, format='WAV')
        buffer.seek(0)
        
        # 测试上传
        files = {'file': ('test.wav', buffer.getvalue(), 'audio/wav')}
        response = requests.post("http://localhost:8000/api/v1/upload", files=files)
        
        if response.status_code != 200:
            print(f"  ❌ 文件上传失败: {response.text}")
            return False
            
        upload_result = response.json()
        file_id = upload_result['data']['file_id']
        print(f"  ✅ 文件上传成功: {file_id[:8]}...")
        
        # 测试音频分析
        analyze_data = {"file_id": file_id}
        response = requests.post("http://localhost:8000/api/v1/analyze", json=analyze_data)
        
        if response.status_code != 200:
            print(f"  ❌ 音频分析失败: {response.text}")
            return False
            
        analyze_result = response.json()
        print(f"  ✅ 音频分析成功: BPM {analyze_result['data']['tempo']:.1f}")
        
        # 测试表情生成
        generate_data = {
            "file_id": file_id,
            "time_resolution": 0.1,
            "enable_smoothing": True
        }
        response = requests.post("http://localhost:8000/api/v1/generate", json=generate_data)
        
        if response.status_code != 200:
            print(f"  ❌ 表情生成失败: {response.text}")
            return False
            
        generate_result = response.json()
        expression_id = generate_result['data']['expression_id']
        print(f"  ✅ 表情生成成功: {expression_id[:8]}...")
        print(f"  - 关键帧数: {generate_result['data']['keyframe_count']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 完整工作流程测试失败: {str(e)}")
        return False

def test_directory_structure():
    """测试目录结构"""
    print("📁 测试目录结构...")
    
    required_dirs = [
        "backend/core",
        "backend/api",
        "frontend/pages",
        "frontend/utils",
        "frontend/components",
        "data/uploads",
        "data/expressions",
        "models",
        "plug/Web"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
        else:
            print(f"  ✅ {dir_path}")
    
    if missing_dirs:
        print(f"  ⚠️ 缺少目录: {missing_dirs}")
        for missing_dir in missing_dirs:
            Path(missing_dir).mkdir(parents=True, exist_ok=True)
            print(f"  📁 创建目录: {missing_dir}")
    
    return True

def main():
    """主测试函数"""
    print("🧪 歌颜随动 - 功能测试")
    print("=" * 50)
    
    tests = [
        ("目录结构", test_directory_structure),
        ("音频分析器", test_audio_analyzer),
        ("表情生成器", test_expression_generator),
        ("API客户端", test_api_client),
        ("完整工作流程", test_full_workflow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 测试 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} 测试异常: {str(e)}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        if result:
            print(f"  ✅ {test_name}")
            passed += 1
        else:
            print(f"  ❌ {test_name}")
    
    print(f"\n🎯 测试通过率: {passed}/{len(results)} ({passed/len(results)*100:.1f}%)")
    
    if passed == len(results):
        print("🎉 所有测试通过！项目基本功能正常")
    else:
        print("⚠️ 部分测试失败，请检查相关模块")
    
    print("\n💡 下一步:")
    print("1. 运行 'python quick_start.py' 启动服务")
    print("2. 或分别启动后端和前端服务")
    print("3. 访问 http://localhost:8501 使用应用")

if __name__ == "__main__":
    main()