import os

# Set API keys
def get_google_api_key():
    api_key = "AIzaSyArUh6ZcPXDvkA47L7ufrExyC8XUWnZbm4"
    os.environ["GOOGLE_API_KEY"] = api_key
    print("get key"+ os.environ.get("GOOGLE_API_KEY"))
    return os.environ.get("GOOGLE_API_KEY")
