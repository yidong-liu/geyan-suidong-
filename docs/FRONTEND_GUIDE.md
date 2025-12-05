# Frontend 使用指南

## 快速启动

### 方法1: 启动完整系统（推荐）
```bash
./start_all.sh
```
这将同时启动Backend和Frontend服务。

### 方法2: 单独启动Frontend
```bash
./start_frontend.sh
```
注意：需要先启动Backend服务。

### 方法3: 手动启动
```bash
python -m streamlit run app.py --server.port 8501
```

## 访问地址

- **Frontend Web界面**: http://localhost:8501
- **Backend API文档**: http://localhost:8000/docs

## 功能说明

### 1. 主页 (🏠 首页)

主页展示系统概览和核心功能介绍：
- 音频分析功能
- 表情生成功能
- Live2D展示功能

### 2. 音频上传 (📤 音频上传)

#### 支持的音频格式
- MP3
- WAV
- M4A
- FLAC
- OGG

#### 使用步骤
1. **选择音频文件**
   - 点击文件上传区域
   - 选择您的音频文件
   - 系统会显示文件信息和音频预览

2. **配置处理选项**
   - Live2D模型: 选择要使用的模型
   - 时间分辨率: 调整表情关键帧间隔（0.05-0.5秒）
   - 平滑处理: 是否启用表情过渡平滑
   - 表情敏感度: 调整对音乐变化的敏感程度

3. **开始处理**
   - 点击"🚀 开始分析与生成"按钮
   - 系统会依次执行：
     - 📤 上传文件到服务器
     - 🎵 分析音频特征（节拍、音高、情感等）
     - 🎭 生成Live2D表情动画
   - 处理完成后显示结果统计

4. **查看结果**
   - 音频时长
   - 关键帧数量
   - 检测到的节拍 (BPM)
   - 情感分析结果

### 3. Live2D预览 (👀 Live2D预览)

#### 功能特性
- **模型展示区域**: 显示Live2D模型动画
- **播放控制**: 播放、暂停、停止、重置
- **进度控制**: 拖动滑块查看不同时间点的表情
- **实时参数**: 显示当前帧的表情参数
- **情感分析**: 展示检测到的情感分数

#### 实时参数显示
- 眼睛开合度
- 嘴部开合度
- 眉毛高度
- 脸颊红晕

#### 数据信息
- 表情ID
- 音频时长
- 关键帧数量
- 节拍 (BPM)
- 情感分析结果

#### 导出功能
- 📥 导出表情文件: 获取表情数据JSON文件路径
- 🔄 生成新表情: 返回上传页面处理新音频

### 4. 系统设置 (⚙️ 系统设置)

配置系统参数：
- **音频处理设置**
  - 采样率: 22050 / 44100 / 48000 Hz
  - 跳跃长度: 256 / 512 / 1024

- **表情生成设置**
  - 时间分辨率: 0.01 - 1.0 秒
  - 平滑处理: 启用/禁用

## 工作流程

### 完整使用流程

```
1. 上传音频
   ↓
2. 配置选项
   ↓
3. 开始处理
   ↓
4. 查看结果
   ↓
5. Live2D预览
   ↓
6. 导出/再次处理
```

### 详细步骤

#### 步骤1: 准备音频文件
- 准备一个音频文件（支持的格式）
- 建议时长: 10秒 - 5分钟
- 音质要求: 清晰，无严重噪音

#### 步骤2: 上传和配置
1. 访问 http://localhost:8501
2. 点击侧边栏"📤 音频上传"
3. 上传您的音频文件
4. 调整处理参数
5. 点击"开始分析与生成"

#### 步骤3: 等待处理
系统会自动完成以下步骤：
- 文件上传到服务器
- 音频特征分析（节拍、音高、能量等）
- AI情感分析
- Live2D表情参数生成
- 生成时间序列关键帧

处理时间取决于音频长度，通常：
- 10秒音频: 约5-10秒
- 1分钟音频: 约30-60秒
- 5分钟音频: 约2-5分钟

