# Backend API 使用指南

## 快速启动

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务

**方式一：使用启动脚本**
```bash
./start_backend.sh
```

**方式二：手动启动**
```bash
python -m backend.api.main
```

服务将在 `http://localhost:8000` 上运行

### 3. 测试服务
```bash
python test_backend.py
```

## API端点

### 1. 健康检查
```bash
GET /health
```

响应示例：
```json
{
  "status": "healthy",
  "service": "geyan-suidong-api"
}
```

### 2. 文件上传
```bash
POST /api/v1/upload
Content-Type: multipart/form-data
```

参数：
- `file`: 音频文件（支持 .mp3, .wav, .m4a, .flac, .ogg）

响应示例：
```json
{
  "success": true,
  "message": "文件上传成功",
  "data": {
    "file_id": "uuid",
    "filename": "audio.wav",
    "file_path": "data/uploads/uuid.wav",
    "file_size": 264644
  }
}
```

### 3. 音频分析
```bash
POST /api/v1/analyze
Content-Type: application/json
```

请求体：
```json
{
  "file_id": "uuid",
  "sample_rate": 44100,
  "hop_length": 512
}
```

响应示例：
```json
{
  "success": true,
  "message": "音频分析完成",
  "data": {
    "file_id": "uuid",
    "duration": 3.0,
    "tempo": 120.0,
    "beat_count": 10,
    "beats": [0.5, 1.0, 1.5, ...],
    "emotion_scores": {
      "happy": 0.3,
      "sad": 0.2,
      "energetic": 0.4,
      "calm": 0.1,
      "angry": 0.0
    },
    "energy_stats": {
      "mean": 0.5,
      "max": 1.0,
      "min": 0.1
    },
    "spectral_stats": {
      "mean": 0.6,
      "max": 1.0,
      "min": 0.2
    }
  }
}
```

### 4. 表情生成
```bash
POST /api/v1/generate
Content-Type: application/json
```

请求体：
```json
{
  "file_id": "uuid",
  "model_name": "default",
  "time_resolution": 0.1,
  "enable_smoothing": true
}
```

响应示例：
```json
{
  "success": true,
  "message": "表情生成完成",
  "data": {
    "expression_id": "uuid",
    "file_id": "uuid",
    "model_name": "default",
    "expression_path": "data/expressions/uuid.json",
    "duration": 3.0,
    "tempo": 120.0,
    "keyframe_count": 30,
    "emotion_scores": {...}
  }
}
```

### 5. 获取表情数据
```bash
GET /api/v1/expression/{expression_id}
```

响应示例：
```json
{
  "success": true,
  "message": "表情数据获取成功",
  "data": {
    "duration": 3.0,
    "tempo": 120.0,
    "emotion_scores": {...},
    "expressions": [
      {
        "timestamp": 0.0,
        "parameters": {
          "eye_open": 1.0,
          "mouth_open": 0.5,
          "eyebrow_height": 0.5,
          ...
        }
      },
      ...
    ]
  }
}
```

### 6. 删除文件
```bash
DELETE /api/v1/upload/{file_id}
```

响应示例：
```json
{
  "success": true,
  "message": "文件删除成功",
  "data": {
    "file_id": "uuid"
  }
}
```

## 完整使用流程

1. **上传音频文件**
```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@audio.wav"
```

2. **分析音频**
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"file_id": "your-file-id"}'
```

3. **生成表情**
```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"file_id": "your-file-id"}'
```

4. **获取表情数据**
```bash
curl http://localhost:8000/api/v1/expression/your-expression-id
```

## 项目结构

```
backend/
├── api/
│   ├── main.py              # FastAPI应用主入口
│   └── routes/              # API路由
│       ├── upload.py        # 文件上传路由
│       ├── analyze.py       # 音频分析路由
│       └── expression.py    # 表情生成路由
├── core/                    # 核心业务逻辑
│   ├── audio_analyzer.py    # 音频分析器
│   ├── expression_generator.py  # 表情生成器
│   ├── langchain_agent.py   # LangChain代理
│   └── live2d_controller.py # Live2D控制器
├── models/                  # 数据模型
│   ├── audio.py
│   ├── expression.py
│   └── response.py
└── utils/                   # 工具函数
    ├── config.py
    ├── audio_utils.py
    └── file_utils.py
```

## 开发指南

### 添加新的API端点

1. 在 `backend/api/routes/` 中创建新路由文件
2. 定义路由和处理函数
3. 在 `backend/api/main.py` 中注册路由

### 修改配置

配置文件位于 `backend/utils/config.py`

### 日志

日志输出到控制台，可以通过修改 `backend/api/main.py` 中的日志配置来调整日志级别

## API文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 故障排除

### 端口被占用
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill <PID>
```

### 依赖问题
```bash
# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### 权限问题
```bash
# 确保数据目录有写权限
chmod -R 755 data/
```

## 性能优化

- 音频分析是CPU密集型操作，建议在生产环境中使用多进程或异步任务队列
- 对于大文件，考虑增加超时时间
- 生产环境建议使用 Gunicorn + Uvicorn 作为ASGI服务器

```bash
gunicorn backend.api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```
