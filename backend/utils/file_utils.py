"""
文件处理工具
"""
import os
import shutil
from pathlib import Path
from typing import Optional, List
import mimetypes
import logging

logger = logging.getLogger(__name__)

def get_file_size(file_path: str) -> int:
    """
    获取文件大小（字节）
    
    Args:
        file_path: 文件路径
        
    Returns:
        int: 文件大小
    """
    return Path(file_path).stat().st_size

def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 字节数
        
    Returns:
        str: 格式化的文件大小
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def is_audio_file(filename: str) -> bool:
    """
    检查是否为音频文件
    
    Args:
        filename: 文件名
        
    Returns:
        bool: 是否为音频文件
    """
    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac'}
    ext = Path(filename).suffix.lower()
    return ext in audio_extensions

def get_mime_type(filename: str) -> Optional[str]:
    """
    获取文件的MIME类型
    
    Args:
        filename: 文件名
        
    Returns:
        str: MIME类型
    """
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type

def ensure_directory(directory: str):
    """
    确保目录存在，不存在则创建
    
    Args:
        directory: 目录路径
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

def safe_delete_file(file_path: str) -> bool:
    """
    安全删除文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 是否删除成功
    """
    try:
        if Path(file_path).exists():
            Path(file_path).unlink()
            logger.info(f"文件已删除: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"删除文件失败: {file_path}, 错误: {str(e)}")
        return False

def clean_temp_files(temp_dir: str, age_hours: int = 24):
    """
    清理临时文件
    
    Args:
        temp_dir: 临时文件目录
        age_hours: 文件保留时长（小时）
    """
    import time
    
    temp_path = Path(temp_dir)
    if not temp_path.exists():
        return
    
    current_time = time.time()
    age_seconds = age_hours * 3600
    
    for file_path in temp_path.rglob('*'):
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > age_seconds:
                safe_delete_file(str(file_path))
                logger.info(f"清理临时文件: {file_path}")

def list_files(directory: str, pattern: str = "*") -> List[str]:
    """
    列出目录下的文件
    
    Args:
        directory: 目录路径
        pattern: 文件模式
        
    Returns:
        List[str]: 文件路径列表
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    
    return [str(f) for f in dir_path.glob(pattern) if f.is_file()]
