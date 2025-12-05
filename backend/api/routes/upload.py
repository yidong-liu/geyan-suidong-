"""
文件上传路由
处理音频文件上传
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import uuid
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# 配置上传目录
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 允许的文件类型
ALLOWED_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.flac', '.ogg'}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    上传音频文件

    Args:
        file: 上传的音频文件

    Returns:
        dict: 包含文件ID和基本信息
    """
    try:
        # 验证文件类型
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式。支持的格式: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # 生成唯一文件ID
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}{file_ext}"

        # 保存文件
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"文件上传成功: {file.filename} -> {file_id}")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "文件上传成功",
                "data": {
                    "file_id": file_id,
                    "filename": file.filename,
                    "file_path": str(file_path),
                    "file_size": file_path.stat().st_size
                }
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.delete("/upload/{file_id}")
async def delete_file(file_id: str):
    """
    删除上传的文件

    Args:
        file_id: 文件ID

    Returns:
        dict: 删除结果
    """
    try:
        # 查找并删除文件
        deleted = False
        for file_path in UPLOAD_DIR.glob(f"{file_id}.*"):
            file_path.unlink()
            deleted = True
            logger.info(f"文件已删除: {file_id}")

        if not deleted:
            raise HTTPException(status_code=404, detail="文件不存在")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "文件删除成功",
                "data": {"file_id": file_id}
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"文件删除失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件删除失败: {str(e)}")
