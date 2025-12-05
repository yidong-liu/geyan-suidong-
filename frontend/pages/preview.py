"""
Live2D预览页面
"""
import streamlit as st
import streamlit.components.v1 as components

def render():
    """渲染预览页面"""
    
    st.markdown("## 👀 Live2D模型预览")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Live2D展示区域
        st.markdown("### 🎭 Live2D展示")
        
        # 这里使用HTML/JavaScript嵌入Live2D
        live2d_html = """
        <div id="live2d-container" style="width: 100%; height: 600px; background: #f0f0f0; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center;">
                <h3>🎨 Live2D模型加载区域</h3>
                <p>模型将在此处显示</p>
                <p style="color: #999;">需要加载Live2D库和模型文件</p>
            </div>
        </div>
        """
        
        components.html(live2d_html, height=600)
        
        # 播放控制
        st.markdown("### 🎮 播放控制")
        
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            if st.button("▶️ 播放", use_container_width=True):
                st.info("播放音乐和表情动画")
        
        with col_b:
            if st.button("⏸️ 暂停", use_container_width=True):
                st.info("暂停播放")
        
        with col_c:
            if st.button("⏹️ 停止", use_container_width=True):
                st.info("停止播放")
        
        with col_d:
            if st.button("🔄 重置", use_container_width=True):
                st.info("重置到开始")
        
        # 进度条
        progress = st.slider("播放进度", 0, 100, 0, format="%d%%")
    
    with col2:
        # 控制面板
        st.markdown("### ⚙️ 控制面板")
        
        # 模型选择
        model = st.selectbox(
            "选择模型",
            ["默认模型", "Hiyori", "赛博朋克"],
            key="model_select"
        )
        
        # 音频选择
        audio = st.selectbox(
            "选择音频",
            ["未上传", "音频文件1.mp3", "音频文件2.wav"],
            key="audio_select"
        )
        
        # 表情文件
        expression = st.selectbox(
            "表情文件",
            ["未生成", "表情1.json", "表情2.json"],
            key="expression_select"
        )
        
        st.markdown("---")
        
        # 实时参数显示
        st.markdown("### 📊 实时参数")
        
        st.metric("眼睛开合", "0.80")
        st.metric("嘴部开合", "0.35")
        st.metric("眉毛高度", "0.50")
        st.metric("脸颊红晕", "0.15")
        
        st.markdown("---")
        
        # 导出选项
        st.markdown("### 💾 导出")
        
        if st.button("📥 导出表情文件", use_container_width=True):
            st.success("表情文件已导出")
        
        if st.button("🎥 录制视频", use_container_width=True):
            st.info("开始录制视频")

if __name__ == "__main__":
    render()
