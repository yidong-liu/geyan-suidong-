"""
LangChain代理模块
基于AI的表情映射生成
"""
from typing import Dict, List, Any
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ExpressionAgent:
    """基于LangChain的表情生成代理"""

    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        初始化表情代理

        Args:
            model_name: 使用的模型名称
            temperature: 创造性参数
            max_tokens: 最大输出token数
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Live2D参数映射
        self.live2d_params = {
            'eye_open': 'ParamEyeLOpen',
            'eye_open_r': 'ParamEyeROpen',
            'eyebrow_height': 'ParamEyeBrowLY',
            'eyebrow_height_r': 'ParamEyeBrowRY',
            'mouth_open': 'ParamMouthOpenY',
            'mouth_form': 'ParamMouthForm',
            'cheek': 'ParamCheek',
            'body_angle_x': 'ParamBodyAngleX',
            'body_angle_y': 'ParamBodyAngleY',
            'breath': 'ParamBreath'
        }

    def generate_expression(
        self,
        timestamp: float,
        tempo: float,
        energy: float,
        spectral_centroid: float,
        pitch: float,
        emotion_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        基于音乐特征生成表情参数

        Args:
            timestamp: 时间戳（秒）
            tempo: 节拍（BPM）
            energy: 能量级别（0-1）
            spectral_centroid: 频谱质心（0-1）
            pitch: 音高（Hz）
            emotion_scores: 情感分数字典

        Returns:
            Dict: Live2D表情参数
        """
        logger.info(f"生成表情参数: 时间点={timestamp}s, BPM={tempo}")

        # 基于规则的简化实现（可替换为LangChain + LLM）
        expression_params = self._rule_based_generation(
            timestamp, tempo, energy, spectral_centroid, pitch, emotion_scores
        )

        return expression_params

    def _rule_based_generation(
        self,
        timestamp: float,
        tempo: float,
        energy: float,
        spectral_centroid: float,
        pitch: float,
        emotion_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """基于规则的表情生成"""
        
        # 默认参数
        params = {
            'eye_open': 0.8,
            'eye_open_r': 0.8,
            'eyebrow_height': 0.5,
            'eyebrow_height_r': 0.5,
            'mouth_open': 0.2,
            'mouth_form': 0.3,
            'cheek': 0.0,
            'body_angle_x': 0.0,
            'body_angle_y': 0.0,
            'breath': 0.5
        }

        # 根据能量调整
        if energy > 0.7:
            params['eye_open'] = 1.0
            params['eye_open_r'] = 1.0
            params['mouth_open'] = 0.5 + (energy - 0.7) * 0.5
        elif energy < 0.3:
            params['eye_open'] = 0.6
            params['eye_open_r'] = 0.6
            params['mouth_open'] = 0.1

        # 根据情感调整
        if emotion_scores.get('happy', 0) > 0.5:
            params['mouth_form'] = 0.7
            params['eyebrow_height'] = 0.6
            params['eyebrow_height_r'] = 0.6
            params['cheek'] = 0.3

        if emotion_scores.get('sad', 0) > 0.5:
            params['eyebrow_height'] = 0.3
            params['eyebrow_height_r'] = 0.3
            params['mouth_form'] = 0.2
            params['eye_open'] = 0.6
            params['eye_open_r'] = 0.6

        if emotion_scores.get('energetic', 0) > 0.5:
            params['body_angle_x'] = 0.1 * (1 if int(timestamp * 2) % 2 == 0 else -1)
            params['breath'] = 0.8

        # 根据节拍调整
        if tempo > 120:
            # 快节奏，增加动作频率
            beat_phase = (timestamp * tempo / 60) % 1
            if beat_phase < 0.1:  # 节拍点
                params['eye_open'] = 0.2  # 眨眼
                params['eye_open_r'] = 0.2

        return params

    def batch_generate_expressions(
        self,
        feature_timeline: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        批量生成表情参数

        Args:
            feature_timeline: 特征时间线列表

        Returns:
            List[Dict]: 表情参数列表
        """
        expressions = []

        for features in feature_timeline:
            expression = self.generate_expression(
                timestamp=features.get('timestamp', 0),
                tempo=features.get('tempo', 100),
                energy=features.get('energy', 0.5),
                spectral_centroid=features.get('spectral_centroid', 0.5),
                pitch=features.get('pitch', 0),
                emotion_scores=features.get('emotion_scores', {})
            )

            expressions.append({
                'timestamp': features.get('timestamp', 0),
                'parameters': expression
            })

        return expressions
