"""
歌颜随动 - Live2D音乐表情同步系统
主应用程序 - 整合版本
"""
import streamlit as st
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def main():
    """主函数"""
    
    # 页面配置
    st.set_page_config(
        page_title="歌颜随动",
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 主标题
    st.title("🎭 歌颜随动")
    st.markdown("### Live2D音乐表情同步系统")
    
    # 侧边栏导航
    with st.sidebar:
        st.markdown("### 🧭 导航菜单")
        
        page = st.radio(
            "选择页面",
            ["📤 上传音频", "🎭 Live2D预览", "ℹ️ 关于"],
            key="navigation"
        )
        
        # 显示系统状态
        st.markdown("---")
        st.markdown("### ⚙️ 系统状态")
        
        # 检查后端连接
        try:
            from frontend.utils.api_client import APIClient
            api_client = APIClient()
            if api_client.health_check():
                st.success("🟢 后端 API")
            else:
                st.warning("🟡 后端连接异常")
        except Exception as e:
            st.error("🔴 后端未启动")
        
        # 显示当前模式
        if st.session_state.get('processing_success'):
            st.info("✅ 有可预览数据")
        else:
            st.info("ℹ️ 等待音频上传")
    
    # 根据选择显示对应页面
    if page == "📤 上传音频":
        from frontend.pages.upload import render
        render()
    elif page == "🎭 Live2D预览":
        from frontend.pages.preview import render
        render()
    elif page == "ℹ️ 关于":
        show_about_page()

def show_about_page():
    """显示关于页面"""
    st.markdown("## ℹ️ 关于格焉随动")
    
    st.markdown("""
    ### 🎯 项目简介
    格焉随动是一个基于音乐分析的Live2D表情同步系统，能够：
    - 分析音频文件的节奏、情感特征
    - 自动生成对应的Live2D表情参数
    - 实时预览表情变化效果
    
    ### 🚀 主要功能
    - **音频分析**: 支持MP3、WAV等多种格式
    - **表情生成**: 基于音乐特征生成表情关键帧
    - **Live2D预览**: 实时预览表情同步效果
    - **参数调整**: 可调节敏感度、平滑度等参数
    
    ### 🛠️ 技术架构
    - **前端**: Streamlit Web界面
    - **后端**: FastAPI + 音频分析引擎
    - **Live2D**: 三月七模型支持
    - **数据处理**: librosa、numpy音频分析
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 系统状态")
        # 检查各组件状态
        st.success("✅ 前端运行正常")
        
        try:
            from frontend.utils.api_client import APIClient
            api_client = APIClient()
            if api_client.health_check():
                st.success("✅ 后端API正常")
            else:
                st.warning("⚠️ 后端API异常")
        except Exception as e:
            st.error("❌ 后端API未启动")
        
        # 检查Live2D资源
        live2d_path = project_root / "plug" / "Web" / "三月七live2d模型 v0.1"
        if live2d_path.exists():
            st.success("✅ Live2D模型可用")
        else:
            st.warning("⚠️ Live2D模型路径异常")
    
    with col2:
        st.markdown("### 🔗 相关链接")
        st.markdown("""
        - [Live2D官网](https://www.live2d.com/)
        - [Streamlit文档](https://docs.streamlit.io/)
        - [FastAPI文档](https://fastapi.tiangolo.com/)
        """)
        
        st.markdown("### 📁 项目结构")
        st.markdown("""
        ```
        格焉随动/
        ├── frontend/        # 前端Streamlit应用
        ├── backend/         # 后端FastAPI服务
        ├── plug/Web/        # Live2D模型资源
        ├── config/          # 配置文件
        └── data/            # 数据存储
        ```
        """)

def show_system_info():
    """显示系统信息（调试用）"""
    with st.expander("🔍 调试信息"):
        st.json({
            "session_state": dict(st.session_state),
            "python_path": sys.path[-3:],  # 显示最后3个路径
            "project_root": str(project_root),
            "current_page": st.session_state.get('navigation', 'None')
        })

if __name__ == "__main__":
    main()
    
    # 在页面底部显示调试信息（可选）
    if st.sidebar.checkbox("显示调试信息", value=False):
        show_system_info()
