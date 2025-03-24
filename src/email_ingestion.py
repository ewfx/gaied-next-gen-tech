import json

def fetch_emails():
    with open("data/sample_emails.json", "r") as file:
        emails = json.load(file)
    return emails