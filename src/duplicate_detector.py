import hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import hashlib
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

