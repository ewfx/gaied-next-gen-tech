def map_ner_labels(ner_results):
    """
    Maps Hugging Face NER labels to custom field names.
    Combines all fields into a single dictionary.
    """
    
    field_mapping = {
        "ORG": "organization",
        "PERSON": "loan_officer",
        "MONEY": "amount_due",
        "DATE": "due_date",
        "PERCENT": "interest_rate",
        "CARDINAL": "loan_id",
        "PHONE": "contact_number",
        "TIME": "time"
    }

    mapped_fields = {}

    for entity in ner_results:
        # ✅ Type check to prevent AttributeError
        if not isinstance(entity, dict):
            print(f"Skipping invalid entity: {entity}")
            continue

        label = entity.get('entity_group') or entity.get('label', 'UNKNOWN')
        text = entity.get('word', '').replace(' ##', '')

        field_name = field_mapping.get(label, label.lower())

        if field_name in mapped_fields:
            if isinstance(mapped_fields[field_name], list):
                mapped_fields[field_name].append(text)
            else:
                mapped_fields[field_name] = [mapped_fields[field_name], text]
        else:
            mapped_fields[field_name] = text

    return mapped_fields
