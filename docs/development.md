# 开发环境配置指南

## 🔧 系统要求

### 最低配置要求

- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 或更高版本
- **Node.js**: 16.0 或更高版本 (Live2D Web 支持)
- **内存**: 最少 8GB RAM (推荐 16GB)
- **存储**: 至少 2GB 可用空间
- **网络**: 稳定的互联网连接 (用于 AI API 调用)

### 推荐配置

- **CPU**: Intel i5 8 代或 AMD Ryzen 5 3600 及以上
- **GPU**: 支持 WebGL 的独立显卡 (Live2D 渲染优化)
- **内存**: 16GB 或更多
- **存储**: SSD 硬盘

## 📦 依赖安装

### 1. Python 环境设置

#### 使用 conda (推荐)

```bash
# 创建虚拟环境
conda create -n geyan-suidong python=3.9
conda activate geyan-suidong

# 安装基础科学计算库
conda install numpy pandas matplotlib scipy
conda install -c conda-forge librosa
```

#### 使用 pip

```bash
# 创建虚拟环境
python -m venv venv

# 激活环境 (Windows)
venv\Scripts\activate

# 激活环境 (macOS/Linux)
source venv/bin/activate

# 升级pip
python -m pip install --upgrade pip
```

### 2. 核心依赖安装

```bash
# 安装核心依赖
pip install -r requirements.txt
```

#### requirements.txt 内容：

```txt
# Web框架
streamlit>=1.28.0
fastapi>=0.104.0
uvicorn>=0.24.0

# 音频处理
librosa>=0.10.1
pydub>=0.25.1
soundfile>=0.12.1
numpy>=1.24.0
scipy>=1.11.0

# AI和机器学习
langchain>=0.0.350
openai>=1.3.0
transformers>=4.35.0
torch>=2.1.0

# 数据处理
pandas>=2.1.0
matplotlib>=3.7.0
seaborn>=0.13.0

# HTTP和API
requests>=2.31.0
aiohttp>=3.9.0
httpx>=0.25.0

# 文件处理
python-multipart>=0.0.6
python-dotenv>=1.0.0

# 数据验证
pydantic>=2.5.0

# 测试
pytest>=7.4.0
pytest-asyncio>=0.21.0

# 开发工具
black>=23.11.0
flake8>=6.1.0
mypy>=1.7.0
```

### 3. FFmpeg 安装

#### Windows

```bash
# 使用 chocolatey
choco install ffmpeg

# 或者下载预编译版本
# 下载: https://ffmpeg.org/download.html#build-windows
# 解压并添加到系统PATH
```

#### macOS

```bash
# 使用 Homebrew
brew install ffmpeg
```

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

### 4. Node.js 和前端依赖 (可选)

```bash
# 安装Node.js (如果需要自定义Live2D组件)
npm install -g npm@latest

# 项目根目录下创建 package.json
npm init -y

# 安装Live2D相关依赖
npm install pixi.js pixi-live2d-display
```

## 🔑 环境变量配置

### 创建 .env 文件

```bash
# 在项目根目录创建 .env 文件
cp .env.example .env
```

### .env.example 内容：

```bash
# === API 配置 ===
# OpenAI API配置 (用于LangChain)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1

# 或者使用其他兼容的API
# OPENAI_API_BASE=https://api.deepseek.com
# OPENAI_API_KEY=your_deepseek_api_key

# === 应用配置 ===
# Streamlit配置
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# FastAPI配置
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true

# === 文件路径配置 ===
# 上传文件存储路径
UPLOAD_DIR=./data/uploads
# Live2D模型存储路径
MODELS_DIR=./models
# 生成的表情文件存储路径
EXPRESSIONS_DIR=./data/expressions
# 临时文件路径
TEMP_DIR=./data/temp

# === Live2D 配置 ===
# 默认模型文件名
DEFAULT_MODEL=hiyori_free_t08.model3.json
# 表情参数映射文件
EXPRESSION_MAPPING=./config/expression_mapping.json

# === 性能配置 ===
# 音频处理配置
AUDIO_SAMPLE_RATE=44100
AUDIO_HOP_LENGTH=512
MAX_AUDIO_LENGTH=300  # 最大音频长度(秒)

# 并发配置
MAX_WORKERS=4
BATCH_SIZE=10

# === 日志配置 ===
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# === 安全配置 ===
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🗂️ 目录结构创建

运行以下脚本创建项目目录结构：

### setup_project.py

```python
import os
from pathlib import Path

