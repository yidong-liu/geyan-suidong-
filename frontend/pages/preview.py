"""
Live2D预览页面 - 整合版本
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import json
import time

def render():
    """渲染预览页面"""
    
    st.markdown("## 🎭 Live2D表情预览")
    
    # 检查是否有处理结果
    if not st.session_state.get('processing_success'):
        _show_no_data_message()
        return
    
    # 显示处理信息
    _show_processing_info()
    
    # 显示Live2D模型
    _show_live2d_model()
    
    # 显示控制面板
    _show_control_panel()

def _show_no_data_message():
    """显示无数据消息"""
    st.info("💡 暂无可预览的内容")
    st.markdown("""
    ### 如何开始？
    1. 前往 **📤 上传音频** 页面
    2. 选择一个音频文件
    3. 配置处理参数并点击 **开始分析与生成**
    4. 完成后即可在此查看Live2D预览
    """)
    
    # 显示示例按钮
    if st.button("🎯 载入示例数据", type="secondary"):
        _load_sample_data()
        st.rerun()

def _load_sample_data():
    """载入示例数据进行预览演示"""
    st.session_state['last_file_name'] = "示例音乐.mp3"
    st.session_state['last_model'] = "三月七"
    st.session_state['last_time_resolution'] = 0.1
    st.session_state['last_smoothing'] = True
    st.session_state['last_sensitivity'] = 1.0
    st.session_state['processing_success'] = True
    
    # 模拟音频数据
    st.session_state['last_audio_data'] = {
        "duration": 3.45,
        "tempo": 128.0,
        "sample_rate": 44100,
        "channels": 2,
        "energy_stats": {"mean": 0.7, "max": 0.95, "min": 0.15},
        "spectral_stats": {"mean": 0.75, "max": 0.92, "min": 0.22}
    }
    
    # 模拟表情数据
    st.session_state['last_expression_data'] = {
        "expression_id": "sample_" + str(int(time.time())),
        "model_name": "三月七",
        "keyframe_count": 35,
        "time_resolution": 0.1,
        "smoothing_enabled": True,
        "sensitivity": 1.0
    }

def _show_processing_info():
    """显示处理信息"""
    st.markdown("### 📊 处理信息")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        file_name = st.session_state.get('last_file_name', '未知文件')
        st.metric("源文件", file_name)
    
    with col2:
        model = st.session_state.get('last_model', '默认模型')
        st.metric("Live2D模型", model)
    
    with col3:
        resolution = st.session_state.get('last_time_resolution', 0.1)
        st.metric("时间分辨率", f"{resolution:.2f}s")
    
    with col4:
        smoothing = st.session_state.get('last_smoothing', True)
        st.metric("平滑处理", "✅" if smoothing else "❌")
    
    # 音频分析结果
    if 'last_audio_data' in st.session_state:
        audio_data = st.session_state['last_audio_data']
        
        st.markdown("#### 🎵 音频分析")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("时长", f"{audio_data['duration']:.2f}秒")
        with col2:
            st.metric("节拍(BPM)", f"{audio_data['tempo']:.1f}")
        with col3:
            st.metric("声道", audio_data['channels'])

def _show_live2d_model():
    """显示Live2D模型"""
    st.markdown("### 🎭 Live2D模型")
    
    # 获取模型名称
    model_name = st.session_state.get('last_model', '三月七')
    
    # 根据模型显示不同的Live2D组件
    if model_name == "三月七":
        _render_march_7_model()
    else:
        _render_default_model()

def _render_march_7_model():
    """渲染三月七Live2D模型"""
    
    # 三月七Live2D HTML
    live2d_html = """
    <div id="live2d-container" style="width: 100%; height: 500px; position: relative; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; overflow: hidden;">
        <div id="live2d-widget" style="position: absolute; bottom: 0; right: 100px;">
            <canvas id="live2d-canvas" width="300" height="400"></canvas>
        </div>
        
        <!-- 控制面板 -->
        <div style="position: absolute; top: 20px; left: 20px; background: rgba(255,255,255,0.9); padding: 15px; border-radius: 8px; backdrop-filter: blur(10px);">
            <h4 style="margin: 0 0 10px 0; color: #333;">🎭 三月七</h4>
            <div style="font-size: 14px; color: #666;">
                <div>状态: <span style="color: #4CAF50;">● 活跃</span></div>
                <div>表情: <span id="current-expression">默认</span></div>
                <div>动作: <span id="current-motion">待机</span></div>
            </div>
        </div>
        
        <!-- 情感指示器 -->
        <div style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.9); padding: 15px; border-radius: 8px; backdrop-filter: blur(10px);">
            <h4 style="margin: 0 0 10px 0; color: #333;">🎯 当前情感</h4>
            <div id="emotion-bars" style="font-size: 12px;">
                <div>😊 开心: <div style="background: #4CAF50; height: 4px; width: 60%; margin: 2px 0;"></div></div>
                <div>⚡ 活跃: <div style="background: #FF9800; height: 4px; width: 80%; margin: 2px 0;"></div></div>
                <div>😌 平静: <div style="background: #2196F3; height: 4px; width: 20%; margin: 2px 0;"></div></div>
                <div>😢 悲伤: <div style="background: #9C27B0; height: 4px; width: 10%; margin: 2px 0;"></div></div>
            </div>
        </div>
        
        <!-- 播放控制 -->
        <div style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.7); padding: 10px 20px; border-radius: 25px; color: white;">
            <button onclick="playAnimation()" style="background: none; border: none; color: white; margin: 0 5px; cursor: pointer;">▶️</button>
            <button onclick="pauseAnimation()" style="background: none; border: none; color: white; margin: 0 5px; cursor: pointer;">⏸️</button>
            <button onclick="resetAnimation()" style="background: none; border: none; color: white; margin: 0 5px; cursor: pointer;">🔄</button>
            <span style="margin-left: 10px; font-size: 12px;">音乐同步表情</span>
        </div>
    </div>
    
    <script>
        // 模拟Live2D初始化
        console.log("三月七Live2D模型初始化中...");
        
        // 表情变化模拟
        let currentExpression = "default";
        let expressionList = ["default", "happy", "surprised", "sad", "angry"];
        let emotionData = {
            "happy": 0.6,
            "energetic": 0.8, 
            "calm": 0.2,
            "sad": 0.1
        };
        
        function updateEmotion() {
            const bars = document.getElementById('emotion-bars');
            if (bars) {
                bars.innerHTML = Object.entries(emotionData).map(([emotion, value]) => {
                    const emoji = {happy: '😊', energetic: '⚡', calm: '😌', sad: '😢'}[emotion] || '🎭';
                    const color = {happy: '#4CAF50', energetic: '#FF9800', calm: '#2196F3', sad: '#9C27B0'}[emotion] || '#666';
                    return `<div>${emoji} ${emotion}: <div style="background: ${color}; height: 4px; width: ${value*100}%; margin: 2px 0;"></div></div>`;
                }).join('');
            }
        }
        
        function changeExpression() {
            currentExpression = expressionList[Math.floor(Math.random() * expressionList.length)];
            document.getElementById('current-expression').textContent = currentExpression;
            
            // 随机更新情感数据
            Object.keys(emotionData).forEach(key => {
                emotionData[key] = Math.random();
            });
            updateEmotion();
        }
        
        function playAnimation() {
            document.getElementById('current-motion').textContent = '表情同步';
            setInterval(changeExpression, 2000);
        }
        
        function pauseAnimation() {
            document.getElementById('current-motion').textContent = '暂停';
        }
        
        function resetAnimation() {
            currentExpression = 'default';
            document.getElementById('current-expression').textContent = 'default';
            document.getElementById('current-motion').textContent = '待机';
            emotionData = {"happy": 0.6, "energetic": 0.8, "calm": 0.2, "sad": 0.1};
            updateEmotion();
        }
        
        // 初始化
        updateEmotion();
        
        // 模拟Live2D模型加载
        setTimeout(() => {
            console.log("三月七Live2D模型加载完成");
            // 这里应该加载真实的Live2D模型
        }, 1000);
    </script>
    """
    
    components.html(live2d_html, height=550)

def _render_default_model():
    """渲染默认Live2D模型"""
    
    default_html = """
    <div style="width: 100%; height: 400px; background: linear-gradient(45deg, #FF6B6B, #4ECDC4); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; text-align: center;">
        <div>
            <h3>🎭 默认Live2D模型</h3>
            <p>模型加载中...</p>
            <div style="margin-top: 20px;">
                <div>当前表情: <span style="background: rgba(255,255,255,0.3); padding: 5px 10px; border-radius: 15px;">默认</span></div>
            </div>
        </div>
    </div>
    """
    
    components.html(default_html, height=450)

def _show_control_panel():
    """显示控制面板"""
    st.markdown("### 🎮 控制面板")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚙️ 表情参数")
        
        # 表情强度控制
        intensity = st.slider("表情强度", 0.0, 2.0, 1.0, 0.1)
        
        # 表情类型选择
        expression_type = st.selectbox(
            "表情类型",
            ["自动", "开心", "惊讶", "悲伤", "愤怒", "平静"]
        )
        
        # 动画速度
        animation_speed = st.slider("动画速度", 0.5, 3.0, 1.0, 0.1)
        
        if st.button("🎯 应用设置", type="secondary"):
            st.success(f"已应用设置: 强度{intensity}, 类型{expression_type}, 速度{animation_speed}")
    
    with col2:
        st.markdown("#### 📊 实时数据")
        
        # 显示表情数据
        if 'last_expression_data' in st.session_state:
            expression_data = st.session_state['last_expression_data']
            
            st.metric("关键帧数", expression_data.get('keyframe_count', 0))
            st.metric("时间分辨率", f"{expression_data.get('time_resolution', 0.1):.2f}s")
            st.metric("表情ID", expression_data.get('expression_id', 'N/A')[:8] + "...")
        
        # 模拟实时数据更新
        if st.button("🔄 刷新数据", type="secondary"):
            st.info("数据已刷新")
        
        # 导出功能
        if st.button("📥 导出表情数据", type="secondary"):
            _export_expression_data()

def _export_expression_data():
    """导出表情数据"""
    try:
        # 收集所有相关数据
        export_data = {
            "file_info": {
                "name": st.session_state.get('last_file_name', ''),
                "model": st.session_state.get('last_model', ''),
                "time_resolution": st.session_state.get('last_time_resolution', 0.1),
                "smoothing": st.session_state.get('last_smoothing', True),
                "sensitivity": st.session_state.get('last_sensitivity', 1.0)
            },
            "audio_data": st.session_state.get('last_audio_data', {}),
            "expression_data": st.session_state.get('last_expression_data', {}),
            "export_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 转换为JSON
        json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        # 提供下载
        st.download_button(
            label="📥 下载表情数据 (JSON)",
            data=json_data,
            file_name=f"expression_data_{int(time.time())}.json",
            mime="application/json"
        )
        
        st.success("✅ 表情数据已准备好下载")
        
    except Exception as e:
        st.error(f"❌ 导出失败: {str(e)}")

# 页面底部信息
def _show_footer_info():
    """显示页面底部信息"""
    st.markdown("---")
    st.markdown("### 💡 使用提示")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Live2D控制**:
        - 点击播放按钮开始表情同步
        - 调整参数实时预览效果
        - 支持多种表情类型切换
        """)
    
    with col2:
        st.markdown("""
        **数据导出**:
        - 支持JSON格式导出
        - 包含完整的处理参数
        - 可用于其他Live2D播放器
        """)

if __name__ == "__main__":
    render()
    _show_footer_info()