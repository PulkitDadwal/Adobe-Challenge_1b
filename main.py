"""
Persona-Driven Document Intelligence System
==========================================

A lightweight CPU-only system for extracting and ranking relevant sections
from PDF documents based on user persona and job requirements.

Usage:
    python main.py --pdfs doc1.pdf doc2.pdf doc3.pdf \
                   --persona "PhD Researcher in Computational Biology" \
                   --job "Prepare literature review on GNNs for drug discovery"

Requirements:
    - Python 3.8+
    - Libraries: PyMuPDF, nltk, scikit-learn, numpy
    - CPU-only processing
    - Model size ≤ 1GB
    - Processing time ≤ 60 seconds for 3-5 PDFs
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from pdf_extractor import PDFExtractor
from keyword_analyzer import KeywordAnalyzer
from section_ranker import SectionRanker
from subsection_analyzer import SubsectionAnalyzer
from output_formatter import OutputFormatter


class DocumentIntelligenceSystem:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.keyword_analyzer = KeywordAnalyzer()
        self.section_ranker = SectionRanker()
        self.subsection_analyzer = SubsectionAnalyzer()
        self.output_formatter = OutputFormatter()
    
    def process_documents(self, pdf_files: List[str], persona: str, job_to_be_done: str) -> Dict[str, Any]:
        """Main processing pipeline"""
        start_time = time.time()
        
        print(f"Processing {len(pdf_files)} PDF files...")
        
        # Step 1: Extract text from PDFs
        print("1. Extracting text from PDFs...")
        extracted_texts = self.pdf_extractor.extract_all(pdf_files)
        
        # Step 2: Extract keywords from persona and job
        print("2. Analyzing keywords...")
        keywords = self.keyword_analyzer.extract_keywords(persona, job_to_be_done)
        
        # Step 3: Rank sections by relevance
        print("3. Ranking sections...")
        ranked_sections = self.section_ranker.rank_sections(extracted_texts, keywords)
        
        # Step 4: Generate subsection summaries
        print("4. Generating summaries...")
        subsection_summaries = self.subsection_analyzer.analyze_subsections(
            ranked_sections[:10], keywords  # Top 10 sections
        )
        
        # Step 5: Format output
        print("5. Formatting output...")
        result = self.output_formatter.format_output(
            pdf_files, persona, job_to_be_done, 
            ranked_sections[:10], subsection_summaries
        )
        
        processing_time = time.time() - start_time
        result["metadata"]["processing_time_seconds"] = round(processing_time, 2)
        
        print(f"Processing completed in {processing_time:.2f} seconds")
        return result


def main():
    parser = argparse.ArgumentParser(description="Persona-Driven Document Intelligence")
    parser.add_argument("--pdfs", nargs="+", required=True, help="PDF files to process")
    parser.add_argument("--persona", required=True, help="User persona string")
    parser.add_argument("--job", required=True, help="Job to be done string")
    parser.add_argument("--output", default="output.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    # Validate PDF files exist
    for pdf_file in args.pdfs:
        if not Path(pdf_file).exists():
            print(f"Error: PDF file not found: {pdf_file}")
            return
    
    # Initialize system
    system = DocumentIntelligenceSystem()
    
    try:
        # Process documents
        result = system.process_documents(args.pdfs, args.persona, args.job)
        
        # Save output
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to: {args.output}")
        
        # Print summary
        print(f"\nSummary:")
        print(f"- Documents processed: {len(args.pdfs)}")
        print(f"- Top sections found: {len(result['extracted_sections'])}")
        print(f"- Processing time: {result['metadata']['processing_time_seconds']}s")
        
    except Exception as e:
        print(f"Error processing documents: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()