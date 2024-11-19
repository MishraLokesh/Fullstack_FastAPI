import React, { useState } from "react";
import axios from "axios";

export default function Upload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setMessage("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://localhost:8000/upload/chunk-resume", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
          setUploadProgress(progress);
        },
      });

      setMessage(response.data.message || "File uploaded successfully!");
    } catch (err) {
      console.error(err);
      setMessage("Error uploading file.");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>Upload File to MinIO</h1>
      <form onSubmit={handleUpload}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit" style={{ marginLeft: "10px" }}>Upload</button>
      </form>
      {uploadProgress > 0 && <p>Upload Progress: {uploadProgress}%</p>}
      {message && <p>{message}</p>}
    </div>
  );
}
