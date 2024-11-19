import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from minio import Minio
from app.database import get_db
from app.models import FileMetadata
from io import BytesIO

# MinIO client configuration
minio_client = Minio(
    "127.0.0.1:9000",
    access_key="E73DmxZVLQv5sldAZ7ia",
    secret_key="lX43QnpE0D6uhka2EwrXDosxoCQylC9uh8UwJAVU",
    secure=False  # Use True if you are using HTTPS
)

# MinIO Bucket
BUCKET_NAME = "lokbucket" 

CHUNK_SIZE = 1024 * 1024  # 1MB per chunk
router = APIRouter()

logging.basicConfig(level=logging.INFO)  # Enable logging for debugging

@router.post("/upload_file")
async def upload_file_resumable(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        # Loop through each file
        for file in files:
            # Check if the file exists in the database
            file_metadata = db.query(FileMetadata).filter(FileMetadata.filename == file.filename).first()

            if file_metadata:
                # File already exists, resume from the last uploaded chunk
                uploaded_chunks = file_metadata.uploaded_chunks
                file_size = file_metadata.file_size
            else:
                # New upload, initialize metadata
                uploaded_chunks = 0
                file_size = len(await file.read())  # Calculate file size for new files
                file_metadata = FileMetadata(filename=file.filename, file_size=file_size)
                db.add(file_metadata)
                db.commit()

            # Rewind the file to the beginning to start reading
            await file.seek(0)

            # Initialize an in-memory buffer to simulate file writing (used for chunk upload)
            buffer = BytesIO()

            # Upload in chunks directly to MinIO
            while chunk := await file.read(CHUNK_SIZE):
                buffer.write(chunk)
                uploaded_chunks += 1  # Increment chunk count after each write

                # Upload the chunk to MinIO
                chunk_data = buffer.getvalue()  # Get the contents of the buffer
                minio_client.put_object(
                    BUCKET_NAME,  # The MinIO bucket name
                    f"{file.filename}",  # The filename in the bucket (e.g., file.chunk1)
                    BytesIO(chunk_data),  # Convert the chunk data into a stream to upload
                    len(chunk_data)  # Size of the chunk
                )

                # Update metadata in the database
                file_metadata.uploaded_chunks = uploaded_chunks
                db.commit()

                # Calculate and log the percentage progress
                progress = (uploaded_chunks * CHUNK_SIZE / file_size) * 100
                logging.info(f"Uploading {file.filename}: {progress:.2f}% completed.")

                # If the uploaded chunks cover the full file size, stop
                if uploaded_chunks * CHUNK_SIZE >= file_size:
                    break

            # After upload completion, update the status in the database
            file_metadata.upload_status = "completed"
            db.commit()

        return {"message": "Chunks uploaded successfully"}

    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
