"""
项目目录结构创建脚本
根据所有文档生成完整的项目目录结构
"""
import os
from pathlib import Path

def create_project_structure():
    """创建项目目录结构"""
    
    print("=" * 60)
    print("开始创建「歌颜随动」项目目录结构")
    print("=" * 60)
    
    directories = [
        # 后端目录
        "backend\\core",
        "backend\\api\\routes",
        "backend\\utils",
        "backend\\models",
        "backend\\tests",
        
        # 前端目录
        "frontend\\pages",
        "frontend\\components",
        "frontend\\static\\css",
        "frontend\\static\\js",
        "frontend\\static\\images",
        "frontend\\utils",
        
        # 数据目录
        "data\\uploads",
        "data\\expressions",
        "data\\temp",
        "data\\cache",
        
        # Live2D模型目录
        "models\\hiyori",
        "models\\assets",
        
        # 配置目录
        "config",
        
        # 测试目录
        "tests\\backend",
        "tests\\frontend",
        "tests\\integration",
        
        # 日志目录
        "logs",
        
        # 脚本目录
        "scripts",
        
        # 文档目录 (docs已存在，不重复创建)
        # "docs",
    ]
    
    # 创建目录
    print("\n📁 创建目录...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")
    
    # 创建Python包的__init__.py文件
    print("\n📄 创建Python包文件...")
    init_files = [
        "backend\\__init__.py",
        "backend\\core\\__init__.py",
        "backend\\api\\__init__.py",
        "backend\\api\\routes\\__init__.py",
        "backend\\utils\\__init__.py",
        "backend\\models\\__init__.py",
        "backend\\tests\\__init__.py",
        
        "frontend\\__init__.py",
        "frontend\\pages\\__init__.py",
        "frontend\\components\\__init__.py",
        "frontend\\utils\\__init__.py",
        
        "tests\\__init__.py",
        "tests\\backend\\__init__.py",
        "tests\\frontend\\__init__.py",
        "tests\\integration\\__init__.py",
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"  ✓ {init_file}")
    
    # 创建.gitkeep文件保持空目录
    print("\n📌 创建.gitkeep文件...")
    gitkeep_dirs = [
        "data\\uploads",
        "data\\expressions",
        "data\\temp",
        "data\\cache",
        "models\\hiyori",
        "models\\assets",
        "logs",
        "frontend\\static\\images",
    ]
    
    for directory in gitkeep_dirs:
        gitkeep_file = Path(directory) / ".gitkeep"
        gitkeep_file.touch()
        print(f"  ✓ {directory}\\.gitkeep")
    
    print("\n" + "=" * 60)
    print("✅ 项目目录结构创建完成!")
    print("=" * 60)
    
    # 打印目录树预览
    print("\n📊 目录结构预览:")
    print_tree()

def print_tree():
    """打印项目目录树结构"""
    tree = """
geyan-suidong-/
├── backend/                    # 后端服务
│   ├── core/                  # 核心业务逻辑
│   │   ├── __init__.py
│   │   ├── audio_analyzer.py  # 音频分析器
│   │   ├── expression_generator.py  # 表情生成器
│   │   ├── langchain_agent.py # LangChain代理
│   │   └── live2d_controller.py  # Live2D控制器
│   ├── api/                   # API路由和接口
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI主应用
│   │   ├── dependencies.py   # 依赖注入
│   │   └── routes/           # 路由模块
│   │       ├── __init__.py
│   │       ├── upload.py     # 文件上传路由
│   │       ├── analyze.py    # 分析处理路由
│   │       └── expression.py # 表情相关路由
│   ├── models/               # 数据模型
│   │   ├── __init__.py
│   │   ├── audio.py         # 音频相关模型
│   │   ├── expression.py    # 表情相关模型
│   │   └── response.py      # 响应模型
│   ├── utils/               # 工具函数
│   │   ├── __init__.py
│   │   ├── file_utils.py    # 文件处理工具
│   │   ├── audio_utils.py   # 音频处理工具
│   │   └── config.py        # 配置管理
│   └── tests/               # 后端测试
│       ├── __init__.py
│       ├── test_audio_analyzer.py
│       ├── test_expression_generator.py
│       └── test_api.py
│
├── frontend/                 # 前端界面
│   ├── pages/               # Streamlit页面
│   │   ├── __init__.py
│   │   ├── upload.py        # 音频上传页面
│   │   ├── preview.py       # Live2D预览页面
│   │   └── config.py        # 配置页面
│   ├── components/          # 可复用组件
│   │   ├── __init__.py
│   │   ├── audio_player.py  # 音频播放器组件
│   │   ├── live2d_viewer.py # Live2D查看器组件
│   │   ├── progress_tracker.py  # 进度跟踪组件
│   │   └── file_uploader.py # 文件上传组件
│   ├── static/              # 静态资源
│   │   ├── css/
│   │   │   ├── main.css    # 主样式文件
│   │   │   └── live2d.css  # Live2D相关样式
│   │   ├── js/
│   │   │   ├── live2d-controller.js  # Live2D控制器
│   │   │   ├── audio-sync.js         # 音频同步脚本
│   │   │   └── utils.js              # 工具函数
│   │   └── images/         # 图片资源
│   └── utils/              # 前端工具函数
│       ├── __init__.py
│       ├── api_client.py   # API客户端
│       ├── validators.py   # 表单验证
│       └── formatters.py   # 数据格式化
│
├── models/                  # Live2D模型文件
│   ├── hiyori/             # 示例模型
│   └── assets/             # 模型资源
│
├── data/                    # 数据文件
│   ├── uploads/            # 上传的音频文件
│   ├── expressions/        # 生成的表情文件
│   ├── temp/               # 临时文件
│   └── cache/              # 缓存文件
│
├── config/                  # 配置文件
│   ├── expression_mapping.json  # 表情映射配置
│   └── model_config.json   # 模型配置
│
├── tests/                   # 测试文件
│   ├── backend/            # 后端测试
│   ├── frontend/           # 前端测试
│   └── integration/        # 集成测试
│
├── scripts/                 # 脚本工具
│   ├── download_models.py  # 下载模型脚本
│   └── verify_setup.py     # 环境验证脚本
│
├── logs/                    # 日志文件
│
├── docs/                    # 文档
│   ├── development.md      # 开发环境配置指南
│   ├── backend_guide.md    # 后端开发指南
│   ├── frontend_guide.md   # 前端开发指南
│   └── architecture.md     # 技术架构文档
│
├── app.py                   # Streamlit主应用入口
├── requirements.txt         # Python依赖
├── .env.example            # 环境变量模板
├── .gitignore              # Git忽略文件
├── README.md               # 项目说明
└── setup_project.py        # 本脚本文件
"""
    print(tree)

if __name__ == "__main__":
    create_project_structure()
