# 项目结构说明

## 核心文件

### 启动脚本
- `start_all.sh` - 启动后端和前端（推荐）
- `start_backend.sh` - 仅启动后端API服务
- `start_frontend.sh` - 仅启动前端Streamlit界面
- `stop_all.sh` - 停止所有服务
- `restart_backend.sh` - 重启后端服务

### 主应用
- `app.py` - Streamlit前端应用入口
- `README.md` - 项目主文档
- `requirements.txt` - Python依赖包

## 目录结构

### backend/ - 后端服务
```
backend/
├── api/           # FastAPI接口
│   ├── main.py    # API主入口
│   └── routes/    # 路由模块
│       ├── upload.py    # 文件上传
│       ├── analyze.py   # 音频分析
│       └── expression.py # 表情生成
├── core/          # 核心业务逻辑
│   ├── audio_analyzer.py      # 音频分析（AI驱动）
│   ├── expression_generator.py # 表情生成
│   ├── langchain_agent.py     # LangChain代理
│   └── live2d_controller.py   # Live2D控制
├── models/        # 数据模型
├── utils/         # 工具函数
└── tests/         # 后端测试
```

### frontend/ - 前端应用
```
frontend/
├── pages/         # Streamlit页面
│   ├── upload.py     # 上传页面
│   ├── realtime.py   # 实时分析
│   └── settings.py   # 设置页面
├── components/    # UI组件
├── utils/         # 工具函数
└── assets/        # 静态资源
```

### config/ - 配置文件
- API配置
- 模型配置
- 环境变量

### data/ - 数据目录
```
data/
├── uploads/       # 上传的音频文件
├── results/       # 分析结果
└── expressions/   # 生成的表情数据
```

### tests/ - 测试文件
- 集成测试
- 单元测试

### archive/ - 归档文件
- `old_tests/` - 旧测试文件
- `old_docs/` - 旧文档
- `old_scripts/` - 旧脚本

## 快速启动

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量（.env文件）：
```
GOOGLE_API_KEY=your_api_key
GOOGLE_MODEL=gemini-2.0-flash-exp
```

3. 启动服务：
```bash
./start_all.sh
```

4. 访问应用：
- 前端: http://localhost:8501
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 服务端口
- Backend API: 8000
- Frontend Streamlit: 8501

## 日志文件
- `logs/backend.log` - 后端日志
- `logs/frontend.log` - 前端日志
