from fastapi import FastAPI
from app.database import Base, engine
from app.routers import upload, list_files

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["File Upload"])
app.include_router(list_files.router, prefix="/files", tags=["File List"])
