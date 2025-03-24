import React from "react";
import { Pie } from "react-chartjs-2";
import "chart.js/auto";

const MultiCategoryPieChart = ({ emailData = [] }) => {
  if (!Array.isArray(emailData) || emailData.length === 0) {
    return <div className="alert alert-warning text-center mt-3">No data available</div>;
  }

  // Function to count occurrences and store details
  const processCategory = (categoryArray) => {
    return {
      count: categoryArray.length,
      details: categoryArray.join(", "), // Joining for tooltip details
    };
  };

  // Extract relevant fields
  let loanTypes = [];
  let organizations = [];
  let documentTypes = [];
  let paymentAmounts = [];
  let loanAmounts = [];
  let confidenceScores = [];

  emailData.forEach((email) => {
    if (email.fields) {
      if (email.fields["Loan Type"]) loanTypes.push(email.fields["Loan Type"]);
      if (email.fields["Organizations"]) organizations.push(...email.fields["Organizations"]);
      if (email.fields["Document Types"]) documentTypes.push(...email.fields["Document Types"]);

      // Group Payment Amounts into Ranges
      if (email.fields["Payment Amount"]) {
        const amount = parseFloat(email.fields["Payment Amount"].replace(/[^0-9.]/g, ""));
        if (amount < 5000) paymentAmounts.push("Less than $5K");
        else if (amount < 25000) paymentAmounts.push("$5K - $25K");
        else paymentAmounts.push("More than $25K");
      }

      // Group Loan Amounts into Ranges
      if (email.fields["Loan Amount"]) {
        const loanAmount = parseFloat(email.fields["Loan Amount"].replace(/[^0-9.]/g, ""));
        if (loanAmount < 50000) loanAmounts.push("Less than $50K");
        else if (loanAmount < 500000) loanAmounts.push("$50K - $500K");
        else loanAmounts.push("More than $500K");
      }

      // Group Confidence Scores into Ranges
      if (email.fields["confidence_score"]) {
        const confidence = email.fields["confidence_score"];
        if (confidence < 0.5) confidenceScores.push("Low Confidence (<50%)");
        else if (confidence < 0.8) confidenceScores.push("Medium Confidence (50%-80%)");
        else confidenceScores.push("High Confidence (>80%)");
      }
    }
  });

  // Store processed data for each category
  const categories = {
    "Loan Types": processCategory(loanTypes),
    "Organizations": processCategory(organizations),
    "Document Types": processCategory(documentTypes),
    "Payment Amounts": processCategory(paymentAmounts),
    "Loan Amounts": processCategory(loanAmounts),
    "Confidence Scores": processCategory(confidenceScores),
  };

  // Prepare data for Pie Chart
  const labels = Object.keys(categories);
  const dataValues = labels.map((label) => categories[label].count);
  const colors = ["#FF6384", "#36A2EB", "#FFCE56", "#4CAF50", "#8E44AD", "#E67E22"];

  // Chart data
  const data = {
    labels: labels,
    datasets: [
      {
        data: dataValues,
        backgroundColor: colors.slice(0, labels.length),
        hoverBackgroundColor: colors.slice(0, labels.length).map((color) => color + "CC"),
      },
    ],
  };

  // Custom tooltip to show detailed info on hover
  const options = {
    plugins: {
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            let categoryName = tooltipItem.label;
            return [
              `Total: ${categories[categoryName].count}`,
              `Details: ${categories[categoryName].details}`,
            ];
          },
        },
      },
    },
  };

  return (
    <div className="container mt-4 text-center">
      <h2 className="text-white bg-dark p-3 rounded">📊 Email Insights Overview</h2>
      <div className="d-flex justify-content-center">
        <div style={{ width: "60%", minWidth: "300px" }}>
          <Pie data={data} options={options} />
        </div>
      </div>
    </div>
  );
};

export default MultiCategoryPieChart;
