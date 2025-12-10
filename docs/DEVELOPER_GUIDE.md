# 开发者文档 v1.0

歌颜随动项目开发指南，包含架构说明、环境配置、开发规范等。

## 📚 目录

- [技术架构](#技术架构)
- [环境配置](#环境配置)
- [代码结构](#代码结构)
- [开发指南](#开发指南)
- [测试规范](#测试规范)
- [部署说明](#部署说明)

---

## 🏗️ 技术架构

### 整体架构图

```
┌─────────────────────────────────────────┐
│         Streamlit Frontend              │
│  ┌──────────┐  ┌──────────┐            │
│  │上传页面  │  │预览页面  │            │
│  └────┬─────┘  └────┬─────┘            │
└───────┼─────────────┼──────────────────┘
        │             │
        │ HTTP REST   │
        ▼             ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│  ┌──────────┐  ┌──────────┐            │
│  │上传路由  │  │分析路由  │            │
│  └────┬─────┘  └────┬─────┘            │
│       │             │                   │
│       ▼             ▼                   │
│  ┌─────────────────────────────┐       │
│  │     Core Business Logic      │       │
│  ├─────────────────────────────┤       │
│  │ 音频分析器 (AudioAnalyzer)   │       │
│  │ 表情生成器 (ExpressionGen)   │       │
│  │ LangChain代理 (Agent)        │       │
│  └───────┬──────────────────────┘       │
└──────────┼──────────────────────────────┘
           │
           ▼
    ┌──────────────┐
    │  AI Models   │
    │  - Gemini    │
    │  - OpenAI    │
    └──────────────┘
```

### 技术栈

#### 后端

- **框架**: FastAPI 0.104+
- **音频处理**: librosa, pydub, soundfile
- **AI集成**: LangChain, langchain-google-genai
- **数据处理**: numpy, pandas
- **异步支持**: uvicorn, aiohttp

#### 前端

- **框架**: Streamlit 1.28+
- **UI组件**: streamlit原生组件
- **API客户端**: requests, httpx

#### AI模型

- **主要**: Google Gemini 2.0
- **备选**: OpenAI GPT-4
- **本地**: 可扩展支持本地模型

---

## 🔧 环境配置

### 1. 基础环境

#### 系统要求

- Python 3.8+
- FFmpeg（音频解码）
- Git

#### Python环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. API密钥配置

创建 `.env` 文件：

```env
# Google Gemini API
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MODEL=gemini-2.0-flash-exp

# OpenAI API（可选）
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4

# 服务配置
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_PORT=8501

# 路径配置
UPLOAD_DIR=./data/uploads
EXPRESSIONS_DIR=./data/expressions
TEMP_DIR=./data/temp

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

### 3. 目录结构初始化

```bash
# 创建必要目录
mkdir -p data/{uploads,expressions,temp,cache}
mkdir -p logs
mkdir -p models
```

### 4. 验证安装

```bash
# 检查Python依赖
python -c "import librosa, streamlit, fastapi; print('OK')"

# 检查FFmpeg
ffmpeg -version

# 测试后端
python -m backend.api.main &
curl http://localhost:8000/health

# 测试前端
streamlit run app.py
```

---

## 📁 代码结构

### 目录结构

```
geyan-suidong-/
├── backend/                    # 后端代码
│   ├── api/                   # API层
│   │   ├── main.py           # FastAPI应用入口
│   │   └── routes/           # 路由模块
│   │       ├── upload.py     # 文件上传
│   │       ├── analyze.py    # 音频分析
│   │       └── expression.py # 表情生成
│   ├── core/                 # 核心业务逻辑
│   │   ├── audio_analyzer.py        # 音频分析
│   │   ├── expression_generator.py  # 表情生成
│   │   ├── langchain_agent.py       # AI代理
│   │   └── live2d_controller.py     # Live2D控制
│   ├── models/               # 数据模型
│   │   ├── audio.py         # 音频数据模型
│   │   ├── expression.py    # 表情数据模型
│   │   └── response.py      # API响应模型
│   └── utils/               # 工具函数
│       ├── audio_utils.py   # 音频工具
│       └── file_utils.py    # 文件工具
├── frontend/                 # 前端代码
│   ├── pages/               # Streamlit页面
│   │   └── upload.py        # 上传页面
│   ├── components/          # UI组件
│   │   └── live2d_viewer.py # Live2D查看器
│   └── utils/               # 工具函数
│       └── api_client.py    # API客户端
├── config/                  # 配置文件
│   └── expression_mapping.json
├── data/                    # 数据目录
├── docs/                    # 文档
├── tests/                   # 测试
└── app.py                   # Streamlit主应用
```

### 核心模块说明

#### 1. AudioAnalyzerAgent

音频分析核心类，负责：

- 音频特征提取（节拍、音调、能量）
- AI情感分析
- 时间序列数据构建

```python
# backend/core/audio_analyzer.py
class AudioAnalyzerAgent:
    def analyze_audio(self, audio_path: str) -> AudioFeatures:
        """分析音频返回特征数据"""
        pass
```

#### 2. ExpressionGenerator

表情生成器，负责：

- 整合音频分析和AI生成
- 创建表情关键帧
- 参数平滑处理

```python
# backend/core/expression_generator.py
class ExpressionGenerator:
    def generate_from_audio(self, audio_path: str) -> Dict:
        """从音频生成表情数据"""
        pass
```

#### 3. LangChain Agent

AI表情映射代理，负责：

- 音乐特征到表情的智能映射
- 多模型支持（Gemini/OpenAI）
- Prompt优化

```python
# backend/core/langchain_agent.py
class ExpressionAgentV2:
    def generate_expression_keyframe(self, features: Dict) -> Dict:
        """生成单个表情关键帧"""
        pass
```

---

## 🛠️ 开发指南

### API开发

#### 添加新路由

1. 在 `backend/api/routes/` 创建路由文件
2. 定义路由和处理函数
3. 在 `main.py` 注册路由

```python
# backend/api/routes/new_route.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/new-endpoint")
async def new_endpoint():
    return {"message": "Hello"}

# backend/api/main.py
from backend.api.routes import new_route
app.include_router(new_route.router, prefix="/api/v1", tags=["new"])
```

#### 数据模型定义

使用Pydantic定义请求/响应模型：

```python
# backend/models/custom.py
from pydantic import BaseModel, Field

class CustomRequest(BaseModel):
    field1: str = Field(..., description="字段1")
    field2: int = Field(default=0, ge=0, description="字段2")

class CustomResponse(BaseModel):
    success: bool
    data: dict
```

### 前端开发

#### 添加新页面

```python
# frontend/pages/new_page.py
import streamlit as st

def show():
    st.title("新页面")
    st.write("页面内容")

# app.py中添加
if page == "新页面":
    from frontend.pages import new_page
    new_page.show()
```

#### API调用

```python
# frontend/utils/api_client.py
class APIClient:
    def custom_api_call(self, data):
        response = requests.post(
            f"{self.base_url}/api/v1/custom",
            json=data
        )
        return response.json()
```

### 核心功能扩展

#### 添加新的表情参数

1. 更新 `live2d_expression_mapper.py`
2. 修改参数映射规则
3. 更新配置文件

```python
# backend/core/live2d_expression_mapper.py
EXPRESSION_PARAMETERS = [
    "ParamEyeLOpen",
    "ParamEyeROpen",
    "ParamMouthOpenY",
    # 添加新参数
    "ParamNewParameter"
]
```

#### 集成新AI模型

1. 在 `ai_config.py` 添加模型配置
2. 在 `langchain_agent.py` 添加模型初始化
3. 更新环境变量

```python
# backend/core/ai_config.py
def get_custom_model(api_key: str):
    from langchain_custom import ChatCustomModel
    return ChatCustomModel(api_key=api_key)
```

---

## 🧪 测试规范

### 单元测试

```python
# tests/backend/test_audio_analyzer.py
import pytest
from backend.core.audio_analyzer import AudioAnalyzerAgent

def test_audio_analysis():
    analyzer = AudioAnalyzerAgent()
    result = analyzer.analyze_audio("test_audio.wav")
    
    assert result.duration > 0
    assert result.tempo > 0
    assert len(result.beats) > 0
```

### 集成测试

```python
# tests/integration/test_workflow.py
import pytest
from backend.api.main import app
from fastapi.testclient import TestClient

def test_full_workflow():
    client = TestClient(app)
    
    # 1. 上传
    with open("test.mp3", "rb") as f:
        response = client.post("/api/v1/upload", files={"file": f})
    file_id = response.json()["data"]["file_id"]
    
    # 2. 分析
    response = client.post("/api/v1/analyze", json={"file_id": file_id})
    assert response.status_code == 200
    
    # 3. 生成
    response = client.post(
        "/api/v1/expression/generate",
        json={"file_id": file_id}
    )
    assert response.status_code == 200
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/backend/

# 生成覆盖率报告
pytest --cov=backend --cov-report=html
```

---

## 🚀 部署说明

### 本地部署

```bash
# 使用启动脚本
./start_all.sh

# 或手动启动
./start_backend.sh &
./start_frontend.sh
```

### Docker部署

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000 8501

# 启动命令
CMD ["./start_all.sh"]
```

```bash
# 构建镜像
docker build -t geyan-suidong .

# 运行容器
docker run -p 8000:8000 -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -e GOOGLE_API_KEY=your_key \
  geyan-suidong
```

### 生产环境

#### 使用Nginx反向代理

```nginx
# nginx.conf
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 使用PM2管理进程

```bash
# 安装PM2
npm install -g pm2

# 启动服务
pm2 start start_backend.sh --name backend
pm2 start start_frontend.sh --name frontend

# 保存配置
pm2 save

# 开机自启
pm2 startup
```

---

## 📊 性能优化

### 后端优化

1. **音频处理优化**
   - 使用多进程并行处理
   - 缓存常用分析结果
   - 限制音频文件大小

2. **AI调用优化**
   - 批量处理请求
   - 实现请求队列
   - 添加重试机制

3. **文件管理**
   - 定期清理临时文件
   - 实现文件压缩存储
   - 使用CDN加速访问

### 前端优化

1. **加载优化**
   - 懒加载大文件
   - 压缩静态资源
   - 使用缓存策略

2. **渲染优化**
   - 减少不必要的重渲染
   - 优化Live2D模型大小
   - 使用Web Workers处理数据

---

## 🔍 调试技巧

### 日志查看

```bash
# 后端日志
tail -f logs/backend.log

# 前端日志
tail -f logs/frontend.log
```

### 开启调试模式

```python
# backend/api/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### API调试

```bash
# 使用httpie
http POST localhost:8000/api/v1/upload file@test.mp3

# 使用curl
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@test.mp3"
```

---

## 📝 代码规范

### Python代码风格

- 遵循PEP 8
- 使用Black格式化
- 使用类型注解

```python
def process_audio(
    file_path: str,
    sample_rate: int = 44100
) -> Dict[str, Any]:
    """处理音频文件
    
    Args:
        file_path: 文件路径
        sample_rate: 采样率
        
    Returns:
        处理结果字典
    """
    pass
```

### 文档字符串

使用Google风格文档字符串：

```python
def function(arg1: str, arg2: int) -> bool:
    """函数简短描述
    
    详细描述（可选）
    
    Args:
        arg1: 参数1说明
        arg2: 参数2说明
        
    Returns:
        返回值说明
        
    Raises:
        ValueError: 错误情况说明
    """
    pass
```

---

## 🔗 相关资源

- **用户文档**: [USER_GUIDE.md](USER_GUIDE.md)
- **API文档**: [API_REFERENCE.md](API_REFERENCE.md)
- **表情格式**: [EXPRESSION_FORMAT.md](EXPRESSION_FORMAT.md)

---

**版本**: v1.0.0  
**更新日期**: 2024-12  
**维护者**: [@yidong-liu](https://github.com/yidong-liu)
