"""
配置管理模块
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置"""
    
    # 应用基础配置
    APP_NAME = "歌颜随动"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("API_DEBUG", "false").lower() == "true"
    
    # API配置
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Streamlit配置
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    STREAMLIT_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")
    
    # 文件路径配置
    BASE_DIR = Path(__file__).parent.parent.parent
    UPLOAD_DIR = BASE_DIR / os.getenv("UPLOAD_DIR", "data/uploads")
    MODELS_DIR = BASE_DIR / os.getenv("MODELS_DIR", "models")
    EXPRESSIONS_DIR = BASE_DIR / os.getenv("EXPRESSIONS_DIR", "data/expressions")
    TEMP_DIR = BASE_DIR / os.getenv("TEMP_DIR", "data/temp")
    LOGS_DIR = BASE_DIR / "logs"
    
    # Live2D配置
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "hiyori_free_t08.model3.json")
    EXPRESSION_MAPPING = BASE_DIR / os.getenv("EXPRESSION_MAPPING", "config/expression_mapping.json")
    
    # 音频处理配置
    AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "44100"))
    AUDIO_HOP_LENGTH = int(os.getenv("AUDIO_HOP_LENGTH", "512"))
    MAX_AUDIO_LENGTH = int(os.getenv("MAX_AUDIO_LENGTH", "300"))  # 秒
    
    # AI配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    
    # 性能配置
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = BASE_DIR / os.getenv("LOG_FILE", "logs/app.log")
    
    # 安全配置
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    
    @classmethod
    def create_directories(cls):
        """创建必要的目录"""
        for dir_path in [cls.UPLOAD_DIR, cls.MODELS_DIR, cls.EXPRESSIONS_DIR, 
                         cls.TEMP_DIR, cls.LOGS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

# 创建必要的目录
Config.create_directories()
