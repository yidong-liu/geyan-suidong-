# 后端开发指南

## 🏗️ 后端架构概述

后端采用 **FastAPI + LangChain** 架构，负责音频分析、表情生成和 API 服务。主要模块包括：

- **音频分析模块**: 使用 librosa 进行音频特征提取
- **LangChain 代理**: 基于 AI 的表情映射生成
- **FastAPI 服务**: RESTful API 接口提供
- **数据模型**: Pydantic 数据验证和序列化

## 📁 后端目录结构

```
backend/
├── core/                           # 核心业务逻辑
│   ├── __init__.py
│   ├── audio_analyzer.py          # 音频分析器
│   ├── expression_generator.py    # 表情生成器
│   ├── langchain_agent.py         # LangChain代理
│   └── live2d_controller.py       # Live2D控制器
├── api/                           # API路由和接口
│   ├── __init__.py
│   ├── main.py                   # FastAPI主应用
│   ├── routes/                   # 路由模块
│   │   ├── __init__.py
│   │   ├── upload.py            # 文件上传路由
│   │   ├── analyze.py           # 分析处理路由
│   │   └── expression.py        # 表情相关路由
│   └── dependencies.py          # 依赖注入
├── models/                      # 数据模型
│   ├── __init__.py
│   ├── audio.py                # 音频相关模型
│   ├── expression.py           # 表情相关模型
│   └── response.py             # 响应模型
├── utils/                      # 工具函数
│   ├── __init__.py
│   ├── file_utils.py          # 文件处理工具
│   ├── audio_utils.py         # 音频处理工具
│   └── config.py              # 配置管理
└── tests/                     # 后端测试
    ├── test_audio_analyzer.py
    ├── test_expression_generator.py
    └── test_api.py
```

## 🔧 核心模块开发

### 1. 音频分析器 (AudioAnalyzer)

#### `backend/core/audio_analyzer.py`

