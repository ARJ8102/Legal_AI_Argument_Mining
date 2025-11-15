from transformers import pipeline
from pymongo import MongoClient
import numpy as np

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]

# Working default NER model
NER_MODEL = "dslim/bert-base-NER"

print(f"🔍 Loading HuggingFace NER model: {NER_MODEL}")

# Load HuggingFace NER pipeline
ner_pipeline = pipeline(
    "ner",
    model=NER_MODEL,
    aggregation_strategy="simple",
)

def clean_value(v):
    """Convert numpy types to Python native types so MongoDB accepts them."""
    if isinstance(v, (np.float32, np.float64)):
        return float(v)
    if isinstance(v, (np.int32, np.int64)):
        return int(v)
    return v

def extract_entities(text, doc_id):
    """Run NER on text and store the results in MongoDB."""
    if not text or text.strip() == "":
        raise ValueError("❌ NER received empty text input!")

    print(f"🔎 Running NER on document: {doc_id}")
    raw_entities = ner_pipeline(text)

    # Convert to MongoDB-safe objects
    entities = []
    for ent in raw_entities:
        clean_ent = {
            "entity_group": clean_value(ent.get("entity_group")),
            "word": clean_value(ent.get("word")),
            "start": clean_value(ent.get("start")),
            "end": clean_value(ent.get("end")),
            "score": clean_value(ent.get("score")),
        }
        entities.append(clean_ent)

    # Save results in MongoDB
    documents_collection.update_one(
        {"_id": doc_id},
        {"$set": {"entities": entities}},
        upsert=True
    )

    print(f"✅ Extracted {len(entities)} entities for {doc_id}")



def get_entities(doc_id):
    doc = documents_collection.find_one({"_id": doc_id})
    return doc.get("entities", [])
