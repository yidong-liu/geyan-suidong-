"""
API客户端工具
与后端API通信
"""
import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """API客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            response = self.session.get(f"{self.base_url.replace('/api/v1', '')}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"健康检查失败: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def upload_file(self, file) -> Dict[str, Any]:
        """上传文件"""
        try:
            files = {"file": (file.name, file.getvalue(), file.type)}
            response = self.session.post(f"{self.base_url}/upload", files=files)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"文件上传失败: {str(e)}")
            raise
    
    def analyze_audio(self, file_id: str) -> Dict[str, Any]:
        """分析音频"""
        try:
            data = {"file_id": file_id}
            response = self.session.post(f"{self.base_url}/analyze", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"音频分析失败: {str(e)}")
            raise
    
    def generate_expression(
        self,
        file_id: str,
        model_name: str = "default",
        time_resolution: float = 0.1,
        enable_smoothing: bool = True
    ) -> Dict[str, Any]:
        """生成表情"""
        try:
            data = {
                "file_id": file_id,
                "model_name": model_name,
                "time_resolution": time_resolution,
                "enable_smoothing": enable_smoothing
            }
            response = self.session.post(f"{self.base_url}/generate", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"表情生成失败: {str(e)}")
            raise
    
    def get_expression(self, expression_id: str) -> Dict[str, Any]:
        """获取表情数据"""
        try:
            response = self.session.get(f"{self.base_url}/expression/{expression_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"获取表情失败: {str(e)}")
            raise
