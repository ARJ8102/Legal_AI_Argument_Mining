from transformers import pipeline
from pymongo import MongoClient
import numpy as np

client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
entities_collection = db["entities"]

NER_MODEL = "dslim/bert-base-NER"

print(f"🔍 Loading HuggingFace NER model: {NER_MODEL}")
ner_pipeline = pipeline("ner", model=NER_MODEL, aggregation_strategy="simple")


def clean_numpy(o):
    if isinstance(o, np.float32):
        return float(o)
    return o


def extract_entities(text, doc_id):
    if not text or text.strip() == "":
        raise ValueError("NER received empty text")

    ents = ner_pipeline(text)
    cleaned_ents = [{k: clean_numpy(v) for k, v in e.items()} for e in ents]

    entities_collection.update_one(
        {"_id": doc_id},
        {"$set": {"entities": cleaned_ents}},
        upsert=True
    )

    print(f"✅ Extracted {len(cleaned_ents)} entities for {doc_id}")
    return cleaned_ents


def get_entities(doc_id):
    rec = entities_collection.find_one({"_id": doc_id})
    return rec.get("entities", []) if rec else []
