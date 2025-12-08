"""
快速启动脚本
用于测试项目基本功能
"""
import subprocess
import sys
import time
from pathlib import Path

def check_dependencies():
    """检查依赖项"""
    print("🔍 检查Python依赖...")
    
    required_packages = [
        'streamlit',
        'fastapi',
        'uvicorn',
        'librosa',
        'numpy',
        'pandas',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️ 缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("\n✅ 所有依赖检查完成！")
    return True

def start_backend():
    """启动后端服务"""
    print("\n🚀 启动后端API服务...")
    
    try:
        # 启动FastAPI服务
        backend_cmd = [
            sys.executable, "-m", "uvicorn", 
            "backend.api.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        
        backend_process = subprocess.Popen(
            backend_cmd,
            cwd=Path.cwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("⏳ 等待后端服务启动...")
        time.sleep(3)
        
        # 检查进程是否还在运行
        if backend_process.poll() is None:
            print("✅ 后端服务启动成功！")
            print("📡 API地址: http://localhost:8000")
            print("📖 API文档: http://localhost:8000/docs")
            return backend_process
        else:
            print("❌ 后端服务启动失败")
            stdout, stderr = backend_process.communicate()
            print(f"错误信息: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ 启动后端服务时出错: {str(e)}")
        return None

def start_frontend():
    """启动前端服务"""
    print("\n🎨 启动前端服务...")
    
    try:
        # 启动Streamlit应用
        frontend_cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ]
        
        frontend_process = subprocess.Popen(
            frontend_cmd,
            cwd=Path.cwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("⏳ 等待前端服务启动...")
        time.sleep(3)
        
        if frontend_process.poll() is None:
            print("✅ 前端服务启动成功！")
            print("🌐 应用地址: http://localhost:8501")
            return frontend_process
        else:
            print("❌ 前端服务启动失败")
            stdout, stderr = frontend_process.communicate()
            print(f"错误信息: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ 启动前端服务时出错: {str(e)}")
        return None

def main():
    """主函数"""
    print("🎵 歌颜随动 - 项目启动脚本")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 创建必要的目录
    directories = [
        "data/uploads",
        "data/expressions",
        "data/cache",
        "data/temp",
        "logs"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 创建目录: {dir_path}")
    
    # 启动后端
    backend_process = start_backend()
    if not backend_process:
        print("❌ 后端启动失败，退出...")
        return
    
    # 启动前端
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ 前端启动失败，但后端仍在运行")
        print("你可以手动访问 http://localhost:8000 查看API")
        return
    
    print("\n🎉 项目启动完成！")
    print("=" * 50)
    print("🌐 前端地址: http://localhost:8501")
    print("📡 后端地址: http://localhost:8000")
    print("📖 API文档: http://localhost:8000/docs")
    print("=" * 50)
    print("\n💡 使用说明:")
    print("1. 打开浏览器访问前端地址")
    print("2. 上传音频文件进行分析")
    print("3. 生成Live2D表情动画")
    print("4. 在预览页面查看效果")
    print("\n按 Ctrl+C 停止服务")
    
    try:
        # 等待用户中断
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 正在停止服务...")
        
        if backend_process and backend_process.poll() is None:
            backend_process.terminate()
            print("✅ 后端服务已停止")
        
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
            print("✅ 前端服务已停止")
        
        print("👋 感谢使用歌颜随动！")

if __name__ == "__main__":
    main()