#### 步骤4: 查看结果
处理完成后，页面会显示：
- ✅ 处理成功提示
- 📊 统计信息（时长、帧数、BPM）
- 🎭 情感分析结果

#### 步骤5: Live2D预览
1. 点击侧边栏"👀 Live2D预览"
2. 查看生成的表情动画
3. 使用播放控制
4. 拖动进度条查看不同时间点
5. 观察实时参数变化

#### 步骤6: 导出或继续
- 点击"导出表情文件"获取JSON文件路径
- 点击"生成新表情"处理新音频

## API集成

Frontend通过API客户端与Backend通信。

### API客户端使用示例

```python
from frontend.utils.api_client import APIClient

# 创建客户端
api_client = APIClient()

# 健康检查
health = api_client.health_check()

# 上传文件
upload_result = api_client.upload_file(file_object)
file_id = upload_result['data']['file_id']

# 分析音频
analyze_result = api_client.analyze_audio(file_id)

# 生成表情
expression_result = api_client.generate_expression(
    file_id=file_id,
    model_name="default",
    time_resolution=0.1,
    enable_smoothing=True
)

# 获取表情数据
expression_id = expression_result['data']['expression_id']
expression_data = api_client.get_expression(expression_id)
```

## 侧边栏功能

### 导航菜单
- 🏠 首页: 系统概览
- 📤 音频上传: 上传和处理音频
- 👀 Live2D预览: 查看表情动画
- ⚙️ 系统设置: 配置参数

### 服务状态
实时显示Backend和Frontend服务状态：
- ✅ 服务正常
- ❌ 服务离线

如果Backend离线，会提示启动命令。

### 项目信息
- 版本号
- 作者信息
- GitHub链接

## 测试

### 运行集成测试
```bash
python test_frontend.py
```

测试内容：
- ✅ Backend服务健康检查
- ✅ Frontend服务健康检查
- ✅ API集成测试（上传、分析、生成、获取）
- ✅ 前端页面可访问性

## 故障排除

### 问题1: Frontend无法启动
```bash
# 检查Streamlit是否安装
python -c "import streamlit"

# 重新安装
pip install streamlit --force-reinstall
```

### 问题2: 无法连接Backend
```bash
# 检查Backend是否运行
curl http://localhost:8000/health

# 启动Backend
./start_backend.sh
```

### 问题3: 端口被占用
```bash
# 查找占用端口的进程
lsof -i :8501

# 停止进程
kill <PID>
```

### 问题4: 页面空白或加载失败
1. 清除浏览器缓存
2. 使用无痕模式访问
3. 检查浏览器控制台错误
4. 重启Frontend服务

### 问题5: 文件上传失败
1. 检查文件格式是否支持
2. 检查文件大小（建议<100MB）
3. 检查Backend服务状态
4. 查看Backend日志: `logs/backend.log`

## 性能优化

### 建议配置
- **时间分辨率**: 
  - 高质量: 0.05秒
  - 标准: 0.1秒
  - 快速: 0.2秒

- **音频长度**:
  - 演示: 10-30秒
  - 正常使用: 1-3分钟
  - 完整歌曲: 3-5分钟

### 浏览器要求
- Chrome 90+ (推荐)
- Firefox 88+
- Safari 14+
- Edge 90+

## 日志文件

- Frontend日志: `logs/frontend.log`
- Backend日志: `logs/backend.log`

查看实时日志:
```bash
# Frontend
tail -f logs/frontend.log

# Backend
tail -f logs/backend.log
```

## 停止服务

### 停止所有服务
```bash
./stop_all.sh
```

### 单独停止
```bash
# 停止Frontend
ps aux | grep "streamlit run app.py" | grep -v grep | awk '{print $2}' | xargs kill

# 停止Backend
ps aux | grep "python -m backend.api.main" | grep -v grep | awk '{print $2}' | xargs kill
```

## 下一步

1. 了解 [Backend API文档](BACKEND_API.md)
2. 查看 [项目架构说明](PROJECT_SETUP_SUMMARY.md)
3. 集成Live2D模型
4. 自定义表情映射规则
5. 添加更多音频分析特性

---

*文档更新于 2025-12-05*
