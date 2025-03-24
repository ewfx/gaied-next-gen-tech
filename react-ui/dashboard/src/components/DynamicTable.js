import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";

const DynamicTable = ({ emailData = [] }) => {
  if (!Array.isArray(emailData) || emailData.length === 0) {
    return <div className="alert alert-warning text-center mt-3">No data available</div>;
  }

  const allFields = new Set();
  emailData.forEach((email) => {
    if (email.fields && typeof email.fields === "object") {
      Object.keys(email.fields).forEach((key) => allFields.add(key));
    }
  });

  const headers = ["Email ID", "Classification", ...Array.from(allFields), "Duplicate"];

  return (
    <div className="container mt-4">
            <h2 className="text-center text-white bg-danger p-3 rounded">📧 Email Insights Overview</h2>
      <div className="table-responsive">
        <table className="table table-bordered text-center">
          <thead style={{ backgroundColor: "#ADD8E6" }}>  {/* Light Blue Header */}
            <tr>
              {headers.map((header, index) => (
                <th key={index} className="p-2">{header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {emailData.map((email, emailIndex) => (
              <tr key={emailIndex}>
                <td className="fw-bold">{email.email_id || "N/A"}</td>
                <td className="text-start">{email.classification || "N/A"}</td>
                {Array.from(allFields).map((field, fieldIndex) => (
                  <td key={fieldIndex} className="text-break">
                    {Array.isArray(email.fields?.[field])
                      ? email.fields[field].join(", ")
                      : typeof email.fields?.[field] === "object"
                      ? JSON.stringify(email.fields[field], null, 2)
                      : email.fields?.[field] || "N/A"}
                  </td>
                ))}
                <td>{email.duplicate ? "true" : "false"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DynamicTable;
