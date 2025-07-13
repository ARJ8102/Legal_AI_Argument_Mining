from transformers import pipeline

def extract_legal_entities(text):
    ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
    entities = ner(text)
    return entities

if __name__ == "__main__":
    input_path = "extracted_text.txt"
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    entities = extract_legal_entities(text)

    print("\n🔍 Named Entities Found:\n")
    for ent in entities:
        print(f"{ent['entity_group']:12} → {ent['word']}")
