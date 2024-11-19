from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class FileMetadata(Base):
    __tablename__ = "file_metadata"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, unique=True)
    file_path = Column(String)
    upload_status = Column(String, default="completed")  # or 'in-progress'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
