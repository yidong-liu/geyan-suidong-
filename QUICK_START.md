# 🚀 快速开始 - 歌颜随动

> 让歌声拥有表情，让虚拟陪伴真实 🎵✨

## ⚡ 5秒启动

```bash
# 一键启动所有服务
./start_all.sh

# 访问Web界面
open http://localhost:8501
```

就这么简单！🎉

---

## 📋 前置要求

- Python 3.8+
- 已安装依赖: `pip install -r requirements.txt`

---

## 🎯 系统状态

当前系统已完全配置并可运行：

- ✅ Backend API: `http://localhost:8000`
- ✅ Frontend Web: `http://localhost:8501`
- ✅ 所有测试通过: 11/11
- ✅ 文档完整

---

## �� 使用流程

### 1️⃣ 启动系统
```bash
./start_all.sh
```

### 2️⃣ 打开浏览器
访问: http://localhost:8501

### 3️⃣ 上传音频
- 点击 "📤 音频上传"
- 选择音频文件（MP3/WAV/M4A/FLAC/OGG）
- 配置处理选项
- 点击 "🚀 开始分析与生成"

### 4️⃣ 查看结果
- 查看音频分析结果
- 查看情感分析
- 切换到 "👀 Live2D预览"

### 5️⃣ 预览表情
- 使用播放控制
- 查看实时参数
- 导出表情文件

### 6️⃣ 停止系统
```bash
./stop_all.sh
```

---

## 🧪 运行测试

### Backend测试
```bash
python test_backend.py
```

### 前端集成测试
```bash
python test_frontend.py
```

### 健康检查
```bash
python monitor_backend.py
```

---

## 📚 详细文档

### 快速参考
- [项目完成报告](PROJECT_COMPLETE.md) - 完整状态总览
- [Backend就绪](BACKEND_READY.md) - Backend快速开始
- [Frontend就绪](FRONTEND_READY.md) - Frontend快速开始

### 使用指南
- [Backend API文档](docs/BACKEND_API.md) - API完整文档
- [Frontend使用指南](docs/FRONTEND_GUIDE.md) - Web界面使用

### 技术文档
- [Backend详细状态](BACKEND_STATUS.md) - 技术细节
- [项目设置总结](PROJECT_SETUP_SUMMARY.md) - 架构说明

---

## 🛠️ 可用脚本

| 脚本 | 说明 |
|------|------|
| `./start_all.sh` | 启动Backend和Frontend |
| `./start_backend.sh` | 仅启动Backend |
| `./start_frontend.sh` | 仅启动Frontend |
| `./stop_all.sh` | 停止所有服务 |
| `python test_backend.py` | Backend功能测试 |
| `python test_frontend.py` | 集成测试 |
| `python monitor_backend.py` | 服务监控 |

---

## 🔧 故障排除

### 端口被占用
```bash
./stop_all.sh
./start_all.sh
```

### Backend无法连接
```bash
curl http://localhost:8000/health
```

### Frontend无法访问
```bash
curl http://localhost:8501/_stcore/health
```

### 重新安装依赖
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📊 功能特性

### 🎵 音频分析
- 支持多种格式
- 节拍检测
- 音高分析
- 情感识别

### 🎭 表情生成
- AI驱动映射
- 时间序列关键帧
- 平滑处理
- 实时预览

### 👀 Live2D展示
- 模型展示
- 播放控制
- 实时参数
- 数据导出

---

## 🎯 性能数据

- 上传速度: < 1秒
- 分析时间: 2-5秒 (3秒音频)
- 生成时间: 3-6秒
- API响应: < 100ms

---

## 💡 提示

1. **首次使用**: 建议使用短音频（10-30秒）测试
2. **最佳体验**: 使用Chrome浏览器
3. **查看日志**: `tail -f logs/*.log`
4. **API文档**: http://localhost:8000/docs

---

## 📞 帮助

遇到问题？查看：
- [常见问题](docs/FRONTEND_GUIDE.md#故障排除)
- [API文档](docs/BACKEND_API.md)
- [项目完成报告](PROJECT_COMPLETE.md)

---

**现在就开始体验吧！** 🚀

```bash
./start_all.sh
```

然后访问: http://localhost:8501 🎨
