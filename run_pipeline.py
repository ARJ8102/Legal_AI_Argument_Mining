import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from processing import pdf_parser, ocr_test
from nlp import ner_extractor
from argument_mining import sentence_splitter, arg_classifier

def run_pipeline_for_pdf(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    doc_id = os.path.basename(file_path)
    try:
        print(f"\nProcessing {doc_id} ...")
        pdf_parser.parse_pdf(file_path, doc_id=doc_id)
        ner_extractor.extract_entities(doc_id=doc_id)
        sentence_splitter.split_sentences_for_doc(doc_id=doc_id)
        arg_classifier.classify_sentences(doc_id=doc_id)
        print(f"✅ Completed {doc_id}")
    except Exception as e:
        print(f"❌ Error processing {doc_id}: {e}")

def run_pipeline_for_folder(pdf_folder):
    if not os.path.exists(pdf_folder):
        print(f"❌ Folder not found: {pdf_folder}")
        return

    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"No PDF files found in folder: {pdf_folder}")
        return

    for pdf_file in pdf_files:
        run_pipeline_for_pdf(os.path.join(pdf_folder, pdf_file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Legal PDF Processing Pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="Path to a single PDF file")
    group.add_argument("--folder", type=str, help="Path to a folder containing PDF files")
    args = parser.parse_args()

    if args.file:
        run_pipeline_for_pdf(args.file)
    elif args.folder:
        run_pipeline_for_folder(args.folder)
