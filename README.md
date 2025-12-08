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
cp .env.example .env
# 编辑 .env 文件，添加必要的API密钥

# 4. 启动应用
streamlit run app.py
```

## 📁 项目结构

```
geyan-suidong-/
├── backend/                    # 后端服务
│   ├── core/                  # 核心模块
│   │   ├── audio_analyzer.py  # 音频分析
│   │   ├── expression_generator.py # 表情生成
│   │   └── langchain_agent.py # LangChain代理
│   ├── api/                   # API接口
│   │   └── main.py           # FastAPI主应用
│   └── utils/                 # 工具函数
├── frontend/                  # 前端页面
│   ├── pages/                # Streamlit页面
│   │   ├── upload.py        # 上传页面
│   │   └── preview.py       # 预览页面
│   ├── components/           # 组件
│   └── static/              # 静态资源
├── models/                   # Live2D模型
├── data/                    # 数据文件
├── docs/                    # 文档
├── tests/                   # 测试
├── requirements.txt         # Python依赖
├── app.py                  # Streamlit主应用
└── .env.example            # 环境变量模板
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

- [开发环境配置](docs/development.md)
- [后端开发指南](docs/backend_guide.md)
- [前端开发指南](docs/frontend_guide.md)
- [API 文档](docs/api.md)
- [部署指南](docs/deployment.md)

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
