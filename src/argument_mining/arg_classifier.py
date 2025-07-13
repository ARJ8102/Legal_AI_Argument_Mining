from transformers import pipeline

# Load a zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

CANDIDATE_LABELS = ["Claim", "Premise", "Conclusion", "None"]

def classify_argument(sentences):
    results = []
    for sent in sentences:
        output = classifier(sent, CANDIDATE_LABELS)
        top_label = output['labels'][0]
        results.append((sent, top_label))
    return results
