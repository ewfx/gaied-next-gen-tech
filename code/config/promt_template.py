from langchain.prompts import PromptTemplate

def promt():
    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="""
    You are an AI tasked with extracting structured information from raw text.

    ### Text:
    {text}

   ### **1. Classify the request type** into one of the following categories:
    - Commercial Banking
    - Lending Services
    - Account Management
    - Loan Application
    - Payment Inquiry
    - General Inquiry
    - Adjustment
    - AU Transfer
    - Closing Notice
    - Commitment Change
    - Fee Payment
    - Money Movement-Inbound
    - Money Movement - Outbound
    - Cash Management
    - Credit Facility Management
    - Trade Finance
    - Collateral Management
    - Loan Status Inquiry
    - Interest Rate Modification 
    - Prepayment or Foreclosure Request
    - Loan Document Retrieval 
    - Default / Delinquency Handling

    ---

    ### **2. Classify the Sub-Request type** based on the parent request type:

    - **If the request type is "Money Movement-Inbound":**
      - Principal
      - Interest
      - Principal + Interest
      - Principal + Interest + Fee

      - **If the request type is "Money Movement-Outbound":**
      - Timebound
      - Foreign Currency
      
    - **If the request type is "Fee Payment":**
      - Late Payment Fee
      - Penalty Fee
      - Service Charge
      - Processing Fee

    - **If the request type is "Loan Application":**
      - New Loan
      - Refinance
      - Loan Modification
      - Pre-Approval

    - **If the request type is "Payment Inquiry":**
      -  Transaction Status
      -  Payment Confirmation
      -  Failed Payment
      -  Refund Request

    - **If the request type is "Account Management":**
      -  Account Closure
      -  Account Update
      -  Account Verification
      -  Account Reactivation

      - **If the request type is "Commitment Change":**
      -  Cashless Roll
      -  Increase 
      -  Decrease

    - **If the request type is "Adjustment":**
    - Only return one of the following:
      - `Principal Adjustment`
      - `Interest Adjustment`
      - `Fee Adjustment`
      - `Balance Correction`
      - **If no valid sub-request type is detected**, always return `sub_request_type: "N/A"`

      ---

      ###  **Missing Sub-Request Handling**
    - **If no valid sub-request is detected or applicable:**  
      - Always return `sub_request_type: "N/A"`
    
      ### **4. Assign the Appropriate Team**
    **Extract Key Entities:**  
    - Identify `loan IDs`, `payment terms`, `fees`, `payments`, `compliance issues`, and `technical references`.  
    - Detect `request type` and `sub-request type` based on context. 
     **Classify by Teams:**  
     - **Loan Processing:**  
        - Keywords → `loan`, `interest rate`, `loan ID`, `principal balance`, `due date`.  
        - Request Type → `Loan Management`  
        - Sub-request Types → `Disbursement`, `Approval`, `Modification`, `Renewal`.  
    - **Payment & Money Movement:**  
        - Keywords → `payment`, `fund transfer`, `wire`, `ACH`, `transaction ID`.  
        - Request Type → `Payment Operations`  
        - Sub-request Types → `Wire Transfer`, `ACH`, `Remittance`, `Money Movement`.  
    - **Fee & Adjustment:**  
        - Keywords → `fee`, `adjustment`, `penalty`, `service charge`.  
        - Request Type → `Fee Management`  
        - Sub-request Types → `Interest Adjustment`, `Penalty Fee`, `Correction`.
    **Assign the Appropriate Team:**  
    - **Combine the content of the text, request type, and sub-request type** to determine the most appropriate team.  
    - Use **key entity matching** (loan ID, payment terms, fee details, transaction references, compliance keywords) to compare the content with the team responsibilities.  
    - **Prioritize key entity matching** over the request type alone.  
    - Assign the most relevant team based on the overall context.

    ###  **Fallback Team Assignment**
    - **If no valid team is identified**, Always return `assign_teams: "Commercial Lending Support Team"`.

    ###  **Fallback Team Assignment**
    - **If no valid team is identified**, Always return `assign_teams: **"Commercial Lending Support Team"**.

    ---

    ### **5. Assign Overall Confidence Score**
    - Generate a **single confidence score** representing the **accuracy of the entire extraction process**.
    - Score should be a **value between 0.0 and 1.0**.
    - Confidence should reflect the AI's certainty in the **overall correctness of the extraction**.


    ### **6. Extract the following fields if they are present**:
    - Person Names
    - Dates
    - Phone Numbers
    - Loan IDs / Reference Numbers
    - Interest Rates
    - Currency Amounts
    - Organizations
    - Bank Account Details
    - Job Titles
    - Department
    - Loan Amount
    - Payment Due Dates
    - Long Term Duration
    - Loan Type
    - Outstanding Balance
    - Loan Status
    - Installment Details
    - EMI Amount
    - Bank Names
    - Bank Account Numbers
    - Routing Numbers
    - IBAN / SWIFT Codes
    - Payment References / Transaction IDs
    - Bank Branch Names
    - Wire Transfer Details
    - Payment Amount
    - Payment Status
    - Transaction Dates
    - Payment Instructions
    - Fund Allocation Details
    - Remittance Details
    - Late Payment Fees / Penalties
    - Document Types
    - Attachment Names
    - File References
    - Document Dates

    **Exclude fields that are missing or empty.**
    Only include fields with extracted values.

    ---

    ---

    ### **Output Requirements**
    - **Strictly valid JSON format**
    - **Double quotes** around all keys and values
    - Properly formatted nested objects and arrays
    - No comments or extra text
    - **Global confidence score**
    - **Exclude empty or missing fields**

    ---

    ### **Self-Validation Instructions**
    Before returning the JSON:
    - **Validate the JSON structure**
    - If invalid, **correct it** automatically
    - Ensure the output is strictly valid JSON with no trailing commas or invalid characters
    - **Exclude empty fields**
    - Return **only the JSON output**
    """
    )
    # Return the prompt instance
    return prompt_template
