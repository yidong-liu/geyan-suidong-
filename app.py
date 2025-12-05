"""
Streamlit主应用
歌颜随动 - 音乐表情生成系统
"""
import streamlit as st
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

# 页面配置
st.set_page_config(
    page_title="歌颜随动",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yidong-liu/geyan-suidong-',
        'Report a bug': 'https://github.com/yidong-liu/geyan-suidong-/issues',
        'About': '# 歌颜随动\n让歌声拥有表情，让虚拟陪伴真实 🎵✨'
    }
)

def load_custom_css():
    """加载自定义CSS样式"""
    css = """
    <style>
    /* 主题色彩 */
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --bg-color: #F7F7F7;
    }
    
    /* 标题样式 */
    .main-title {
        text-align: center;
        color: var(--primary-color);
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* 卡片样式 */
    .stCard {
        border-radius: 10px;
        padding: 20px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 按钮样式 */
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    """主应用函数"""
    
    # 加载样式
    load_custom_css()
    
    # 主标题
    st.markdown('<h1 class="main-title">🎵 歌颜随动</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">让歌声拥有表情，让虚拟陪伴真实</p>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.title("📋 导航菜单")
        st.markdown("---")
        
        # 页面选择
        page = st.radio(
            "选择功能",
            [
                "🏠 首页",
                "📤 音频上传",
                "👀 Live2D预览",
                "⚙️ 系统设置"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # API状态
        st.markdown("### 📡 服务状态")
        
        api_healthy = check_api_health()
        
        col1, col2 = st.columns(2)
        with col1:
            if api_healthy:
                st.success("✅ 后端API")
            else:
                st.error("❌ 后端API")
        with col2:
            st.success("✅ 前端服务")
        
        if not api_healthy:
            st.warning("⚠️ 后端服务未运行，请先启动backend")
            st.code("./start_backend.sh", language="bash")
        
        st.markdown("---")
        
        # 项目信息
        st.markdown("### 📖 项目信息")
        st.info("""
        **版本**: v1.0.0  
        **作者**: @yidong-liu  
        **GitHub**: [geyan-suidong](https://github.com/yidong-liu/geyan-suidong-)
        """)
    
    # 根据选择显示不同页面
    if page == "🏠 首页":
        show_home_page()
    elif page == "📤 音频上传":
        show_upload_page()
    elif page == "👀 Live2D预览":
        show_preview_page()
    elif page == "⚙️ 系统设置":
        show_settings_page()

def check_api_health() -> bool:
    """检查API健康状态"""
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def show_home_page():
    """显示首页"""
    st.markdown("## 👋 欢迎使用歌颜随动")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎵 音频分析")
        st.write("实时分析音乐的节拍、音调、情感特征")
        st.button("开始分析", key="analyze", use_container_width=True)
    
    with col2:
        st.markdown("### 🎭 表情生成")
        st.write("基于音乐特征生成对应的Live2D表情参数")
        st.button("生成表情", key="generate", use_container_width=True)
    
    with col3:
        st.markdown("### 🎮 实时预览")
        st.write("Live2D模型与音乐同步播放表情动画")
        st.button("查看预览", key="preview", use_container_width=True)
    
    st.markdown("---")
    
    # 功能介绍
    st.markdown("## ✨ 核心功能")
    
    tab1, tab2, tab3 = st.tabs(["音频分析", "表情生成", "Live2D展示"])
    
    with tab1:
        st.markdown("""
        ### 实时音频分析
        
        - 🥁 **节拍检测**: 自动识别音乐节奏和BPM
        - 🎼 **音高分析**: 实时跟踪旋律变化
        - 💫 **情感识别**: AI分析音乐情感特征
        - 📊 **可视化**: 直观展示音频特征
        """)
    
    with tab2:
        st.markdown("""
        ### 智能表情生成
        
        - 🤖 **AI驱动**: 基于LangChain的智能映射
        - 🎨 **多样化**: 丰富的表情参数组合
        - ⚡ **实时**: 快速生成表情关键帧
        - 🎯 **精准**: 与音乐完美同步
        """)
    
    with tab3:
        st.markdown("""
        ### Live2D动画展示
        
        - 👀 **实时渲染**: 流畅的Live2D动画
        - 🎵 **音乐同步**: 表情与音乐完美配合
        - 💾 **导出功能**: 保存表情动画文件
        - 🎮 **交互控制**: 灵活的播放控制
        """)

def show_upload_page():
    """显示上传页面"""
    st.markdown("## 📤 音频上传")
    st.info("上传您的音频文件，系统将自动分析并生成表情动画")
    
    # 这里导入实际的上传页面
    try:
        from frontend.pages import upload
        upload.render()
    except:
        st.warning("上传页面模块尚未完全加载，请稍后重试")

def show_preview_page():
    """显示预览页面"""
    st.markdown("## 👀 Live2D预览")
    st.info("查看Live2D模型的表情动画效果")
    
    # 这里导入实际的预览页面
    try:
        from frontend.pages import preview
        preview.render()
    except:
        st.warning("预览页面模块尚未完全加载，请稍后重试")

def show_settings_page():
    """显示设置页面"""
    st.markdown("## ⚙️ 系统设置")
    
    with st.form("settings_form"):
        st.markdown("### 🎵 音频处理设置")
        
        sample_rate = st.select_slider(
            "采样率",
            options=[22050, 44100, 48000],
            value=44100
        )
        
        hop_length = st.slider(
            "跳跃长度",
            min_value=256,
            max_value=1024,
            value=512,
            step=256
        )
        
        st.markdown("### 🎭 表情生成设置")
        
        time_resolution = st.slider(
            "时间分辨率（秒）",
            min_value=0.01,
            max_value=1.0,
            value=0.1,
            step=0.01
        )
        
        enable_smoothing = st.checkbox("启用平滑处理", value=True)
        
        submitted = st.form_submit_button("保存设置")
        
        if submitted:
            st.success("设置已保存！")

if __name__ == "__main__":
    main()
