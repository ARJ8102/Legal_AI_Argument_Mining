from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]

# Dummy argument classifier
def classify_sentences(doc_id):
    doc = documents_collection.find_one({"_id": doc_id})
    if not doc or "sentences" not in doc:
        raise ValueError(f"No sentences found for document {doc_id}")

    classified_sentences = []
    for s in doc["sentences"]:
        text = s["text"]
        # Simple heuristic: first sentence = Premise, contains 'whereas' = Claim, 'therefore' = Conclusion
        if "therefore" in text.lower():
            role = "Conclusion"
        elif "whereas" in text.lower():
            role = "Claim"
        else:
            role = "Premise"
        classified_sentences.append({"sentence_id": s["sentence_id"], "text": text, "role": role})

    documents_collection.update_one(
        {"_id": doc_id},
        {"$set": {"sentences": classified_sentences}}
    )
    print(f"✅ Classified {len(classified_sentences)} sentences for document _id={doc_id}")


def get_classified_sentences(doc_id):
    doc = documents_collection.find_one({"_id": doc_id})
    return doc.get("classified_sentences", [])
