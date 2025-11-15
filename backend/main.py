from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

sys.path.append(os.path.abspath(".."))

from run_pipeline import run_pipeline_for_pdf

app = FastAPI()

# CORS fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add project root to Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from run_pipeline import run_pipeline_for_pdf
from processing import pdf_parser
from argument_mining import sentence_splitter, arg_classifier
from nlp import ner_extractor


@app.get("/")
def home():
    return {"message": "Legal AI backend is running"}


@app.post("/process_pdf")
async def process_pdf(file: UploadFile = File(...)):
    try:
        # Save uploaded file to backend/uploads folder
        uploads_dir = os.path.join(ROOT_DIR, "uploads")
        os.makedirs(uploads_dir, exist_ok=True)

        file_path = os.path.join(uploads_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Run pipeline
        run_pipeline_for_pdf(file_path)

        doc_id = file.filename

        # Gather results
        output = {
            "text": pdf_parser.get_raw_text(doc_id),
            "entities": ner_extractor.get_entities(doc_id),
            "sentences": sentence_splitter.get_sentences(doc_id),
            "arguments": arg_classifier.get_classifications(doc_id)
        }

        return {"status": "success", "filename": file.filename, "results": output}

    except Exception as e:
        return {"status": "error", "message": str(e)}
