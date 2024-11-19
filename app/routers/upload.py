import os
import logging
from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from minio import Minio
from app.database import get_db
from app.models import FileMetadata
from io import BytesIO
from minio.error import S3Error

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

# MinIO Bucket
BUCKET_NAME = "lokbucket" 

CHUNK_SIZE = 1024 * 1024  # 1MB per chunk
router = APIRouter()

logging.basicConfig(level=logging.INFO)  # Enable logging for debugging

# Ensure the bucket exists
if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
    minio_client.make_bucket(MINIO_BUCKET_NAME)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload the entire file to MinIO in one go.
    """
    try:
        # Read the entire file content
        file_content = await file.read()

        # Upload the file to MinIO
        minio_client.put_object(
            MINIO_BUCKET_NAME,
            file.filename,  # The file will be saved with its original name
            BytesIO(file_content),
            length=len(file_content)
        )

        logging.info(f"File {file.filename} uploaded successfully to MinIO.")
        return {"message": f"File {file.filename} uploaded successfully to MinIO."}

    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
