import React, { useState, useEffect } from "react";
import axios from "axios";

export default function Preview() {
  const [files, setFiles] = useState([]);
  const [previewContent, setPreviewContent] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Fetch list of available files
    axios.get("http://localhost:8000/minio/list-files")
      .then((res) => setFiles(res.data.files))
      .catch((err) => console.error(err));
  }, []);

  const handlePreview = async (filename) => {
    try {
      const response = await axios.get(`http://localhost:8000/minio/preview-from-minio/${filename}`, {
        responseType: "blob",
      });

      // Preview text files
      if (filename.endsWith(".txt") || filename.endsWith(".csv")) {
        const reader = new FileReader();
        reader.onload = () => setPreviewContent(reader.result);
        reader.readAsText(response.data);
      } else if (filename.endsWith(".jpg") || filename.endsWith(".png")) {
        const imageUrl = URL.createObjectURL(response.data);
        setPreviewContent(<img src={imageUrl} alt={filename} style={{ maxWidth: "100%" }} />);
      } else {
        setMessage("Preview not supported for this file type.");
      }
    } catch (err) {
      console.error(err);
      setMessage("Error previewing file.");
    }
  };

  const handleDownload = (filename) => {
    axios({
      url: `http://localhost:8000/minio/download-from-minio/${filename}`,
      method: "GET",
      responseType: "blob",
    })
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      })
      .catch((err) => console.error(err));
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>Preview & Download Files</h1>
      {files.length > 0 ? (
        <ul>
          {files.map((file) => (
            <li key={file}>
              {file}{" "}
              <button onClick={() => handlePreview(file)}>Preview</button>{" "}
              <button onClick={() => handleDownload(file)}>Download</button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No files available</p>
      )}
      {previewContent && (
        <div>
          <h3>Preview:</h3>
          <div>{previewContent}</div>
        </div>
      )}
      {message && <p>{message}</p>}
    </div>
  );
}
