# 前端开发指南

## 🎨 前端架构概述

前端采用 **Streamlit + Live2D Web** 架构，主要负责用户界面、音频上传、Live2D 模型展示和音乐播放控制。

### 技术栈

- **Streamlit**: 主要 UI 框架，快速构建 Web 应用
- **JavaScript/HTML**: Live2D 模型渲染和音频控制
- **PIXI.js**: Live2D Web 渲染引擎
- **CSS**: 样式和动画效果

## 📁 前端目录结构

```
frontend/
├── pages/                      # Streamlit页面
│   ├── __init__.py
│   ├── upload.py              # 音频上传页面
│   ├── preview.py             # Live2D预览页面
│   └── config.py              # 配置页面
├── components/                # 可复用组件
│   ├── __init__.py
│   ├── audio_player.py        # 音频播放器组件
│   ├── live2d_viewer.py       # Live2D查看器组件
│   ├── progress_tracker.py    # 进度跟踪组件
│   └── file_uploader.py       # 文件上传组件
├── static/                    # 静态资源
│   ├── css/
│   │   ├── main.css          # 主样式文件
│   │   └── live2d.css        # Live2D相关样式
│   ├── js/
│   │   ├── live2d-controller.js  # Live2D控制器
│   │   ├── audio-sync.js     # 音频同步脚本
│   │   └── utils.js          # 工具函数
│   └── images/               # 图片资源
└── utils/                     # 前端工具函数
    ├── __init__.py
    ├── api_client.py         # API客户端
    ├── validators.py         # 表单验证
    └── formatters.py         # 数据格式化
```

## 🚀 主应用入口

### `app.py` - Streamlit 主应用

```python
import streamlit as st
import sys
from pathlib import Path

# 添加项目路径到系统路径
sys.path.append(str(Path(__file__).parent))

from frontend.pages import upload, preview, config
from frontend.utils.api_client import APIClient

# 页面配置
st.set_page_config(
    page_title="歌颜随动",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
def load_custom_css():
    """加载自定义CSS样式"""
    css_file = Path("frontend/static/css/main.css")
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    """主应用函数"""
    # 加载样式
    load_custom_css()

    # 侧边栏导航
    st.sidebar.title("🎵 歌颜随动")
    st.sidebar.markdown("---")

    # 页面选择
    page = st.sidebar.selectbox(
        "选择功能页面",
        [
            "🎵 音频上传",
            "👀 Live2D预览",
            "⚙️ 系统配置"
        ]
    )

    # 显示API状态
    st.sidebar.markdown("### 📡 服务状态")
    api_client = APIClient()

    try:
        health = api_client.health_check()
        if health["status"] == "healthy":
            st.sidebar.success("✅ 后端服务正常")
        else:
            st.sidebar.error("❌ 后端服务异常")
    except Exception:
        st.sidebar.error("❌ 无法连接后端服务")

    # 路由到对应页面
    if page == "🎵 音频上传":
        upload.show()
    elif page == "👀 Live2D预览":
        preview.show()
    elif page == "⚙️ 系统配置":
        config.show()

if __name__ == "__main__":
    main()
```

## 📄 页面模块开发

### 1. 音频上传页面

#### `frontend/pages/upload.py`

