# 项目结构说明 v1.0

歌颜随动项目的目录和文件组织说明。

## 📁 总体结构

```
geyan-suidong-/
├── backend/                 # 后端服务代码
├── frontend/                # 前端应用代码
├── config/                  # 配置文件
├── data/                    # 数据存储
├── docs/                    # 📚 项目文档
├── tests/                   # 测试代码
├── logs/                    # 日志文件
├── models/                  # Live2D模型资源（未包含）
├── archive/                 # 归档文件
├── app.py                   # Streamlit主应用
├── requirements.txt         # Python依赖
├── .env                     # 环境变量（不提交）
└── *.sh                     # 启动脚本
```

---

## 🔧 后端 (backend/)

### 目录结构

```
backend/
├── __init__.py
├── api/                     # API层
│   ├── __init__.py
│   ├── main.py             # FastAPI应用入口
│   └── routes/             # 路由模块
│       ├── __init__.py
│       ├── upload.py       # 文件上传路由
│       ├── analyze.py      # 音频分析路由
│       └── expression.py   # 表情生成路由
├── core/                   # 核心业务逻辑
│   ├── __init__.py
│   ├── ai_config.py        # AI模型配置
│   ├── audio_analyzer.py   # 音频分析器（AI驱动）
│   ├── expression_generator.py  # 表情生成器
│   ├── langchain_agent.py  # LangChain AI代理
│   ├── live2d_controller.py    # Live2D控制器
│   └── live2d_expression_mapper.py  # 表情参数映射
├── models/                 # 数据模型
│   ├── __init__.py
│   ├── audio.py           # 音频数据模型
│   ├── expression.py      # 表情数据模型
│   └── response.py        # API响应模型
├── utils/                 # 工具函数
│   ├── __init__.py
│   ├── audio_utils.py     # 音频处理工具
│   └── file_utils.py      # 文件处理工具
└── tests/                 # 后端测试
    └── __init__.py
```

### 核心文件说明

| 文件 | 功能 | 代码行数 |
|-----|------|---------|
| `api/main.py` | FastAPI应用主入口 | ~80 |
| `core/audio_analyzer.py` | 音频分析（librosa + AI） | ~320 |
| `core/expression_generator.py` | 表情生成整合 | ~180 |
| `core/langchain_agent.py` | AI表情映射代理 | ~390 |
| `core/live2d_controller.py` | Live2D参数控制 | ~120 |

---

## 🎨 前端 (frontend/)

### 目录结构

```
frontend/
├── __init__.py
├── pages/                  # Streamlit页面
│   ├── __init__.py
│   └── upload.py          # 音频上传和处理页面
├── components/            # UI组件
│   ├── __init__.py
│   └── live2d_viewer.py   # Live2D查看器组件
├── utils/                 # 工具函数
│   ├── __init__.py
│   └── api_client.py      # 后端API客户端
└── static/                # 静态资源
    ├── css/              # 样式文件
    ├── js/               # JavaScript文件
    └── images/           # 图片资源
```

### 核心文件说明

| 文件 | 功能 |
|-----|------|
| `pages/upload.py` | 音频上传、处理和预览界面 |
| `components/live2d_viewer.py` | Live2D模型展示组件 |
| `utils/api_client.py` | 封装后端API调用 |

---

## ⚙️ 配置 (config/)

```
config/
└── expression_mapping.json  # 表情映射配置文件
```

**expression_mapping.json** 示例：

```json
{
  "emotion_thresholds": {
    "happy": 0.6,
    "sad": 0.4,
    "energetic": 0.7,
    "calm": 0.3
  },
  "parameter_ranges": {
    "eye_open": [0.3, 1.0],
    "mouth_open": [0.0, 0.8],
    "eyebrow_height": [-0.5, 0.5]
  }
}
```

---

## 💾 数据 (data/)

### 目录结构

```
data/
├── uploads/               # 上传的音频文件
│   └── {uuid}.mp3/wav    # 以UUID命名的音频文件
├── expressions/          # 生成的表情文件
│   └── {uuid}.json       # 表情数据JSON
├── temp/                 # 临时文件
└── cache/                # 缓存数据
```

### 文件命名规范

- **音频文件**: `{uuid}.{extension}` (如: `a1b2c3d4-e5f6...mp3`)
- **表情文件**: `{expression_id}.json`
- **自动清理**: 临时文件保留24小时，表情文件保留7天

