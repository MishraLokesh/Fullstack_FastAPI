import { useState, useEffect } from 'react';

const ListFiles = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch the list of files from the backend API
    const fetchFiles = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/files/list-files');
        const data = await response.json();

        if (response.ok) {
          setFiles(data.files);
        } else {
          setError(data.message || 'Failed to fetch files.');
        }
      } catch (err) {
        setError('An error occurred while fetching files.');
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  // Display a loading message or an error message if there is an issue
  if (loading) {
    return <div>Loading files...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Uploaded Files</h1>
      <ul>
        {files.length > 0 ? (
          files.map((file, index) => (
            <li key={index}>
              {file}
              {/* Add buttons for download and preview */}
              <button onClick={() => handleDownload(file)}>Download</button>
              <button onClick={() => handlePreview(file)}>Preview</button>
            </li>
          ))
        ) : (
          <p>No files found in the bucket.</p>
        )}
      </ul>
    </div>
  );

  // Handle download file
  const handleDownload = (filename) => {
    window.location.href = `http://127.0.0.1:8000/files/download/${filename}`;
  };

  // Handle preview file
  const handlePreview = (filename) => {
    window.location.href = `http://127.0.0.1:8000/files/preview/${filename}`;
  };
};

export default ListFiles;
