import base64
import json
import multiprocessing
import sys
import os
import logging
import tempfile
import traceback
from fastapi import FastAPI, HTTPException
from rules import requesttype
from src.duplicate_detector import  clear_redis_cache, detect_duplicate, generate_email_id
from src.email_ingestion import fetch_emails_from_eml
from src.pdf_extractor import load_rules
from rules.requesttype import request_type_rules
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("email_pipeline")
# Enable CORS


# Load Rules
rules = load_rules("rules/priority_rules.json")
# Add the source directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set multiprocessing start method for Windows
if sys.platform.startswith('win'):
    multiprocessing.set_start_method('spawn', force=True)

# Import modules
try:
    from src.email_ingestion import fetch_emails
    from src.classifier import classify_email
    from src.extractor import extract_fields
    from src.extractor import extract_dynamic_fields
    from services.email_service import save_extracted_data
    from src.pdf_extractor import extract_text_from_pdf_bytes
except ImportError as e:
    logger.error(f"ImportError: {str(e)}")
    logger.error(traceback.format_exc())
    raise HTTPException(status_code=500, detail=f"Module Import Error: {str(e)}")

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
@app.get("/")
def read_root():
    return {"message": "Email AI Pipeline is running"}

@app.get("/process-emails")
def process_emails():
    logger.info("Starting email processing...")
    clear_redis_cache()
    try:
        directory = "D:/next-gen-tech/gaied-next-gen-tech/data/emails"
        emails = fetch_emails_from_eml()
        if not emails:
            logger.info("No emails fetched.")
            return {"message": "No emails to process."}

        extracted_data = []
        existing_hashes =  set()  #  Use a set for unique hashes

        for email in emails:
            try:
                 # Create email_data object before continuing
                email_data = {
                    "classification": {},
                    "fields": {},
                    "duplicate": False,
                    "matched_email_id": None,
                    "similarity": None,
                }

 
                pdf_text=""
                numerical_fields = {}
                 #  Extract PDF text from attachments
                if "attachments" in email:
                    for attachment in email["attachments"]:
                      try:
                         # Decode Base64 data
                         binary_data = base64.b64decode(attachment["data"])
                         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                          tmp_file.write(binary_data)
                          tmp_file_path = tmp_file.name

                        # Process all attachments when rules are disabled
                         allowed_types = rules["extraction"]["attachment_types"]  
                         if rules.get("disable_rules", False) or tmp_file_path.endswith(tuple(allowed_types)):
                                with open(tmp_file_path, "rb") as f:
                                    pdf_bytes = f.read()
                                pdf_content, pdf_numerical = extract_text_from_pdf_bytes(pdf_bytes, rules)
                                if pdf_content:
                                    pdf_text += f"\n[PDF Attachment Text]\n{pdf_content}"
                                    if not rules.get("disable_rules", False):
                                        numerical_fields.update(pdf_numerical)

                            # Clean up temp file
                         os.remove(tmp_file_path)

                      except Exception as e:
                            logger.error(f"Failed to process PDF: {str(e)}")
                            logger.error(traceback.format_exc())

                # Apply content prioritization rules
                use_email_body = rules["priority"]["email_body_over_attachments"]
                fallback = rules["priority"]["fallback_to_attachments"]

                # Disable all rules: use all content
                if rules.get("disable_rules", False):
                    combined_text = email['body'] + "\n" + pdf_text
                else:
                    # Prioritize email body
                    if use_email_body or not pdf_text:
                        combined_text = email['body']
                        if pdf_text and fallback:
                            combined_text += f"\n{pdf_text}"
                    else:
                        combined_text = pdf_text

                email_id=generate_email_id()
                result = detect_duplicate(combined_text)
                if not result["duplicate"]:
                    
                    email_data.update({
                        "classification": classify_email(combined_text),
                        "fields":extract_fields(combined_text),
                        "duplicate": False,
                        "email_id":email_id,
                        "similarity": result["similarity"],
                        "reason": result["reason"]
                    })
                else:
                    email_data.update({
                        "duplicate": True,
                        "similarity": result["similarity"],
                        "reason": result["reason"],
                        "matched_email_id": result.get("existing_email_id", None),
                    })
                
                # checking for the request type if under request type we have any field needs to be priority over other fiels
                #data = json.loads(email_data)
                #email = data.get("data", [])[0]
                
                
                request_type = email_data.get("fields", {}).get("request_type")

                if request_type in requesttype.request_type_rules:
                    print("request_type"+ request_type)
                    filterres = extract_by_request_type(email_data, requesttype.request_type_rules)
                    extracted_data.append(filterres)
                else:
                    extracted_data.append(email_data)


            except Exception as e:
                logger.error(f"Error processing email {email.get('id', 'Unknown')}: {str(e)}")
                logger.error(traceback.format_exc())

        save_extracted_data(extracted_data)

        logger.info("Email processing completed.")
        return {"message": "Emails processed successfully", "data": extracted_data}

    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

def extract_by_request_type(email_data, rules):
    """Extract fields based on request type configuration and keep them under 'fields'."""
    try:
        # Extract request type
        request_type = email_data.get("fields", {}).get("request_type", "Unknown")
        
        if request_type not in rules:
            print(f"No rules defined for request type: {request_type}")
            return email_data  # Return the original data if no rule found
            
        # Get allowed fields based on rules
        allowed_fields = rules[request_type]["fields"]
        # Create the result structure
        result = {
            "classification": email_data.get("classification", ""),
            "duplicate": email_data.get("duplicate", False),
            "email_id": email_data.get("email_id", ""),
            "fields": {
                "request_type": email_data["fields"].get("request_type"),
                "sub_request_type": email_data["fields"].get("sub_request_type"),
                "assign_teams": email_data["fields"].get("assign_teams"),
                "confidence_score": email_data["fields"].get("confidence_score")
            }
        }

        # Add only allowed fields
        for field in allowed_fields:
            if field in email_data["fields"]:
                result["fields"][field] = email_data["fields"][field]

        return result

    except Exception as e:
        print(f"Error: {e}")
        return email_data

# Ensure the server is only started in the main process
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)