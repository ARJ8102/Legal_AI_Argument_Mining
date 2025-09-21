# ner_extractor.py
import spacy
from transformers import pipeline
from pymongo import MongoClient

# Global instances to avoid repeated loading
_hf_ner = None
_spacy_nlp = None

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
documents_collection = db["documents"]


def get_huggingface_ner():
    global _hf_ner
    if _hf_ner is None:
        _hf_ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
    return _hf_ner


def get_spacy_nlp():
    global _spacy_nlp
    if _spacy_nlp is None:
        _spacy_nlp = spacy.load("en_core_web_sm")  # swap with legal-specific model later
    return _spacy_nlp


def extract_entities(doc_id, source="huggingface", collection_name="entities"):
    """
    Fetches raw_text from MongoDB, extracts entities, and saves them back.

    Args:
        doc_id (str): _id of the document in MongoDB
        source (str): "huggingface" or "spacy"
        collection_name (str): field to store entities in the document
    """
    doc = documents_collection.find_one({"_id": doc_id})
    if not doc:
        raise ValueError(f"Document with _id={doc_id} not found in MongoDB.")

    text = doc.get("raw_text", "")
    if not text:
        raise ValueError(f"No text found for document _id={doc_id}.")

    entities = []

    if source == "huggingface":
        ner = get_huggingface_ner()
        results = ner(text)
        for ent in results:
            entities.append({
                "entity": ent["word"],
                "type": ent["entity_group"],
                "source": "huggingface"
            })

    elif source == "spacy":
        nlp = get_spacy_nlp()
        spacy_doc = nlp(text)
        for ent in spacy_doc.ents:
            entities.append({
                "entity": ent.text,
                "type": ent.label_,
                "source": "spacy"
            })
    else:
        raise ValueError("Invalid source. Choose 'huggingface' or 'spacy'.")

    # Save entities back into the same MongoDB document
    documents_collection.update_one(
        {"_id": doc_id},
        {"$set": {collection_name: entities}}
    )

    print(f"✅ Extracted {len(entities)} entities for document _id={doc_id}")
    return entities


# Standalone test
if __name__ == "__main__":
    test_doc_id = "sample.pdf"  # must exist in MongoDB
    print("\n🔍 Hugging Face NER:")
    hf_entities = extract_entities(test_doc_id, source="huggingface")
    for e in hf_entities[:10]:  # print first 10 for brevity
        print(e)

    print("\n🔍 spaCy NER:")
    spacy_entities = extract_entities(test_doc_id, source="spacy")
    for e in spacy_entities[:10]:
        print(e)
