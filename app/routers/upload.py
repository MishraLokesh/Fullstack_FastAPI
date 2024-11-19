from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
import logging
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FileMetadata

router = APIRouter()

STORAGE_PATH = "storage"
CHUNK_SIZE = 1024 * 1024  # 1MB per chunk
logging.basicConfig(level=logging.DEBUG)  # Enable logging for debugging

@router.post("/chunk-resume")
async def upload_file_resumable(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        # Create storage directory if it doesn't exist
        os.makedirs(STORAGE_PATH, exist_ok=True)

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

          file_path = os.path.join(STORAGE_PATH, file.filename)

          # Open the file in append mode if resuming
          with open(file_path, "ab") as f:
              # Skip the chunks already uploaded
              f.seek(uploaded_chunks * CHUNK_SIZE)

              while chunk := await file.read(CHUNK_SIZE):
                  f.write(chunk)
                  uploaded_chunks += 1  # Increment chunk count after each write

                  # Update metadata in the database
                  file_metadata.uploaded_chunks = uploaded_chunks
                  db.commit()

                  # Calculate and log the percentage progress
                  progress = (uploaded_chunks * CHUNK_SIZE / file_size) * 100
                  logging.debug(f"Uploading {file.filename}: {progress:.2f}% completed.")

                  # If the uploaded chunks cover the full file size, stop
                  if uploaded_chunks * CHUNK_SIZE >= file_size:
                      break

          # After upload completion, update the status in the database
          file_metadata.upload_status = "completed"
          db.commit()

          return {"message": "Chunk uploaded successfully", "file_path": file_path}

    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/progress/{filename}")
def get_upload_progress(filename: str, db: Session = Depends(get_db)):
    file_metadata = db.query(FileMetadata).filter(FileMetadata.filename == filename).first()
    
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    total_chunks = file_metadata.total_chunks
    uploaded_chunks = file_metadata.uploaded_chunks
    progress = (uploaded_chunks / total_chunks) * 100 if total_chunks else 0

    return {"filename": filename, "uploaded_chunks": uploaded_chunks, "total_chunks": total_chunks, "progress": progress}