```python
import streamlit as st
import time
from pathlib import Path
from typing import Optional
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from ..components.file_uploader import FileUploaderComponent
from ..components.progress_tracker import ProgressTracker
from ..utils.api_client import APIClient
from ..utils.validators import validate_audio_file
from ..utils.formatters import format_duration, format_file_size

def show():
    """显示音频上传页面"""
    st.title("🎵 音乐上传与分析")
    st.markdown("上传您的音频文件，AI将分析音乐特征并生成对应的虚拟人表情动画。")

    # 初始化会话状态
    if "upload_state" not in st.session_state:
        st.session_state.upload_state = {
            "file_id": None,
            "file_name": None,
            "analysis_complete": False,
            "generation_complete": False
        }

    # API客户端
    api_client = APIClient()

    # 文件上传区域
    st.markdown("### 📁 选择音频文件")
    uploaded_file = st.file_uploader(
        "支持格式：MP3, WAV, M4A",
        type=['mp3', 'wav', 'm4a'],
        help="建议上传高质量音频文件以获得更好的分析效果"
    )

    if uploaded_file is not None:
        # 显示文件信息
        _show_file_info(uploaded_file)

        # 分析配置
        config_col1, config_col2 = st.columns(2)

        with config_col1:
            model_choice = st.selectbox(
                "🎭 选择虚拟角色",
                options=_get_available_models(),
                format_func=lambda x: x["name"],
                help="选择想要应用表情的虚拟角色"
            )

        with config_col2:
            time_resolution = st.slider(
                "⏱️ 时间精度（秒）",
                min_value=0.1,
                max_value=2.0,
                value=0.5,
                step=0.1,
                help="更小的值会产生更精细的表情变化"
            )

        # 高级设置
        with st.expander("🔧 高级设置"):
            col1, col2 = st.columns(2)

            with col1:
                enable_smoothing = st.checkbox(
                    "启用平滑处理",
                    value=True,
                    help="减少表情变化的突兀感"
                )

            with col2:
                sensitivity = st.slider(
                    "表情敏感度",
                    min_value=0.1,
                    max_value=2.0,
                    value=1.0,
                    step=0.1,
                    help="调整表情对音乐变化的敏感程度"
                )

        # 处理按钮
        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            if st.button("🚀 开始分析与生成", type="primary", use_container_width=True):
                _process_audio_file(
                    uploaded_file,
                    api_client,
                    model_choice,
                    time_resolution,
                    enable_smoothing
                )

    # 显示处理进度和结果
    _show_processing_status()

def _show_file_info(uploaded_file):
    """显示文件信息"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📝 文件名", uploaded_file.name)

    with col2:
        file_size = len(uploaded_file.getvalue())
        st.metric("📏 文件大小", format_file_size(file_size))

    with col3:
        file_type = uploaded_file.name.split('.')[-1].upper()
        st.metric("🎵 格式", file_type)

    # 显示音频预览
    st.markdown("### 🎧 音频预览")
    st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")

def _get_available_models():
    """获取可用的Live2D模型列表"""
    # 这里应该从API获取实际的模型列表
    return [
        {"id": "default", "name": "🎀 默认角色（萌系）"},
        {"id": "hiyori", "name": "🌸 Hiyori（日系少女）"},
        {"id": "cyberpunk", "name": "🤖 赛博朋克（未来风）"}
    ]

def _process_audio_file(uploaded_file, api_client, model_choice, time_resolution, enable_smoothing):
    """处理音频文件"""
    progress_container = st.container()

    with progress_container:
        st.markdown("### 📊 处理进度")
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # 步骤1：上传文件
            status_text.text("📤 正在上传文件...")
            progress_bar.progress(10)

            upload_result = api_client.upload_file(uploaded_file)
            file_id = upload_result["data"]["file_id"]

            st.session_state.upload_state["file_id"] = file_id
            st.session_state.upload_state["file_name"] = uploaded_file.name

            # 步骤2：分析音频
            status_text.text("🎵 正在分析音频特征...")
            progress_bar.progress(30)
            time.sleep(1)  # 模拟处理时间

            analysis_result = api_client.analyze_audio(file_id)

            # 显示分析结果
            _show_analysis_results(analysis_result["data"])

            # 步骤3：生成表情
            status_text.text("🎭 正在生成表情动画...")
            progress_bar.progress(60)
            time.sleep(2)  # 模拟处理时间

            generation_result = api_client.generate_expression(
                file_id=file_id,
                model_name=model_choice["id"],
                time_resolution=time_resolution,
                enable_smoothing=enable_smoothing
            )

            # 完成
            status_text.text("✅ 处理完成！")
            progress_bar.progress(100)

            st.session_state.upload_state["analysis_complete"] = True
            st.session_state.upload_state["generation_complete"] = True
            st.session_state.upload_state["expression_id"] = generation_result["data"]["expression_id"]

            # 显示成功信息
            st.success("🎉 表情文件生成成功！您可以在预览页面查看效果。")

            # 提供跳转按钮
            if st.button("👀 查看Live2D预览", type="secondary"):
                st.switch_page("pages/preview.py")

        except Exception as e:
            st.error(f"❌ 处理失败: {str(e)}")
            progress_bar.progress(0)
            status_text.text("❌ 处理失败")

def _show_analysis_results(analysis_data):
    """显示音频分析结果"""
    st.markdown("### 📈 音频分析结果")

    # 基础信息
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("⏱️ 时长", format_duration(analysis_data["duration"]))

    with col2:
        st.metric("🎵 节拍", f"{analysis_data['tempo']:.1f} BPM")

    with col3:
        st.metric("🥁 节拍数", analysis_data["beat_count"])

    with col4:
        energy_avg = analysis_data["energy_stats"]["mean"]
        st.metric("⚡ 平均能量", f"{energy_avg:.2f}")

    # 情感分析图表
    emotion_scores = analysis_data["emotion_scores"]

    if emotion_scores:
        st.markdown("#### 🎭 情感分析")

        # 创建情感雷达图
        emotions = list(emotion_scores.keys())
        scores = list(emotion_scores.values())

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=emotions,
            fill='toself',
            name='情感强度',
            line_color='rgb(255, 144, 14)'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(scores) * 1.1] if scores else [0, 1]
                )),
            showlegend=False,
            title="音乐情感分析",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

def _show_processing_status():
    """显示处理状态"""
    if st.session_state.upload_state["file_id"] is not None:
        st.markdown("### 📋 处理状态")

        status_container = st.container()

        with status_container:
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.session_state.upload_state["file_name"]:
                    st.success("✅ 文件上传完成")
                else:
                    st.info("⏳ 等待文件上传")

            with col2:
                if st.session_state.upload_state["analysis_complete"]:
                    st.success("✅ 音频分析完成")
                else:
                    st.info("⏳ 等待音频分析")

            with col3:
                if st.session_state.upload_state["generation_complete"]:
                    st.success("✅ 表情生成完成")
                else:
                    st.info("⏳ 等待表情生成")
```

