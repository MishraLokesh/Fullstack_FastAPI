from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FileMetadata

router = APIRouter()

STORAGE_PATH = "storage"
CHUNK_SIZE = 1024 * 1024  # 1MB per chunk

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
async def upload_file_resumable(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Check if the file exists in the database
        file_metadata = db.query(FileMetadata).filter(FileMetadata.filename == file.filename).first()

        if file_metadata:
            # File already exists, resume from the last uploaded chunk
            uploaded_chunks = file_metadata.uploaded_chunks
            file_size = file_metadata.file_size
        else:
            # New upload, initialize metadata
            uploaded_chunks = 0
            file_size = file.spool_max_size or len(await file.read())  # Determine total size for new files
            file_metadata = FileMetadata(filename=file.filename, file_size=file_size)
            db.add(file_metadata)
            db.commit()

        # Create storage directory if it doesn't exist
        os.makedirs(STORAGE_PATH, exist_ok=True)

        file_path = os.path.join(STORAGE_PATH, file.filename)

         # Open the file in append mode if resuming
        with open(file_path, "ab") as f:
            chunk = await file.read(CHUNK_SIZE)
            while chunk:
                f.write(chunk)
                uploaded_chunks += 1  # Increment chunk count after each write

                # Update metadata in the database
                file_metadata.uploaded_chunks = uploaded_chunks
                db.commit()

                # Check if we've uploaded all chunks
                if uploaded_chunks * CHUNK_SIZE >= file_size:
                    break

                chunk = await file.read(CHUNK_SIZE)

        # After upload completion, update the status
        file_metadata.upload_status = "completed"
        db.commit()


        return {"message": "Chunk uploaded successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
