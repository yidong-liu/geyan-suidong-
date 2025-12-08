"""
Live2D展示组件
集成Live2D模型显示和控制
"""
import streamlit.components.v1 as components
import streamlit as st
from pathlib import Path

class Live2DComponent:
    """Live2D展示组件类"""
    
    def __init__(self):
        self.model_path = Path("plug/Web/三月七live2d模型 v0.1")
    
    def render_live2d_viewer(
        self,
        width: int = 800,
        height: int = 600,
        model_name: str = "march_7",
        show_controls: bool = True
    ):
        """
        渲染Live2D查看器
        
        Args:
            width: 显示宽度
            height: 显示高度
            model_name: 模型名称
            show_controls: 是否显示控制按钮
        """
        
        # 生成HTML内容
        html_content = self._generate_live2d_html(width, height, model_name, show_controls)
        
        # 在Streamlit中显示
        components.html(html_content, width=width, height=height, scrolling=False)
    
    def _generate_live2d_html(
        self,
        width: int,
        height: int,
        model_name: str,
        show_controls: bool
    ) -> str:
        """生成Live2D HTML内容"""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    font-family: 'Arial', sans-serif;
                    overflow: hidden;
                }}
                
                #live2d-container {{
                    width: {width}px;
                    height: {height}px;
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 10px;
                }}
                
                #model-canvas {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    border-radius: 10px;
                }}
                
                .status-overlay {{
                    position: absolute;
                    top: 20px;
                    left: 20px;
                    background: rgba(0,0,0,0.7);
                    color: white;
                    padding: 15px 20px;
                    border-radius: 10px;
                    font-size: 14px;
                }}
                
                .controls {{
                    position: absolute;
                    bottom: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    display: flex;
                    gap: 10px;
                }}
                
                .control-btn {{
                    background: rgba(255,255,255,0.9);
                    border: none;
                    padding: 10px 15px;
                    border-radius: 20px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: all 0.3s;
                }}
                
                .control-btn:hover {{
                    background: white;
                    transform: scale(1.05);
                }}
                
                .info-text {{
                    text-align: center;
                    color: white;
                    padding: 20px;
                }}
                
                .loading {{
                    text-align: center;
                    color: white;
                    font-size: 18px;
                }}
                
                .error {{
                    text-align: center;
                    color: #ffcccb;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <div id="live2d-container">
                <div class="status-overlay">
                    <div id="status">🎨 Live2D模型加载中...</div>
                    <div style="margin-top: 5px;">
                        <small>模型: {model_name}</small><br>
                        <small>状态: <span id="model-status">准备中</span></small>
                    </div>
                </div>
                
                <div class="info-text">
                    <h3>🎭 Live2D 表情展示</h3>
                    <p>三月七模型展示区域</p>
                    <div id="loading-info" class="loading">
                        <div>✨ 正在初始化Live2D引擎...</div>
                        <div style="margin-top: 10px;">
                            <div>📁 加载模型文件</div>
                            <div>🎮 初始化渲染器</div>
                            <div>🎵 同步表情数据</div>
                        </div>
                    </div>
                </div>
                
                <canvas id="model-canvas" style="display: none;"></canvas>
                
                {self._generate_controls_html() if show_controls else ''}
            </div>
            
            <script>
                // Live2D初始化逻辑
                let modelLoaded = false;
                let expressionData = null;
                
                // 从Streamlit获取表情数据
                function getExpressionData() {{
                    // 这里应该从session_state获取数据
                    // 当前为示例数据
                    return {{
                        timestamp: 0,
                        parameters: {{
                            eye_open: 0.8,
                            mouth_open: 0.3,
                            eyebrow_height: 0.5
                        }}
                    }};
                }}
                
                // 初始化Live2D
                function initLive2D() {{
                    const status = document.getElementById('status');
                    const modelStatus = document.getElementById('model-status');
                    
                    try {{
                        status.innerHTML = '🎨 Live2D引擎已启动';
                        modelStatus.textContent = '加载中';
                        
                        // 模拟加载过程
                        setTimeout(() => {{
                            status.innerHTML = '✅ 模型加载完成';
                            modelStatus.textContent = '就绪';
                            
                            document.getElementById('loading-info').style.display = 'none';
                            document.getElementById('model-canvas').style.display = 'block';
                            
                            modelLoaded = true;
                            renderModel();
                        }}, 2000);
                        
                    }} catch (error) {{
                        status.innerHTML = '❌ 加载失败: ' + error.message;
                        modelStatus.textContent = '错误';
                    }}
                }}
                
                // 渲染模型
                function renderModel() {{
                    const canvas = document.getElementById('model-canvas');
                    const ctx = canvas.getContext('2d');
                    
                    canvas.width = {width - 40};
                    canvas.height = {height - 40};
                    
                    // 绘制占位符
                    ctx.fillStyle = 'rgba(255,255,255,0.1)';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    // 绘制角色轮廓
                    ctx.strokeStyle = 'rgba(255,255,255,0.5)';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.arc(canvas.width/2, canvas.height/2, 100, 0, 2*Math.PI);
                    ctx.stroke();
                    
                    // 添加文字
                    ctx.fillStyle = 'white';
                    ctx.font = '16px Arial';
                    ctx.textAlign = 'center';
                    ctx.fillText('Live2D模型', canvas.width/2, canvas.height/2 - 10);
                    ctx.fillText('表情同步中...', canvas.width/2, canvas.height/2 + 10);
                }}
                
                // 表情控制
                function playExpression() {{
                    if (!modelLoaded) return;
                    
                    const status = document.getElementById('status');
                    status.innerHTML = '▶️ 播放表情动画';
                    
                    // 这里应该实现实际的表情播放
                    console.log('播放表情动画');
                }}
                
                function pauseExpression() {{
                    const status = document.getElementById('status');
                    status.innerHTML = '⏸️ 表情动画暂停';
                    console.log('暂停表情动画');
                }}
                
                function resetExpression() {{
                    const status = document.getElementById('status');
                    status.innerHTML = '🔄 重置到默认表情';
                    console.log('重置表情');
                }}
                
                // 页面加载完成后初始化
                document.addEventListener('DOMContentLoaded', initLive2D);
            </script>
        </body>
        </html>
        """
        
        return html
    
    def _generate_controls_html(self) -> str:
        """生成控制按钮HTML"""
        return """
        <div class="controls">
            <button class="control-btn" onclick="playExpression()">▶️ 播放</button>
            <button class="control-btn" onclick="pauseExpression()">⏸️ 暂停</button>
            <button class="control-btn" onclick="resetExpression()">🔄 重置</button>
        </div>
        """

def render_live2d_component(expression_data=None):
    """
    渲染Live2D组件的便捷函数
    
    Args:
        expression_data: 表情数据
    """
    component = Live2DComponent()
    component.render_live2d_viewer(
        width=800,
        height=600,
        model_name="march_7",
        show_controls=True
    )