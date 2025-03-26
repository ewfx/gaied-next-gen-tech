# Field mapping with rules
request_type_rules = {
    "Commitment Change": {
        "fields": ["person_names", "loan_ids", "phone_numbers", "currency_amounts"]
    },
    "Adjustment": {
        "fields": ["loan_ids", "currency_amounts", "document_types", "bank_names"]
    }
}
