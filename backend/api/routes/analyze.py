"""
音频分析路由
处理音频分析请求
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
import logging
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.core.audio_analyzer import AudioAnalyzerAgent
from backend.core.ai_config import AIConfig

logger = logging.getLogger(__name__)

router = APIRouter()

# 上传目录
UPLOAD_DIR = Path("data/uploads")

class AnalyzeRequest(BaseModel):
    file_id: str
    sample_rate: int = 44100
    hop_length: int = 512

@router.post("/analyze")
async def analyze_audio(request: AnalyzeRequest):
    """
    分析音频文件

    Args:
        request: 分析请求参数

    Returns:
        dict: 音频分析结果
    """
    try:
        # 查找文件
        file_path = None
        for f in UPLOAD_DIR.glob(f"{request.file_id}.*"):
            file_path = f
            break

        if not file_path or not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")

        # 执行分析
        ai_config = AIConfig.get_analyzer_config()
        analyzer = AudioAnalyzerAgent(
            sample_rate=request.sample_rate,
            hop_length=request.hop_length,
            **ai_config
        )

        features = analyzer.analyze(str(file_path))

        # 构建响应
        import numpy as np
        energy_array = np.array(features.energy)
        spectral_array = np.array(features.spectral_centroid)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "音频分析完成",
                "data": {
                    "file_id": request.file_id,
                    "duration": features.duration,
                    "tempo": features.tempo,
                    "beat_count": len(features.beats),
                    "beats": features.beats[:100],  # 限制返回数量
                    "emotion_scores": features.emotion_scores,
                    "energy_stats": {
                        "mean": float(energy_array.mean()),
                        "max": float(energy_array.max()),
                        "min": float(energy_array.min())
                    },
                    "spectral_stats": {
                        "mean": float(spectral_array.mean()),
                        "max": float(spectral_array.max()),
                        "min": float(spectral_array.min())
                    }
                }
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"音频分析失败: {error_msg}", exc_info=True)
        
        # 返回详细的错误信息给前端
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "音频分析失败",
                "error": error_msg,
                "error_type": type(e).__name__,
                "details": {
                    "file_id": request.file_id,
                    "error_location": "audio_analyzer"
                }
            }
        )
