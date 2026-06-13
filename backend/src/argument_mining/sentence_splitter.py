import nltk
nltk.download('punkt')
nltk.download('punkt_tab')  # Add this line

import os
import nltk

# Force NLTK to download to a writable directory
nltk_data_dir = "/tmp/nltk_data"
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.insert(0, nltk_data_dir)
nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)
nltk.download('punkt_tab', download_dir=nltk_data_dir, quiet=True)

from nltk.tokenize import sent_tokenize
from pymongo import MongoClient

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URI)

db = client["legal_pipeline"]
sentences_collection = db["sentences"]
cases_collection = db["cases"]


def split_sentences_for_doc(doc_id):
    doc = cases_collection.find_one({"_id": doc_id})
    text = doc.get("raw_text", "") if doc else ""

    if not text:
        print(f"No raw_text found for doc_id={doc_id}")
        return []

    sentences = sent_tokenize(text)

    sentences_collection.update_one(
        {"_id": doc_id},
        {"$set": {"sentences": sentences}},
        upsert=True
    )

    print(f"Split {len(sentences)} sentences for document _id={doc_id}")
    return sentences


def get_sentences(doc_id):
    record = sentences_collection.find_one({"_id": doc_id})
    return record.get("sentences", []) if record else []