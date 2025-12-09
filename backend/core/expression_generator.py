"""
表情生成器模块
整合音频分析和AI生成，创建完整的表情动画 - 完全AI驱动
"""
from typing import Dict, List, Any, Optional
import json
import logging
from pathlib import Path
from .audio_analyzer import AudioAnalyzerAgent, AudioFeatures
from .langchain_agent import ExpressionAgentV2

logger = logging.getLogger(__name__)


class ExpressionGenerator:
    """表情生成器 - 完全AI驱动"""

    def __init__(
        self,
        audio_analyzer: Optional[AudioAnalyzerAgent] = None,
        expression_agent: Optional[ExpressionAgentV2] = None,
        api_key: Optional[str] = None,
        model_name: str = "gpt-4.1",
        use_gemini: bool = False
    ):
        """
        初始化表情生成器

        Args:
            audio_analyzer: 音频分析器实例
            expression_agent: 表情代理实例
            api_key: API密钥
            model_name: 模型名称
            use_gemini: 是否使用Gemini
        """
        self.audio_analyzer = audio_analyzer or AudioAnalyzerAgent(
            api_key=api_key,
            model_name=model_name,
            use_gemini=use_gemini
        )
        self.expression_agent = expression_agent or ExpressionAgentV2(
            api_key=api_key,
            model_name=model_name,
            use_gemini=use_gemini
        )

    def generate_from_audio(
        self,
        audio_path: str,
        time_resolution: float = 0.1,
        enable_smoothing: bool = True
    ) -> Dict[str, Any]:
        """
        从音频文件生成表情动画

        Args:
            audio_path: 音频文件路径
            time_resolution: 时间分辨率（秒）
            enable_smoothing: 是否启用平滑处理

        Returns:
            Dict: 表情动画数据
        """
        logger.info(f"开始生成表情动画: {audio_path}")

        # 1. 分析音频
        audio_features = self.audio_analyzer.analyze(audio_path)

        # 2. 构建特征时间线
        feature_timeline = self._build_feature_timeline(
            audio_features, time_resolution
        )

        # 3. 生成表情参数
        expressions = self.expression_agent.batch_generate_expressions(
            feature_timeline
        )

        # 4. 平滑处理
        if enable_smoothing:
            expressions = self._smooth_expressions(expressions)

        # 5. 构建输出数据
        result = {
            'duration': audio_features.duration,
            'tempo': audio_features.tempo,
            'emotion_scores': audio_features.emotion_scores,
            'expressions': expressions,
            'metadata': {
                'time_resolution': time_resolution,
                'smoothing_enabled': enable_smoothing,
                'total_keyframes': len(expressions)
            }
        }

        logger.info(f"表情动画生成完成，共 {len(expressions)} 个关键帧")
        return result

    def _build_feature_timeline(
        self,
        audio_features: AudioFeatures,
        time_resolution: float
    ) -> List[Dict[str, Any]]:
        """构建特征时间线"""
        timeline = []
        num_frames = int(audio_features.duration / time_resolution)

        for i in range(num_frames):
            timestamp = i * time_resolution
            frame_index = int(timestamp / (len(audio_features.energy) / audio_features.duration))
            frame_index = min(frame_index, len(audio_features.energy) - 1)

            features = {
                'timestamp': timestamp,
                'tempo': audio_features.tempo,
                'energy': float(audio_features.energy[frame_index]),
                'spectral_centroid': float(audio_features.spectral_centroid[frame_index]),
                'pitch': float(audio_features.pitch[frame_index]) if frame_index < len(audio_features.pitch) else 0,
                'emotion_scores': audio_features.emotion_scores
            }

            timeline.append(features)

        return timeline

    def _smooth_expressions(
        self,
        expressions: List[Dict[str, Any]],
        window_size: int = 3
    ) -> List[Dict[str, Any]]:
        """平滑表情参数"""
        if len(expressions) < window_size:
            return expressions

        smoothed = []

        for i, expr in enumerate(expressions):
            # 获取窗口内的表情
            start = max(0, i - window_size // 2)
            end = min(len(expressions), i + window_size // 2 + 1)
            window = expressions[start:end]

            # 对每个参数取平均
            smoothed_params = {}
            param_keys = expr['parameters'].keys()

            for key in param_keys:
                values = [e['parameters'][key] for e in window]
                smoothed_params[key] = sum(values) / len(values)

            smoothed.append({
                'timestamp': expr['timestamp'],
                'parameters': smoothed_params
            })

        return smoothed

    def export_to_file(
        self,
        expression_data: Dict[str, Any],
        output_path: str,
        format: str = 'json'
    ) -> str:
        """
        导出表情数据到文件

        Args:
            expression_data: 表情数据
            output_path: 输出文件路径
            format: 输出格式（json）

        Returns:
            str: 输出文件路径
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if format == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(expression_data, f, indent=2, ensure_ascii=False)

        logger.info(f"表情数据已导出到: {output_file}")
        return str(output_file)
