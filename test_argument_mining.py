from src.argument_mining.sentence_splitter import split_sentences
from src.argument_mining.arg_classifier import classify_argument

def main():
    # Load your sample legal text
    with open("sample_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # Split text into sentences using NLTK sent_tokenize
    sentences = split_sentences(text)

    # Classify sentences into argument roles
    classified = classify_argument(sentences)

    # Print the results
    print("\n🔍 Argument Roles Detected:\n")
    for sent, label in classified:
        print(f"{label:10} → {sent}")

if __name__ == "__main__":
    main()
