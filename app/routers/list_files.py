from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FileMetadata

router = APIRouter()

@router.get("/")
def list_files(db: Session = Depends(get_db)):
    files = db.query(FileMetadata).all()
    return [{"filename": file.filename, "file_path": file.file_path} for file in files]
