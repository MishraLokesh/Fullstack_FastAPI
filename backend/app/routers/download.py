import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FileMetadata
from minio import Minio
from io import BytesIO
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()

# MinIO Configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = "E73DmxZVLQv5sldAZ7ia"
MINIO_SECRET_KEY = "lX43QnpE0D6uhka2EwrXDosxoCQylC9uh8UwJAVU"
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")


# Initialize MinIO Client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

@router.get("/download/{filename}")
async def download_file(filename: str):
    try:
        # Check if the file exists in the MinIO bucket
        if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
            raise HTTPException(status_code=404, detail="Bucket does not exist")

        # Fetch the file from MinIO
        try:
            file_data = minio_client.get_object(MINIO_BUCKET_NAME, filename)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")

        # Send the file to the client
        return StreamingResponse(file_data, media_type="application/octet-stream", headers={
            "Content-Disposition": f"attachment; filename={filename}"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))