"""
Challenge 1b Processor
=====================
Processes Challenge 1b input JSON files and generates output using the main system.
"""

import json
import os
from pathlib import Path
from main import DocumentIntelligenceSystem

def process_challenge1b_collection(collection_path: str, output_base: str = None):
    """Process a single Challenge 1b collection"""
    collection_dir = Path(collection_path)
    
    # Use output directory if specified
    if output_base:
        output_dir = Path(output_base)
        output_dir.mkdir(exist_ok=True)
    else:
        output_dir = collection_dir
    
    # Read input JSON
    input_file = collection_dir / "challenge1b_input.json"
    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        return
    
    with open(input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    # Extract data
    documents = input_data["documents"]
    persona = input_data["persona"]["role"]
    job_to_be_done = input_data["job_to_be_done"]["task"]
    
    # Build PDF file paths
    pdfs_dir = collection_dir / "PDFs"
    pdf_files = []
    
    for doc in documents:
        pdf_path = pdfs_dir / doc["filename"]
        if pdf_path.exists():
            pdf_files.append(str(pdf_path))
        else:
            print(f"Warning: PDF not found: {pdf_path}")
    
    if not pdf_files:
        print(f"No PDF files found in {pdfs_dir}")
        return
    
    print(f"Processing {len(pdf_files)} PDFs for persona: {persona}")
    print(f"Task: {job_to_be_done}")
    
    # Process documents
    system = DocumentIntelligenceSystem()
    result = system.process_documents(pdf_files, persona, job_to_be_done)
    
    # Save to output directory
    collection_name = collection_dir.name.replace(" ", "_").lower()
    output_filename = f"{collection_name}_output.json"
    output_file = output_dir / output_filename
    
    # Save output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    print(f"Results saved to: {output_file}")
    return result

def process_all_collections(base_dir: str, output_base: str = None):
    """Process all Challenge 1b collections"""
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"Base directory not found: {base_dir}")
        return
    
    collections = [d for d in base_path.iterdir() if d.is_dir() and "Collection" in d.name]
    
    for collection_dir in sorted(collections):
        print(f"\n{'='*50}")
        print(f"Processing: {collection_dir.name}")
        print(f"{'='*50}")
        
        try:
            process_challenge1b_collection(str(collection_dir), output_base)
        except Exception as e:
            print(f"Error processing {collection_dir.name}: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Process Challenge 1b collections")
    parser.add_argument("--collection", help="Process specific collection")
    parser.add_argument("--all", action="store_true", help="Process all collections")
    parser.add_argument("--base", default="/app/input", help="Base directory path")
    parser.add_argument("--output", default="/app/output", help="Output directory path")
    
    args = parser.parse_args()
    
    if args.collection:
        process_challenge1b_collection(args.collection, args.output)
    elif args.all:
        process_all_collections(args.base, args.output)
    else:
        print("Usage:")
        print("  python challenge1b_processor.py --all")
        print("  python challenge1b_processor.py --collection 'input/Collection 1'")


