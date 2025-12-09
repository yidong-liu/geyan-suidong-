"""
Backend Core Module
"""
from .audio_analyzer import AudioAnalyzerAgent, AudioFeatures, EmotionScores
from .langchain_agent import ExpressionAgentV2, Live2DExpression
from .expression_generator import ExpressionGenerator

# 向后兼容：提供旧的类名
AudioAnalyzer = AudioAnalyzerAgent

__all__ = [
    'AudioAnalyzerAgent',
    'AudioAnalyzer',  # 兼容旧代码
    'AudioFeatures',
    'EmotionScores',
    'ExpressionAgentV2',
    'Live2DExpression',
    'ExpressionGenerator',
]
