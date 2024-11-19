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
