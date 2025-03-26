import hashlib
import re
import spacy
import redis
from sentence_transformers import SentenceTransformer, util
import uuid

# Load NLP and Sentence Transformer models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-mpnet-base-v2')

# Redis connection setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)
def clear_redis_cache():
    """
    Clears all email-related data from Redis.
    """
    # Remove all email hashes
    hashes = redis_client.smembers(HASH_SET_KEY)

    # Delete all metadata associated with the hashes
    for h in hashes:
        redis_client.delete(f"{EMAIL_META_PREFIX}{h.decode('utf-8')}")
    
    # Clear the hash set itself
    redis_client.delete(HASH_SET_KEY)
# Constants
HASH_SET_KEY = "email_hashes"
EMAIL_META_PREFIX = "email_meta:"
THRESHOLD = 0.85

### ✅ Step 1: Helper Functions
def generate_hash(email_body):
    """Generate MD5 hash for email body."""
    return hashlib.md5(email_body.encode()).hexdigest()

def extract_key_phrases(text, min_length=3):
    """Extract key phrases and entities."""
    doc = nlp(text)
    phrases = {chunk.text.lower().strip() for chunk in doc.noun_chunks if len(chunk.text) >= min_length}
    entities = {ent.text.lower().strip() for ent in doc.ents if len(ent.text) >= min_length}
    
    # ✅ Extract financial & lending-related patterns
    loan_amounts = set(re.findall(r'\b(?:USD|EUR|GBP)?[\s]*[0-9,]+(?:\.\d{1,2})?\b', text))
    dates = set(re.findall(r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s\w+\s\d{4})\b', text))

    # ✅ Extract financial terms & industry-specific keywords
    financial_terms = {
        "loan", "interest", "principal", "payment", "repayment", 
        "SOFR", "LIBOR", "due date", "balance", "outstanding amount",
        "term loan", "lending rate", "credit facility", "loan agreement",
        "remittance", "fixed income", "variable rate", "maturity date"
    }
    
    # ✅ Extract custom keywords from text
    custom_keywords = {word for word in text.lower().split() if word in financial_terms}

    # ✅ Combine all extracted entities
    extracted_phrases = phrases.union(entities, loan_amounts, dates, custom_keywords)
    #print("phrases" +str(phrases))
    #print("entities"+str(entities))
    return phrases, entities

def store_email(email_id, email_body, email_hash, embedding):
    """Store email details in Redis."""
    redis_client.sadd(HASH_SET_KEY, email_hash)
    metadata = {
        "id": email_id,
        "body": email_body,
        "embedding": ','.join(map(str, embedding.tolist()))
    }
    redis_client.hset(f"{EMAIL_META_PREFIX}{email_hash}", mapping=metadata)

def get_stored_emails():
    """Retrieve all stored emails from Redis."""
    emails = []
    hashes = redis_client.smembers(HASH_SET_KEY)

    for h in hashes:
        h = h.decode('utf-8')
        metadata = redis_client.hgetall(f"{EMAIL_META_PREFIX}{h}")

        if metadata:
            email_id = metadata.get(b'id', b'').decode('utf-8')
            email_body = metadata.get(b'body', b'').decode('utf-8')
            embedding = list(map(float, metadata.get(b'embedding', b'').decode('utf-8').split(',')))
            
            emails.append({
                "id": email_id,
                "body": email_body,
                "embedding": embedding
            })

    return emails

def generate_email_id():
    """Generate a unique email ID."""
    return str(uuid.uuid4()).replace('-', '')

### ✅ Step 2: Simplified Duplicate Detection
def detect_duplicate(email_body):
    """Detect if the email is a duplicate or unique."""
    email_id = generate_email_id()
    email_hash = generate_hash(email_body)
    new_embedding = model.encode(email_body, convert_to_tensor=True)
    phrases, entities = extract_key_phrases(email_body)

    # ✅ Exact Hash Match
    if redis_client.sismember(HASH_SET_KEY, email_hash):
        return {
            "email_id": email_id,
            "duplicate": True,
            "matched_email_id": email_id,
            "similarity": 1.0,
            "reason": "Exact match (identical email)"
        }

    # ✅ Near-Duplicate Detection
    for stored_email in get_stored_emails():
        stored_embedding = stored_email['embedding']
        stored_phrases, stored_entities = extract_key_phrases(stored_email['body'])

        # Phrase-based match
        if phrases.intersection(stored_phrases) or entities.intersection(stored_entities):
            return {
                "email_id": email_id,
                "duplicate": True,
                "matched_email_id": stored_email['id'],
                "similarity": 1.0,
                "reason": "Key phrases or entities match"
            }

        # Semantic similarity check
        similarity = util.pytorch_cos_sim(new_embedding, stored_embedding).item()

        if similarity >= THRESHOLD:
            return {
                "email_id": email_id,
                "duplicate": True,
                "matched_email_id": stored_email['id'],
                "similarity": similarity,
                "reason": "Semantic similarity"
            }

    # ✅ Store new email
    store_email(email_id, email_body, email_hash, new_embedding)

    return {
        "email_id": email_id,
        "duplicate": False,
        "matched_email_id": None,
        "similarity": 0.0,
        "reason": "Unique email stored"
    }

### ✅ Step 3: Main Processing Function
def process_emails(emails):
    """Process multiple emails and return a simplified JSON response."""
    results = []

    for email in emails:
        result = detect_duplicate(email)
        results.append(result)

    return {
        "message": "Emails processed successfully",
        "data": results
    }

