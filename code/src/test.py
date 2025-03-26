import re
import pyjson5
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI  # Correct import



import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyCR8KgoHikSU5tVRyavvd4a8SviZveR-w0"

# Initialize Gemini AI Model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)

# Example Text
text2= """
BANK OF AMERICA
Bank of America, N.A.
To: WELLS FARGO BANK NATIONAL ASSOCIATION
Date: 8-Nov-2023

ATTN: AGENT DEFAULT
Phone: 999-999-9999
Fax: 877-606-9426
Email: DENLCFX@wellsfargo.com
Re: CANTOR FITZGERALD LP USD 425MM MAR22 / REVOLVER / CANTOR FIT00037

Deal CUSIP: 13861EAEO
Deal ISIN: US13861EAE05
Facility CUSIP: 13864EAF7
Facility ISIN: US13861EAF79
Lender MEI: US1L058422
Effective 10-Nov-2023, CANTOR FITZGERALD LP has elected to repay under the SOFR (US) Term option, a total of USD 20,000,000.00.

Previous Global principal balance: USD 45,000,000.00
New Global principal balance: USD 25,000,000.00
This loan was effective 20-Jul-2023 and is scheduled to reprice on 20-Nov-2023.
Your share of the USD 20,000,000.00 SOFR (US) Term option payment is USD 1,411,764.71.
Previous Lender Share Principal Balance: USD 3,176,470.59
We will remit USD 1,411,764.71 on the effective date.
Please note that (i) if the Borrower has not in fact made such payment; or (ii) any payment you receive is in excess of what was paid by the Borrower or (iii) we notify you that the payment was erroneously made, then pursuant to the provisions of the credit facility, you agree to return such payment.
For: WELLS FARGO BANK NATIONAL ASSOCIATION
To: WELLS FARGO BANK, NA

ABA Number: 121000248
Account No: XXXXXXXXXX0720
Reference: CANTOR FITZGERALD LP USD 425MM MAR22, SOFR (US) Term Principal Payment (CANTOR FIT00037)
Thanks & Regards,
JONNY HERNANDEZ

Telephone #: +1 980 388 3225
Email: jonny.hernandez@bofa.com
"""

text = """
Dear John, your loan ID 12345 is due on 25th March. The amount due is $1,200. 
Please contact your loan officer, Mary Smith, at (123) 456-7890 for any inquiries. 
Your loan term is 5 years with an interest rate of 3.5%.

[PDF Attachment Text]
Citizens Bank, N.A.
Loan Agency Services
Date: 05-Feb-2025
TO: WELLS FARGO BANK, NATIONAL ASSOCIATION
ATTN: RAMAKRISHNA KUNCHALA
Fax: 877-606-9426
Re: ABTB MID-ATLANTIC LLC $171.3MM 11-4-2022, TERM LOAN A-2
Description: Facility Lender Share Adjustment
BORROWER: ABTB MID-ATLANTIC LLC
DEAL NAME: ABTB MID-ATLANTIC LLC $171.3MM 11-4-2022
Effective 04-Feb-2025, the Lender Shares of facility TERM LOAN A-2 have been adjusted.
Your share of the commitment was USD 5,518,249.19. It has been Increased to USD 5,542,963.55.
For: WELLS FARGO BANK, NA
Reference: ABTB MID-ATLANTIC LLC $171.3MM 11-4-2022,
If you have any questions, please call the undersigned.
PLEASE FUND YOUR SHARE OF $24,714.36
Bank Name: Citizens Bank NA
ABA #: 011500120
Account #: 002663901
Account Name: LIQ CLO Operating Account
"""

