import os
import sys
import argparse

# Ensure src folder is in Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from processing import pdf_parser
from nlp import ner_extractor
from argument_mining import sentence_splitter, arg_classifier


def run_pipeline_for_pdf(file_path):
    """Run the full legal AI pipeline on a single PDF."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    doc_id = os.path.basename(file_path)

    try:
        print(f"\nProcessing {doc_id} ...")

        # Step 1: PDF parsing / OCR
        pdf_parser.parse_pdf(file_path, doc_id=doc_id)

        # Step 2: Named Entity Recognition
        raw_text = sentence_splitter.get_raw_text(doc_id)
        ner_extractor.extract_entities(text=raw_text, doc_id=doc_id)

        # Step 3: Sentence Splitting
        sentence_splitter.split_sentences_for_doc(doc_id=doc_id)

        # Step 4: Argument Classification
        arg_classifier.classify_sentences(doc_id=doc_id)

        print(f"✅ Completed {doc_id}")

    except Exception as e:
        print(f"❌ Error processing {doc_id}: {e}")


def run_pipeline_for_folder(folder_path):
    """Run the pipeline over all PDFs in a folder."""
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"No PDF files found in folder: {folder_path}")
        return

    for pdf in pdf_files:
        run_pipeline_for_pdf(os.path.join(folder_path, pdf))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Legal PDF Processing Pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="Path to a single PDF file")
    group.add_argument("--folder", type=str, help="Folder containing PDF files")
    args = parser.parse_args()

    if args.file:
        run_pipeline_for_pdf(args.file)
    else:
        run_pipeline_for_folder(args.folder)
