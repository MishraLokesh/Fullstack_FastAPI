import React from "react";
import axios from "axios";

export default function DownloadFile({ filename }) {
  const handleDownload = async () => {
    const response = await axios.get(`http://localhost:8000/download/${filename}`, {
      responseType: "blob",
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div>
      <h1>Download: {filename}</h1>
      <button onClick={handleDownload}>Download</button>
    </div>
  );
}
