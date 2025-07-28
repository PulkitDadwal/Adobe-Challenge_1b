"""
Subsection Analysis Module
=========================
Generates concise summaries for top-ranked sections.
"""

import re
from typing import List, Dict
from collections import Counter


class SubsectionAnalyzer:
    def __init__(self):
        self.summary_sentences = 3  # Target number of sentences in summary
    
    def analyze_subsections(self, top_sections: List[Dict], 
                          keywords: Dict[str, List[str]]) -> List[Dict]:
        """Generate summaries for top sections"""
        
        summaries = []
        combined_keywords = keywords['combined_keywords']
        
        for section in top_sections:
            summary = self._generate_extractive_summary(
                section['section_text'], combined_keywords
            )
            
            summary_data = {
                'document': section['document'],
                'page_number': section['page_number'],
                'section_title': section['section_title'],
                'importance_rank': section['importance_rank'],
                'refined_text': summary
            }
            
            summaries.append(summary_data)
        
        return summaries
    
    def _generate_extractive_summary(self, text: str, keywords: List[str]) -> str:
        """Generate extractive summary based on keyword frequency"""
        if not text:
            return ""
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        if len(sentences) <= self.summary_sentences:
            return text  # Return original if already short
        
        # Score sentences based on keyword presence
        sentence_scores = []
        
        for sentence in sentences:
            score = self._score_sentence(sentence, keywords)
            sentence_scores.append((sentence, score))
        
        # Sort by score and select top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = sentence_scores[:self.summary_sentences]
        
        # Sort selected sentences by original order
        selected_sentences = [sent for sent, score in top_sentences]
        original_order_sentences = []
        
        for sentence in sentences:
            if sentence in selected_sentences:
                original_order_sentences.append(sentence)
        
        return ' '.join(original_order_sentences)
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+\s+', text)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Filter out very short sentences
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def _score_sentence(self, sentence: str, keywords: List[str]) -> float:
        """Score a sentence based on keyword presence"""
        if not sentence or not keywords:
            return 0.0
        
        sentence_lower = sentence.lower()
        score = 0.0
        
        # Count keyword occurrences
        for keyword in keywords:
            if keyword.lower() in sentence_lower:
                # Weight by keyword length (longer keywords are more specific)
                score += len(keyword)
        
        # Bonus for sentences with multiple keywords
        keyword_count = sum(1 for keyword in keywords 
                          if keyword.lower() in sentence_lower)
        if keyword_count > 1:
            score *= (1 + keyword_count * 0.2)
        
        # Normalize by sentence length
        normalized_score = score / (len(sentence) / 100)  # Per 100 characters
        
        return normalized_score