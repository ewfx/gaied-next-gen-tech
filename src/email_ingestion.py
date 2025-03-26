import json
import os
import chardet
import base64
from email import message_from_bytes
from email.policy import default
def fetch_emails():
    with open("data/sample_emails.json", "r") as file:
        emails = json.load(file)
    return emails


def fetch_emails_from_eml(directory="D:/next-gen-tech/gaied-next-gen-tech/data/"):
    """
    Reads and parses all .eml files in the specified directory, prioritizing by filename order.

    Args:
        directory (str): The folder containing .eml files.

    Returns:
        List[dict]: List of parsed emails with fields like 'subject', 'from', 'to', 'body', and 'attachments'.
    """
    email_list = []

    # Get all .eml files and sort them by filename (prioritization)
    eml_files = [f for f in os.listdir(directory) if f.endswith(".eml")]
    eml_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]) if '_' in x and x.split('_')[1].split('.')[0].isdigit() else float('inf'))

    for filename in eml_files:
        filepath = os.path.join(directory, filename)

        # Read the .eml file with encoding detection
        with open(filepath, "rb") as f:
            raw_data = f.read()

        # Detect encoding
        encoding = chardet.detect(raw_data)['encoding']
        if encoding is None:
            encoding = 'utf-8'  # Fallback encoding

        # Parse the .eml file
        try:
            msg = message_from_bytes(raw_data, policy=default)
        except Exception as e:
            print(f"Error parsing {filename}: {e}")
            continue

        # Extract email details
        email_data = {
            "filename": filename,
            "subject": msg["subject"],
            "from": msg["from"],
            "to": msg["to"],
            "body": "",
            "attachments": []
        }

        # Extract the body and attachments
        for part in msg.walk():
            content_type = part.get_content_type()

            # Extract the body
            if content_type in ["text/plain", "text/html"]:
                try:
                    email_data["body"] += part.get_payload(decode=True).decode(encoding, errors="ignore")
                except Exception as e:
                    print(f"Error decoding body in {filename}: {e}")

            # Extract attachments
            if part.get_content_disposition() == "attachment":
                attachment_filename = part.get_filename()
                if attachment_filename:
                    binary_data = part.get_payload(decode=True)

                    # Base64 encoding to make it JSON serializable
                    encoded_data = base64.b64encode(binary_data).decode('utf-8')

                    attachment_data = {
                        "filename": attachment_filename,
                        "content_type": content_type,
                        "data": encoded_data  # Store as Base64 string
                    }
                    email_data["attachments"].append(attachment_data)

        # Skip empty or invalid emails
        if email_data["subject"] or email_data["from"] or email_data["to"] or email_data["body"]:
            # Avoid duplicate appending
            if email_data not in email_list:
                email_list.append(email_data)
            else:
                print(f"Duplicate email skipped: {filename}")
        else:
            print(f"Empty or invalid email skipped: {filename}")

    # Display output nicely formatted
    # print(json.dumps(email_list, indent=4))

    return email_list


# def fetch_emails_from_eml(directory="D:/next-gen-tech/gaied-next-gen-tech/data/"):
#     """
#     Reads and parses all .eml files in the specified directory.

#     Args:
#         directory (str): The folder containing .eml files.

#     Returns:
#         List[dict]: List of parsed emails with fields like 'subject', 'from', 'to', 'body', and 'attachments'.
#     """
#     email_list = []

#     # Iterate through all .eml files in the directory
#     for filename in os.listdir(directory):
#         if filename.endswith(".eml"):
#             filepath = os.path.join(directory, filename)

#             # Read the .eml file with encoding detection
#             with open(filepath, "rb") as f:
#                 raw_data = f.read()

#             # Detect encoding
#             encoding = chardet.detect(raw_data)['encoding']
#             if encoding is None:
#                 encoding = 'utf-8'  # Fallback encoding

#             # Parse the .eml file
#             try:
#                 msg = message_from_bytes(raw_data, policy=default)
#             except Exception as e:
#                 print(f"Error parsing {filename}: {e}")
#                 continue

#             # Extract email details
#             email_data = {
#                 "filename": filename,
#                 "subject": msg["subject"],
#                 "from": msg["from"],
#                 "to": msg["to"],
#                 "body": "",
#                 "attachments": []
#             }

#             # Extract the body and attachments
#             for part in msg.walk():
#                 content_type = part.get_content_type()

#                 # Extract the body
#                 if content_type in ["text/plain", "text/html"]:
#                     try:
#                         email_data["body"] += part.get_payload(decode=True).decode(encoding, errors="ignore")
#                     except Exception as e:
#                         print(f"Error decoding body in {filename}: {e}")

#                 # Extract attachments
#                 if part.get_content_disposition() == "attachment":
#                     attachment_filename = part.get_filename()
#                     #print("attachment file name"+attachment_filename)
#                     if attachment_filename:
#                         binary_data = part.get_payload(decode=True)
                        
#                         #  Base64 encoding to make it JSON serializable
#                         encoded_data = base64.b64encode(binary_data).decode('utf-8')

#                         attachment_data = {
#                             "filename": attachment_filename,
#                             "content_type": content_type,
#                             "data": encoded_data  # Store as Base64 string
#                         }
#                         email_data["attachments"].append(attachment_data)

#             #  Skip empty or invalid emails
#             if email_data["subject"] or email_data["from"] or email_data["to"] or email_data["body"]:
#                 #  Avoid duplicate appending
#                 if email_data not in email_list:
#                     email_list.append(email_data)
#                 else:
#                     print(f"Duplicate email skipped: {filename}")
#             else:
#                 print(f"Empty or invalid email skipped: {filename}")

#     #  Display output nicely formatted
#     #print(json.dumps(email_list, indent=4))
    
#     return email_list