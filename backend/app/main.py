from fastapi import FastAPI
from app.database import Base, engine
from app.routers import upload, list_files, download, preview
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["File Upload"])
app.include_router(list_files.router, prefix="/files", tags=["File List"])
app.include_router(download.router, prefix="/files", tags=["File Download"])
app.include_router(preview.router, prefix="/files", tags=["File Preview"])
