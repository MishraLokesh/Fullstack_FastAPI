# File Upload Application

## Overview

This project implements a full-stack file upload mechanism allowing users to upload CSV files to cloud or local object storage, with features for file progress tracking, resuming interrupted uploads, and file previews. The solution also includes a backend API with FastAPI, a frontend built with Next.js, and cloud storage integration using MinIO. The solution is containerized using Docker Compose for seamless deployment.

---

## Technologies Used

- **Backend**: FastAPI, MinIO (for object storage)
- **Frontend**: Next.js, React
- **Database**: PostgreSQL (for storing metadata)
- **Testing**: Pytest (Backend tests), Cypress (Frontend tests)
- **Containerization**: Docker, Docker Compose
- **Cloud Storage**: MinIO (locally hosted for object storage)
- **Environment Variables**: dotenv, Docker secrets (for secure storage credentials)
- **Other Libraries**: python-dotenv, async-upload, react-dropzone, axios, and more.

---

## Approach, Cloud Storage Integration, and Assumptions

### Approach

The goal of this project was to create a file upload system that supports uploading multiple files, tracks upload progress, allows for the resumption of interrupted uploads, and provides a way to preview and download the uploaded files. The backend was built using **FastAPI**, while the frontend was developed using **Next.js** to offer a responsive and modern user interface.

- **Backend**: I designed the backend to handle file uploads using FastAPI's asynchronous capabilities to ensure it could handle large files efficiently. To support file upload progress tracking and resumption, I implemented a chunked file upload mechanism where files are divided into smaller parts. Each part's upload status is tracked, and if the upload is interrupted, it can be resumed from the last successful chunk.

- **Frontend**: The frontend is a simple yet intuitive React-based interface built with Next.js. The UI allows users to select one or more files for upload, view real-time progress with a progress bar, and resume interrupted uploads. Additionally, the frontend also provides options for previewing and downloading files. The frontend communicates with the backend API via **axios** to handle file uploads and downloads, and uses a dynamic progress bar to show the status of ongoing uploads.

### Cloud Storage Integration

For cloud storage, I used **MinIO** (an open-source alternative to AWS S3) to handle object storage. MinIO offers S3-compatible object storage, making it easy to integrate with applications that expect S3 APIs. In this project, the backend uses MinIO for storing the uploaded files, while metadata about the uploads (e.g., file names, status, and URLs) is stored in a **PostgreSQL** database using **SQLAlchemy**. The integration with MinIO allows the application to support file uploads to an object storage system, making it scalable and robust for production environments.

The credentials for cloud storage (such as access key, secret key, and endpoint) are handled through **environment variables** for security purposes. These variables are configured in a `.env` file and used by the backend during file upload operations. This ensures that sensitive data is not hardcoded in the application.

### Assumptions Made

- **File Type**: This implementation assumes that users will only upload CSV files, as specified in the requirements. File type validation is included to ensure that only CSV files are processed.

- **Cloud Storage Provider**: I used MinIO as the cloud storage solution, as it is easy to set up and provides an S3-compatible API. However, the architecture is designed to be extensible, so the system could easily be adapted to other cloud storage services like **AWS S3** or **Azure Blob Storage** with minimal changes to the configuration and storage interaction logic.

- **Authentication and Authorization**: For simplicity, this project assumes that no user authentication or authorization is needed. In a real-world scenario, securing the file upload API with proper authentication mechanisms (OAuth, API tokens, etc.) would be crucial.

- **Error Handling**: The system assumes the backend will handle most errors (e.g., file size limitations, storage issues, file format errors) gracefully by returning meaningful error messages to the user.

- **File Validation**: The system assesses the file type while previewing the file. It is required as preview works differently for different types of files.


# Project Setup Instructions

## Prerequisites
1. **MinIO** must be running locally on your system.
2. Ensure Docker and Docker Compose are installed on your machine.

---

## Backend Setup

### 1. Update the `.env` File
Edit the `.env` file in the `backend` directory with the following values:
- **MINIO_ENDPOINT**: Set this to your host's IP address. You can find your host IP by running the following command:
  ```bash
  hostname -I | awk '{print $1}'
- **MINIO_ACCESS_KEY**: Use the MinIO access key.
- **MINIO_SECRET_KEY**: Use the MinIO secret key.
- **MINIO_BUCKET_NAME**: Use the MinIO bucket name.

### 2. Update MinIO Credentials in Backend Code
Edit the following files in the backend/app/routers directory to match the MinIO credentials:
- **upload.py**
- **upload.py**
- **upload.py**
- **upload.py**

### 3. Docker Compose Configuration
Update docker-compose.yml file with the following values:
- **MINIO_ENDPOINT**: Set this to your host's IP address. You can find your host IP by running the following command:
  ```bash
  hostname -I | awk '{print $1}'
- **MINIO_ACCESS_KEY**: Use the MinIO access key.
- **MINIO_SECRET_KEY**: Use the MinIO secret key.

### 4. Running the project
```bash
  docker-compose up --build
```

### 5. Additional Notes
  MinIO Accessibility: Ensure MinIO is accessible from the host IP and port 9000.

### 6. Accessibility
  Access the frontend on:
  ```bash
    localhost:3000
  ```
  And the backend on:
  ```bash
    localhost:8000 or localhost:8000/docs
