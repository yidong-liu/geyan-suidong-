"""
音频相关数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class AudioUploadRequest(BaseModel):
    """音频上传请求"""
    filename: str = Field(..., description="文件名")
    file_size: int = Field(..., description="文件大小（字节）")

class AudioUploadResponse(BaseModel):
    """音频上传响应"""
    file_id: str = Field(..., description="文件ID")
    filename: str = Field(..., description="文件名")
    file_path: str = Field(..., description="文件路径")
    file_size: int = Field(..., description="文件大小")

class AudioAnalysisRequest(BaseModel):
    """音频分析请求"""
    file_id: str = Field(..., description="文件ID")
    sample_rate: int = Field(default=44100, description="采样率")
    hop_length: int = Field(default=512, description="跳跃长度")

class AudioFeatures(BaseModel):
    """音频特征"""
    duration: float = Field(..., description="时长（秒）")
    tempo: float = Field(..., description="节拍（BPM）")
    beats: List[float] = Field(..., description="节拍时间点列表")
    energy_mean: float = Field(..., description="平均能量")
    spectral_centroid_mean: float = Field(..., description="平均频谱质心")
    emotion_scores: Dict[str, float] = Field(..., description="情感分数")

class AudioAnalysisResponse(BaseModel):
    """音频分析响应"""
    file_id: str = Field(..., description="文件ID")
    features: AudioFeatures = Field(..., description="音频特征")
