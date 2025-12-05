"""
Live2D控制器模块
管理Live2D模型参数和动画
"""
from typing import Dict, List, Any
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Live2DController:
    """Live2D控制器"""

    def __init__(self, model_path: str = None):
        """
        初始化Live2D控制器

        Args:
            model_path: Live2D模型文件路径
        """
        self.model_path = model_path
        self.current_parameters = {}
        self.parameter_mapping = self._load_parameter_mapping()

    def _load_parameter_mapping(self) -> Dict[str, str]:
        """加载参数映射配置"""
        # 默认参数映射
        return {
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

    def update_parameters(self, parameters: Dict[str, float]):
        """
        更新Live2D参数

        Args:
            parameters: 参数字典
        """
        for key, value in parameters.items():
            if key in self.parameter_mapping:
                self.current_parameters[key] = value

    def get_current_state(self) -> Dict[str, float]:
        """获取当前参数状态"""
        return self.current_parameters.copy()

    def export_animation(
        self,
        expressions: List[Dict[str, Any]],
        output_path: str
    ) -> str:
        """
        导出动画文件

        Args:
            expressions: 表情关键帧列表
            output_path: 输出路径

        Returns:
            str: 输出文件路径
        """
        animation_data = {
            'Version': 3,
            'Meta': {
                'Duration': expressions[-1]['timestamp'] if expressions else 0,
                'Fps': 30,
                'Loop': False,
                'AreBeziersRestricted': True,
                'CurveCount': len(self.parameter_mapping),
                'TotalPointCount': len(expressions),
                'TotalSegmentCount': len(expressions) - 1 if len(expressions) > 1 else 0,
                'UserDataCount': 0,
                'TotalUserDataSize': 0
            },
            'Curves': self._build_curves(expressions)
        }

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(animation_data, f, indent=2)

        logger.info(f"动画文件已导出: {output_file}")
        return str(output_file)

    def _build_curves(self, expressions: List[Dict[str, Any]]) -> List[Dict]:
        """构建动画曲线"""
        curves = []

        for param_key, param_id in self.parameter_mapping.items():
            segments = []

            for i, expr in enumerate(expressions):
                value = expr['parameters'].get(param_key, 0.0)

                segments.append({
                    'Time': expr['timestamp'],
                    'Value': value
                })

            curves.append({
                'Target': 'Parameter',
                'Id': param_id,
                'Segments': segments
            })

        return curves
