import json
import imaplib
import email
from email import policy
import base64

def load_emails():
    with open('data/sample_emails.json', 'r') as file:
        return json.load(file)

def save_extracted_data(data):
    with open('data/extracted_data.json', 'w') as file:
        json.dump(data, file, indent=4)

# email_ingestion.py

def fetch_emails():
    # Connect to IMAP Server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("ravindrasingh446@gmail.com", "pwd")
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()

    emails = []
    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1], policy=policy.default)
                subject = msg["subject"]
                sender = msg["from"]
                body = msg.get_payload(decode=True).decode()
                
                emails.append({
                    "sender": sender,
                    "subject": subject,
                    "body": body
                })
    
    mail.logout()
    return emails
