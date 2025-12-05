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

from backend.core.audio_analyzer import AudioAnalyzer

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
        analyzer = AudioAnalyzer(
            sample_rate=request.sample_rate,
            hop_length=request.hop_length
        )

        features = analyzer.analyze(str(file_path))

        # 构建响应
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
                        "mean": float(features.energy.mean()),
                        "max": float(features.energy.max()),
                        "min": float(features.energy.min())
                    },
                    "spectral_stats": {
                        "mean": float(features.spectral_centroid.mean()),
                        "max": float(features.spectral_centroid.max()),
                        "min": float(features.spectral_centroid.min())
                    }
                }
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"音频分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"音频分析失败: {str(e)}")