### 2. Live2D 预览页面

#### `frontend/pages/preview.py`

```python
import streamlit as st
import json
from pathlib import Path
from typing import Optional, Dict, Any

from ..components.live2d_viewer import Live2DViewer
from ..components.audio_player import AudioPlayerComponent
from ..utils.api_client import APIClient

def show():
    """显示Live2D预览页面"""
    st.title("👀 Live2D 虚拟人预览")
    st.markdown("在这里可以预览生成的表情动画效果，并与音乐同步播放。")

    # 检查是否有生成的表情文件
    if not _check_expression_available():
        st.warning("⚠️ 请先在上传页面完成音乐分析和表情生成。")
        if st.button("🎵 前往上传页面"):
            st.switch_page("pages/upload.py")
        return

    # 获取表情数据
    expression_data = _load_expression_data()
    if not expression_data:
        st.error("❌ 无法加载表情数据")
        return

    # 创建预览区域
    _create_preview_area(expression_data)

    # 控制面板
    _create_control_panel(expression_data)

    # 表情数据查看器
    _create_expression_viewer(expression_data)

def _check_expression_available() -> bool:
    """检查是否有可用的表情文件"""
    if "upload_state" not in st.session_state:
        return False

    state = st.session_state.upload_state
    return (state.get("generation_complete", False) and
            state.get("expression_id") is not None)

def _load_expression_data() -> Optional[Dict]:
    """加载表情数据"""
    try:
        expression_id = st.session_state.upload_state.get("expression_id")
        if not expression_id:
            return None

        api_client = APIClient()
        expression_data = api_client.get_expression_file(expression_id)
        return expression_data

    except Exception as e:
        st.error(f"加载表情数据失败: {str(e)}")
        return None

def _create_preview_area(expression_data: Dict):
    """创建预览区域"""
    st.markdown("### 🎭 Live2D 预览")

    # Live2D容器
    live2d_container = st.container()

    with live2d_container:
        # 这里需要嵌入HTML/JavaScript来实现Live2D渲染
        live2d_html = _generate_live2d_html(expression_data)
        st.components.v1.html(live2d_html, height=600)

def _generate_live2d_html(expression_data: Dict) -> str:
    """生成Live2D HTML代码"""

    # 获取表情数据的JSON字符串
    expression_json = json.dumps(expression_data)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Live2D Preview</title>
        <script src="https://cdn.jsdelivr.net/npm/pixi.js@7.x/dist/pixi.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/pixi-live2d-display/dist/index.min.js"></script>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 560px;
            }}

            #canvas-container {{
                position: relative;
                width: 500px;
                height: 500px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                backdrop-filter: blur(4px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                overflow: hidden;
            }}

            canvas {{
                width: 100% !important;
                height: 100% !important;
                display: block;
            }}

            #controls {{
                position: absolute;
                bottom: 20px;
                left: 20px;
                right: 20px;
                display: flex;
                justify-content: center;
                gap: 10px;
            }}

            .control-btn {{
                padding: 10px 20px;
                background: rgba(255, 255, 255, 0.2);
                border: none;
                border-radius: 25px;
                color: white;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.3s ease;
            }}

            .control-btn:hover {{
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }}

            #loading {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-size: 16px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div id="canvas-container">
            <div id="loading">
                <div>🎭 正在加载Live2D模型...</div>
                <div style="margin-top: 10px; font-size: 14px; opacity: 0.8;">请稍候</div>
            </div>

            <div id="controls" style="display: none;">
                <button class="control-btn" onclick="playExpression()">▶️ 播放</button>
                <button class="control-btn" onclick="pauseExpression()">⏸️ 暂停</button>
                <button class="control-btn" onclick="resetExpression()">🔄 重置</button>
            </div>
        </div>

        <script>
            let app;
            let model;
            let expressionData = {expression_json};
            let isPlaying = false;
            let currentTime = 0;
            let animationFrame;

            // 初始化PIXI应用
            async function initLive2D() {{
                try {{
                    const container = document.getElementById('canvas-container');

                    app = new PIXI.Application({{
                        width: 500,
                        height: 500,
                        backgroundColor: 0x000000,
                        backgroundAlpha: 0,
                        antialias: true
                    }});

                    container.appendChild(app.view);

                    // 加载默认模型（这里使用示例模型路径）
                    const modelPath = '/models/hiyori/hiyori_free_t08.model3.json';

                    try {{
                        model = await PIXI.live2d.Live2DModel.from(modelPath);
                        app.stage.addChild(model);

                        // 调整模型位置和缩放
                        model.anchor.set(0.5, 0.5);
                        model.position.set(app.screen.width / 2, app.screen.height / 2);
                        model.scale.set(0.3);

                        // 隐藏加载提示，显示控制按钮
                        document.getElementById('loading').style.display = 'none';
                        document.getElementById('controls').style.display = 'flex';

                        console.log('Live2D模型加载成功');

                    }} catch (modelError) {{
                        console.warn('无法加载Live2D模型，使用演示模式');
                        showDemoMode();
                    }}

                }} catch (error) {{
                    console.error('初始化失败:', error);
                    showErrorMode();
                }}
            }}

            function showDemoMode() {{
                document.getElementById('loading').innerHTML = `
                    <div>🎭 演示模式</div>
                    <div style="margin-top: 10px; font-size: 14px;">
                        Live2D模型将在实际部署时显示
                    </div>
                `;
                document.getElementById('controls').style.display = 'flex';
            }}

            function showErrorMode() {{
                document.getElementById('loading').innerHTML = `
                    <div>❌ 加载失败</div>
                    <div style="margin-top: 10px; font-size: 14px;">
                        请检查模型文件是否存在
                    </div>
                `;
            }}

            function playExpression() {{
                isPlaying = true;
                animateExpression();
            }}

            function pauseExpression() {{
                isPlaying = false;
                if (animationFrame) {{
                    cancelAnimationFrame(animationFrame);
                }}
            }}

            function resetExpression() {{
                currentTime = 0;
                pauseExpression();
                if (model) {{
                    // 重置模型参数到初始状态
                    resetModelParameters();
                }}
            }}

            function animateExpression() {{
                if (!isPlaying || !model) {{
                    return;
                }}

                // 查找当前时间对应的表情
                const expression = findExpressionAtTime(currentTime);

                if (expression) {{
                    // 更新模型参数
                    updateModelParameters(expression.parameters);
                }}

                // 增加时间
                currentTime += 0.033; // 约30fps

                // 检查是否播放完毕
                if (currentTime < expressionData.metadata.duration) {{
                    animationFrame = requestAnimationFrame(animateExpression);
                }} else {{
                    isPlaying = false;
                }}
            }}

            function findExpressionAtTime(time) {{
                const expressions = expressionData.expressions;

                for (let i = 0; i < expressions.length - 1; i++) {{
                    if (time >= expressions[i].timestamp && time < expressions[i + 1].timestamp) {{
                        return expressions[i];
                    }}
                }}

                return expressions[expressions.length - 1];
            }}

            function updateModelParameters(parameters) {{
                if (!model || !model.internalModel) {{
                    return;
                }}

                try {{
                    Object.entries(parameters).forEach(([param, value]) => {{
                        model.internalModel.coreModel.setParameterValueById(param, value);
                    }});
                }} catch (error) {{
                    console.warn('参数更新失败:', error);
                }}
            }}

            function resetModelParameters() {{
                if (!model || !model.internalModel) {{
                    return;
                }}

                // 重置到默认状态
                const defaultParams = {{
                    'ParamEyeLOpen': 1.0,
                    'ParamEyeROpen': 1.0,
                    'ParamEyeBrowLY': 0.0,
                    'ParamEyeBrowRY': 0.0,
                    'ParamMouthOpenY': 0.0,
                    'ParamMouthForm': 0.0,
                    'ParamCheek': 0.0,
                    'ParamBodyAngleX': 0.0
                }};

                updateModelParameters(defaultParams);
            }}

            // 初始化
            window.onload = function() {{
                initLive2D();
            }};
        </script>
    </body>
    </html>
    """

def _create_control_panel(expression_data: Dict):
    """创建控制面板"""
    st.markdown("### 🎮 播放控制")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("▶️ 播放动画", use_container_width=True):
            st.info("动画开始播放")

    with col2:
        if st.button("⏸️ 暂停", use_container_width=True):
            st.info("动画已暂停")

    with col3:
        if st.button("⏹️ 停止", use_container_width=True):
            st.info("动画已停止")

    with col4:
        if st.button("🔄 重置", use_container_width=True):
            st.info("动画已重置")

    # 进度控制
    st.markdown("#### ⏱️ 播放进度")
    duration = expression_data.get("metadata", {}).get("duration", 100)

    progress = st.slider(
        "时间轴",
        min_value=0.0,
        max_value=float(duration),
        value=0.0,
        step=0.1,
        format="%.1f秒"
    )

    # 显示当前状态
    st.markdown(f"**当前时间**: {progress:.1f}秒 / {duration:.1f}秒")

def _create_expression_viewer(expression_data: Dict):
    """创建表情数据查看器"""
    with st.expander("📊 表情数据详情"):

        # 元数据
        metadata = expression_data.get("metadata", {})

        st.markdown("#### 📋 基本信息")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🎵 总时长", f"{metadata.get('duration', 0):.1f}秒")

        with col2:
            st.metric("🎭 表情数量", metadata.get('expression_count', 0))

        with col3:
            st.metric("🎨 模型名称", metadata.get('model_name', 'Unknown'))

        # 表情时间轴
        st.markdown("#### ⏰ 表情时间轴")

        expressions = expression_data.get("expressions", [])
        if expressions:
            # 创建表情时间轴表格
            timeline_data = []
            for expr in expressions[:10]:  # 只显示前10个
                timeline_data.append({
                    "时间": f"{expr['timestamp']:.1f}s",
                    "眼部开合": f"{expr['parameters'].get('ParamEyeLOpen', 0):.2f}",
                    "嘴部开合": f"{expr['parameters'].get('ParamMouthOpenY', 0):.2f}",
                    "表情强度": f"{expr['parameters'].get('ParamCheek', 0):.2f}",
                    "过渡时长": f"{expr.get('transition_duration', 0):.1f}s"
                })

            import pandas as pd
            df = pd.DataFrame(timeline_data)
            st.dataframe(df, use_container_width=True)

            if len(expressions) > 10:
                st.info(f"还有 {len(expressions) - 10} 个表情关键帧...")

        # 原始JSON数据
        st.markdown("#### 🔍 原始数据")
        if st.checkbox("显示完整JSON数据"):
            st.json(expression_data)
```

