import re
import pyjson5
import json
import fitz
from scipy import io
import spacy
from transformers import pipeline
from config.promt_extractfield import promtextract
from config.promt_template import promt
from config.setting import get_google_api_key
from src.utils.regex_patterns import PATTERNS
from src.utils.field_mapper import map_ner_labels

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI 
import json
import os

# extractor.py

os.environ["GOOGLE_API_KEY"] = get_google_api_key()
nlp = spacy.load("en_core_web_sm")
# Initialize Gemini AI Model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)
prompt_instance = promt()
prompt_inst=promtextract()




def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)  # Extracts JSON block
    if match:
        return match.group(0).strip()  # Remove extra whitespace
    return text.strip()  # Return original if no match

#   Validate and auto-correct JSON
def validate_and_correct_json(response):
    json_part = extract_json(response)

    try:
        # Try to parse with standard JSON
        valid_json = json.loads(json_part)
        print("\n JSON is valid!")
        #print(json.dumps(valid_json, indent=4))
        return valid_json

    except json.JSONDecodeError:
        print("\n Invalid JSON. Trying auto-correction...")

        try:
            # Use pyjson5 for auto-correction
            corrected_json = pyjson5.loads(json_part)
            print("\n🔧 Auto-corrected JSON:")
            #print(json.dumps(corrected_json, indent=4))
            return corrected_json

        except Exception as e:
            print(f"\n Could not auto-correct JSON: {e}")
            return None
def extract_fields(text):

    chain = LLMChain(llm=llm, prompt=prompt_instance)

    # Run the pipeline
    response = chain.run({"text": text})
    # Extract and validate/correct JSON
    extracted_fields = validate_and_correct_json(response)

    # Ensure a valid JSON structure is always returned
    if extracted_fields is None:
        extracted_fields = {}  # Return empty JSON if invalid

    # Return corrected JSON to main.py
    return extracted_fields
###############################################
def extract_text_from_pdf_bytes(pdf_bytes):
    """Extracts text from PDF bytes."""
    try:
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")

        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        return text.strip()

    except Exception as e:
        print(f"Error extracting PDF text: {str(e)}")
        return ""
    



def extract_dynamic_fields(email_body: str):
    """
    Extracts dynamic fields from the email content using SpaCy NER.
    
    Returns:
        - dict: Field names with their corresponding values and confidence scores.
    """
    if not isinstance(email_body, str):
        raise ValueError(f"Invalid type for email body: {type(email_body)}")

    # Process the content with SpaCy
    doc = nlp(email_body)

    # Dynamic fields dictionary
    dynamic_fields = {}

    for ent in doc.ents:
        field_name = ent.label_.lower()
        field_value = ent.text

        # Confidence score (using SpaCy's scoring is not directly available, so use a default value)
        confidence = 0.90

        # Handle multiple entities of the same type
        if field_name in dynamic_fields:
            if isinstance(dynamic_fields[field_name], list):
                dynamic_fields[field_name].append({"value": field_value, "confidence": confidence})
            else:
                dynamic_fields[field_name] = [
                    {"value": dynamic_fields[field_name], "confidence": confidence},
                    {"value": field_value, "confidence": confidence}
                ]
        else:
            dynamic_fields[field_name] = {"value": field_value, "confidence": confidence}

    return dynamic_fields