```python
import librosa
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class AudioFeatures:
    """音频特征数据类"""
    duration: float
    tempo: float
    beats: List[float]
    pitch: List[float]
    energy: List[float]
    spectral_centroid: List[float]
    mfcc: np.ndarray
    emotion_scores: Dict[str, float]
    timestamps: List[float]

class AudioAnalyzer:
    """音频分析器"""

    def __init__(self, sample_rate: int = 44100, hop_length: int = 512):
        self.sample_rate = sample_rate
        self.hop_length = hop_length
        self.frame_length = 2048

    def analyze(self, audio_path: str) -> AudioFeatures:
        """
        分析音频文件，提取所有特征

        Args:
            audio_path: 音频文件路径

        Returns:
            AudioFeatures: 提取的音频特征
        """
        logger.info(f"开始分析音频文件: {audio_path}")

        try:
            # 加载音频
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            duration = librosa.get_duration(y=y, sr=sr)

            # 提取各种特征
            tempo, beats = self._extract_tempo_and_beats(y, sr)
            pitch = self._extract_pitch(y, sr)
            energy = self._extract_energy(y, sr)
            spectral_centroid = self._extract_spectral_centroid(y, sr)
            mfcc = self._extract_mfcc(y, sr)
            emotion_scores = self._analyze_emotion(y, sr)

            # 生成时间戳
            timestamps = librosa.frames_to_time(
                np.arange(len(energy)),
                sr=sr,
                hop_length=self.hop_length
            ).tolist()

            features = AudioFeatures(
                duration=duration,
                tempo=tempo,
                beats=beats.tolist(),
                pitch=pitch.tolist(),
                energy=energy.tolist(),
                spectral_centroid=spectral_centroid.tolist(),
                mfcc=mfcc,
                emotion_scores=emotion_scores,
                timestamps=timestamps
            )

            logger.info(f"音频分析完成，时长: {duration:.2f}秒, BPM: {tempo:.1f}")
            return features

        except Exception as e:
            logger.error(f"音频分析失败: {str(e)}")
            raise

    def _extract_tempo_and_beats(self, y: np.ndarray, sr: int) -> Tuple[float, np.ndarray]:
        """提取节拍和BPM"""
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
        beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=self.hop_length)
        return float(tempo), beat_times

    def _extract_pitch(self, y: np.ndarray, sr: int) -> np.ndarray:
        """提取音高"""
        pitches, magnitudes = librosa.piptrack(
            y=y, sr=sr, hop_length=self.hop_length
        )

        # 提取主要音高
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t] if magnitudes[index, t] > 0 else 0
            pitch_values.append(pitch)

        return np.array(pitch_values)

    def _extract_energy(self, y: np.ndarray, sr: int) -> np.ndarray:
        """提取能量"""
        # RMS能量
        rms = librosa.feature.rms(
            y=y, hop_length=self.hop_length, frame_length=self.frame_length
        )[0]

        # 归一化到0-1
        rms = rms / np.max(rms) if np.max(rms) > 0 else rms
        return rms

    def _extract_spectral_centroid(self, y: np.ndarray, sr: int) -> np.ndarray:
        """提取频谱质心"""
        spectral_centroid = librosa.feature.spectral_centroid(
            y=y, sr=sr, hop_length=self.hop_length
        )[0]

        # 归一化
        spectral_centroid = spectral_centroid / np.max(spectral_centroid)
        return spectral_centroid

    def _extract_mfcc(self, y: np.ndarray, sr: int, n_mfcc: int = 13) -> np.ndarray:
        """提取MFCC特征"""
        mfcc = librosa.feature.mfcc(
            y=y, sr=sr, n_mfcc=n_mfcc, hop_length=self.hop_length
        )
        return mfcc

    def _analyze_emotion(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """
        简单的情感分析
        基于音频特征推断情感状态
        """
        # 提取特征用于情感分析
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        energy = np.mean(librosa.feature.rms(y=y, hop_length=self.hop_length))
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))

        # 简单的规则基础情感分析
        emotion_scores = {
            'happy': 0.0,
            'sad': 0.0,
            'energetic': 0.0,
            'calm': 0.0,
            'angry': 0.0
        }

        # 基于节拍判断
        if tempo > 120:
            emotion_scores['happy'] += 0.3
            emotion_scores['energetic'] += 0.4
        elif tempo < 80:
            emotion_scores['sad'] += 0.3
            emotion_scores['calm'] += 0.4

        # 基于能量判断
        if energy > 0.1:
            emotion_scores['energetic'] += 0.3
            emotion_scores['angry'] += 0.2
        else:
            emotion_scores['calm'] += 0.3
            emotion_scores['sad'] += 0.2

        # 基于频谱质心判断
        if spectral_centroid > 3000:
            emotion_scores['happy'] += 0.2
            emotion_scores['energetic'] += 0.2
        else:
            emotion_scores['sad'] += 0.2
            emotion_scores['calm'] += 0.2

        # 归一化情感分数
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            emotion_scores = {k: v/total_score for k, v in emotion_scores.items()}

        return emotion_scores

    def extract_features_at_time(self, audio_path: str, time_point: float) -> Dict:
        """
        提取指定时间点的音频特征

        Args:
            audio_path: 音频文件路径
            time_point: 时间点（秒）

        Returns:
            Dict: 该时间点的特征
        """
        y, sr = librosa.load(audio_path, sr=self.sample_rate)

        # 计算对应的帧索引
        frame = int(time_point * sr // self.hop_length)

        # 提取该帧的特征
        rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

        if frame < len(rms):
            return {
                'time': time_point,
                'energy': float(rms[frame]),
                'spectral_centroid': float(spectral_centroid[frame]),
                'pitch': self._get_pitch_at_frame(y, sr, frame)
            }
        else:
            return None

    def _get_pitch_at_frame(self, y: np.ndarray, sr: int, frame: int) -> float:
        """获取指定帧的音高"""
        # 简化的音高提取
        start_sample = frame * self.hop_length
        end_sample = start_sample + self.frame_length

        if end_sample < len(y):
            segment = y[start_sample:end_sample]
            pitches, magnitudes = librosa.piptrack(
                y=segment, sr=sr, hop_length=self.hop_length
            )

            if pitches.size > 0 and magnitudes.size > 0:
                index = magnitudes[:, 0].argmax()
                return float(pitches[index, 0]) if magnitudes[index, 0] > 0 else 0.0

        return 0.0
```

### 2. LangChain 代理 (ExpressionAgent)

#### `backend/core/langchain_agent.py`

