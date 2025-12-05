"""
音频分析器模块
使用librosa进行音频特征提取
"""
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
