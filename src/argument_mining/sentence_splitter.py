import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
sentences_collection = db["sentences"]
documents_collection = db["documents"]


def split_sentences_for_doc(doc_id):
    doc = documents_collection.find_one({"_id": doc_id})
    text = doc.get("raw_text", "") if doc else ""

    sentences = sent_tokenize(text)

    sentences_collection.update_one(
        {"_id": doc_id},
        {"$set": {"sentences": sentences}},
        upsert=True
    )

    print(f"✅ Split {len(sentences)} sentences for document _id={doc_id}")


def get_sentences(doc_id):
    record = sentences_collection.find_one({"_id": doc_id})
    return record.get("sentences", []) if record else []
