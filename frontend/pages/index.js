import Link from "next/link";

export default function Home() {
  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px", textAlign: "center" }}>
      <h1>File Management System</h1>
      <p>Welcome! Choose an action below:</p>
      <div style={{ marginTop: "20px" }}>
        <Link href="/upload">
          <button style={buttonStyle}>Upload Files</button>
        </Link>
        <Link href="/file-details">
          <button style={buttonStyle}>List Files</button>
        </Link>
        <Link href="/preview">
          <button style={buttonStyle}>Preview & Download Files</button>
        </Link>
      </div>
    </div>
  );
}

// Inline CSS for buttons
const buttonStyle = {
  margin: "10px",
  padding: "10px 20px",
  fontSize: "16px",
  backgroundColor: "#0070f3",
  color: "white",
  border: "none",
  borderRadius: "5px",
  cursor: "pointer",
};
