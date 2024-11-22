import React, { useState } from "react";
import axios from "axios";

export default function DownloadFile() {
  const [inputFilename, setInputFilename] = useState("");

  const handleDownload = async () => {
    if (!inputFilename) {
      alert("Please enter the file identifier to download.");
      return;
    }

    try {
      const response = await axios.get(`http://localhost:8000/files/download/${inputFilename}`, {
        responseType: "blob",
      });

      // Extract filename from Content-Disposition header
      const contentDisposition = response.headers["content-disposition"];
      const filenameMatch = contentDisposition?.match(/filename="?([^"]+)"?/);
      const filename = filenameMatch ? filenameMatch[1] : "downloaded_file";

      // Create a download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link); // Clean up the DOM
    } catch (error) {
      console.error("Error downloading the file:", error);
      alert("Failed to download the file. Please check the identifier and try again.");
    }
  };

  return (
    <div>
      <h1>Download File</h1>
      <input
        type="text"
        placeholder="Enter file identifier"
        value={inputFilename}
        onChange={(e) => setInputFilename(e.target.value)}
        style={{ marginBottom: "10px", padding: "5px", width: "300px" }}
      />
      <br />
      <button onClick={handleDownload}>Download</button>
    </div>
  );
}
