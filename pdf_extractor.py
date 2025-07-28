"""
PDF Text Extraction Module
==========================
Extracts text page-wise from PDF files using PyMuPDF (fitz).
"""

import fitz  # PyMuPDF
from typing import Dict, List
from pathlib import Path


class PDFExtractor:
    def __init__(self):
        self.max_pages_per_pdf = 100  # Limit for performance
    
    def extract_text(self, pdf_path: str) -> List[str]:
        """Extract text from a single PDF file, page by page"""
        try:
            doc = fitz.open(pdf_path)
            pages_text = []
            
            # Limit pages for performance
            max_pages = min(len(doc), self.max_pages_per_pdf)
            
            for page_num in range(max_pages):
                page = doc[page_num]
                text = page.get_text()
                
                # Clean and filter text
                cleaned_text = self._clean_text(text)
                if cleaned_text:  # Only add non-empty pages
                    pages_text.append(cleaned_text)
            
            doc.close()
            return pages_text
            
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return []
    
    def extract_all(self, pdf_files: List[str]) -> Dict[str, List[str]]:
        """Extract text from multiple PDF files"""
        extracted_texts = {}
        
        for pdf_file in pdf_files:
            filename = Path(pdf_file).name
            print(f"  Extracting: {filename}")
            
            pages_text = self.extract_text(pdf_file)
            extracted_texts[filename] = pages_text
            
            print(f"    Pages extracted: {len(pages_text)}")
        
        return extracted_texts
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 3:  # Filter out very short lines
                cleaned_lines.append(line)
        
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove pages with too little content
        if len(cleaned_text) < 100:
            return ""
        
        return cleaned_text