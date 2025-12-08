"""
音频上传页面 - 整合版本
"""
import streamlit as st
import sys
from pathlib import Path
import time
import traceback

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent.parent))

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
    else:
        _show_usage_tips()

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
                ["三月七", "默认模型"],
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
    
    # 处理表单提交
    if submitted:
        _process_file_with_real_api(uploaded_file, model_choice, time_resolution, enable_smoothing, sensitivity)
    
    # 显示跳转按钮（如果有处理结果）
    if st.session_state.get('processing_success'):
        st.markdown("---")
        if st.button("👀 查看预览", type="primary", use_container_width=True):
            # 这里应该跳转到预览页面，但由于Streamlit页面结构，我们显示提示
            st.info("💡 请使用侧边栏导航到 'Live2D预览' 页面查看结果")

def _process_file_with_real_api(uploaded_file, model_choice, time_resolution, enable_smoothing, sensitivity):
    """使用真实API处理文件"""
    progress_placeholder = st.empty()
    
    try:
        from frontend.utils.api_client import APIClient
        
        st.write("🔍 调试信息：开始处理文件", uploaded_file.name)
        
        api_client = APIClient()
        
        # 步骤1: 上传文件
        with progress_placeholder.container():
            st.progress(0.2, text="📤 上传文件中...")
            st.write("📤 步骤1: 正在上传文件到后端...")
        
        upload_result = api_client.upload_file(uploaded_file)
        if not upload_result.get('success'):
            raise Exception(upload_result.get('message', '上传失败'))
        
        file_id = upload_result['data']['file_id']
        st.session_state['last_file_id'] = file_id
        
        # 显示上传结果
        upload_data = {
            "file_id": file_id,
            "filename": upload_result['data']['filename'],
            "file_size": upload_result['data']['file_size']
        }
        st.write("📤 上传成功！文件信息：")
        st.json(upload_data)
        
        # 步骤2: 分析音频
        with progress_placeholder.container():
            st.progress(0.4, text="🎵 分析音频特征...")
            st.write("🎵 步骤2: 正在分析音频特征...")
        
        analyze_result = api_client.analyze_audio(file_id)
        if not analyze_result.get('success'):
            raise Exception(analyze_result.get('message', '分析失败'))
        
        st.session_state['last_analysis'] = analyze_result['data']
        
        # 显示分析结果
        st.write("🎵 音频分析完成！结果：")
        st.json(analyze_result['data'])
        
        # 步骤3: 生成表情
        with progress_placeholder.container():
            st.progress(0.7, text="🎭 生成表情动画...")
            st.write("🎭 步骤3: 正在生成表情参数...")
        
        model_mapping = {
            "三月七": "march_7",
            "默认模型": "default"
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
        
        # 显示表情生成结果
        st.write("🎭 表情生成完成！参数：")
        expression_data = {
            "expression_id": expression_result['data']['expression_id'],
            "model_name": model_choice,
            "time_resolution": time_resolution,
            "smoothing_enabled": enable_smoothing,
            "sensitivity": sensitivity,
            "keyframe_count": expression_result['data']['keyframe_count']
        }
        st.json(expression_data)
        
        # 完成
        with progress_placeholder.container():
            st.progress(1.0, text="✅ 处理完成!")
        
        # 保存处理参数
        st.session_state['last_file_name'] = uploaded_file.name
        st.session_state['last_model'] = model_choice
        st.session_state['last_time_resolution'] = time_resolution
        st.session_state['last_smoothing'] = enable_smoothing
        st.session_state['last_sensitivity'] = sensitivity
        
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
        
        st.write("🎭 详细情感分析结果：")
        st.json(emotion_scores)
        
        cols = st.columns(len(emotion_scores))
        for i, (emotion, score) in enumerate(emotion_scores.items()):
            with cols[i]:
                st.metric(emotion.capitalize(), f"{score:.1%}")
        
        # 设置成功标志
        st.session_state['processing_success'] = True
        
        # 输出完整的处理结果（便于调试）
        complete_result = {
            "file_info": {
                "name": uploaded_file.name,
                "size_mb": len(uploaded_file.getvalue()) / 1024 / 1024,
                "type": uploaded_file.name.split('.')[-1].upper()
            },
            "upload_result": upload_data,
            "audio_analysis": analyze_result['data'],
            "expression_generation": expression_data,
            "emotion_analysis": emotion_scores,
            "status": "success"
        }
        
        st.markdown("#### 🔍 完整处理结果")
        st.json(complete_result)
        
    except Exception as e:
        st.error(f"❌ 处理失败: {str(e)}")
        
        # 如果是API连接错误，提供模拟数据
        if "连接" in str(e) or "Connection" in str(e) or "requests" in str(e).lower():
            st.warning("⚠️ 后端API连接失败，使用模拟数据演示功能")
            _process_file_with_mock_data(uploaded_file, model_choice, time_resolution, enable_smoothing, sensitivity)
        else:
            # 错误信息也输出到控制台
            error_info = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "status": "failed"
            }
            st.json(error_info)
            st.code(traceback.format_exc())

