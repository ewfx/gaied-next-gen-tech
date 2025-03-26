import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

const UploadFile = () => {
  const [file, setFile] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setMessage("");
  };

  const handleSubmit = () => {
    if (!file) {
      setMessage("Please upload a file first.");
      return;
    }
    setMessage(`File "${file.name}" uploaded successfully!`);
  };

  const handleProcess = () => {
    if (!file) {
      setMessage("Please upload a file first.");
      return;
    }
    setProcessing(true);
    setMessage("Processing file...");

    setTimeout(() => {
      setProcessing(false);
      setMessage(`File "${file.name}" processed successfully!`);
    }, 2000);
  };

  return (
    <div className="container mt-5">
      <div className="card p-4 shadow">
        <h2 className="text-center">File Upload & Processing</h2>

        <div className="mb-3">
         
          <input type="file" className="form-control" onChange={handleFileChange} />
        </div>

        <div className="d-flex gap-3">
          <button className="btn btn-primary" onClick={handleSubmit}>Upload File</button>
          <button className="btn btn-success" onClick={handleProcess} disabled={processing}>
            {processing ? "Processing..." : "Process File"}
          </button>
        </div>




        {message && <div className="alert alert-info mt-3">{message}</div>}
      </div>
    </div>
  );
};

export default UploadFile;
