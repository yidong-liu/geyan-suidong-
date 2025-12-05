"""
API响应数据模型
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

class APIResponse(BaseModel):
    """标准API响应"""
    success: bool = Field(..., description="请求是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[Any] = Field(default=None, description="响应数据")
    error: Optional[str] = Field(default=None, description="错误信息")

class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = Field(default=False, description="请求失败")
    message: str = Field(..., description="错误消息")
    error: str = Field(..., description="错误详情")
    error_code: Optional[str] = Field(default=None, description="错误代码")

class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    status: str = Field(..., description="服务状态")
    service: str = Field(..., description="服务名称")
    version: Optional[str] = Field(default=None, description="服务版本")
