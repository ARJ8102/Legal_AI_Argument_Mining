import os
import sys
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

# ===== FIX PYTHON PATH =====
# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

for path in [PROJECT_ROOT, SRC_PATH]:
    if path not in sys.path:
        sys.path.insert(0, path)

# ===== NOW IMPORT PIPELINE MODULES =====
from processing import pdf_parser
from nlp import ner_extractor
from argument_mining import sentence_splitter, arg_classifier

# ===== FASTAPI APP =====
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Legal AI backend is running"}


@app.post("/process_pdf")
async def process_pdf(file: UploadFile = File(...)):

    try:
        # Save file temporarily
        save_path = f"uploaded_{file.filename}"
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        doc_id = file.filename

        # Step 1 — Parse PDF
        pdf_parser.parse_pdf(save_path, doc_id=doc_id)

        # Step 2 — Get raw text from DB
        raw_text = sentence_splitter.get_raw_text(doc_id)

        # Step 3 — Run NER
        ner_extractor.extract_entities(text=raw_text, doc_id=doc_id)

        # Step 4 — Sentence Split
        sentence_splitter.split_sentences_for_doc(doc_id)

        # Step 5 — Argument Mining
        arg_classifier.classify_sentences(doc_id)

        # Fetch results from MongoDB
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017/")
        db = client["legal_pipeline"]
        doc = db["documents"].find_one({"_id": doc_id})

        return {
            "status": "success",
            "filename": file.filename,
            "results": {
                "entities": doc.get("entities", []),
                "sentences": doc.get("sentences", []),
                "classification": doc.get("argument_labels", []),
            }
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)},
        )
