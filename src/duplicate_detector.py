import hashlib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import hashlib
from sentence_transformers import SentenceTransformer, util
import spacy
import quopri
import re

# Load the model
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-mpnet-base-v2')


# In-memory storage for email deduplication
email_db = {}


#  Decode quoted-printable encoded text
def decode_quoted_printable(text):
    """Decodes quoted-printable encoded text."""
    return quopri.decodestring(text).decode('utf-8')


#  Normalize email body
def normalize_text(text):
    """Removes encoding artifacts and normalizes text."""
    text = decode_quoted_printable(text)
    text = re.sub(r'=\n', '', text)  # Remove line breaks caused by encoding
    text = re.sub(r'=\s*', '', text)  # Remove trailing '='
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text


#  Extract key phrases AFTER normalization
def extract_key_phrases(text, min_length=3):
    """Extracts and normalizes key phrases."""
    doc = nlp(text)
    phrases = [
        chunk.text.lower().strip() for chunk in doc.noun_chunks
        if len(chunk.text) >= min_length and not chunk.text.isspace()
    ]
    return phrases


#  Generate email ID
def generate_email_id(eml_content):
    """
    Generates a unique email ID by hashing the content.
    """
    hash_object = hashlib.sha256(eml_content.encode('utf-8'))
    email_id = hash_object.hexdigest()
    return email_id


#  Compare new email with stored emails
def compare_with_existing(email_id, email_body, threshold=0.85):
    """Compares the new email against stored emails."""

    # Normalize the incoming email body
    normalized_body = normalize_text(email_body)
    new_embedding = model.encode(normalized_body, convert_to_tensor=True)

    for stored_id, record in email_db.items():
        stored_embedding = record['embedding']

        # Fallback to normalize old email bodies
        stored_body = record.get('normalized_body', normalize_text(record['body']))
        
        # Extract key phrases from both emails
        phrases1 = set(extract_key_phrases(normalized_body))
        phrases2 = set(extract_key_phrases(stored_body))

        similarity = util.pytorch_cos_sim(new_embedding, stored_embedding).item()

        if similarity >= threshold:
            common_phrases = phrases1.intersection(phrases2)
            reason = ", ".join(common_phrases) if common_phrases else "No common phrases"

            print(f"Common phrases: {common_phrases}")
            return {
                "duplicate": True,
                "existing_email_id": stored_id,
                "similarity": similarity,
                "reason": reason
            }

    return {
        "duplicate": False,
        "similarity": 0.0,
        "reason": "No match"
    }


#  Store emails in the database with normalized bodies
def store_email(email_id, email_body):
    normalized_body = normalize_text(email_body)
    embedding = model.encode(normalized_body, convert_to_tensor=True)

    email_db[email_id] = {
        "body": email_body,
        "normalized_body": normalized_body,  # Store normalized body for phrase extraction
        "embedding": embedding
    }


# Function to store the email
def store_email(email_id, email_body):
    """Stores the email with its ID, embedding, and body."""
    embedding = model.encode(email_body, convert_to_tensor=True)
    email_db[email_id] = {
        "embedding": embedding,
        "body": email_body
    }
def generate_hash(email_body):
    return hashlib.md5(email_body.encode()).hexdigest()

def check_duplicate(email, existing_hashes):
    email_hash = generate_hash(email['body'])
    return email_hash in existing_hashes, email_hash

# duplicate_detector.py


def detect_duplicates(email_list):
    """
    Detects duplicate emails using hashing.
    """
   

    # Ensure input is a list
    if isinstance(email_list, dict):
        email_list = [email_list]

    # Initialize variables
    existing_hashes = set()
    duplicates = []

    # Extract body content and compute hash
    for email in email_list:
        email_body = email.get('body', '')
        email_hash = hashlib.md5(email_body.encode('utf-8')).hexdigest()

        if email_hash in existing_hashes:
            duplicates.append(True)
        else:
            duplicates.append(False)
            existing_hashes.add(email_hash)

    # Return if the first email is duplicate and the hash
    return duplicates[0], email_hash

