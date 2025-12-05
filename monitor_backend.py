#!/usr/bin/env python
"""
Backend服务健康监测和自动修复脚本
"""
import subprocess
import requests
import time
import sys
import os
from pathlib import Path

class BackendMonitor:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.max_retries = 3
        self.retry_delay = 5
        
    def check_health(self):
        """检查服务健康状态"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def find_backend_pid(self):
        """查找backend进程PID"""
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )
            for line in result.stdout.split('\n'):
                if 'python -m backend.api.main' in line and 'grep' not in line:
                    parts = line.split()
                    return parts[1]
            return None
        except:
            return None
    
    def start_backend(self):
        """启动backend服务"""
        print("🚀 启动Backend服务...")
        
        # 创建必要的目录
        os.makedirs("data/uploads", exist_ok=True)
        os.makedirs("data/expressions", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # 启动服务
        subprocess.Popen(
            ["python", "-m", "backend.api.main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 等待服务启动
        for i in range(10):
            time.sleep(1)
            if self.check_health():
                print("✅ Backend服务启动成功")
                return True
        
        return False
    
    def stop_backend(self):
        """停止backend服务"""
        pid = self.find_backend_pid()
        if pid:
            print(f"⏹️  停止Backend服务 (PID: {pid})")
            subprocess.run(["kill", pid])
            time.sleep(2)
            return True
        return False
    
    def restart_backend(self):
        """重启backend服务"""
        print("🔄 重启Backend服务...")
        self.stop_backend()
        time.sleep(2)
        return self.start_backend()
    
    def test_endpoints(self):
        """测试所有端点"""
        tests = {
            "健康检查": f"{self.base_url}/health",
            "根路径": f"{self.base_url}/",
            "API文档": f"{self.base_url}/docs",
        }
        
        print("\n📋 测试API端点:")
        all_passed = True
        
        for name, url in tests.items():
            try:
                response = requests.get(url, timeout=5)
                status = "✅" if response.status_code == 200 else "❌"
                print(f"  {status} {name}: {response.status_code}")
                if response.status_code != 200:
                    all_passed = False
            except Exception as e:
                print(f"  ❌ {name}: 连接失败 - {str(e)}")
                all_passed = False
        
        return all_passed
    
    def monitor(self):
        """持续监控服务状态"""
        print("\n" + "="*60)
        print("  Backend服务健康监测")
        print("="*60 + "\n")
        
        # 检查服务是否运行
        if not self.check_health():
            print("⚠️  Backend服务未运行")
            
            # 尝试启动服务
            if self.start_backend():
                print("✅ 服务启动成功")
            else:
                print("❌ 服务启动失败")
                return False
        else:
            print("✅ Backend服务正在运行")
        
        # 测试端点
        if self.test_endpoints():
            print("\n✅ 所有端点测试通过")
        else:
            print("\n⚠️  部分端点测试失败")
        
        # 显示服务信息
        print("\n📊 服务信息:")
        print(f"  - 服务地址: {self.base_url}")
        print(f"  - API文档: {self.base_url}/docs")
        print(f"  - 进程PID: {self.find_backend_pid() or '未找到'}")
        
        return True

def main():
    monitor = BackendMonitor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            monitor.start_backend()
        elif command == "stop":
            monitor.stop_backend()
        elif command == "restart":
            monitor.restart_backend()
        elif command == "test":
            monitor.test_endpoints()
        else:
            print(f"未知命令: {command}")
            print("可用命令: start, stop, restart, test")
    else:
        # 默认执行健康检查
        monitor.monitor()

if __name__ == "__main__":
    main()
