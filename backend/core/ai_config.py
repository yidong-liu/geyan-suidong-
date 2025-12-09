"""
AI模型配置模块
统一管理AI API配置，支持Google Gemini和OpenAI兼容API
"""
import os
from typing import Dict, Any, Optional


class AIConfig:
    """AI配置管理类"""
    
    # 默认配置
    DEFAULT_USE_GEMINI = True
    DEFAULT_MODEL_GEMINI = "gemini-1.5-flash"
    DEFAULT_MODEL_OPENAI = "gpt-4o-mini"
    DEFAULT_TEMP_EMOTION = 0.3
    DEFAULT_TEMP_EXPRESSION = 0.7
    DEFAULT_MAX_TOKENS = 1000
    
    @staticmethod
    def get_use_gemini() -> bool:
        """获取是否使用Gemini"""
        return os.getenv("AI_USE_GEMINI", "true").lower() == "true"
    
    @staticmethod
    def get_api_key() -> Optional[str]:
        """根据配置获取对应的API Key"""
        if AIConfig.get_use_gemini():
            return os.getenv("GOOGLE_API_KEY")
        else:
            return os.getenv("OPENAI_API_KEY")
    
    @staticmethod
    def get_model_name(use_gemini: Optional[bool] = None) -> str:
        """获取模型名称"""
        if use_gemini is None:
            use_gemini = AIConfig.get_use_gemini()
        
        if use_gemini:
            return os.getenv("GOOGLE_MODEL", AIConfig.DEFAULT_MODEL_GEMINI)
        else:
            return os.getenv("OPENAI_MODEL", AIConfig.DEFAULT_MODEL_OPENAI)
    
    @staticmethod
    def get_base_url() -> Optional[str]:
        """获取API基础URL（仅OpenAI）"""
        if not AIConfig.get_use_gemini():
            return os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        return None
    
    @staticmethod
    def get_analyzer_config() -> Dict[str, Any]:
        """
        获取AudioAnalyzerAgent配置
        
        Returns:
            Dict: 包含所有必要配置的字典
        """
        use_gemini = AIConfig.get_use_gemini()
        
        return {
            "use_gemini": use_gemini,
            "api_key": AIConfig.get_api_key(),
            "model_name": AIConfig.get_model_name(use_gemini),
            "base_url": AIConfig.get_base_url(),
            "temperature": float(os.getenv("AI_TEMP_EMOTION", str(AIConfig.DEFAULT_TEMP_EMOTION))),
            "max_tokens": int(os.getenv("AI_MAX_TOKENS", str(AIConfig.DEFAULT_MAX_TOKENS))),
        }
    
    @staticmethod
    def get_expression_config() -> Dict[str, Any]:
        """
        获取ExpressionAgentV2配置
        
        Returns:
            Dict: 包含所有必要配置的字典
        """
        use_gemini = AIConfig.get_use_gemini()
        
        return {
            "use_gemini": use_gemini,
            "api_key": AIConfig.get_api_key(),
            "model_name": AIConfig.get_model_name(use_gemini),
            "api_base": AIConfig.get_base_url(),
            "temperature": float(os.getenv("AI_TEMP_EXPRESSION", str(AIConfig.DEFAULT_TEMP_EXPRESSION))),
            "max_tokens": int(os.getenv("AI_MAX_TOKENS", str(AIConfig.DEFAULT_MAX_TOKENS))),
        }
    
    @staticmethod
    def validate_config() -> tuple[bool, str]:
        """
        验证API配置是否完整
        
        Returns:
            tuple: (是否有效, 错误信息)
        """
        use_gemini = AIConfig.get_use_gemini()
        api_key = AIConfig.get_api_key()
        
        if not api_key:
            if use_gemini:
                return False, "未设置 GOOGLE_API_KEY 环境变量"
            else:
                return False, "未设置 OPENAI_API_KEY 环境变量"
        
        return True, ""

