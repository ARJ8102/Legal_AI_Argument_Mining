import fitz  # PyMuPDF
import os
import io
from pymongo import MongoClient
from PIL import Image
import pytesseract

client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]

MIN_CHAR_THRESHOLD = 5


def parse_pdf(pdf_path, doc_id):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ File not found: {pdf_path}")

    print(f"📄 Opening PDF: {pdf_path}")
    doc = fitz.open(pdf_path)

    final_text = ""
    ocr_used_pages = 0

    print("🔎 Checking pages for OCR fallback...")

    for i, page in enumerate(doc):
        text = page.get_text()
        cleaned = text.strip()

        print(f"PAGE {i+1}: extracted length = {len(cleaned)}")

        if len(cleaned) >= MIN_CHAR_THRESHOLD:
            final_text += text + "\n"
            continue

        # OCR fallback
        print(f"⚠️ Page {i+1}: Low text. Using OCR...")
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        ocr_text = pytesseract.image_to_string(img)

        if ocr_text.strip():
            final_text += ocr_text + "\n"
            ocr_used_pages += 1
        else:
            print(f"⚠️ OCR also failed. Keeping original text.")
            final_text += text + "\n"

    if not final_text.strip():
        raise ValueError("PDF parsing returned empty text. Cannot continue.")

    documents_collection.update_one(
        {"_id": doc_id},
        {"$set": {"raw_text": final_text}},
        upsert=True
    )

    print(f"\n✅ PDF processed: {doc_id}")
    print(f"📌 OCR used on {ocr_used_pages}/{len(doc)} pages")
    print("📦 Stored text in MongoDB\n")
