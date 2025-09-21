# run_pipeline.py

import sys
import os

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Now you can import your modules
from processing import pdf_parser, ocr_test
from nlp import ner_extractor
from argument_mining import sentence_splitter, arg_classifier

from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]

# ... rest of your pipeline code remains the same

def run_pipeline(file_path, file_type="pdf", ner_source="huggingface"):
    """
    Run the full pipeline on a document.
    
    Args:
        file_path (str): Path to PDF or image file
        file_type (str): "pdf" or "image"
        ner_source (str): "huggingface" or "spacy"
    """
    doc_id = os.path.basename(file_path)

    # Step 1: Extract raw text
    if file_type.lower() == "pdf":
        pdf_parser.parse_pdf(file_path, doc_id=doc_id)
    elif file_type.lower() == "image":
        ocr_test.ocr_image(file_path, doc_id=doc_id)
    else:
        raise ValueError("file_type must be 'pdf' or 'image'")

    # Step 2: Named Entity Recognition
    ner_extractor.extract_entities(doc_id, source=ner_source)

    # Step 3: Sentence Splitting
    sentence_splitter.split_sentences(doc_id)

    # Step 4: Argument Classification
    arg_classifier.classify_sentences(doc_id)

    print(f"\n✅ Pipeline completed for {file_path} (doc_id={doc_id})")


# Standalone run
if __name__ == "__main__":
    # Example usage
    sample_pdf = "uspdf.pdf"
    run_pipeline(sample_pdf, file_type="pdf", ner_source="huggingface")

    # For images:
    # sample_img = "scanned_doc.png"
    # run_pipeline(sample_img, file_type="image", ner_source="spacy")
