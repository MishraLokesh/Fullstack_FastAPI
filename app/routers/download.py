from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
import os
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FileMetadata

router = APIRouter()

STORAGE_PATH = "storage"

@router.get("/download/{filename}")
async def download_file(filename: str, db: Session = Depends(get_db)):
    """
    Endpoint to download a file by its filename.
    """
    try:
        # Check if the file metadata exists in the database
        file_metadata = db.query(FileMetadata).filter(FileMetadata.filename == filename).first()
        if not file_metadata:
            raise HTTPException(status_code=404, detail="File not found")

        # Construct the file path
        file_path = os.path.join(STORAGE_PATH, filename)

        # Check if the file exists on disk
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found on the server")

        # Return the file as a response
        return FileResponse(file_path, media_type="application/octet-stream", filename=filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {e}")
