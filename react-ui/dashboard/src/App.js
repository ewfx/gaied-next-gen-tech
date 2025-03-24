import React, { useState, useEffect } from "react";
import "./styles.css";
import DynamicChart from "./components/DynamicChart";  
import DynamicTable from "./components/DynamicTable";
import "bootstrap/dist/css/bootstrap.min.css";
import PieChart from "./components/DynamicPieChart";
var jsonData=[

  {
    "message": "Emails processed successfully",
    "data": [
        {
            "email_id": "email_001",
            "classification": "John's personal loan (ID 12345) for $1,200 is due on March 25th, with a 5-year term and a 3.5% interest rate.  Separately, a PDF from Citizens Bank to Wells Fargo details an adjustment to the ABTB Mid-Atlantic LLC Term Loan A-2, dated February 5, 2025.  Wells Fargo's commitment has increased to $5,542,963.55, effective February 4, 2025, requiring a funding of $24,714.36.  The loan reference is ABTB MID-ATLANTIC LLC $171.3MM 11-4-2022.  For inquiries regarding the personal loan, contact Mary Smith at (123) 456-7890. ",
            "fields": {
                "Person Names": [
                    "John",
                    "Mary Smith",
                    "Ramakrishna Kunchala"
                ],
                "Dates": [
                    "25th March",
                    "05-Feb-2025",
                    "04-Feb-2025",
                    "11-4-2022"
                ],
                "Phone Numbers": [
                    "(123) 456-7890"
                ],
                "Loan IDs / Reference Numbers": [
                    "12345",
                    "ABTB MID-ATLANTIC LLC $171.3MM 11-4-2022"
                ],
                "Interest Rates": [
                    "3.5%"
                ],
                "Currency Amounts": [
                    "$1,200",
                    "$171.3MM",
                    "USD 5,518,249.19",
                    "USD 5,542,963.55",
                    "$24,714.36"
                ],
                "Organizations": [
                    "Citizens Bank, N.A.",
                    "WELLS FARGO BANK, NATIONAL ASSOCIATION",
                    "ABTB MID-ATLANTIC LLC",
                    "WELLS FARGO BANK, NA",
                    "Citizens Bank NA"
                ],
                "Bank Account Details": {
                    "Bank Name": "Citizens Bank NA",
                    "ABA #:": "011500120",
                    "Account #:": "002663901",
                    "Account Name": "LIQ CLO Operating Account"
                },
                "Job Titles": [
                    "loan officer"
                ],
                "Department": [
                    "Loan Agency Services"
                ],
                "Loan Amount": "171.3MM",
                "Payment Due Dates": [
                    "25th March"
                ],
                "Long Term Duration": "5 years",
                "Loan Type": "TERM LOAN A-2",
                "Bank Names": [
                    "Citizens Bank, N.A.",
                    "WELLS FARGO BANK, NATIONAL ASSOCIATION",
                    "Citizens Bank NA"
                ],
                "Bank Account Numbers": [
                    "002663901"
                ],
                "Routing Numbers": [
                    "011500120"
                ],
                "Payment Amount": "24,714.36",
                "Payment Instructions": "PLEASE FUND YOUR SHARE OF $24,714.36",
                "Document Types": [
                    "PDF"
                ],
                "Document Dates": [
                    "05-Feb-2025"
                ],
                "request_type": "Lending Services",
                "confidence_score": 0.95
            },
            "duplicate": false
        }
    ]
}
]
function App() {
  const [emailData, setEmailData] = useState([]);
  const emailData1 = jsonData.length > 0 ? jsonData[0].data : [];

  const API_URL = "http://localhost:8000/process-emails";
  useEffect(() => {
    fetch(API_URL)
      .then((response) => response.json())
      .then((data) => {
        console.log('data',jsonData);
        if (data && data.data) {
          setEmailData(data);
        }
      })
      .catch((error) => console.error("Error fetching:", error));
  }, []);

  return (
    <>
    <div className="App">
      <header>
      </header>
    </div>
    <div className="container">
      <h1>Data Dashboard</h1>
      {/* {emailData.length > 0 ? (
        <DynamicChart emailData={emailData} />
      ) : (
        <p>Loading data...</p>
      )} */}
      <DynamicTable emailData={emailData} />
      <PieChart emailData={emailData} />
    </div>
  </>
  );
}

export default App;
