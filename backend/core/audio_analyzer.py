"""
音频分析器模块
使用librosa进行音频特征提取，使用LangChain AI进行情感分析
"""
import librosa
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging
import os
from dotenv import load_dotenv

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
logger = logging.getLogger(__name__)

class EmotionScores(BaseModel):
    """情感分数模型"""
    happy: float = Field(description="快乐程度 (0-1)", ge=0.0, le=1.0)
    sad: float = Field(description="悲伤程度 (0-1)", ge=0.0, le=1.0)
    energetic: float = Field(description="活力程度 (0-1)", ge=0.0, le=1.0)
    calm: float = Field(description="平静程度 (0-1)", ge=0.0, le=1.0)
    angry: float = Field(description="愤怒程度 (0-1)", ge=0.0, le=1.0)


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


class AudioAnalyzerAgent:
    """基于LangChain的音频分析代理 - 完全AI驱动"""

    def __init__(
        self,
        sample_rate: int = 44100,
        hop_length: int = 512,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: str = "gpt-4.1",
        temperature: float = 0.3,
        max_tokens: int = 500,
        use_gemini: bool = False
    ):
        """
        初始化音频分析代理

        Args:
            sample_rate: 采样率
            hop_length: 跳跃长度
            api_key: API密钥
            base_url: API基础URL (仅OpenAI)
            model_name: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            use_gemini: 是否使用Gemini（默认True）
        """
        self.sample_rate = sample_rate
        self.hop_length = hop_length
        self.frame_length = 2048
        
        # AI配置
        self.use_gemini = use_gemini
        if self.use_gemini:
            self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
            self.model_name = model_name or os.getenv('GOOGLE_MODEL', 'gemini-1.5-flash')
            self.base_url = None
        else:
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            self.base_url = base_url or os.getenv('OPENAI_API_BASE')
            self.model_name = model_name
            
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if not self.api_key:
            raise ValueError("未找到 API 密钥，请设置 GOOGLE_API_KEY 或 OPENAI_API_KEY 环境变量")
        
        # 初始化LLM
        self._setup_llm()
        self._setup_emotion_chain()

    def _setup_llm(self):
        """初始化LLM"""
        try:
            if self.use_gemini:
                llm_kwargs = {
                    "model": self.model_name,
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                    "google_api_key": self.api_key,
                }
                self.llm = ChatGoogleGenerativeAI(**llm_kwargs)
                logger.info(f"Google Gemini LLM 初始化成功: {self.model_name}")
            else:
                llm_kwargs = {
                    "model": self.model_name,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "api_key": self.api_key,
                }
                if self.base_url:
                    llm_kwargs["base_url"] = self.base_url
                    logger.info(f"使用自定义 base_url: {self.base_url}")
                self.llm = ChatOpenAI(**llm_kwargs)
                logger.info(f"OpenAI LLM 初始化成功: {self.model_name}")
        except Exception as e:
            logger.error(f"LLM 初始化失败: {e}")
            raise

    def _setup_emotion_chain(self):
        """设置情感分析链"""
        system_template = """你是一个专业的音频情感分析专家。
你需要根据音频的特征参数（节奏、能量、频谱、零交叉率等）来判断音乐的情感分布。

分析维度：
- happy: 快乐、欢快的程度
- sad: 悲伤、忧郁的程度
- energetic: 活力、激昂的程度
- calm: 平静、舒缓的程度
- angry: 愤怒、激烈的程度

音频特征解释：
- tempo (BPM): 节拍速度，快节奏通常更energetic/happy，慢节奏更calm/sad
- energy: 能量强度，高能量通常更energetic/angry，低能量更calm/sad
- spectral_centroid: 频谱质心，高值表示明亮音色(happy/energetic)，低值表示暗沉音色(sad/calm)
- zero_crossing_rate: 零交叉率，高值表示噪音或打击乐(energetic/angry)，低值表示纯音(calm)

输出要求：
1. 所有情感分数必须在 0-1 之间
2. 所有分数之和应该接近 1.0（允许0.9-1.1范围）
3. 必须返回严格的JSON格式
4. 根据特征给出合理的情感分布"""

        human_template = """请分析以下音频特征的情感分布：

节奏(BPM): {tempo}
能量强度: {energy}
频谱质心: {spectral_centroid}
零交叉率: {zero_crossing_rate}

请返回JSON格式的情感分数："""

        self.emotion_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template)
        ])
        
        self.emotion_parser = JsonOutputParser(pydantic_object=EmotionScores)

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
        AI驱动的情感分析
        使用 LangChain + Gemini/OpenAI 进行情感判断
        """
        # 提取特征用于情感分析
        tempo_raw, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(tempo_raw) if isinstance(tempo_raw, (int, float)) else float(tempo_raw.item())
        energy = float(np.mean(librosa.feature.rms(y=y, hop_length=self.hop_length)))
        spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        zero_crossing_rate = float(np.mean(librosa.feature.zero_crossing_rate(y)))

        logger.info(f"情感分析输入 - BPM:{tempo:.1f}, 能量:{energy:.3f}, 质心:{spectral_centroid:.1f}, ZCR:{zero_crossing_rate:.3f}")

        try:
            # 准备输入数据
            input_data = {
                "tempo": f"{tempo:.2f}",
                "energy": f"{energy:.4f}",
                "spectral_centroid": f"{spectral_centroid:.2f}",
                "zero_crossing_rate": f"{zero_crossing_rate:.4f}"
            }

            # 构建链并执行
            chain = self.emotion_prompt | self.llm | self.emotion_parser
            result = chain.invoke(input_data)
            
            # 验证和归一化
            emotion_scores = self._validate_emotion_scores(result)
            
            logger.info(f"AI情感分析成功: {emotion_scores}")
            return emotion_scores

        except Exception as e:
            logger.error(f"AI情感分析失败: {e}")
            raise RuntimeError(f"情感分析失败: {e}")

    def _validate_emotion_scores(self, scores: Dict[str, Any]) -> Dict[str, float]:
        """验证并归一化情感分数"""
        emotion_keys = ['happy', 'sad', 'energetic', 'calm', 'angry']
        validated = {}
        
        # 提取分数
        for key in emotion_keys:
            value = scores.get(key, 0.0)
            validated[key] = max(0.0, min(1.0, float(value)))
        
        # 归一化使总和为1
        total = sum(validated.values())
        if total > 0:
            validated = {k: v/total for k, v in validated.items()}
        else:
            # 如果全是0，设置为平均分布
            validated = {k: 0.2 for k in emotion_keys}
        
        return validated
