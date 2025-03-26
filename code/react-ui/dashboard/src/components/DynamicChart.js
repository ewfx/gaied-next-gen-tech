import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

const DynamicChart = ({ emailData }) => {
  // Extract numerical data dynamically
  const formattedData = emailData.map((email) => {
    let numericFields = {};

    // Iterate over fields in JSON and extract only numeric values
    Object.entries(email.fields).forEach(([key, value]) => {
      if (typeof value === "string" && value.match(/^\d+(\.\d+)?$/)) {
        numericFields[key] = parseFloat(value);
      }
    });

    return {
      email_id: email.email_id,
      ...numericFields,
    };
  });

  return (
    <div className="chart-container">
      <h2>Loan Data Overview</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="email_id" />
          <YAxis />
          <Tooltip />
          {Object.keys(formattedData[0] || {})
            .filter((key) => key !== "email_id")
            .map((key, index) => (
              <Bar key={index} dataKey={key} fill={`#${Math.floor(Math.random() * 16777215).toString(16)}`} />
            ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DynamicChart;
