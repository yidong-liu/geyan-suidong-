"""
表情相关数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ExpressionParameters(BaseModel):
    """Live2D表情参数"""
    eye_open: float = Field(default=0.8, ge=0.0, le=1.0, description="眼睛开合")
    eye_open_r: float = Field(default=0.8, ge=0.0, le=1.0, description="右眼开合")
    eyebrow_height: float = Field(default=0.5, ge=0.0, le=1.0, description="眉毛高度")
    eyebrow_height_r: float = Field(default=0.5, ge=0.0, le=1.0, description="右眉高度")
    mouth_open: float = Field(default=0.2, ge=0.0, le=1.0, description="嘴部开合")
    mouth_form: float = Field(default=0.3, ge=0.0, le=1.0, description="嘴型")
    cheek: float = Field(default=0.0, ge=0.0, le=1.0, description="脸颊红晕")
    body_angle_x: float = Field(default=0.0, ge=-1.0, le=1.0, description="身体X轴角度")
    body_angle_y: float = Field(default=0.0, ge=-1.0, le=1.0, description="身体Y轴角度")
    breath: float = Field(default=0.5, ge=0.0, le=1.0, description="呼吸")

class ExpressionKeyframe(BaseModel):
    """表情关键帧"""
    timestamp: float = Field(..., description="时间戳（秒）")
    parameters: ExpressionParameters = Field(..., description="表情参数")

class GenerateExpressionRequest(BaseModel):
    """生成表情请求"""
    file_id: str = Field(..., description="音频文件ID")
    model_name: str = Field(default="default", description="Live2D模型名称")
    time_resolution: float = Field(default=0.1, ge=0.01, le=1.0, description="时间分辨率")
    enable_smoothing: bool = Field(default=True, description="是否启用平滑")

class GenerateExpressionResponse(BaseModel):
    """生成表情响应"""
    expression_id: str = Field(..., description="表情ID")
    file_id: str = Field(..., description="音频文件ID")
    model_name: str = Field(..., description="模型名称")
    duration: float = Field(..., description="时长")
    keyframe_count: int = Field(..., description="关键帧数量")
    emotion_scores: Dict[str, float] = Field(..., description="情感分数")