```python
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, SystemMessage
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

        # 初始化LLM
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # 构建表情生成链
        self.expression_chain = self._build_expression_chain()

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

    def _build_expression_chain(self) -> LLMChain:
        """构建表情生成链"""

        system_template = """
你是一个专业的虚拟人表情设计师，擅长根据音乐特征为Live2D角色设计表情动画。

Live2D参数说明：
- eye_open (眼部开合): 0.0=闭眼, 1.0=完全睁开
- eyebrow_height (眉毛高度): 0.0=下垂, 0.5=正常, 1.0=上扬
- mouth_open (嘴部开合): 0.0=闭嘴, 1.0=张大嘴
- mouth_form (嘴型): 0.0=默认, 0.5=微笑, 1.0=大笑
- cheek (脸颊红晕): 0.0=无红晕, 1.0=满红晕
- body_angle_x (身体X轴角度): -1.0到1.0，左右摆动
- breath (呼吸): 0.0到1.0，呼吸幅度

表情设计原则：
1. 根据音乐节拍调整眨眼和点头频率
2. 根据情感强度调整表情夸张程度
3. 保持表情自然过渡，避免突兀变化
4. 考虑音乐类型的文化特征
"""

        human_template = """
基于以下音乐特征，为虚拟角色设计表情参数：

时间点: {timestamp}秒
节拍: {tempo} BPM
能量级别: {energy} (0-1)
频谱质心: {spectral_centroid} (0-1)
音高: {pitch} Hz
情感分析: {emotion_scores}

请生成Live2D表情参数，格式如下：
{{
    "eye_open": 0.8,
    "eyebrow_height": 0.5,
    "mouth_open": 0.3,
    "mouth_form": 0.4,
    "cheek": 0.1,
    "body_angle_x": 0.0,
    "breath": 0.6,
    "transition_duration": 0.5,
    "reasoning": "基于当前音乐特征的设计思路"
}}

只返回JSON格式，不要其他解释。
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", human_template)
        ])

        return LLMChain(llm=self.llm, prompt=prompt)

    def generate_expression(self, audio_features: Dict) -> Dict:
        """
        基于音频特征生成表情参数

        Args:
            audio_features: 音频特征字典

        Returns:
            Dict: Live2D表情参数
        """
        try:
            # 调用LLM生成表情
            response = self.expression_chain.run(**audio_features)

            # 解析JSON响应
            expression_data = json.loads(response)

            # 验证和修正参数范围
            expression_data = self._validate_parameters(expression_data)

            # 转换为Live2D参数名
            live2d_params = self._convert_to_live2d_params(expression_data)

            logger.info(f"生成表情参数: {live2d_params}")
            return live2d_params

        except Exception as e:
            logger.error(f"表情生成失败: {str(e)}")
            # 返回默认表情
            return self._get_default_expression()

    def generate_expression_timeline(
        self,
        audio_features_timeline: List[Dict],
        smoothing: bool = True
    ) -> List[Dict]:
        """
        生成完整的表情时间轴

        Args:
            audio_features_timeline: 音频特征时间轴列表
            smoothing: 是否启用平滑处理

        Returns:
            List[Dict]: 表情参数时间轴
        """
        expression_timeline = []

        for i, features in enumerate(audio_features_timeline):
            try:
                # 生成当前时间点的表情
                expression = self.generate_expression(features)

                # 添加时间戳
                expression['timestamp'] = features.get('timestamp', 0)

                # 如果启用平滑处理
                if smoothing and i > 0:
                    expression = self._smooth_expression(
                        expression_timeline[-1],
                        expression
                    )

                expression_timeline.append(expression)

            except Exception as e:
                logger.error(f"时间点 {features.get('timestamp', 0)} 表情生成失败: {str(e)}")
                continue

        logger.info(f"生成表情时间轴，共 {len(expression_timeline)} 个关键帧")
        return expression_timeline

    def _validate_parameters(self, params: Dict) -> Dict:
        """验证和修正参数范围"""
        valid_params = {}

        # 参数范围定义
        param_ranges = {
            'eye_open': (0.0, 1.0),
            'eyebrow_height': (0.0, 1.0),
            'mouth_open': (0.0, 1.0),
            'mouth_form': (0.0, 1.0),
            'cheek': (0.0, 1.0),
            'body_angle_x': (-1.0, 1.0),
            'breath': (0.0, 1.0),
            'transition_duration': (0.1, 3.0)
        }

        for param, (min_val, max_val) in param_ranges.items():
            if param in params:
                value = params[param]
                # 确保是数字
                if isinstance(value, (int, float)):
                    # 限制范围
                    valid_params[param] = max(min_val, min(max_val, float(value)))
                else:
                    valid_params[param] = (min_val + max_val) / 2  # 默认中间值
            else:
                valid_params[param] = (min_val + max_val) / 2

        # 保留推理信息
        if 'reasoning' in params:
            valid_params['reasoning'] = params['reasoning']

        return valid_params

    def _convert_to_live2d_params(self, expression_params: Dict) -> Dict:
        """转换为Live2D参数格式"""
        live2d_data = {
            'parameters': {},
            'metadata': {}
        }

        # 转换参数
        for key, value in expression_params.items():
            if key in self.live2d_params:
                live2d_param_name = self.live2d_params[key]
                live2d_data['parameters'][live2d_param_name] = value
            elif key == 'transition_duration':
                live2d_data['metadata']['transition_duration'] = value
            elif key == 'reasoning':
                live2d_data['metadata']['reasoning'] = value

        return live2d_data

    def _smooth_expression(self, prev_expression: Dict, curr_expression: Dict) -> Dict:
        """表情平滑处理"""
        smoothed = curr_expression.copy()

        # 获取前一帧的参数
        prev_params = prev_expression.get('parameters', {})
        curr_params = curr_expression.get('parameters', {})

        # 平滑因子
        alpha = 0.3

        # 对每个参数进行平滑
        for param_name in curr_params:
            if param_name in prev_params:
                prev_val = prev_params[param_name]
                curr_val = curr_params[param_name]
                # 线性插值平滑
                smoothed_val = prev_val * (1 - alpha) + curr_val * alpha
                smoothed['parameters'][param_name] = smoothed_val

        return smoothed

    def _get_default_expression(self) -> Dict:
        """获取默认表情"""
        return {
            'parameters': {
                'ParamEyeLOpen': 1.0,
                'ParamEyeROpen': 1.0,
                'ParamEyeBrowLY': 0.5,
                'ParamEyeBrowRY': 0.5,
                'ParamMouthOpenY': 0.2,
                'ParamMouthForm': 0.3,
                'ParamCheek': 0.0,
                'ParamBodyAngleX': 0.0,
                'ParamBreath': 0.5
            },
            'metadata': {
                'transition_duration': 0.5,
                'reasoning': '默认中性表情'
            }
        }

    def customize_expression_rules(self, custom_rules: Dict) -> None:
        """
        自定义表情映射规则

        Args:
            custom_rules: 自定义规则字典
        """
        # 这里可以实现用户自定义的表情映射规则
        # 例如：特定BPM范围对应特定表情强度
        pass
```

