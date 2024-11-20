from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from minio import Minio
from io import BytesIO

# Initialize FastAPI
router = APIRouter()

# MinIO Configuration
MINIO_ENDPOINT = "127.0.0.1:9000"
MINIO_ACCESS_KEY = "E73DmxZVLQv5sldAZ7ia"
MINIO_SECRET_KEY = "lX43QnpE0D6uhka2EwrXDosxoCQylC9uh8UwJAVU"
MINIO_BUCKET_NAME = "lokbucket"

# Initialize MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Set to True if you are using HTTPS
)

@router.get("/preview/{filename}")
async def preview_file(filename: str):
    try:
        # Check if the file exists in the MinIO bucket
        if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
            raise HTTPException(status_code=404, detail="Bucket does not exist")

        # Fetch the file from MinIO
        try:
            file_data = minio_client.get_object(MINIO_BUCKET_NAME, filename)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")

        # Determine content type based on file extension
        file_extension = filename.split('.')[-1].lower()
        if file_extension in ["jpg", "jpeg", "png", "gif"]:
            media_type = "image/" + file_extension
        elif file_extension in ["pdf"]:
            media_type = "application/pdf"
        elif file_extension in ["txt", "csv"]:
            media_type = "text/plain"
        else:
            media_type = "application/octet-stream"  # Default for unknown file types

        # Return the file as a StreamingResponse
        return StreamingResponse(file_data, media_type=media_type)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
