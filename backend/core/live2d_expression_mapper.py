"""
Live2D表情映射器
使用OpenAI将情感分析结果映射到Live2D表情序列
"""
import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any
from openai import OpenAI
from langchain_openai import ChatOpenAI
from backend.core.ai_config import AIConfig

logger = logging.getLogger(__name__)


class Live2DExpressionMapper:
    """Live2D表情映射器"""
    
    # Live2D模型配置路径
    LIVE2D_MODEL_PATH = Path("/workspaces/geyan-suidong-/plug/Web/三月七live2d模型 v0.1/model/march_7")
    EXPRESSIONS_DIR = LIVE2D_MODEL_PATH / "expressions"
    MODEL_CONFIG = LIVE2D_MODEL_PATH / "march_7.model3.json"
    
    def __init__(self):
        """初始化映射器"""
        # 使用统一的AI配置
        config = AIConfig.get_expression_config()
        self.use_gemini = config['use_gemini']
        
        if not self.use_gemini:
            # 使用OpenAI
            llm_kwargs = {
                "model": config['model_name'],
                "temperature": config['temperature'],
                "max_tokens": config['max_tokens'],
            }
            if config.get('api_base'):
                llm_kwargs['base_url'] = config['api_base']
            if config.get('api_key'):
                llm_kwargs['api_key'] = config['api_key']
            
            self.client = ChatOpenAI(**llm_kwargs)
        else:
            # 使用Gemini需要不同的初始化
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.client = ChatGoogleGenerativeAI(
                model=config['model_name'],
                temperature=config['temperature'],
                google_api_key=config['api_key']
            )
        
        self.expressions_config = self._load_expressions_config()
        
    def _load_expressions_config(self) -> Dict[str, Any]:
        """加载表情配置"""
        try:
            # 读取模型配置获取表情名称
            with open(self.MODEL_CONFIG, 'r', encoding='utf-8') as f:
                model_config = json.load(f)
            
            expressions = []
            for idx, expr in enumerate(model_config['FileReferences']['Expressions']):
                # 读取表情文件获取时间
                expr_file = self.LIVE2D_MODEL_PATH / expr['File']
                with open(expr_file, 'r', encoding='utf-8') as f:
                    expr_data = json.load(f)
                
                duration = expr_data.get('FadeInTime', 0) + expr_data.get('FadeOutTime', 0)
                
                expressions.append({
                    'index': idx,
                    'name': expr['Name'],
                    'file': expr['File'],
                    'duration': duration,
                    'fade_in': expr_data.get('FadeInTime', 0),
                    'fade_out': expr_data.get('FadeOutTime', 0)
                })
            
            return {
                'expressions': expressions,
                'total_count': len(expressions)
            }
        except Exception as e:
            logger.error(f"加载表情配置失败: {e}")
            raise
    
    def map_emotions_to_expressions(
        self, 
        emotion_scores: Dict[str, float],
        duration: float
    ) -> List[str]:
        """
        使用AI将情感分数映射到Live2D表情序列
        
        Args:
            emotion_scores: 情感分数字典
            duration: 音频总时长
            
        Returns:
            表情索引数组，例如 ["0", "1", "1", "2"]
        """
        try:
            # 构建表情信息
            expressions_info = []
            for expr in self.expressions_config['expressions']:
                expressions_info.append({
                    'index': expr['index'],
                    'name': expr['name'],
                    'description': self._get_emotion_description(expr['name'])
                })
            
            # 构建prompt
            system_prompt = "你是一个专业的动画表情设计师，擅长根据情感选择合适的表情动画。你必须只返回JSON格式的数据，不要包含任何其他文字。"
            
            user_prompt = f"""你是一个Live2D表情动画专家。根据情感分析结果，为角色三月七选择合适的表情序列。

可用表情列表：
{json.dumps(expressions_info, ensure_ascii=False, indent=2)}

情感分析结果：
{json.dumps(emotion_scores, ensure_ascii=False, indent=2)}

音频总时长：{duration}秒

要求：
1. 根据情感分析结果选择最匹配的表情序列
2. 表情切换要自然流畅
3. 表情持续时间总和应接近音频时长，每个表情持续6s左右,应该有 duration / 6 个表情,列表应有 duration / 6 个元素
4. 情感分析结果中timestamp每过6s，就需要分割一次内容，生成一个表情，根据parameters的动作变化选择不同的表情，处理完整个情感分析结果，不可以省略
5. 返回表情索引数组，索引从0开始，可以重复使用同一表情
6. 数组格式示例：{{"expressions": ["0", "1", "1", "2"]}} 表示依次播放索引0、1、1、2的表情
7. 检测生成的表情序列长度是否和要求的长度一致，如果不一致，请继续生成，直到一致为止

请直接返回JSON格式的表情序列，格式为：{{"expressions": ["索引1", "索引2", ...]}}
"""
            
            # 使用LangChain调用
            from langchain_core.messages import HumanMessage, SystemMessage
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.client.invoke(messages)
            
            # 解析响应
            content = response.content.strip()
            
            # 如果响应包含markdown代码块，提取JSON部分
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            result = json.loads(content)
            expression_sequence = result.get('expressions', result.get('expression_sequence', []))
            
            # 转换为字符串数组
            expression_sequence = [str(idx) for idx in expression_sequence]
            
            logger.info(f"生成表情序列: {expression_sequence}")
            return expression_sequence
            
        except Exception as e:
            logger.error(f"表情映射失败: {e}", exc_info=True)
            # 返回默认表情序列
            return ["0"]
    
    def _get_emotion_description(self, emotion_name: str) -> str:
        """获取情感描述"""
        descriptions = {
            '生气': '愤怒、不满、生气的表情',
            '星星眼': '兴奋、惊喜、开心的表情',
            '睡觉': '困倦、疲惫、睡眠的表情',
            '流汗': '尴尬、紧张、为难的表情',
            '冒烟': '愤怒到极点、非常生气的表情'
        }
        return descriptions.get(emotion_name, emotion_name)
    
    def get_expression_info(self) -> Dict[str, Any]:
        """获取表情配置信息"""
        return self.expressions_config
