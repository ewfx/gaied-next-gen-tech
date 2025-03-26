from langchain.chains import LLMChain
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from config.promt_summarzing import promtsummary
from config.setting import get_google_api_key


# Set API Key from function
os.environ["GOOGLE_API_KEY"] = get_google_api_key()
#print("key "+get_google_api_key())
# Initialize the LLM model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)

# Use the corrected prompt template
prompt_instance = promtsummary()
chain = LLMChain(llm=llm, prompt=prompt_instance)

def classify_email(email_body):
    # Invoke the chain with the corrected input variable name
    response = chain.invoke({"text": email_body})  

    # Extract and return the content
    if response and 'text' in response:
        return response['text']  
    else:
        return "No content received"