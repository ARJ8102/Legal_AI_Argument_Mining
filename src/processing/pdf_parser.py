import fitz  # PyMuPDF
import os
import io
from pymongo import MongoClient
from PIL import Image
import pytesseract

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]

# Minimum characters required to consider a page "valid" (otherwise OCR it)
MIN_CHAR_THRESHOLD = 40


def extract_text_from_pdf(pdf_path):
    """Extracts text from PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    page_texts = []

    for page in doc:
        text = page.get_text()
        page_texts.append(text)

    return page_texts


def ocr_page(page):
    """Runs OCR on a single PDF page."""
    pix = page.get_pixmap(dpi=300)
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))

    return pytesseract.image_to_string(img)


def parse_pdf(pdf_path, doc_id):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ File not found: {pdf_path}")

    print(f"📄 Opening PDF: {pdf_path}")
    doc = fitz.open(pdf_path)

    extracted_pages = extract_text_from_pdf(pdf_path)
    final_text = ""
    ocr_used_pages = 0

    print("🔎 Checking pages for OCR fallback...")

    for i, page_text in enumerate(extracted_pages):
        page = doc[i]

        if len(page_text.strip()) < MIN_CHAR_THRESHOLD:
            print(f"⚠️ Page {i+1}: Too little text extracted ({len(page_text)} chars). Running OCR...")
            ocr_text = ocr_page(page)
            final_text += ocr_text + "\n"
            ocr_used_pages += 1
        else:
            final_text += page_text + "\n"

    # Store final text in MongoDB
    documents_collection.update_one(
        {"_id": doc_id},
        {"$set": {"raw_text": final_text}},
        upsert=True
    )

    print(f"\n✅ PDF processed: {doc_id}")
    print(f"📌 OCR used on {ocr_used_pages}/{len(extracted_pages)} pages")
    print("📦 Stored text in MongoDB\n")
