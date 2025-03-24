import fitz  # PyMuPDF
import io
import json
import re

def load_rules(rule_file="rules.json"):
    """Load extraction rules from rules.json."""
    try:
        with open(rule_file, "r") as file:
            rules = json.load(file)
        return rules.get("rules", {})
    except Exception as e:
        print(f"Error loading rules: {str(e)}")
        return {}
    
def extract_numerical_fields(text, numerical_patterns):
    """Extract numerical fields based on patterns from the rules.json."""
    extracted_values = {}

    for field, pattern in numerical_patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            extracted_values[field] = matches

    return extracted_values

def extract_text_from_pdf_bytes(pdf_bytes, rules):
    """Extract and filter PDF text with numerical extraction rules."""
    try:
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")

        extracted_text = ""
        numerical_values = {}

        # Extract all content if rules are disabled
        print("Priority Rules:", json.dumps(rules["priority"], indent=4))
        print("Extraction Rules:", json.dumps(rules["extraction"], indent=4))
        print("Disable Rules:", rules.get("disable_rules", False))
        if rules.get("disable_rules", False):
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                extracted_text += page.get_text()

            return extracted_text.strip(), {}

        # Apply rules if not disabled
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()

            # Apply numerical field extraction rules
            if rules.get("extraction", {}).get("numerical_fields_from_attachments", False):
                numerical_values.update(
                    extract_numerical_fields(page_text, rules["extraction"]["numerical_patterns"])
                )

            extracted_text += page_text

        # Return both the extracted text and numerical values
        return extracted_text.strip(), numerical_values

    except Exception as e:
        print(f"Error extracting PDF text: {str(e)}")
        return "", {}

# def extract_text_from_pdf_bytes(pdf_bytes):
#     """Extracts text from PDF bytes."""
#     try:
#         pdf_stream = io.BytesIO(pdf_bytes)
#         pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")

#         text = ""
#         for page_num in range(len(pdf_document)):
#             page = pdf_document.load_page(page_num)
#             text += page.get_text()

#         return text.strip()

#     except Exception as e:
#         print(f"Error extracting PDF text: {str(e)}")
#         return ""
