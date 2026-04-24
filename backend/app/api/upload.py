import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.config import settings
from app.middleware.auth_middleware import get_current_user

router = APIRouter()


def save_upload_file(upload_file: UploadFile, subdir: str = "images") -> str:
    """保存上传文件到本地"""
    upload_dir = os.path.join(settings.UPLOAD_DIR, subdir)
    os.makedirs(upload_dir, exist_ok=True)

    ext = os.path.splitext(upload_file.filename or "")[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(upload_dir, filename)

    with open(filepath, "wb") as f:
        content = upload_file.file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="文件大小超过限制")
        f.write(content)

    return f"/uploads/{subdir}/{filename}"


@router.post("/image")
async def upload_image(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """通用图片上传"""
    urls = []
    for file in files:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="只支持图片文件")
        url = save_upload_file(file, "images")
        urls.append(url)
    return {"urls": urls}


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """用户头像上传"""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只支持图片文件")
    url = save_upload_file(file, "avatars")
    current_user.avatar_url = url
    db.commit()
    return {"url": url}
