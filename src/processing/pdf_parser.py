import fitz  # PyMuPDF
from pymongo import MongoClient
import os

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
collection = db["documents"]

def parse_pdf(pdf_path, doc_id=None):
    """Extracts text from PDF and stores it in MongoDB."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ File not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        text += page.get_text("text")

    if not doc_id:
        doc_id = os.path.basename(pdf_path)

    # Save into MongoDB
    result = collection.update_one(
        {"_id": doc_id},
        {"$set": {"raw_text": text, "source": pdf_path}},
        upsert=True
    )

    print(f"✅ Stored PDF text in MongoDB with _id={doc_id}")
    return doc_id


if __name__ == "__main__":
    sample_pdf = "sample.pdf"
    parse_pdf(sample_pdf)
