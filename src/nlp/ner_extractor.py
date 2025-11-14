from transformers import pipeline
from pymongo import MongoClient
import torch

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]

print("🔍 Loading HuggingFace NER model: dslim/bert-base-NER")

device = 0 if torch.cuda.is_available() else -1

ner_pipeline = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple",
    device=device
)

def extract_entities(doc_id):
    doc = documents_collection.find_one({"_id": doc_id})

    if not doc or "raw_text" not in doc:
        raise ValueError(f"No text found for document {doc_id}")

    text = doc["raw_text"]

    print(f"🔎 Running NER on document: {doc_id}")

    ents = ner_pipeline(text)

    # Store CLEAN output
    clean_entities = [
        {"text": ent["word"], "label": ent["entity_group"]}
        for ent in ents
    ]

    documents_collection.update_one(
        {"_id": doc_id},
        {"$set": {"entities": clean_entities}}
    )

    print(f"✅ Extracted {len(clean_entities)} entities for {doc_id}")
