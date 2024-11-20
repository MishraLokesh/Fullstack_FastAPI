import { useState } from "react";

const Preview = () => {
  const [filename, setFilename] = useState("");
  const [previewUrl, setPreviewUrl] = useState("");
  const [error, setError] = useState("");

  const handlePreview = async () => {
    setError("");
    setPreviewUrl("");

    if (!filename) {
      setError("Please enter a filename to preview.");
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/files/preview/${filename}`);

      if (!response.ok) {
        throw new Error(`Failed to fetch file: ${response.statusText}`);
      }

      // Convert the response into a Blob for preview
      const blob = await response.blob();

      // Generate a URL for previewing the file
      const objectUrl = window.URL.createObjectURL(blob);
      setPreviewUrl(objectUrl);
    } catch (err) {
      console.error("Error previewing file:", err);
      setError("Failed to fetch the file. Please check the filename and try again.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>File Preview</h1>
      <input
        type="text"
        placeholder="Enter filename"
        value={filename}
        onChange={(e) => setFilename(e.target.value)}
        style={{ padding: "10px", marginRight: "10px", width: "300px" }}
      />
      <button onClick={handlePreview}>Preview</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {previewUrl && (
        <div style={{ marginTop: "20px" }}>
          <h2>Preview:</h2>
          {filename.endsWith(".pdf") ? (
            <iframe
              src={previewUrl}
              width="100%"
              height="500px"
              title="PDF Preview"
            ></iframe>
          ) : filename.endsWith(".txt") || filename.endsWith(".csv") ? (
            <iframe
              src={previewUrl}
              width="100%"
              height="500px"
              title="Text Preview"
            ></iframe>
          ) : filename.endsWith(".jpg") ||
            filename.endsWith(".jpeg") ||
            filename.endsWith(".png") ||
            filename.endsWith(".gif") ? (
            <img
              src={previewUrl}
              alt="Image Preview"
              style={{ maxWidth: "100%", maxHeight: "500px" }}
            />
          ) : (
            <p>Unsupported file type for preview.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Preview;
