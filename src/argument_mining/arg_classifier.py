from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
sentences_collection = db["sentences"]
classes_collection = db["classified_sentences"]


def classify_sentences(doc_id):
    record = sentences_collection.find_one({"_id": doc_id})
    sentences = record.get("sentences", []) if record else []

    # Dummy classifier
    classified = [{"sentence": s, "label": "UNKNOWN"} for s in sentences]

    classes_collection.update_one(
        {"_id": doc_id},
        {"$set": {"classified": classified}},
        upsert=True
    )

    print(f"✅ Classified {len(classified)} sentences for document _id={doc_id}")
    return classified


def get_classifications(doc_id):
    record = classes_collection.find_one({"_id": doc_id})
    return record.get("classified", []) if record else []
