# sentence_splitter.py
import nltk
from nltk.tokenize import sent_tokenize
from pymongo import MongoClient

# Ensure punkt tokenizer is downloaded
nltk.download("punkt")

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]

def split_sentences(doc_id, collection_field="sentences"):
    """
    Fetch raw_text from MongoDB, split into sentences, and store back in the document.
    
    Args:
        doc_id (str): _id of the document in MongoDB
        collection_field (str): field name to store sentence-level data
    """
    doc = documents_collection.find_one({"_id": doc_id})
    if not doc:
        raise ValueError(f"Document with _id={doc_id} not found.")

    text = doc.get("raw_text", "")
    if not text:
        raise ValueError(f"No raw_text found for document _id={doc_id}.")

    # Split into sentences
    sentences = sent_tokenize(text)

    # Prepare sentence-level documents
    sentence_data = []
    for idx, sent in enumerate(sentences):
        sentence_data.append({
            "sentence_id": idx,
            "text": sent,
            "role": None  # to be filled later by argument classifier
        })

    # Store in MongoDB
    documents_collection.update_one(
        {"_id": doc_id},
        {"$set": {collection_field: sentence_data}}
    )

    print(f"✅ Split {len(sentences)} sentences for document _id={doc_id}")
    return sentence_data


# Standalone test
if __name__ == "__main__":
    test_doc_id = "sample.pdf"  # must exist in MongoDB
    split_sentences(test_doc_id)