def _process_file_with_mock_data(uploaded_file, model_choice, time_resolution, enable_smoothing, sensitivity):
    """使用模拟数据处理文件（用于演示）"""
    progress_placeholder = st.empty()
    
    try:
        st.write("🔍 演示模式：使用模拟数据处理", uploaded_file.name)
        
        # 模拟处理过程
        with progress_placeholder.container():
            st.progress(0.2, text="📤 模拟文件上传...")
            time.sleep(1)
        
        # 模拟音频分析
        with progress_placeholder.container():
            st.progress(0.4, text="🎵 模拟音频分析...")
            audio_data = {
                "duration": 2.34,
                "tempo": 120.5,
                "sample_rate": 44100,
                "channels": 2,
                "energy_stats": {"mean": 0.65, "max": 0.98, "min": 0.12},
                "spectral_stats": {"mean": 0.72, "max": 0.95, "min": 0.18}
            }
            st.write("🎵 音频分析结果：")
            st.json(audio_data)
            time.sleep(1)
        
        # 模拟表情生成
        with progress_placeholder.container():
            st.progress(0.7, text="🎭 模拟表情生成...")
            expression_data = {
                "expression_id": "mock_" + str(int(time.time())),
                "model_name": model_choice,
                "keyframe_count": 23,
                "time_resolution": time_resolution,
                "smoothing_enabled": enable_smoothing,
                "sensitivity": sensitivity
            }
            st.write("🎭 表情生成结果：")
            st.json(expression_data)
            time.sleep(1)
        
        with progress_placeholder.container():
            st.progress(1.0, text="✅ 模拟处理完成!")
        
        # 保存模拟结果
        st.session_state['last_file_name'] = uploaded_file.name
        st.session_state['last_model'] = model_choice
        st.session_state['last_time_resolution'] = time_resolution
        st.session_state['last_smoothing'] = enable_smoothing
        st.session_state['last_audio_data'] = audio_data
        st.session_state['last_expression_data'] = expression_data
        st.session_state['processing_success'] = True
        
        st.success("🎉 模拟处理完成！")
        
        # 显示统计信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("音频时长", f"{audio_data['duration']:.2f}秒")
        with col2:
            st.metric("关键帧数", str(expression_data['keyframe_count']))
        with col3:
            st.metric("节拍 (BPM)", f"{audio_data['tempo']:.1f}")
        
        # 模拟情感分数
        emotion_scores = {
            "happy": 0.6,
            "energetic": 0.8,
            "calm": 0.2,
            "sad": 0.1
        }
        
        st.markdown("#### 🎭 检测到的情感")
        st.write("🎭 情感分析结果：")
        st.json(emotion_scores)
        
        cols = st.columns(len(emotion_scores))
        for i, (emotion, score) in enumerate(emotion_scores.items()):
            with cols[i]:
                st.metric(emotion.capitalize(), f"{score:.1%}")
        
        # 完整结果
        complete_result = {
            "mode": "simulation",
            "file_info": {
                "name": uploaded_file.name,
                "size_mb": len(uploaded_file.getvalue()) / 1024 / 1024,
                "type": uploaded_file.name.split('.')[-1].upper()
            },
            "audio_analysis": audio_data,
            "expression_generation": expression_data,
            "emotion_analysis": emotion_scores,
            "status": "success"
        }
        
        st.markdown("#### 🔍 完整处理结果（模拟）")
        st.json(complete_result)
        
    except Exception as e:
        st.error(f"❌ 模拟处理失败: {str(e)}")

def _show_usage_tips():
    """显示使用提示"""
    st.info("💡 请选择一个音频文件开始分析")
    
    st.markdown("### 📝 使用说明")
    st.markdown("""
    1. **选择文件**: 点击上方的文件选择器
    2. **支持格式**: MP3, WAV, M4A, FLAC, OGG
    3. **文件大小**: 建议不超过50MB
    4. **音频长度**: 建议2-10分钟以获得最佳效果
    """)
    
    st.markdown("### 🎵 音频要求")
    st.markdown("""
    - **质量**: 建议使用44.1kHz采样率
    - **内容**: 歌曲、纯音乐效果最佳
    - **时长**: 太短(<10s)或太长(>30min)可能影响效果
    """)
    
    st.markdown("### ⚙️ 系统状态")
    # 检查后端API状态
    try:
        from frontend.utils.api_client import APIClient
        api_client = APIClient()
        is_healthy = api_client.health_check()
        
        if is_healthy:
            st.success("✅ 后端API连接正常")
        else:
            st.warning("⚠️ 后端API连接失败，将使用模拟数据演示")
    except Exception as e:
        st.error(f"❌ API检查失败: {str(e)}")
        st.info("💡 将使用模拟数据进行演示")

if __name__ == "__main__":
    render()