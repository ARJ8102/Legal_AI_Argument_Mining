from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv

import os
import sys
import uuid
import tempfile
import traceback


# ---------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_SRC_DIR = os.path.join(BACKEND_DIR, "src")

sys.path.append(BACKEND_DIR)
sys.path.append(BACKEND_SRC_DIR)


# ---------------------------------------------------------
# ENV + MONGODB
# ---------------------------------------------------------
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URI)
db = client["legal_pipeline"]


# ---------------------------------------------------------
# INTERNAL IMPORTS
# ---------------------------------------------------------
from routes.cases import router as cases_router
from src.processing import pdf_parser
from src.nlp import ner_extractor
from src.argument_mining import sentence_splitter, arg_classifier


# ---------------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------------
app = FastAPI(title="Legal AI Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cases_router)


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------
@app.get("/")
def home():
    return {"message": "Legal AI backend is running"}


# ---------------------------------------------------------
# PROCESS PDF ENDPOINT
# ---------------------------------------------------------
@app.post("/process_pdf")
async def process_pdf(file: UploadFile = File(...)):
    tmp_path = None

    try:
        doc_id = str(uuid.uuid4())
        original_filename = file.filename or f"{doc_id}.pdf"

        suffix = os.path.splitext(original_filename)[1]
        if not suffix:
            suffix = ".pdf"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        pdf_text = pdf_parser.parse_pdf(tmp_path, doc_id)

        if not pdf_text or not isinstance(pdf_text, str) or not pdf_text.strip():
            return {
                "status": "error",
                "message": "Failed to extract text from PDF",
            }

        entities = ner_extractor.extract_entities(pdf_text[:5000], doc_id)

        sentences = []
        classifications = []

        try:
            sentences = sentence_splitter.split_sentences_for_doc(doc_id)
        except Exception as e:
            print("Sentence splitter failed:", str(e))

        try:
            classifications = arg_classifier.classify_sentences(doc_id)
        except Exception as e:
            print("Argument classifier failed:", str(e))

        db.cases.update_one(
            {"_id": doc_id},
            {
                "$set": {
                    "filename": original_filename,
                    "raw_text": pdf_text,
                    "text_preview": pdf_text[:1000],
                    "entities": entities,
                    "sentences": sentences,
                    "classifications": classifications,
                }
            },
            upsert=True,
        )

        return {
            "status": "success",
            "message": "PDF processed successfully",
            "doc_id": doc_id,
            "filename": original_filename,
            "text_preview": pdf_text[:500],
            "entities_count": len(entities),
            "sentences_count": len(sentences) if sentences else 0,
            "classifications_count": len(classifications) if classifications else 0,
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e),
        }

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)