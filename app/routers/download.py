from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FileMetadata
from minio import Minio
from io import BytesIO

router = APIRouter()

# MinIO Configuration
MINIO_ENDPOINT = "127.0.0.1:9000"
MINIO_ACCESS_KEY = "E73DmxZVLQv5sldAZ7ia"
MINIO_SECRET_KEY = "lX43QnpE0D6uhka2EwrXDosxoCQylC9uh8UwJAVU"
MINIO_BUCKET_NAME = "lokbucket"

# Initialize MinIO Client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

@router.get("/download/{filename}")
async def download_file(filename: str, db: Session = Depends(get_db)):
    """
    Endpoint to download a file by its filename from MinIO.
    """
    try:
        # Check if the file metadata exists in the database
        file_metadata = db.query(FileMetadata).filter(FileMetadata.filename == filename).first()
        if not file_metadata:
            raise HTTPException(status_code=404, detail="File not found")

        # Check if the file exists in MinIO
        if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
            raise HTTPException(status_code=404, detail="Bucket not found")
        
        # Get the file object from MinIO
        try:
            file_data = minio_client.get_object(MINIO_BUCKET_NAME, filename)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"File not found in MinIO: {e}")

        # Stream the file back to the client
        return StreamingResponse(
            BytesIO(file_data.read()),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {e}")
