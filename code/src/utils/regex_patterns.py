PATTERNS = {
    "phone_number": r"\(\d{3}\) \d{3}-\d{4}",
    "loan_id": r"(Loan ID\s*[\d]+)",
    "interest_rate": r"(\d+(\.\d+)?%)",
    "date": r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b\s\d{1,2},?\s\d{4}",
    "amount_due": r"\b(?:payment\s*of|amount\s*due)\s*[:\-]?\s*([$€£]?\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\b",
    "loan_officer": r"\b(?:Loan Officer|Contact)\s*[:\-]?\s*([A-Z][a-z]+\s[A-Z][a-z]+)\b",
    "contact_number": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
}