### 3. 表情生成器 (ExpressionGenerator)

#### `backend/core/expression_generator.py`

```python
import json
import numpy as np
from typing import Dict, List, Optional
from pathlib import Path
import logging
from .audio_analyzer import AudioAnalyzer, AudioFeatures
from .langchain_agent import ExpressionAgent

logger = logging.getLogger(__name__)

class ExpressionGenerator:
    """表情文件生成器"""

    def __init__(
        self,
        analyzer: Optional[AudioAnalyzer] = None,
        agent: Optional[ExpressionAgent] = None
    ):
        """
        初始化表情生成器

        Args:
            analyzer: 音频分析器实例
            agent: 表情代理实例
        """
        self.analyzer = analyzer or AudioAnalyzer()
        self.agent = agent or ExpressionAgent()

    def generate_expression_file(
        self,
        audio_path: str,
        output_path: str,
        model_name: str = "default",
        time_resolution: float = 0.5,
        enable_smoothing: bool = True
    ) -> Dict:
        """
        生成完整的Live2D表情文件

        Args:
            audio_path: 音频文件路径
            output_path: 输出表情文件路径
            model_name: Live2D模型名称
            time_resolution: 时间分辨率（秒）
            enable_smoothing: 是否启用平滑处理

        Returns:
            Dict: 生成结果信息
        """
        try:
            logger.info(f"开始生成表情文件: {audio_path} -> {output_path}")

            # 1. 分析音频特征
            logger.info("步骤1: 分析音频特征")
            audio_features = self.analyzer.analyze(audio_path)

            # 2. 构建时间轴
            logger.info("步骤2: 构建时间轴")
            timeline = self._build_timeline(audio_features, time_resolution)

            # 3. 生成表情序列
            logger.info("步骤3: 生成表情序列")
            expressions = self.agent.generate_expression_timeline(
                timeline,
                smoothing=enable_smoothing
            )

            # 4. 构建最终的表情文件
            logger.info("步骤4: 构建表情文件")
            expression_file = self._build_expression_file(
                audio_features,
                expressions,
                model_name
            )

            # 5. 保存文件
            logger.info("步骤5: 保存表情文件")
            self._save_expression_file(expression_file, output_path)

            result = {
                'success': True,
                'output_path': output_path,
                'duration': audio_features.duration,
                'expression_count': len(expressions),
                'model_name': model_name,
                'metadata': {
                    'tempo': audio_features.tempo,
                    'emotion_scores': audio_features.emotion_scores,
                    'time_resolution': time_resolution
                }
            }

            logger.info(f"表情文件生成成功: {len(expressions)} 个关键帧")
            return result

        except Exception as e:
            logger.error(f"表情文件生成失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'output_path': output_path
            }

    def _build_timeline(self, audio_features: AudioFeatures, time_resolution: float) -> List[Dict]:
        """
        构建音频特征时间轴

        Args:
            audio_features: 音频特征
            time_resolution: 时间分辨率

        Returns:
            List[Dict]: 时间轴特征列表
        """
        timeline = []
        duration = audio_features.duration

        # 生成时间点
        time_points = np.arange(0, duration, time_resolution)

        for time_point in time_points:
            # 找到最接近的特征索引
            frame_idx = int(time_point * len(audio_features.timestamps) / duration)
            frame_idx = min(frame_idx, len(audio_features.timestamps) - 1)

            # 构建该时间点的特征
            timeline_point = {
                'timestamp': float(time_point),
                'tempo': audio_features.tempo,
                'energy': float(audio_features.energy[frame_idx]) if frame_idx < len(audio_features.energy) else 0.0,
                'spectral_centroid': float(audio_features.spectral_centroid[frame_idx]) if frame_idx < len(audio_features.spectral_centroid) else 0.0,
                'pitch': float(audio_features.pitch[frame_idx]) if frame_idx < len(audio_features.pitch) else 0.0,
                'emotion_scores': audio_features.emotion_scores,
                'is_beat': self._is_beat_at_time(time_point, audio_features.beats)
            }

            timeline.append(timeline_point)

        return timeline

    def _is_beat_at_time(self, time_point: float, beats: List[float], tolerance: float = 0.1) -> bool:
        """判断时间点是否接近节拍"""
        for beat_time in beats:
            if abs(time_point - beat_time) <= tolerance:
                return True
        return False

    def _build_expression_file(
        self,
        audio_features: AudioFeatures,
        expressions: List[Dict],
        model_name: str
    ) -> Dict:
        """
        构建最终的表情文件格式

        Args:
            audio_features: 音频特征
            expressions: 表情参数列表
            model_name: 模型名称

        Returns:
            Dict: 完整的表情文件
        """
        expression_file = {
            "metadata": {
                "version": "1.0",
                "format": "geyan-suidong-expression",
                "model_name": model_name,
                "duration": audio_features.duration,
                "fps": 30,  # 假设30fps
                "total_frames": int(audio_features.duration * 30),
                "expression_count": len(expressions),
                "generated_at": self._get_current_timestamp(),
                "audio_analysis": {
                    "tempo": audio_features.tempo,
                    "emotion_scores": audio_features.emotion_scores,
                    "beat_count": len(audio_features.beats)
                }
            },
            "expressions": []
        }

        # 处理表情数据
        for i, expr in enumerate(expressions):
            expression_entry = {
                "id": i,
                "timestamp": expr.get('timestamp', 0.0),
                "parameters": expr.get('parameters', {}),
                "transition_duration": expr.get('metadata', {}).get('transition_duration', 0.5),
                "easing": "easeInOutQuad",  # 缓动函数
                "metadata": {
                    "reasoning": expr.get('metadata', {}).get('reasoning', ''),
                    "energy_level": self._get_energy_level_at_time(
                        expr.get('timestamp', 0.0),
                        audio_features
                    )
                }
            }

            expression_file["expressions"].append(expression_entry)

        # 添加关键事件标记
        expression_file["events"] = self._extract_key_events(audio_features)

        return expression_file

    def _get_energy_level_at_time(self, timestamp: float, audio_features: AudioFeatures) -> float:
        """获取指定时间的能量级别"""
        if not audio_features.timestamps:
            return 0.0

        # 找到最接近的时间索引
        time_array = np.array(audio_features.timestamps)
        closest_idx = np.argmin(np.abs(time_array - timestamp))

        if closest_idx < len(audio_features.energy):
            return float(audio_features.energy[closest_idx])
        return 0.0

    def _extract_key_events(self, audio_features: AudioFeatures) -> List[Dict]:
        """提取关键音乐事件"""
        events = []

        # 添加节拍事件
        for i, beat_time in enumerate(audio_features.beats):
            events.append({
                "type": "beat",
                "timestamp": float(beat_time),
                "index": i,
                "metadata": {
                    "tempo": audio_features.tempo
                }
            })

        # 添加能量峰值事件
        energy_threshold = np.percentile(audio_features.energy, 90)
        for i, energy in enumerate(audio_features.energy):
            if energy > energy_threshold:
                timestamp = audio_features.timestamps[i] if i < len(audio_features.timestamps) else 0
                events.append({
                    "type": "energy_peak",
                    "timestamp": float(timestamp),
                    "intensity": float(energy),
                    "metadata": {
                        "threshold": float(energy_threshold)
                    }
                })

        # 按时间排序
        events.sort(key=lambda x: x['timestamp'])
        return events

    def _save_expression_file(self, expression_data: Dict, output_path: str) -> None:
        """保存表情文件"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(expression_data, f, indent=2, ensure_ascii=False)

        logger.info(f"表情文件已保存: {output_path}")

    def _get_current_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    def validate_expression_file(self, file_path: str) -> Dict:
        """
        验证表情文件格式

        Args:
            file_path: 表情文件路径

        Returns:
            Dict: 验证结果
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 检查必需字段
            required_fields = ['metadata', 'expressions']
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return {
                    'valid': False,
                    'error': f'缺少必需字段: {missing_fields}'
                }

            # 检查表情参数
            expressions = data.get('expressions', [])
            invalid_expressions = []

            for i, expr in enumerate(expressions):
                if 'timestamp' not in expr or 'parameters' not in expr:
                    invalid_expressions.append(i)

            if invalid_expressions:
                return {
                    'valid': False,
                    'error': f'表情 {invalid_expressions} 格式无效'
                }

            return {
                'valid': True,
                'metadata': data.get('metadata', {}),
                'expression_count': len(expressions),
                'duration': data.get('metadata', {}).get('duration', 0)
            }

        except Exception as e:
            return {
                'valid': False,
                'error': f'文件读取错误: {str(e)}'
            }
```