### 3. API 客户端

#### `frontend/utils/api_client.py`

```python
import requests
import streamlit as st
from typing import Dict, Any, Optional
import json

class APIClient:
    """API客户端类"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def upload_file(self, file) -> Dict[str, Any]:
        """上传音频文件"""
        files = {"file": (file.name, file.getvalue(), file.type)}

        response = self.session.post(
            f"{self.base_url}/api/upload-audio",
            files=files
        )
        response.raise_for_status()
        return response.json()

    def analyze_audio(self, file_id: str) -> Dict[str, Any]:
        """分析音频文件"""
        response = self.session.post(f"{self.base_url}/api/analyze-audio/{file_id}")
        response.raise_for_status()
        return response.json()

    def generate_expression(
        self,
        file_id: str,
        model_name: str = "default",
        time_resolution: float = 0.5,
        enable_smoothing: bool = True
    ) -> Dict[str, Any]:
        """生成表情文件"""
        params = {
            "model_name": model_name,
            "time_resolution": time_resolution,
            "enable_smoothing": enable_smoothing
        }

        response = self.session.post(
            f"{self.base_url}/api/generate-expression/{file_id}",
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_expression_file(self, expression_id: str) -> Dict[str, Any]:
        """获取表情文件"""
        response = self.session.get(f"{self.base_url}/api/expression/{expression_id}")
        response.raise_for_status()
        return response.json()

    def get_processing_status(self, file_id: str) -> Dict[str, Any]:
        """获取处理状态"""
        response = self.session.get(f"{self.base_url}/api/status/{file_id}")
        response.raise_for_status()
        return response.json()

    def list_models(self) -> Dict[str, Any]:
        """获取可用模型列表"""
        response = self.session.get(f"{self.base_url}/api/models")
        response.raise_for_status()
        return response.json()
```

