from langchain.prompts import PromptTemplate

def promtextract():
    # Define the prompt template
    prompt_template = PromptTemplate(
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

        **Exclude fields that are missing or empty.**
        Only include fields with extracted values.

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

        ### **4. Detect and Assign Primary Intent**
        - Identify all individual requests in the conversation thread.
        - Group related emails by **id or thread_id** (if available).
        - Analyze the entire context of the thread.
        - Determine the **primary intent** of the conversation by considering the initiating request and the overall context.
        - Assign the **primary intent** category with a **confidence score** and a **reason**.
        """
     )
    
    return promtextract
