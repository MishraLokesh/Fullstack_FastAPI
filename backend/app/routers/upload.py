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
from dotenv import load_dotenv

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

# MinIO Bucket
BUCKET_NAME = "lokbucket" 

CHUNK_SIZE = 1024 * 1024  # 1MB per chunk
router = APIRouter()

logging.basicConfig(level=logging.INFO)  # Enable logging for debugging

# Ensure the bucket exists
if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
    minio_client.make_bucket(MINIO_BUCKET_NAME)

@router.post("/upload")
async def upload_chunk(
    filename: str = Form(...),
    chunk_index: int = Form(...),
    total_chunks: int = Form(...),
    file: UploadFile = File(...),
):
    """
    Upload a file chunk and handle resumable uploads.
    """
    try:
        # Read the chunk data from the file
        chunk_data = await file.read()

        # Generate the chunk name
        chunk_name = f"{filename}.chunk{chunk_index}"

        # Upload the chunk to MinIO
        minio_client.put_object(
            MINIO_BUCKET_NAME,
            chunk_name,
            BytesIO(chunk_data),
            length=len(chunk_data)
        )

        logging.info(f"Uploaded chunk {chunk_index} for {filename}.")

        # Check if all chunks have been uploaded
        if chunk_index == total_chunks - 1:
            # Combine chunks if the last chunk is uploaded
            combine_chunks_in_minio(filename, total_chunks)
            return {"message": f"File {filename} uploaded and combined successfully."}

        return {"message": f"Chunk {chunk_index} uploaded successfully for {filename}."}

    except Exception as e:
        logging.error(f"Error uploading chunk for {filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def combine_chunks_in_minio(filename: str, total_chunks: int):
    """
    Combine all chunks of a file stored in MinIO into a single file.
    """
    try:
        # Initialize the output object for the combined file
        combined_file = BytesIO()

        # Fetch and combine each chunk
        for chunk_index in range(total_chunks):
            chunk_name = f"{filename}.chunk{chunk_index}"
            logging.info(f"Fetching chunk: {chunk_name}")

            # Retrieve the chunk from MinIO
            try:
                response = minio_client.get_object(MINIO_BUCKET_NAME, chunk_name)
                chunk_data = response.read()
                response.close()
                response.release_conn()
                logging.info(f"Chunk {chunk_name} size: {len(chunk_data)}")

                # Append the chunk to the combined file
                combined_file.write(chunk_data)
            except Exception as chunk_error:
                logging.error(f"Error retrieving chunk {chunk_name}: {chunk_error}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Error retrieving chunk {chunk_name}: {chunk_error}"
                )

        # Upload the combined file to MinIO
        combined_file_size = combined_file.tell()
        combined_file.seek(0)
        logging.info(f"Combined file size before upload: {combined_file_size}")
        minio_client.put_object(
            MINIO_BUCKET_NAME,
            filename,
            combined_file,
            length=combined_file_size,
        )
        logging.info(f"Combined file {filename} uploaded to MinIO.")

        # Clean up individual chunks only after successful upload
        for chunk_index in range(total_chunks):
            chunk_name = f"{filename}.chunk{chunk_index}"
            minio_client.remove_object(MINIO_BUCKET_NAME, chunk_name)
        logging.info(f"Chunks cleaned up for {filename}.")

    except Exception as e:
        logging.error(f"Error combining chunks for {filename}: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error combining chunks: {e}"
        )
