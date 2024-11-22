import os
from fastapi import APIRouter, HTTPException
from minio import Minio
from dotenv import load_dotenv

# Initialize FastAPI
router = APIRouter()

load_dotenv()

# MinIO Configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = ""
MINIO_SECRET_KEY = ""
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")


# Initialize MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Set to True if using HTTPS
)

@router.get("/list-files")
async def list_files():
    try:
        # Ensure the bucket exists
        if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
            raise HTTPException(status_code=404, detail="Bucket does not exist")

        # List objects (files) in the MinIO bucket
        objects = minio_client.list_objects(MINIO_BUCKET_NAME)

        # Collect file names
        file_names = [obj.object_name for obj in objects]

        if not file_names:
            return {"message": "No files found in the bucket."}

        return {"files": file_names}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
