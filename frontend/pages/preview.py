"""
Live2D预览页面
"""
import streamlit as st
import streamlit.components.v1 as components

def render():
    """渲染预览页面"""
    
    st.markdown("## 👀 Live2D模型预览")
    
    # 检查是否有表情数据
    has_data = 'last_expression_id' in st.session_state
    
    if not has_data:
        st.info("💡 请先上传音频文件并生成表情动画")
        if st.button("📤 前往上传页面"):
            st.switch_page("pages/upload.py")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Live2D展示区域
        st.markdown("### 🎭 Live2D展示")
        
        # 这里使用HTML/JavaScript嵌入Live2D
        live2d_html = """
        <div id="live2d-container" style="width: 100%; height: 600px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center; color: white;">
                <h3>🎨 Live2D模型展示区域</h3>
                <p>模型将在此处显示动画</p>
                <p style="color: rgba(255,255,255,0.8);">Live2D库和模型文件准备中...</p>
                <p style="font-size: 0.9em; margin-top: 20px;">✨ 表情数据已加载</p>
            </div>
        </div>
        """
        
        components.html(live2d_html, height=600)
        
        # 播放控制
        st.markdown("### 🎮 播放控制")
        
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            if st.button("▶️ 播放", use_container_width=True):
                st.session_state['playing'] = True
                st.success("开始播放")
        
        with col_b:
            if st.button("⏸️ 暂停", use_container_width=True):
                st.session_state['playing'] = False
                st.info("已暂停")
        
        with col_c:
            if st.button("⏹️ 停止", use_container_width=True):
                st.session_state['playing'] = False
                st.session_state['progress'] = 0
                st.info("已停止")
        
        with col_d:
            if st.button("🔄 重置", use_container_width=True):
                st.session_state['progress'] = 0
                st.success("已重置")
        
        # 进度条
        progress = st.slider("播放进度", 0, 100, st.session_state.get('progress', 0), format="%d%%")
        st.session_state['progress'] = progress
    
    with col2:
        # 控制面板
        st.markdown("### ⚙️ 控制面板")
        
        # 显示当前表情数据信息
        if 'last_expression_data' in st.session_state:
            data = st.session_state['last_expression_data']
            
            st.markdown("#### 📊 表情数据")
            st.metric("表情ID", data['expression_id'][:8] + "...")
            st.metric("音频时长", f"{data['duration']:.2f}秒")
            st.metric("关键帧数", data['keyframe_count'])
            st.metric("节拍 (BPM)", f"{data['tempo']:.1f}")
        
        st.markdown("---")
        
        # 实时参数显示
        st.markdown("### 📊 实时参数")
        
        # 从表情数据中获取当前帧的参数
        if 'last_expression_id' in st.session_state:
            from frontend.utils.api_client import APIClient
            try:
                api_client = APIClient()
                expression_data = api_client.get_expression(st.session_state['last_expression_id'])
                
                if expression_data.get('success'):
                    expressions = expression_data['data']['expressions']
                    if expressions:
                        # 根据进度获取当前帧
                        frame_index = int((progress / 100) * (len(expressions) - 1))
                        current_frame = expressions[frame_index]
                        params = current_frame['parameters']
                        
                        st.metric("眼睛开合", f"{params.get('eye_open', 0):.2f}")
                        st.metric("嘴部开合", f"{params.get('mouth_open', 0):.2f}")
                        st.metric("眉毛高度", f"{params.get('eyebrow_height', 0):.2f}")
                        st.metric("脸颊红晕", f"{params.get('cheek', 0):.2f}")
                        
                        # 显示时间戳
                        st.caption(f"时间: {current_frame['timestamp']:.2f}秒")
                    else:
                        st.warning("没有表情数据")
            except Exception as e:
                st.error(f"加载表情数据失败: {str(e)}")
        else:
            st.metric("眼睛开合", "N/A")
            st.metric("嘴部开合", "N/A")
            st.metric("眉毛高度", "N/A")
            st.metric("脸颊红晕", "N/A")
        
        st.markdown("---")
        
        # 情感分数
        if 'last_expression_data' in st.session_state:
            st.markdown("### 🎭 情感分析")
            emotion_scores = st.session_state['last_expression_data']['emotion_scores']
            for emotion, score in emotion_scores.items():
                st.progress(score, text=f"{emotion.capitalize()}: {score:.2%}")
        
        st.markdown("---")
        
        # 导出选项
        st.markdown("### 💾 导出")
        
        if st.button("📥 导出表情文件", use_container_width=True):
            if 'last_expression_id' in st.session_state:
                st.success(f"表情文件ID: {st.session_state['last_expression_id']}")
                st.code(f"data/expressions/{st.session_state['last_expression_id']}.json")
            else:
                st.warning("没有可导出的表情文件")
        
        if st.button("🔄 生成新表情", use_container_width=True):
            st.switch_page("pages/upload.py")

if __name__ == "__main__":
    render()
