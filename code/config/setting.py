import os

# Set API keys

def get_google_api_key():
    api_key = ""
    os.environ["GOOGLE_API_KEY"] = api_key
    print("get key"+ os.environ.get("GOOGLE_API_KEY"))
    return os.environ.get("GOOGLE_API_KEY")
