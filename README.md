# 歌颜随动 (Geyan-Suidong)

![项目状态](https://img.shields.io/badge/status-development-orange)
![Python版本](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-red)
![Live2D](https://img.shields.io/badge/live2d-web-green)

## 🎵 项目简介

歌颜随动是一个基于 AI 的音乐表情生成系统，能够自动分析音乐的节拍、音调、情感特征，为 Live2D 虚拟角色生成相应的表情动画，实现音乐与虚拟人表情的实时同步。

## ✨ 核心功能

- 🎵 **音频分析**：实时分析音乐的节拍、音调、情感特征
- 🎭 **表情生成**：基于音乐特征生成对应的 Live2D 表情参数
- 🎮 **实时预览**：Live2D 模型与音乐同步播放表情动画
- 💾 **导出功能**：生成可用于 Live2D Web 库的表情文件

## 🏗️ 技术架构

### 后端 (Python + LangChain)

- **音频处理**：librosa, pydub
- **AI 分析**：LangChain + OpenAI/本地模型
- **数据处理**：pandas, numpy
- **API 服务**：FastAPI

### 前端 (Streamlit)

- **工具页面**：音乐上传、参数配置
- **展示页面**：Live2D 模型展示、音乐播放
- **Live2D 集成**：pixi-live2d-display

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- FFmpeg

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/yidong-liu/geyan-suidong-.git
cd geyan-suidong-

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 配置环境变量
# 创建 .env 文件并添加 API 密钥
echo "GOOGLE_API_KEY=your_api_key_here" > .env
echo "GOOGLE_MODEL=gemini-2.0-flash-exp" >> .env

# 4. 启动应用
# 方式1：启动所有服务（推荐）
./start_all.sh

# 方式2：分别启动
./start_backend.sh   # 后端API (端口8000)
./start_frontend.sh  # 前端界面 (端口8501)
```

**访问地址：**
- 前端界面: http://localhost:8501
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📁 项目结构

详细结构请查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

```
geyan-suidong-/
├── backend/                    # 后端服务 (FastAPI)
│   ├── api/                   # API接口
│   │   ├── main.py           # FastAPI主应用
│   │   └── routes/           # 路由模块
│   ├── core/                 # 核心业务逻辑
│   │   ├── audio_analyzer.py      # 音频分析（AI驱动）
│   │   ├── expression_generator.py # 表情生成
│   │   ├── langchain_agent.py     # LangChain代理
│   │   └── live2d_controller.py   # Live2D控制
│   ├── models/               # 数据模型
│   └── utils/                # 工具函数
├── frontend/                 # 前端 (Streamlit)
│   ├── pages/               # 页面
│   │   ├── upload.py       # 上传页面
│   │   ├── realtime.py     # 实时分析
│   │   └── settings.py     # 设置页面
│   ├── components/          # UI组件
│   └── utils/              # 工具函数
├── config/                  # 配置文件
├── data/                   # 数据目录
│   ├── uploads/           # 上传的音频
│   ├── results/           # 分析结果
│   └── expressions/       # 表情数据
├── tests/                  # 测试文件
├── archive/               # 归档文件
├── start_all.sh          # 启动所有服务
├── start_backend.sh      # 启动后端
├── start_frontend.sh     # 启动前端
├── stop_all.sh          # 停止所有服务
├── app.py              # Streamlit主应用
└── requirements.txt    # Python依赖
```

## 🎯 开发路线图

- [X] 项目规划和架构设计
- [X] 后端音频分析模块
- [X] LangChain 表情映射系统
- [X] Streamlit 前端界面
- [X] Live2D 集成和展示
- [ ] 测试和优化
- [ ] 部署和发布

## 📚 文档

- [项目结构说明](PROJECT_STRUCTURE.md) - 详细的项目结构和文件说明
- [清理总结](CLEANUP_SUMMARY.md) - 后端修复和项目清理记录
- [文档索引](DOC_INDEX.md) - 所有文档的索引

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👨‍💻 作者

- [@yidong-liu](https://github.com/yidong-liu)

---

**让歌声拥有表情，让虚拟陪伴真实** 🎵✨
