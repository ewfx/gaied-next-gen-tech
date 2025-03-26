from langchain.prompts import PromptTemplate

def promtsummary():
    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["text"],  # Match this with the chain invocation variable
        template="""
        You are an AI tasked with extracting and summarizing the key information from an email and its PDF attachment.

        ### **Input:**
        {text}

        ### **Task:**
        1. Extract and combine the most important details from the email and PDF attachment into a **concise paragraph**.
        2. Prioritize the following details if present:
            - Loan ID / Reference Number
            - Borrower Name / Organization
            - Loan Type
            - Amount Due / Commitment Amount
            - Due Dates / Adjustment Dates
            - Lender / Loan Agent
            - Key Actions / Notifications
        3. Ensure the paragraph clearly differentiates between the **email content** and the **PDF content**.
        4. Make the summary **3-5 sentences long**, clear, and professional.
        """
    )
    
    return prompt_template
