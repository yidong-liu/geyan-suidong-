"""
音频上传页面
"""
import streamlit as st
import requests
import time
from pathlib import Path

def render():
    """渲染上传页面"""
    
    st.markdown("## 📤 上传音频文件")
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "选择音频文件",
        type=['mp3', 'wav', 'm4a', 'flac', 'ogg'],
        help="支持的格式: MP3, WAV, M4A, FLAC, OGG"
    )
    
    if uploaded_file is not None:
        _show_file_info(uploaded_file)
        _show_processing_options(uploaded_file)

def _show_file_info(uploaded_file):
    """显示文件信息"""
    st.markdown("### 📋 文件信息")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("文件名", uploaded_file.name)
    
    with col2:
        file_size = len(uploaded_file.getvalue())
        st.metric("文件大小", f"{file_size / 1024 / 1024:.2f} MB")
    
    with col3:
        file_type = uploaded_file.name.split('.')[-1].upper()
        st.metric("格式", file_type)
    
    # 音频预览
    st.markdown("### 🎧 音频预览")
    st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")

def _show_processing_options(uploaded_file):
    """显示处理选项"""
    st.markdown("### ⚙️ 处理选项")
    
    with st.form("processing_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            model_choice = st.selectbox(
                "Live2D模型",
                ["默认模型", "Hiyori", "赛博朋克"],
                help="选择要使用的Live2D模型"
            )
            
            time_resolution = st.slider(
                "时间分辨率（秒）",
                min_value=0.05,
                max_value=0.5,
                value=0.1,
                step=0.05,
                help="表情关键帧的时间间隔"
            )
        
        with col2:
            enable_smoothing = st.checkbox(
                "启用平滑处理",
                value=True,
                help="平滑表情过渡，避免突兀变化"
            )
            
            sensitivity = st.slider(
                "表情敏感度",
                min_value=0.1,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="调整表情对音乐变化的敏感程度"
            )
        
        submitted = st.form_submit_button(
            "🚀 开始分析与生成",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            _process_file(uploaded_file, model_choice, time_resolution, enable_smoothing)

def _process_file(uploaded_file, model_choice, time_resolution, enable_smoothing):
    """处理文件"""
    from frontend.utils.api_client import APIClient
    
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        api_client = APIClient()
        
        # 步骤1: 上传文件
        with progress_placeholder.container():
            st.progress(0.2, text="📤 上传文件中...")
        
        upload_result = api_client.upload_file(uploaded_file)
        if not upload_result.get('success'):
            raise Exception(upload_result.get('message', '上传失败'))
        
        file_id = upload_result['data']['file_id']
        st.session_state['last_file_id'] = file_id
        
        # 步骤2: 分析音频
        with progress_placeholder.container():
            st.progress(0.4, text="🎵 分析音频特征...")
        
        analyze_result = api_client.analyze_audio(file_id)
        if not analyze_result.get('success'):
            raise Exception(analyze_result.get('message', '分析失败'))
        
        st.session_state['last_analysis'] = analyze_result['data']
        
        # 步骤3: 生成表情
        with progress_placeholder.container():
            st.progress(0.7, text="🎭 生成表情动画...")
        
        model_mapping = {
            "默认模型": "default",
            "Hiyori": "hiyori",
            "赛博朋克": "cyberpunk"
        }
        
        expression_result = api_client.generate_expression(
            file_id=file_id,
            model_name=model_mapping.get(model_choice, "default"),
            time_resolution=time_resolution,
            enable_smoothing=enable_smoothing
        )
        
        if not expression_result.get('success'):
            raise Exception(expression_result.get('message', '生成失败'))
        
        st.session_state['last_expression_id'] = expression_result['data']['expression_id']
        st.session_state['last_expression_data'] = expression_result['data']
        
        # 完成
        with progress_placeholder.container():
            st.progress(1.0, text="✅ 处理完成!")
        
        # 显示结果信息
        st.success("🎉 表情文件生成成功！")
        
        # 显示统计信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("音频时长", f"{expression_result['data']['duration']:.2f}秒")
        with col2:
            st.metric("关键帧数", expression_result['data']['keyframe_count'])
        with col3:
            st.metric("节拍 (BPM)", f"{expression_result['data']['tempo']:.1f}")
        
        # 情感分数
        st.markdown("#### 🎭 检测到的情感")
        emotion_scores = expression_result['data']['emotion_scores']
        cols = st.columns(len(emotion_scores))
        for i, (emotion, score) in enumerate(emotion_scores.items()):
            with cols[i]:
                st.metric(emotion.capitalize(), f"{score:.2%}")
    
    except Exception as e:
        status_placeholder.error(f"❌ 处理失败: {str(e)}")
        import traceback
        st.error(traceback.format_exc())

if __name__ == "__main__":
    render()
