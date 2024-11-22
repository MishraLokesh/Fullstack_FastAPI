import { useState } from "react";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const CHUNK_SIZE = 1024 * 1024; // 1MB

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadProgress(0);  // Reset the progress bar to 0
  };

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }

    const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
    let uploadedChunks = 0;

    for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
      const start = chunkIndex * CHUNK_SIZE;
      const end = Math.min(start + CHUNK_SIZE, file.size);
      const chunk = file.slice(start, end);

      const formData = new FormData();
      formData.append("filename", file.name);
      formData.append("chunk_index", chunkIndex);
      formData.append("total_chunks", totalChunks);
      formData.append("file", chunk);

      try {
        const response = await fetch("http://127.0.0.1:8000/upload/upload", {
          method: "POST",
          body: formData,
        });
        // Log response body (assuming it's JSON)
        const responseBody = await response.json(); // Use `.text()` or `.blob()` if the response isn't JSON
        console.log("Response Body:", responseBody);
        if (!response.ok) {
          throw new Error(`Failed to upload chunk ${chunkIndex}`);
        }

        uploadedChunks += 1;
        setUploadProgress(Math.floor((uploadedChunks / totalChunks) * 100));
      } catch (error) {
        console.error("Error uploading file chunk:", error);
        alert("Error uploading file. Please try again.");
        return;
      }
    }

    alert("File uploaded successfully!");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Resumable File Upload</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={uploadFile} disabled={!file}>
        Upload
      </button>
      <div style={{ marginTop: "20px" }}>
        <p>Upload Progress: {uploadProgress}%</p>
        <div
          style={{
            height: "20px",
            width: "100%",
            backgroundColor: "#ccc",
            position: "relative",
          }}
        >
          <div
            style={{
              height: "100%",
              width: `${uploadProgress}%`,
              backgroundColor: "green",
              transition: "width 0.5s ease-in-out",
            }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default Upload;
