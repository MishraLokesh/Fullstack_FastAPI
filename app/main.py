from fastapi import FastAPI
from app.routers import upload, list_files

app = FastAPI()

app.include_router(upload.router, prefix="/upload", tags=["File Upload"])
app.include_router(list_files.router, prefix="/files", tags=["File List"])

