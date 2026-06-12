import os
from pymongo import MongoClient
from transformers import pipeline

# --- Fix 1: MongoDB from environment variable ---
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URI)
db = client["legal_pipeline"]
sentences_collection = db["sentences"]
classes_collection = db["classified_sentences"]

# --- Fix 2: Load model from HuggingFace Hub on cloud, local path on dev ---
LOCAL_MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "models", "legal_argument_classifier_inlegalbert")
)
HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "AtharvaRJ/legal-argument-classifier")

# Use local path if it exists (your PC), otherwise load from HuggingFace (Render)
MODEL_PATH = LOCAL_MODEL_PATH if os.path.exists(LOCAL_MODEL_PATH) else HF_MODEL_REPO

_classifier = None


def get_classifier():
    global _classifier

    if _classifier is None:
        print(f"Loading LegalBERT argument classifier from: {MODEL_PATH}")
        _classifier = pipeline(
            "text-classification",
            model=MODEL_PATH,
            tokenizer=MODEL_PATH,
            device=-1,
        )

    return _classifier

# ... rest of the file stays exactly the same