---

## 📚 文档 (docs/)

### v1.0 文档体系

```
docs/
├── USER_GUIDE.md           # 用户使用指南
├── DEVELOPER_GUIDE.md      # 开发者指南
├── API_REFERENCE.md        # API接口文档
├── EXPRESSION_FORMAT.md    # 表情格式说明
└── DOC_INDEX.md           # 文档索引
```

### 文档分类

| 文档 | 目标读者 | 内容 |
|-----|---------|------|
| USER_GUIDE.md | 用户 | 安装、使用教程、常见问题 |
| DEVELOPER_GUIDE.md | 开发者 | 架构、开发环境、测试部署 |
| API_REFERENCE.md | 集成开发者 | API接口详细说明 |
| EXPRESSION_FORMAT.md | Live2D开发者 | 表情文件格式规范 |
| DOC_INDEX.md | 所有人 | 文档导航和索引 |

---

## 🧪 测试 (tests/)

```
tests/
├── __init__.py
├── backend/               # 后端测试
│   ├── __init__.py
│   └── test_*.py
├── frontend/             # 前端测试
│   ├── __init__.py
│   └── test_*.py
└── integration/          # 集成测试
    ├── __init__.py
    └── test_workflow.py
```

---

## 📝 日志 (logs/)

```
logs/
├── backend.log            # 后端服务日志
├── frontend.log          # 前端应用日志
└── app.log               # 应用总日志
```

**日志配置**: 在 `.env` 文件中设置 `LOG_LEVEL`

---

## 🚀 启动脚本

### 脚本列表

| 脚本 | 功能 |
|-----|------|
| `start_all.sh` | 启动后端和前端（推荐） |
| `start_backend.sh` | 仅启动后端API服务 |
| `start_frontend.sh` | 仅启动前端界面 |
| `stop_all.sh` | 停止所有服务 |
| `restart_backend.sh` | 重启后端服务 |
| `check_health.sh` | 检查服务健康状态 |
| `setup_api_key.sh` | 配置API密钥 |

### 使用示例

```bash
# 启动完整系统
./start_all.sh

# 检查服务状态
./check_health.sh

# 停止所有服务
./stop_all.sh
```

---

## 📦 依赖管理

### requirements.txt

主要依赖分类：

```
# Web框架
streamlit>=1.28.0
fastapi>=0.104.0
uvicorn>=0.24.0

# 音频处理
librosa>=0.10.1
pydub>=0.25.1
soundfile>=0.12.1

# AI集成
langchain>=0.1.0
langchain-google-genai>=1.0.0
openai>=1.3.0

# 数据处理
numpy>=1.24.0
pandas>=2.1.0
```

---

## 🔐 环境变量 (.env)

**注意**: `.env` 文件不应提交到版本控制

### 必需变量

```env
# AI API配置
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MODEL=gemini-2.0-flash-exp

# 服务配置
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_PORT=8501

# 路径配置
UPLOAD_DIR=./data/uploads
EXPRESSIONS_DIR=./data/expressions
```

### 可选变量

```env
# OpenAI配置（备用）
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# 性能配置
MAX_AUDIO_LENGTH=300
MAX_FILE_SIZE=52428800
```

---

## 📊 项目统计

### 代码规模

- **总代码行数**: ~1,400行（核心代码）
- **后端代码**: ~1,100行
- **前端代码**: ~300行
- **文档**: ~35,000字

### 文件数量

- Python文件: ~30个
- 文档文件: 6个
- 配置文件: 3个
- 脚本文件: 7个

---

## 🔄 版本控制

### .gitignore 关键配置

```gitignore
# Python
__pycache__/
*.pyc
venv/

# 数据文件
data/uploads/*
data/temp/*
data/cache/*
!data/.gitkeep

# 环境变量
.env

# 日志
logs/*.log

# 模型文件（如过大）
models/*.moc3
```

---

## 📖 相关文档

- **主文档**: [README.md](README.md)
- **用户指南**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **开发指南**: [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)
- **文档索引**: [docs/DOC_INDEX.md](docs/DOC_INDEX.md)

---

**版本**: v1.0.0  
**更新日期**: 2024-12  

🎵✨ 清晰的结构，高效的开发！