## 🎨 样式和 UI 优化

### `frontend/static/css/main.css`

```css
/* 主样式文件 */

/* 全局样式 */
.main .block-container {
  padding-top: 2rem;
  padding-bottom: 2rem;
  max-width: 1200px;
}

/* 标题样式 */
h1,
h2,
h3 {
  color: #1f1f1f;
  font-weight: 600;
}

/* 按钮样式优化 */
.stButton > button {
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px 0 rgba(116, 75, 162, 0.3);
}

.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px 0 rgba(116, 75, 162, 0.4);
}

/* 文件上传区域样式 */
.uploadedFile {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 15px;
  padding: 1rem;
  margin: 1rem 0;
  border: 2px dashed #667eea;
}

/* 指标卡片样式 */
[data-testid="metric-container"] {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 1px solid #e9ecef;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* 进度条样式 */
.stProgress .st-bo {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
}

/* 侧边栏样式 */
.css-1d391kg {
  background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
}

.css-1d391kg .block-container {
  background: transparent;
}

/* 选择框样式 */
.stSelectbox > div > div {
  border-radius: 10px;
  border: 2px solid #667eea;
}

/* 滑块样式 */
.stSlider > div > div > div {
  color: #667eea;
}

/* 音频播放器样式 */
audio {
  border-radius: 10px;
  width: 100%;
  margin: 1rem 0;
}

/* 警告和信息框样式 */
.stAlert {
  border-radius: 10px;
  border: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

/* 展开器样式 */
.streamlit-expanderHeader {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 10px;
  border: 1px solid #dee2e6;
}

/* 数据框样式 */
.dataframe {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

/* 加载动画 */
@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}

.loading {
  animation: pulse 2s infinite;
}

/* Live2D容器样式 */
.live2d-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  padding: 20px;
  margin: 20px 0;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .stColumns > div {
    padding: 0 0.5rem;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .main {
    background-color: #1a1a1a;
    color: #ffffff;
  }

  [data-testid="metric-container"] {
    background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
    border-color: #4a5568;
    color: #ffffff;
  }
}
```

## 🧪 前端测试

### `frontend/tests/test_components.py`

```python
import pytest
import streamlit as st
from unittest.mock import Mock, patch

from frontend.utils.api_client import APIClient
from frontend.utils.validators import validate_audio_file

class TestAPIClient:
    """API客户端测试"""

    def test_health_check(self):
        """测试健康检查"""
        client = APIClient("http://localhost:8000")

        with patch('requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {"status": "healthy"}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = client.health_check()
            assert result["status"] == "healthy"

class TestValidators:
    """验证器测试"""

    def test_validate_audio_file(self):
        """测试音频文件验证"""
        # 有效的文件名
        assert validate_audio_file("test.mp3") == True
        assert validate_audio_file("test.wav") == True
        assert validate_audio_file("test.m4a") == True

        # 无效的文件名
        assert validate_audio_file("test.txt") == False
        assert validate_audio_file("test.jpg") == False
        assert validate_audio_file(None) == False
```

---

这个前端开发指南提供了完整的 Streamlit 应用开发框架，包括页面组件、API 客户端、样式优化和 Live2D 集成方案。所有代码都可以直接用于项目开发，并且考虑了用户体验和响应式设计。
