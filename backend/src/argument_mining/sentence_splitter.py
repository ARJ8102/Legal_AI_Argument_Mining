import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from pymongo import MongoClient
import os

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URI)

db = client["legal_pipeline"]
sentences_collection = db["sentences"]
cases_collection = db["cases"]  # Fix: was "documents", should be "cases"


def split_sentences_for_doc(doc_id):
    doc = cases_collection.find_one({"_id": doc_id})  # Fix: read from cases
    text = doc.get("raw_text", "") if doc else ""

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