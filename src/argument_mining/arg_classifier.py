import os
from pymongo import MongoClient
from transformers import pipeline

client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
sentences_collection = db["sentences"]
classes_collection = db["classified_sentences"]

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_PATH = os.path.join(ROOT_DIR, "models", "legal_argument_classifier_inlegalbert")

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


def is_useful_sentence(sentence: str) -> bool:
    if not sentence:
        return False

    text = sentence.strip()

    if len(text) < 30:
        return False

    if len(text.split()) < 5:
        return False

    return True


def classify_sentences(doc_id):
    record = sentences_collection.find_one({"_id": doc_id})
    sentences = record.get("sentences", []) if record else []

    clf = get_classifier()

    useful_sentences = [s.strip() for s in sentences if is_useful_sentence(s)]

    if not useful_sentences:
        classified = []
    else:
        predictions = clf(
            useful_sentences,
            truncation=True,
            max_length=256,
            batch_size=8,
        )

        classified = []
        for sentence, pred in zip(useful_sentences, predictions):
            classified.append({
                "sentence": sentence,
                "label": pred["label"],
                "score": round(float(pred["score"]), 4),
            })

    grouped = {}
    for item in classified:
        grouped.setdefault(item["label"], []).append(item)

    result = {
        "doc_id": doc_id,
        "total_sentences": len(sentences),
        "classified_count": len(classified),
        "labels": grouped,
        "items": classified,
    }

    classes_collection.update_one(
        {"_id": doc_id},
        {"$set": result},
        upsert=True,
    )

    print(f"Classified {len(classified)} useful sentences for document _id={doc_id}")
    return result


def get_classifications(doc_id):
    record = classes_collection.find_one({"_id": doc_id})
    if not record:
        return {
            "doc_id": doc_id,
            "total_sentences": 0,
            "classified_count": 0,
            "labels": {},
            "items": [],
        }

    record.pop("_id", None)
    return record