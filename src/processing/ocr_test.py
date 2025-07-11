import pytesseract
from PIL import Image

# Update this path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image_path = 'testocr.png'  # Put your test image here
image = Image.open(image_path)

text = pytesseract.image_to_string(image)

print("Extracted Text:\n", text)