def create_project_structure():
    """创建项目目录结构"""

    directories = [
        # 后端目录
        "backend/core",
        "backend/api",
        "backend/utils",
        "backend/models",

        # 前端目录
        "frontend/pages",
        "frontend/components",
        "frontend/static/css",
        "frontend/static/js",
        "frontend/static/images",

        # 数据目录
        "data/uploads",
        "data/expressions",
        "data/temp",
        "data/cache",

        # Live2D模型目录
        "models/hiyori",
        "models/assets",

        # 配置目录
        "config",

        # 文档目录 (已存在)
        # "docs",

        # 测试目录
        "tests/backend",
        "tests/frontend",
        "tests/integration",

        # 日志目录
        "logs",

        # 脚本目录
        "scripts"
    ]

    # 创建目录
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

    # 创建空的__init__.py文件
    init_files = [
        "backend/__init__.py",
        "backend/core/__init__.py",
        "backend/api/__init__.py",
        "backend/utils/__init__.py",
        "backend/models/__init__.py",
        "frontend/__init__.py",
        "frontend/pages/__init__.py",
        "frontend/components/__init__.py",
        "tests/__init__.py",
        "tests/backend/__init__.py",
        "tests/frontend/__init__.py"
    ]

    for init_file in init_files:
        Path(init_file).touch()
        print(f"Created file: {init_file}")

    print("\n✅ 项目目录结构创建完成!")

if __name__ == "__main__":
    create_project_structure()
```

### 运行设置脚本

```bash
python setup_project.py
```

## ✅ 环境验证

### 创建验证脚本 verify_setup.py

```python
import sys
import subprocess
import importlib

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("   需要Python 3.8或更高版本")
        return False

def check_package(package_name, import_name=None):
    """检查Python包是否安装"""
    if import_name is None:
        import_name = package_name

    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'Unknown')
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"❌ {package_name}: 未安装")
        return False

def check_ffmpeg():
    """检查FFmpeg是否安装"""
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg: {version_line}")
            return True
    except FileNotFoundError:
        print("❌ FFmpeg: 未安装或未添加到PATH")
        return False

def main():
    """主验证函数"""
    print("🔍 环境验证开始...\n")

    checks = []

    # 检查Python版本
    checks.append(check_python_version())

    # 检查核心包
    packages = [
        ('streamlit', 'streamlit'),
        ('fastapi', 'fastapi'),
        ('librosa', 'librosa'),
        ('numpy', 'numpy'),
        ('pandas', 'pandas'),
        ('langchain', 'langchain'),
        ('openai', 'openai'),
        ('pydub', 'pydub'),
        ('scipy', 'scipy')
    ]

    for package, import_name in packages:
        checks.append(check_package(package, import_name))

    # 检查FFmpeg
    checks.append(check_ffmpeg())

    # 检查环境变量文件
    import os
    if os.path.exists('.env'):
        print("✅ .env文件: 已存在")
        checks.append(True)
    else:
        print("⚠️  .env文件: 不存在，请复制.env.example并配置")
        checks.append(False)

    # 总结
    passed = sum(checks)
    total = len(checks)

    print(f"\n📊 验证结果: {passed}/{total} 项通过")

    if passed == total:
        print("🎉 环境配置完成，可以开始开发!")
    else:
        print("❌ 存在问题，请根据上述提示修复")

if __name__ == "__main__":
    main()
```

### 运行验证

```bash
python verify_setup.py
```

## 🚀 快速启动

### 1. 启动后端 API 服务

```bash
# 进入后端目录
cd backend

# 启动FastAPI服务
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 启动 Streamlit 前端

```bash
# 在项目根目录
streamlit run app.py
```

### 3. 访问应用

- **Streamlit 前端**: http://localhost:8501
- **FastAPI 文档**: http://localhost:8000/docs
- **API Swagger**: http://localhost:8000/redoc

## 🛠️ 开发工具配置

### VS Code 配置

创建 `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/node_modules": true
  }
}
```

创建 `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Streamlit App",
      "type": "python",
      "request": "launch",
      "program": "app.py",
      "console": "integratedTerminal",
      "args": ["run", "streamlit"]
    },
    {
      "name": "FastAPI Server",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["backend.api.main:app", "--reload"],
      "console": "integratedTerminal"
    }
  ]
}
```

## 🐳 Docker 配置 (可选)

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8501 8000

# 启动命令
CMD ["streamlit", "run", "app.py"]
```

### docker-compose.yml

```yaml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "8501:8501"
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    env_file:
      - .env
```

## 📝 Git 配置

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv
.env

# 数据文件
data/uploads/*
data/temp/*
data/cache/*
!data/.gitkeep

# 日志
logs/*.log
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# 模型文件 (如果太大)
models/*.model3
models/*.moc3
models/*.bin

# Streamlit
.streamlit/
```

---

🎉 **环境配置完成后，您就可以开始开发「歌颜随动」项目了！**

如果遇到任何问题，请参考各个依赖库的官方文档或在项目 issue 中提问。
