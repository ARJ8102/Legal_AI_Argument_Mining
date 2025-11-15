import fitz
import os
import io
from pymongo import MongoClient
from PIL import Image
import pytesseract

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]

MIN_CHAR_THRESHOLD = 40


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return [page.get_text() for page in doc]


def ocr_page(page):
    pix = page.get_pixmap(dpi=300)
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))
    return pytesseract.image_to_string(img)


def parse_pdf(pdf_path, doc_id):
    print(f"📄 Opening PDF: {pdf_path}")
    doc = fitz.open(pdf_path)

    extracted_pages = extract_text_from_pdf(pdf_path)
    final_text = ""
    ocr_used = 0

    print("🔎 Checking pages for OCR fallback...")
    for i, ptext in enumerate(extracted_pages):
        page = doc[i]

        if len(ptext.strip()) < MIN_CHAR_THRESHOLD:
            print(f"⚠️ Page {i+1}: Running OCR...")
            final_text += ocr_page(page) + "\n"
            ocr_used += 1
        else:
            final_text += ptext + "\n"

    documents_collection.update_one(
        {"_id": doc_id},
        {"$set": {"raw_text": final_text}},
        upsert=True
    )

    print(f"📌 OCR used on {ocr_used}/{len(extracted_pages)} pages")
    print(f"📦 Stored text in MongoDB\n")


def get_raw_text(doc_id):
    doc = documents_collection.find_one({"_id": doc_id})
    if not doc or "raw_text" not in doc:
        return ""
    return doc["raw_text"]
