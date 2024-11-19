import React, { useEffect, useState } from "react";
import axios from "axios";

export default function FileDetails() {
  const [fileDetails, setFileDetails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchFileDetails = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/files/");
        setFileDetails(response.data.files || []);
      } catch (err) {
        setError("Failed to fetch file details");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchFileDetails();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>Uploaded File Details</h1>
      {fileDetails.length > 0 ? (
        <table border="1" style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Filename</th>
              <th>Size (bytes)</th>
              <th>Upload Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {fileDetails.map((file, index) => (
              <tr key={index}>
                <td>{file.filename}</td>
                <td>{file.file_size || "Unknown"}</td>
                <td>{file.upload_date || "Unknown"}</td>
                <td>{file.upload_status || "Unknown"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No files have been uploaded yet.</p>
      )}
    </div>
  );
}
