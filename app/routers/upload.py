from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FileMetadata

router = APIRouter()

STORAGE_PATH = "storage"

@router.post("/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Create storage directory if not exists
        os.makedirs(STORAGE_PATH, exist_ok=True)

        # Save file to disk for now
        file_path = os.path.join(STORAGE_PATH, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Save file metadata in database
        file_metadata = FileMetadata(filename=file.filename, file_path=file_path)
        db.add(file_metadata)
        db.commit()

        return {"message": "File uploaded successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chunk")
async def upload_file_chunk(file: UploadFile = File(...), chunk_size: int = 1024 * 1024):
    try:
        os.makedirs(STORAGE_PATH, exist_ok=True)
        file_path = os.path.join(STORAGE_PATH, file.filename)

        with open(file_path, "ab") as f:  # Append mode for chunks
            while chunk := await file.read(chunk_size):
                f.write(chunk)

        return {"message": "Chunk uploaded successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chunk-resume")
async def upload_file_resumable(file: UploadFile = File(...), chunk_size: int = 1024 * 1024):
    try:
        os.makedirs(STORAGE_PATH, exist_ok=True)
        file_path = os.path.join(STORAGE_PATH, file.filename)

        mode = "ab" if os.path.exists(file_path) else "wb"
        with open(file_path, mode) as f:
            while chunk := await file.read(chunk_size):
                f.write(chunk)

        return {"message": "Chunk uploaded successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
