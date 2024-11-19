from fastapi import APIRouter, HTTPException, Depends
import os
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FileMetadata
import csv

router = APIRouter()
STORAGE_PATH = "storage"

@router.get("/preview/{filename}")
async def preview_file(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)

    # Ensure the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Handle different file types (CSV, TXT)
    if filename.endswith(".csv"):
        # Read CSV content
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            rows = [row for row in reader][:10]  # Return the first 10 rows as preview
            return {"type": "csv", "content": rows}

    elif filename.endswith(".txt"):
        # Read text file content
        with open(file_path, "r") as file:
            content = file.read(1024)  # Return the first 1KB of the file as preview
            return {"type": "text", "content": content}

    else:
        raise HTTPException(status_code=400, detail="Preview not supported for this file type")