### 4. FastAPI 主应用

#### `backend/api/main.py`

```python
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional, Dict, Any
import uvicorn
import os
import shutil
import uuid
from pathlib import Path
import logging

# 导入自定义模块
from ..core.audio_analyzer import AudioAnalyzer
from ..core.langchain_agent import ExpressionAgent
from ..core.expression_generator import ExpressionGenerator
from ..utils.file_utils import get_file_extension, validate_audio_file
from ..utils.config import get_settings
from ..models.response import ResponseModel, AudioAnalysisResponse, ExpressionGenerationResponse

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取设置
settings = get_settings()

# 创建FastAPI应用
app = FastAPI(
    title="歌颜随动 API",
    description="音乐表情生成API服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化核心组件
audio_analyzer = AudioAnalyzer()
expression_agent = ExpressionAgent()
expression_generator = ExpressionGenerator(audio_analyzer, expression_agent)

# 存储处理状态
processing_status: Dict[str, Dict] = {}

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    logger.info("歌颜随动 API 服务启动")

    # 确保必要的目录存在
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.expressions_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.temp_dir).mkdir(parents=True, exist_ok=True)

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "歌颜随动 API 服务",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": "2024-12-05"}

@app.post("/api/upload-audio", response_model=ResponseModel)
async def upload_audio(file: UploadFile = File(...)):
    """
    上传音频文件

    Args:
        file: 上传的音频文件

    Returns:
        ResponseModel: 包含文件ID的响应
    """
    try:
        # 验证文件类型
        if not validate_audio_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail="不支持的音频格式，请上传 MP3, WAV, M4A 格式的文件"
            )

        # 生成唯一文件ID
        file_id = str(uuid.uuid4())
        file_extension = get_file_extension(file.filename)
        file_path = Path(settings.upload_dir) / f"{file_id}{file_extension}"

        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 记录文件信息
        file_info = {
            "file_id": file_id,
            "original_name": file.filename,
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "status": "uploaded"
        }

        processing_status[file_id] = file_info

        logger.info(f"音频文件上传成功: {file.filename} -> {file_id}")

        return ResponseModel(
            success=True,
            message="文件上传成功",
            data={
                "file_id": file_id,
                "original_name": file.filename,
                "file_size": file_info["file_size"]
            }
        )

    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@app.post("/api/analyze-audio/{file_id}", response_model=AudioAnalysisResponse)
async def analyze_audio(file_id: str):
    """
    分析音频文件

    Args:
        file_id: 文件ID

    Returns:
        AudioAnalysisResponse: 音频分析结果
    """
    try:
        # 检查文件是否存在
        if file_id not in processing_status:
            raise HTTPException(status_code=404, detail="文件不存在")

        file_info = processing_status[file_id]
        file_path = file_info["file_path"]

        if not Path(file_path).exists():
            raise HTTPException(status_code=404, detail="音频文件不存在")

        # 更新状态
        file_info["status"] = "analyzing"

        # 分析音频
        logger.info(f"开始分析音频: {file_id}")
        audio_features = audio_analyzer.analyze(file_path)

        # 构建响应数据
        analysis_result = {
            "file_id": file_id,
            "duration": audio_features.duration,
            "tempo": audio_features.tempo,
            "beat_count": len(audio_features.beats),
            "emotion_scores": audio_features.emotion_scores,
            "energy_stats": {
                "mean": float(audio_features.energy.mean()),
                "max": float(audio_features.energy.max()),
                "min": float(audio_features.energy.min())
            },
            "spectral_stats": {
                "mean": float(audio_features.spectral_centroid.mean()),
                "max": float(audio_features.spectral_centroid.max()),
                "min": float(audio_features.spectral_centroid.min())
            }
        }

        # 更新状态
        file_info["status"] = "analyzed"
        file_info["analysis_result"] = analysis_result

        logger.info(f"音频分析完成: {file_id}, 时长: {audio_features.duration:.2f}秒")

        return AudioAnalysisResponse(
            success=True,
            message="音频分析完成",
            data=analysis_result
        )

    except Exception as e:
        logger.error(f"音频分析失败: {str(e)}")
        if file_id in processing_status:
            processing_status[file_id]["status"] = "error"
            processing_status[file_id]["error"] = str(e)
        raise HTTPException(status_code=500, detail=f"音频分析失败: {str(e)}")

@app.post("/api/generate-expression/{file_id}", response_model=ExpressionGenerationResponse)
async def generate_expression(
    file_id: str,
    background_tasks: BackgroundTasks,
    model_name: str = "default",
    time_resolution: float = 0.5,
    enable_smoothing: bool = True
):
    """
    生成表情文件

    Args:
        file_id: 文件ID
        model_name: Live2D模型名称
        time_resolution: 时间分辨率
        enable_smoothing: 是否启用平滑处理

    Returns:
        ExpressionGenerationResponse: 表情生成结果
    """
    try:
        # 检查文件状态
        if file_id not in processing_status:
            raise HTTPException(status_code=404, detail="文件不存在")

        file_info = processing_status[file_id]

        if file_info.get("status") != "analyzed":
            raise HTTPException(status_code=400, detail="请先完成音频分析")

        file_path = file_info["file_path"]

        # 生成输出路径
        expression_id = str(uuid.uuid4())
        output_path = Path(settings.expressions_dir) / f"{expression_id}.json"

        # 更新状态
        file_info["status"] = "generating"

        # 生成表情文件
        logger.info(f"开始生成表情文件: {file_id} -> {expression_id}")

        result = expression_generator.generate_expression_file(
            audio_path=file_path,
            output_path=str(output_path),
            model_name=model_name,
            time_resolution=time_resolution,
            enable_smoothing=enable_smoothing
        )

        if result["success"]:
            # 更新状态
            file_info["status"] = "completed"
            file_info["expression_id"] = expression_id
            file_info["expression_path"] = str(output_path)

            response_data = {
                "file_id": file_id,
                "expression_id": expression_id,
                "expression_file": str(output_path),
                "duration": result["duration"],
                "expression_count": result["expression_count"],
                "model_name": result["model_name"],
                "metadata": result["metadata"]
            }

            logger.info(f"表情文件生成成功: {expression_id}")

            return ExpressionGenerationResponse(
                success=True,
                message="表情文件生成成功",
                data=response_data
            )
        else:
            # 生成失败
            file_info["status"] = "error"
            file_info["error"] = result["error"]

            raise HTTPException(
                status_code=500,
                detail=f"表情生成失败: {result['error']}"
            )

    except Exception as e:
        logger.error(f"表情生成失败: {str(e)}")
        if file_id in processing_status:
            processing_status[file_id]["status"] = "error"
            processing_status[file_id]["error"] = str(e)
        raise HTTPException(status_code=500, detail=f"表情生成失败: {str(e)}")

@app.get("/api/expression/{expression_id}")
async def get_expression_file(expression_id: str):
    """
    获取表情文件

    Args:
        expression_id: 表情文件ID

    Returns:
        FileResponse: 表情文件
    """
    expression_path = Path(settings.expressions_dir) / f"{expression_id}.json"

    if not expression_path.exists():
        raise HTTPException(status_code=404, detail="表情文件不存在")

    return FileResponse(
        path=expression_path,
        media_type="application/json",
        filename=f"{expression_id}.json"
    )

@app.get("/api/status/{file_id}")
async def get_processing_status(file_id: str):
    """
    获取处理状态

    Args:
        file_id: 文件ID

    Returns:
        Dict: 处理状态信息
    """
    if file_id not in processing_status:
        raise HTTPException(status_code=404, detail="文件不存在")

    return processing_status[file_id]

@app.get("/api/models")
async def list_available_models():
    """
    获取可用的Live2D模型列表

    Returns:
        Dict: 模型列表
    """
    # 这里应该扫描models目录获取实际的模型列表
    models = [
        {
            "id": "default",
            "name": "默认角色",
            "description": "标准的虚拟角色模型",
            "preview_image": "/models/default/preview.png"
        },
        {
            "id": "hiyori",
            "name": "Hiyori",
            "description": "可爱的日系虚拟角色",
            "preview_image": "/models/hiyori/preview.png"
        }
    ]

    return {
        "success": True,
        "data": {
            "models": models,
            "count": len(models)
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug
    )
```

## 🧪 测试示例

### `backend/tests/test_audio_analyzer.py`

```python
import pytest
import numpy as np
from pathlib import Path
from backend.core.audio_analyzer import AudioAnalyzer

class TestAudioAnalyzer:

    def test_analyzer_initialization(self):
        """测试分析器初始化"""
        analyzer = AudioAnalyzer()
        assert analyzer.sample_rate == 44100
        assert analyzer.hop_length == 512

    @pytest.mark.skipif(not Path("tests/data/test.wav").exists(),
                       reason="测试音频文件不存在")
    def test_audio_analysis(self):
        """测试音频分析功能"""
        analyzer = AudioAnalyzer()
        features = analyzer.analyze("tests/data/test.wav")

        assert features.duration > 0
        assert features.tempo > 0
        assert len(features.beats) > 0
        assert len(features.energy) > 0
        assert isinstance(features.emotion_scores, dict)
```

---

这个后端开发指南为您提供了完整的后端开发框架和实现方案。每个模块都有详细的代码示例和说明，可以直接用于项目开发。
