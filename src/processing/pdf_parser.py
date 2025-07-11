import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

# Set path to Tesseract (update if yours is different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def is_text_based(page):
    """Check if page contains selectable text."""
    return bool(page.get_text().strip())

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for i, page in enumerate(doc):
        print(f"Processing page {i+1}...")

        if is_text_based(page):
            text = page.get_text()
            full_text += f"\n--- Page {i+1} (Text) ---\n{text}\n"
        else:
            # Page is likely scanned, convert to image for OCR
            pix = page.get_pixmap(dpi=300)
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))

            text = pytesseract.image_to_string(image)
            full_text += f"\n--- Page {i+1} (OCR) ---\n{text}\n"

    return full_text

def save_text(output_path, text):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    input_pdf = "uspdf.pdf"  # replace with your PDF path
    output_txt = "extracted_text.txt"

    if not os.path.exists(input_pdf):
        print(f"❌ File not found: {input_pdf}")
    else:
        extracted = extract_text_from_pdf(input_pdf)
        save_text(output_txt, extracted)
        print(f"✅ Extraction complete! Text saved to {output_txt}")
