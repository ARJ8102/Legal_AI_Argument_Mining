import nltk
from nltk.tokenize import sent_tokenize
from pymongo import MongoClient

nltk.download("punkt")

client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]

def split_sentences_for_doc(doc_id):
    doc = documents_collection.find_one({"_id": doc_id})
    if not doc or "raw_text" not in doc:
        raise ValueError(f"No text found for document {doc_id}")

    sentences = sent_tokenize(doc["raw_text"])

    # Store sentences in MongoDB
    documents_collection.update_one(
        {"_id": doc_id},
        {"$set": {"sentences": [{"sentence_id": i, "text": s} for i, s in enumerate(sentences)]}}
    )
    print(f"✅ Split {len(sentences)} sentences for document _id={doc_id}")
