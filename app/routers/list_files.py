from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FileMetadata

router = APIRouter()

@router.get("/")
def list_files(db: Session = Depends(get_db)):
    files = db.query(FileMetadata).all()
    if not files:
      return {"message": "No files uploaded yet", "files": []}
    
    # For debugging, print the files to check if file_path is populated
    for file in files:
      print(file.filename, file.file_path)

    return [{"filename": file.filename, "file_path": file.file_path} for file in files]
