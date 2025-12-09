"""
表情生成路由
处理表情生成请求
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
import logging
import uuid
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.core.expression_generator import ExpressionGenerator
from backend.core.live2d_expression_mapper import Live2DExpressionMapper

logger = logging.getLogger(__name__)

router = APIRouter()

# 目录配置
UPLOAD_DIR = Path("data/uploads")
EXPRESSION_DIR = Path("data/expressions")
EXPRESSION_DIR.mkdir(parents=True, exist_ok=True)

# 缓存最后生成的表情序列
_last_live2d_sequence = None

class GenerateRequest(BaseModel):
    file_id: str
    model_name: str = "default"
    time_resolution: float = 0.1
    enable_smoothing: bool = True

@router.post("/generate")
async def generate_expression(request: GenerateRequest):
    """
    生成表情动画

    Args:
        request: 生成请求参数

    Returns:
        dict: 生成结果
    """
    try:
        # 查找音频文件
        audio_path = None
        for f in UPLOAD_DIR.glob(f"{request.file_id}.*"):
            audio_path = f
            break

        if not audio_path or not audio_path.exists():
            raise HTTPException(status_code=404, detail="音频文件不存在")

        # 生成表情
        generator = ExpressionGenerator()

        expression_data = generator.generate_from_audio(
            audio_path=str(audio_path),
            time_resolution=request.time_resolution,
            enable_smoothing=request.enable_smoothing
        )

        # 保存表情文件
        expression_id = str(uuid.uuid4())
        output_path = EXPRESSION_DIR / f"{expression_id}.json"

        generator.export_to_file(
            expression_data=expression_data,
            output_path=str(output_path)
        )

        logger.info(f"表情生成完成: {expression_id}")

        # 使用Live2D表情映射器生成表情序列
        try:
            mapper = Live2DExpressionMapper()
            live2d_sequence = mapper.map_emotions_to_expressions(
                emotion_scores=expression_data["emotion_scores"],
                duration=expression_data["duration"]
            )
            logger.info(f"Live2D表情序列生成完成: {live2d_sequence}")
            
            # 缓存表情序列
            global _last_live2d_sequence
            _last_live2d_sequence = live2d_sequence
        except Exception as e:
            logger.error(f"Live2D表情映射失败: {e}")
            live2d_sequence = ["0"]
            _last_live2d_sequence = live2d_sequence

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "表情生成完成",
                "data": {
                    "expression_id": expression_id,
                    "file_id": request.file_id,
                    "model_name": request.model_name,
                    "expression_path": str(output_path),
                    "duration": expression_data["duration"],
                    "tempo": expression_data["tempo"],
                    "keyframe_count": len(expression_data["expressions"]),
                    "emotion_scores": expression_data["emotion_scores"],
                    "live2d_sequence": live2d_sequence
                }
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"表情生成失败: {error_msg}", exc_info=True)
        
        # 返回详细的错误信息给前端
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "表情生成失败",
                "error": error_msg,
                "error_type": type(e).__name__,
                "details": {
                    "file_id": request.file_id,
                    "error_location": "expression_generator"
                }
            }
        )

@router.get("/expression/{expression_id}")
async def get_expression(expression_id: str):
    """
    获取表情数据

    Args:
        expression_id: 表情ID

    Returns:
        dict: 表情数据
    """
    try:
        expression_path = EXPRESSION_DIR / f"{expression_id}.json"

        if not expression_path.exists():
            raise HTTPException(status_code=404, detail="表情文件不存在")

        import json
        with open(expression_path, 'r', encoding='utf-8') as f:
            expression_data = json.load(f)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "表情数据获取成功",
                "data": expression_data
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取表情数据失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取表情数据失败: {str(e)}")


@router.get("/live2d/expressions")
async def get_live2d_expressions():
    """
    获取Live2D表情配置信息

    Returns:
        dict: Live2D表情配置
    """
    try:
        mapper = Live2DExpressionMapper()
        config = mapper.get_expression_info()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Live2D表情配置获取成功",
                "data": config
            }
        )
    except Exception as e:
        logger.error(f"获取Live2D表情配置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取Live2D表情配置失败: {str(e)}")


@router.get("/getNeutralExpression")
async def get_neutral_expression():
    """
    获取上次生成的Live2D表情序列

    Returns:
        dict: 包含live2d_sequence的响应
    """
    global _last_live2d_sequence
    
    if _last_live2d_sequence is None:
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "暂无表情序列",
                "data": {
                    "live2d_sequence": []
                }
            }
        )
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "获取表情序列成功",
            "data": {
                "live2d_sequence": _last_live2d_sequence
            }
        }
    )
