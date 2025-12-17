"""
File Storage Endpoints
Demonstrates Laravel-like file storage usage.
"""
from typing import List, Any
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.core.storage import storage
from app.models.user import User
import io

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Upload a file to storage.
    Similar to Laravel's file upload.
    """
    try:
        # Read file content
        content = await file.read()
        
        # Generate unique filename
        import uuid
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        unique_filename = f"{uuid.uuid4()}.{file_extension}" if file_extension else str(uuid.uuid4())
        file_path = f"uploads/{current_user.id}/{unique_filename}"
        
        # Store file using storage facade
        success = storage().put(file_path, content)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to store file")
        
        return {
            "message": "File uploaded successfully",
            "path": file_path,
            "filename": file.filename,
            "url": storage().url(file_path),
            "size": storage().size(file_path),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/download/{file_path:path}")
async def download_file(
    file_path: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Download a file from storage.
    """
    try:
        if not storage().exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get file content
        content = storage().get(file_path)
        if content is None:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get filename from path
        filename = file_path.split('/')[-1]
        
        # Return file as streaming response
        return StreamingResponse(
            io.BytesIO(content),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@router.get("/info/{file_path:path}")
async def get_file_info(
    file_path: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get file information.
    """
    try:
        if not storage().exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return {
            "path": file_path,
            "exists": True,
            "size": storage().size(file_path),
            "mime_type": storage().mime_type(file_path),
            "last_modified": storage().last_modified(file_path),
            "url": storage().url(file_path),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file info: {str(e)}")

@router.delete("/delete/{file_path:path}")
async def delete_file(
    file_path: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete a file from storage.
    """
    try:
        if not storage().exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        success = storage().delete(file_path)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete file")
        
        return {"message": "File deleted successfully", "path": file_path}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

@router.get("/list")
async def list_files(
    directory: str = "",
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    List files in a directory.
    """
    try:
        files = storage().files(directory)
        directories = storage().directories(directory)
        
        return {
            "directory": directory,
            "files": files,
            "directories": directories,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

@router.post("/copy")
async def copy_file(
    from_path: str,
    to_path: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Copy a file from one location to another.
    """
    try:
        if not storage().exists(from_path):
            raise HTTPException(status_code=404, detail="Source file not found")
        
        success = storage().copy(from_path, to_path)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to copy file")
        
        return {
            "message": "File copied successfully",
            "from": from_path,
            "to": to_path,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Copy failed: {str(e)}")

@router.post("/move")
async def move_file(
    from_path: str,
    to_path: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Move a file from one location to another.
    """
    try:
        if not storage().exists(from_path):
            raise HTTPException(status_code=404, detail="Source file not found")
        
        success = storage().move(from_path, to_path)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to move file")
        
        return {
            "message": "File moved successfully",
            "from": from_path,
            "to": to_path,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Move failed: {str(e)}")

