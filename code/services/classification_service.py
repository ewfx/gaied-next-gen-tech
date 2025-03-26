from langchain_google_genai import ChatGoogleGenerativeAI

def classify_email(email_body, model):
    response = model.generate_content(email_body)
    return response.text