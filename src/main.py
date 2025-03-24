import json
import multiprocessing
import sys
import os
import logging
import traceback
from fastapi import FastAPI, HTTPException
from src.pdf_extractor import load_rules
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
    from src.duplicate_detector import detect_duplicates
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
    try:
        emails = fetch_emails()
        if not emails:
            logger.info("No emails fetched.")
            return {"message": "No emails to process."}

        extracted_data = []
        existing_hashes =  set()  #  Use a set for unique hashes

        for email in emails:
            try:
                is_duplicate_email = False 
                #  Early duplicate detection before classification & extraction
                is_duplicate, email_hash = detect_duplicates(email)
                
                 # Create email_data object before continuing
                email_data = {
                    "email_id": email['id'],
                    "classification": "",
                    "fields": {},
                    "duplicate": False
                }

                #  Skip duplicate emails immediately
                if email_hash in existing_hashes or is_duplicate:
                    logger.info(f"Skipping duplicate email: {email['id']}")
                    is_duplicate_email = True  #  Mark as duplicate
                    is_duplicate_email = True  #  Mark as duplicate
                    email_data["duplicate"] = True  # Mark it as duplicate
                    extracted_data.append(email_data)  # Add it to the output
                    continue  
                
                #  Add unique hash to the set
                print("existing hash"+email_hash)
                existing_hashes.add(email_hash)
 
                pdf_text=""
                numerical_fields = {}
                 #  Extract PDF text from attachments
                if "attachments" in email:
                    for attachment in email["attachments"]:
                        pdf_path = attachment.get("path")
                        
                        # Process all attachments when rules are disabled
                        allowed_types = rules["extraction"]["attachment_types"]
                        print("Allowed rules: " + str(allowed_types))  
                        if rules.get("disable_rules", False) or (
                            pdf_path and any(pdf_path.endswith(ext) for ext in allowed_types)
                        ):
                            try:
                                with open(pdf_path, "rb") as f:
                                    pdf_bytes = f.read()

                                # Extract all content if rules are disabled
                                pdf_content, pdf_numerical = extract_text_from_pdf_bytes(pdf_bytes, rules)
                                print("extract content")
                                if pdf_content:
                                    pdf_text += f"\n[PDF Attachment Text]\n{pdf_content}"

                                    # Only add numerical fields if rules are enabled
                                    if not rules.get("disable_rules", False):
                                        numerical_fields.update(pdf_numerical)

                            except Exception as e:
                                logger.error(f"Failed to extract PDF {pdf_path}: {str(e)}")
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

                # Classification and Extraction
                classification = classify_email(combined_text)
                
                dynamic_fields = extract_fields(combined_text)

                # Include numerical fields only if rules are enabled
                if not rules.get("disable_rules", False):
                    dynamic_fields.update(numerical_fields)

                is_duplicate, email_hash = detect_duplicates(email)
                logger.info(f"Duplicate: {is_duplicate}, Hash: {email_hash}")

                # if not is_duplicate:
                #     email_data = {
                #         "email_id": email['id'],
                #         "classification": classification,
                #         "fields": dynamic_fields,
                #         "duplicate": is_duplicate
                #     }
                email_data = {
                    "email_id": email['id'],
                    "classification": classification,
                    "fields": dynamic_fields,
                    "duplicate": is_duplicate_email
                }
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
    

# Ensure the server is only started in the main process
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)