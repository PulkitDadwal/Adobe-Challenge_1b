"""
Section Relevance Ranking Module
===============================
Ranks document sections based on keyword relevance.
"""

import re
from typing import Dict, List, Tuple
from collections import Counter
import numpy as np


class SectionRanker:
    def __init__(self):
        self.min_section_length = 100  # Minimum characters for a section
        self.max_sections_per_page = 5  # Limit sections per page
    
    def rank_sections(self, extracted_texts: Dict[str, List[str]], 
                     keywords: Dict[str, List[str]]) -> List[Dict]:
        """Rank all sections from all documents by relevance"""
        
        all_sections = []
        combined_keywords = keywords['combined_keywords']
        keyword_weights = keywords['keyword_weights']
        
        # Extract sections from all documents
        for filename, pages in extracted_texts.items():
            for page_num, page_text in enumerate(pages, 1):
                sections = self._split_into_sections(page_text)
                
                for section_idx, section_text in enumerate(sections):
                    if len(section_text) < self.min_section_length:
                        continue
                    
                    # Calculate relevance score
                    score = self._calculate_relevance_score(
                        section_text, combined_keywords, keyword_weights
                    )
                    
                    # Extract section title
                    title = self._extract_section_title(section_text)
                    
                    section_data = {
                        'document': filename,
                        'page_number': page_num,
                        'section_index': section_idx,
                        'section_title': title,
                        'section_text': section_text,
                        'relevance_score': score,
                        'importance_rank': 0  # Will be set after sorting
                    }
                    
                    all_sections.append(section_data)
        
        # Sort by relevance score (descending)
        all_sections.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Assign importance ranks
        for rank, section in enumerate(all_sections, 1):
            section['importance_rank'] = rank
        
        return all_sections
    
    def _split_into_sections(self, page_text: str) -> List[str]:
        """Split page text into logical sections"""
        if not page_text:
            return []
        
        # Split by double newlines (paragraph breaks)
        paragraphs = re.split(r'\n\s*\n', page_text)
        
        sections = []
        current_section = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Check if this looks like a new section header
            if self._is_section_header(paragraph):
                # Save previous section if it exists
                if current_section:
                    sections.append(current_section.strip())
                # Start new section
                current_section = paragraph + "\n\n"
            else:
                # Add to current section
                current_section += paragraph + "\n\n"
        
        # Add final section
        if current_section:
            sections.append(current_section.strip())
        
        # If no clear sections found, split by length
        if len(sections) <= 1 and len(page_text) > 1000:
            sections = self._split_by_length(page_text)
        
        return sections[:self.max_sections_per_page]
    
    def _is_section_header(self, text: str) -> bool:
        """Check if text looks like a section header"""
        if len(text) > 200:  # Too long to be a header
            return False
        
        # Common header patterns
        header_patterns = [
            r'^\d+\.?\s+[A-Z]',           # "1. Introduction"
            r'^[A-Z][A-Z\s]{2,}$',        # "INTRODUCTION"
            r'^[A-Z][a-z]+(\s[A-Z][a-z]+)*$',  # "Introduction"
            r'^\d+\.\d+\.?\s+[A-Z]',      # "1.1 Background"
        ]
        
        return any(re.match(pattern, text.strip()) for pattern in header_patterns)
    
    def _split_by_length(self, text: str, target_length: int = 800) -> List[str]:
        """Split text into chunks of approximately target_length"""
        sentences = re.split(r'[.!?]+\s+', text)
        sections = []
        current_section = ""
        
        for sentence in sentences:
            if len(current_section) + len(sentence) > target_length and current_section:
                sections.append(current_section.strip())
                current_section = sentence + ". "
            else:
                current_section += sentence + ". "
        
        if current_section:
            sections.append(current_section.strip())
        
        return sections
    
    def _calculate_relevance_score(self, section_text: str, keywords: List[str], 
                                 keyword_weights: Dict[str, int]) -> float:
        """Calculate relevance score based on keyword overlap"""
        if not section_text or not keywords:
            return 0.0
        
        text_lower = section_text.lower()
        score = 0.0
        
        # Count keyword occurrences
        for keyword in keywords:
            count = text_lower.count(keyword.lower())
            if count > 0:
                # Weight by keyword importance and frequency
                weight = keyword_weights.get(keyword, 1)
                score += count * weight * len(keyword)  # Longer keywords get more weight
        
        # Normalize by section length
        normalized_score = score / (len(section_text) / 1000)  # Per 1000 characters
        
        return round(normalized_score, 3)
    
    def _extract_section_title(self, section_text: str, max_length: int = 100) -> str:
        """Extract a title from the section text"""
        lines = section_text.split('\n')
        
        # Try to find a clear title in first few lines
        for line in lines[:3]:
            line = line.strip()
            if line and len(line) < max_length:
                # Check if it looks like a title
                if (line.isupper() or 
                    line.istitle() or 
                    re.match(r'^\d+\.?\s+[A-Z]', line)):
                    return line
        
        # Fallback: use first sentence
        first_sentence = re.split(r'[.!?]', section_text)[0].strip()
        if len(first_sentence) > max_length:
            first_sentence = first_sentence[:max_length] + "..."
        
        return first_sentence