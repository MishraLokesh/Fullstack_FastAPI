// api.test.js
import request from 'supertest'; // For making HTTP requests to the backend
import { expect } from 'chai';  // For assertions

// Replace with the correct path to your backend server (e.g., localhost:8000 or another URL)
const BASE_URL = 'http://127.0.0.1:8000';

describe('File Preview API Tests', function () {
  // Test: Successful file preview
  it('should return status 200 and a blob for a valid file', async function () {
    const filename = 'valid-file.pdf'; // Change to a valid file in your storage
    const res = await request(BASE_URL).get(`/files/preview/${filename}`);
    expect(res.status).to.equal(200);
    expect(res.headers['content-type']).to.include('application/pdf'); // assuming it's a PDF file
  });

  // Test: Invalid file (non-existent)
  it('should return status 404 for a non-existent file', async function () {
    const filename = 'non-existent-file.pdf';
    const res = await request(BASE_URL).get(`/files/preview/${filename}`);
    expect(res.status).to.equal(404);
    expect(res.body.error).to.equal('File not found');
  });

  // Test: Missing filename in the request
  it('should return status 400 if filename is missing', async function () {
    const res = await request(BASE_URL).get('/files/preview/');
    expect(res.status).to.equal(400);
    expect(res.body.error).to.equal('Filename is required');
  });

  // Test: Invalid file type (unsupported file for preview)
  it('should return status 415 for an unsupported file type', async function () {
    const filename = 'unsupported-file.xyz'; // Unsupported file type
    const res = await request(BASE_URL).get(`/files/preview/${filename}`);
    expect(res.status).to.equal(415); // Unsupported Media Type
    expect(res.body.error).to.equal('Unsupported file type');
  });
});