# Define the Prompt Template
prompt_template10 = PromptTemplate(
    input_variables=["text"],    # ✅ Expect only "text" as input
    template="""
You are an AI tasked with extracting structured information from commercial banking and lending service emails.

### **Input Email Text:**
{text}

---

### **Instructions:**
1. **Extract the following fields with accuracy:**
- `person_names`: Person names (e.g., "John Doe")
- `loan_ids`: Loan IDs or reference numbers
- `loan_amount`: Loan amount (e.g., "$100,000")
- `interest_rate`: Interest rate (e.g., "5.5%")
- `currency_amounts`: Currency values (e.g., "$1,200")
- `payment_due_dates`: Payment due dates (e.g., "2025-04-10")
- `loan_type`: Loan type (e.g., "Mortgage", "Auto Loan")
- `bank_names`: Bank names (e.g., "Citizens Bank")
- `bank_account_numbers`: Bank account numbers
- `routing_numbers`: Routing or ABA numbers
- `payment_amount`: Payment amounts
- `transaction_dates`: Transaction dates
- `document_types`: Document types (e.g., "Contract", "Invoice")

---

###  **Output Format:**
Return the result in **strict JSON format** like this:
```json
{
    "fields": {
        "person_names": {"value": ["John Doe"], "confidence": 0.95},
        "loan_ids": {"value": ["12345"], "confidence": 0.90},
        "currency_amounts": {"value": ["$1,200"], "confidence": 0.94},
        "organizations": {"value": ["Citizens Bank"], "confidence": 0.93},
        "bank_account_details": {"value": ["ABA #: 011500120"], "confidence": 0.90}
    },
    "request_type": {
        "value": "Lending Services",
        "confidence": 0.94
    }
}
""" )
prompt_templatelatest = PromptTemplate(
    input_variables=["text"],
    template="""
You are an AI tasked with extracting structured information from raw text.

### Text:
{text}

### **1. Extract the following fields if they are present**:
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

✅ **Exclude fields that are missing or empty.**
✅ Only include fields with extracted values.

---

### **2. Classify the request type** into one of the following categories:
- Commercial Banking
- Lending Services
- Account Management
- Loan Application
- Payment Inquiry
- General Inquiry

---

### **3. Assign Overall Confidence Score**
- Generate a **single confidence score** representing the **accuracy of the entire extraction process**.
- Score should be a **value between 0.0 and 1.0**.
- Confidence should reflect the AI's certainty in the **overall correctness of the extraction**.

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

prompt_template2 = PromptTemplate(
    input_variables=["text"],
    template="""
You are an AI tasked with extracting structured information from raw text.

Text:
{text}

1. Please extract the following fields:
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
- Bank Acount Numbers
- Routing Numbers
- IBAN /SWIFT Codes
- Payment References /Transaction IDs
- Bank Branch Names
- Wire Transfer Details
- Payment Amount
- Payment Status
- Transation Dates
- Payment Instructions
- Fund Allocation Details
- Remittance Details
- Late Payment Fees / Penalties
- Document Types
- Attachment Names
- File References
- Document Dates

2. **Classify the request type** into one of the following categories:
    - Commercial Banking
    - Lending Services
    - Account Management
    - Loan Application
    - Payment Inquiry
    - General Inquiry


Return the output in **strictly valid JSON format** with:
- Double quotes around all keys and values.
- Properly formatted nested objects and arrays.
- No comments or extra text.
- Include confidence scores for all fields.
"""
)
prompt_template22 = PromptTemplate(
    input_variables=["text"],
    template="""
You are an AI tasked with extracting structured information from raw text.

### Text:
{text}

### **1. Extract the following fields:**
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
- Bank Acount Numbers
- Routing Numbers
- IBAN /SWIFT Codes
- Payment References /Transaction IDs
- Bank Branch Names
- Wire Transfer Details
- Payment Amount
- Payment Status
- Transation Dates
- Payment Instructions
- Fund Allocation Details
- Remittance Details
- Late Payment Fees / Penalties
- Document Types
- Attachment Names
- File References
- Document Dates


### **2. Classify the request type** into one of the following categories:
- Commercial Banking
- Lending Services
- Account Management
- Loan Application
- Payment Inquiry
- General Inquiry

---

###  **Output Requirements**
- **Strictly valid JSON format**
- **Double quotes** around all keys and values
- Properly formatted nested objects and arrays
- No comments or extra text
- **Include confidence scores** for all fields

---

###  **Self-Validation Instructions**
Before returning the JSON:
- **Validate the JSON structure**
- If invalid, **correct it** automatically
- Ensure the output is strictly valid JSON with no trailing commas or invalid characters
- Return **only the JSON output**
"""
)

prompt_template3 = PromptTemplate(
    input_variables=["text"],
    template="""
You are an AI tasked with extracting structured information from raw text.

Text:
{text}

Please extract the following fields:
- Person Names
- Dates
- Phone Numbers
- Loan IDs
- Interest Rates
- Currency Amounts
- Organizations
- Bank Account Details

Return the extracted fields in JSON format with confidence scores.
"""
)

prompt_template1 = PromptTemplate(
    input_variables=["text"],
    template="""
You are an AI tasked with extracting structured information from raw text and classifying the request type.

### Text:
{text}

---

###  Instructions:

1. **Extract the following fields:**
    - `person_names`: List of full names mentioned in the text.
    - `dates`: List of all dates present.
    - `phone_numbers`: List of phone numbers.
    - `loan_ids`: List of loan IDs.
    - `interest_rates`: List of interest rates.
    - `currency_amounts`: List of currency values (e.g., USD, EUR).
    - `organizations`: List of organizations or companies mentioned.
    - `bank_account_details`: List of account numbers, ABA numbers, or any relevant bank details.
    - `bank_name`: Name of the bank(s) mentioned.
    - `loan_amount`: Extract the loan amount(s) mentioned.

2. **Classify the request type** into one of the following categories:
    - Commercial Banking
    - Lending Services
    - Account Management
    - Loan Application
    - Payment Inquiry
    - General Inquiry

3. **For each field and the request type**, include:
    - `value`: the extracted data (as a list for multiple occurrences)
    - `confidence`: a score between **0.0 and 1.0**

---

###  Output Format:
Return the result in **strict JSON format** with the following structure:

{{
    "fields": {{
        "person_names": {{"value": ["John Doe"], "confidence": 0.95}},
        "dates": {{"value": ["25th March"], "confidence": 0.92}},
        "phone_numbers": {{"value": ["(123) 456-7890"], "confidence": 0.98}},
        "loan_ids": {{"value": ["12345"], "confidence": 0.90}},
        "interest_rates": {{"value": ["3.5%"], "confidence": 0.96}},
        "currency_amounts": {{"value": ["$1,200"], "confidence": 0.94}},
        "organizations": {{"value": ["Citizens Bank"], "confidence": 0.93}},
        "bank_account_details": {{"value": ["ABA #: 011500120"], "confidence": 0.90}},
        "bank_name": {{"value": "Citizens Bank NA", "confidence": 0.97}},
        "loan_amount": {{"value": ["$171.3MM"], "confidence": 0.95}}
    }},
    "request_type": {{
        "value": "Lending Services",
        "confidence": 0.94
    }}
}}
"""
)


# Create the LangChain LLM Chain
chain = LLMChain(llm=llm, prompt=prompt_template22)

# Run the pipeline
response = chain.run({"text": text2})

# Parse the JSON output
# try:
#     extracted_fields = json.loads(response)
    
#     #valid_json = pyjson5.loads(response)
#     # Pretty-print the corrected JSON
#     #print(json.dumps(valid_json, indent=2))
#     print(json.dumps(extracted_fields, indent=4))
# except json.JSONDecodeError:
#     print("Invalid JSON format. Raw output:")
#     print(response)


def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)  # Extracts JSON block
    if match:
        return match.group(0).strip()  # Remove extra whitespace
    return text.strip()  # Return original if no match

# ✅ 2. Validate and auto-correct JSON
def validate_and_correct_json(response):
    json_part = extract_json(response)

    try:
        # Try to parse with standard JSON
        valid_json = json.loads(json_part)
        print("\n✅ JSON is valid!")
        print(json.dumps(valid_json, indent=4))
        return valid_json

    except json.JSONDecodeError:
        print("\n❌ Invalid JSON. Trying auto-correction...")

        try:
            # Use pyjson5 for auto-correction
            corrected_json = pyjson5.loads(json_part)
            print("\n🔧 Auto-corrected JSON:")
            print(json.dumps(corrected_json, indent=4))
            return corrected_json

        except Exception as e:
            print(f"\n❌ Could not auto-correct JSON: {e}")
            return None

# ✅ 3. Run validation
validate_and_correct_json(response)

