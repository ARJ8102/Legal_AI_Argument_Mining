import pytesseract
from PIL import Image
from pymongo import MongoClient
import os

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
collection = db["documents"]

def ocr_image(image_path, doc_id=None):
    """Runs OCR on an image file and stores text in MongoDB."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ File not found: {image_path}")

    text = pytesseract.image_to_string(Image.open(image_path))

    if not doc_id:
        doc_id = os.path.basename(image_path)

    # Save into MongoDB
    collection.update_one(
        {"_id": doc_id},
        {"$set": {"raw_text": text, "source": image_path}},
        upsert=True
    )

    print(f"✅ Stored OCR text in MongoDB with _id={doc_id}")
    return doc_id


if __name__ == "__main__":
    sample_img = "scanned_doc.png"
    ocr_image(sample_img)
