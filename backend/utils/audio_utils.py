"""
音频处理工具
"""
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

def convert_to_wav(input_path: str, output_path: str, sample_rate: int = 44100) -> str:
    """
    转换音频文件为WAV格式
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        sample_rate: 采样率
        
    Returns:
        str: 输出文件路径
    """
    try:
        # 加载音频
        y, sr = librosa.load(input_path, sr=sample_rate)
        
        # 保存为WAV
        sf.write(output_path, y, sr)
        
        logger.info(f"音频转换完成: {input_path} -> {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"音频转换失败: {str(e)}")
        raise

def get_audio_duration(audio_path: str) -> float:
    """
    获取音频时长
    
    Args:
        audio_path: 音频文件路径
        
    Returns:
        float: 时长（秒）
    """
    try:
        duration = librosa.get_duration(path=audio_path)
        return duration
    except Exception as e:
        logger.error(f"获取音频时长失败: {str(e)}")
        raise

def trim_audio(audio_path: str, output_path: str, start_time: float = 0, 
               end_time: Optional[float] = None) -> str:
    """
    裁剪音频
    
    Args:
        audio_path: 输入音频路径
        output_path: 输出音频路径
        start_time: 开始时间（秒）
        end_time: 结束时间（秒），None表示到结尾
        
    Returns:
        str: 输出文件路径
    """
    try:
        y, sr = librosa.load(audio_path)
        
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr) if end_time else len(y)
        
        y_trimmed = y[start_sample:end_sample]
        
        sf.write(output_path, y_trimmed, sr)
        
        logger.info(f"音频裁剪完成: {start_time}s - {end_time}s")
        return output_path
        
    except Exception as e:
        logger.error(f"音频裁剪失败: {str(e)}")
        raise

def normalize_audio(y: np.ndarray) -> np.ndarray:
    """
    归一化音频信号
    
    Args:
        y: 音频信号数组
        
    Returns:
        np.ndarray: 归一化后的音频信号
    """
    max_val = np.max(np.abs(y))
    if max_val > 0:
        return y / max_val
    return y

def mix_audio(audio1_path: str, audio2_path: str, output_path: str, 
              mix_ratio: float = 0.5) -> str:
    """
    混合两个音频文件
    
    Args:
        audio1_path: 音频文件1路径
        audio2_path: 音频文件2路径
        output_path: 输出文件路径
        mix_ratio: 混合比例（0-1，0表示全部是音频1，1表示全部是音频2）
        
    Returns:
        str: 输出文件路径
    """
    try:
        # 加载音频
        y1, sr1 = librosa.load(audio1_path)
        y2, sr2 = librosa.load(audio2_path, sr=sr1)  # 统一采样率
        
        # 对齐长度
        min_len = min(len(y1), len(y2))
        y1 = y1[:min_len]
        y2 = y2[:min_len]
        
        # 混合
        y_mixed = (1 - mix_ratio) * y1 + mix_ratio * y2
        y_mixed = normalize_audio(y_mixed)
        
        # 保存
        sf.write(output_path, y_mixed, sr1)
        
        logger.info(f"音频混合完成: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"音频混合失败: {str(e)}")
        raise
