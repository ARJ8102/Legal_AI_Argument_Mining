# arg_classifier.py
from pymongo import MongoClient
from transformers import pipeline

# Initialize MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]

# Initialize Hugging Face text classification pipeline
# Replace with your trained argument mining model if available
arg_classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")  
# Note: You can swap this with your real argument classifier model

def classify_sentences(doc_id, sentences_field="sentences"):
    """
    Fetch sentences from MongoDB, classify each into argument roles, and store back.
    
    Args:
        doc_id (str): _id of the document in MongoDB
        sentences_field (str): field name where sentences are stored
    """
    doc = documents_collection.find_one({"_id": doc_id})
    if not doc:
        raise ValueError(f"Document with _id={doc_id} not found.")

    sentences = doc.get(sentences_field, [])
    if not sentences:
        raise ValueError(f"No sentences found for document _id={doc_id}. Run sentence splitter first.")

    for sentence in sentences:
        text = sentence["text"]
        # Run classifier
        result = arg_classifier(text)[0]  # [{'label': 'LABEL', 'score': 0.99}]
        # Save role
        sentence["role"] = result["label"]

    # Update MongoDB document
    documents_collection.update_one(
        {"_id": doc_id},
        {"$set": {sentences_field: sentences}}
    )

    print(f"✅ Classified {len(sentences)} sentences for document _id={doc_id}")
    return sentences


# Standalone test
if __name__ == "__main__":
    test_doc_id = "sample.pdf"
    classified_sentences = classify_sentences(test_doc_id)
    for s in classified_sentences[:5]:  # print first 5
        print(s)
