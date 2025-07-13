import spacy
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")  # We'll switch to a legal model later

def extract_named_entities(text):
    doc = nlp(text)
    entities = []

    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    return entities

if __name__ == "__main__":
    input_path = "extracted_text.txt"  # Output of PDF parser

    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
    else:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        named_entities = extract_named_entities(text)

        print("🔎 Named Entities Found:\n")
        for label, ent in named_entities[:100]:  # limit output
            print(f"{label:15} --> {ent}")
