from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# --- Add project root to Python path ---
import os, sys
BACKEND_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

sys.path.append(ROOT_DIR)
sys.path.append(SRC_DIR)
sys.path.append(BACKEND_DIR)

# --- Internal imports ---
from routes.cases import router as cases_router
from src.processing import pdf_parser
from src.nlp import ner_extractor
from src.argument_mining import sentence_splitter, arg_classifier


# --- MongoDB ---
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]

# --- FastAPI app setup ---
app = FastAPI()

# Attach routes for CRUD operations
app.include_router(cases_router)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Legal AI backend is running"}


# ---------------------------------------------------------
# PROCESS PDF ENDPOINT
# ---------------------------------------------------------
@app.post("/process_pdf")
async def process_pdf(file: UploadFile = File(...)):
    try:
        # --- Save uploaded PDF ---
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        if not os.path.exists(file_path):
            return {"status": "error", "message": "File not saved properly."}

        # --- Generate doc ID ---
        doc_id = file.filename.replace(".pdf", "")

        # --- Extract PDF text ---
        pdf_text = pdf_parser.parse_pdf(file_path, doc_id)

        if not pdf_text or not isinstance(pdf_text, str) or not pdf_text.strip():
            return {"status": "error", "message": "Failed to extract text from PDF"}

        # --- NLP processing ---
        entities = ner_extractor.extract_entities(pdf_text, doc_id)
        sentences = sentence_splitter.split_sentences_for_doc(doc_id)
        classifications = arg_classifier.classify_sentences(doc_id)

        # --- SAVE EVERYTHING IN ONE COLLECTION ---
        db.cases.update_one(
            {"_id": doc_id},
            {
                "$set": {
                    "filename": file.filename,
                    "raw_text": pdf_text,
                    "entities": entities,
                    "sentences": sentences,
                    "classifications": classifications
                }
            },
            upsert=True
        )

        # --- FINAL SUCCESS RESPONSE ---
        return {
            "status": "success",
            "filename": file.filename,
            "doc_id": doc_id,
            "saved": True
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}