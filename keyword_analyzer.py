"""
Keyword Analysis Module
======================
Extracts key terms from persona and job_to_be_done strings.
"""

import re
import nltk
from typing import List, Set
from collections import Counter

# Download ALL required NLTK data with proper error handling
def download_nltk_data():
    """Download all required NLTK data"""
    resources = [
        'punkt',
        'punkt_tab', 
        'stopwords',
        'averaged_perceptron_tagger',
        'averaged_perceptron_tagger_eng'
    ]
    
    for resource in resources:
        try:
            # Try to find the resource in any of the common locations
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            try:
                nltk.data.find(f'corpora/{resource}')
            except LookupError:
                try:
                    nltk.data.find(f'taggers/{resource}')
                except LookupError:
                    # Only download if we're not in a container with pre-downloaded data
                    try:
                        print(f"Downloading NLTK {resource}...")
                        nltk.download(resource, quiet=True)
                    except Exception as e:
                        print(f"Failed to download {resource}: {e}, continuing...")
        except OSError:
            # Resource exists but path issue - skip download
            print(f"NLTK {resource} found but path issue, continuing...")
            continue

# Download data on import
try:
    download_nltk_data()
except Exception as e:
    print(f"Warning: NLTK data download failed: {e}")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag


class KeywordAnalyzer:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            print("Warning: Could not load stopwords, using basic set")
            self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        
        # Add domain-specific stop words
        self.stop_words.update([
            'using', 'used', 'use', 'make', 'get', 'go', 'come', 'take',
            'give', 'want', 'need', 'like', 'know', 'think', 'see', 'look'
        ])
    
    def extract_keywords(self, persona: str, job_to_be_done: str) -> dict[str, List[str]]:
        """Extract keywords from persona and job strings"""
        
        # Extract from persona
        persona_keywords = self._extract_from_text(persona)
        
        # Extract from job description
        job_keywords = self._extract_from_text(job_to_be_done)
        
        # Combine and weight keywords
        all_keywords = persona_keywords + job_keywords
        keyword_weights = Counter(all_keywords)
        
        # Get top keywords
        top_keywords = [word for word, count in keyword_weights.most_common(20)]
        
        return {
            'persona_keywords': persona_keywords,
            'job_keywords': job_keywords,
            'combined_keywords': top_keywords,
            'keyword_weights': dict(keyword_weights)
        }
    
    def _extract_from_text(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        if not text:
            return []
        
        try:
            # Tokenize and clean
            tokens = word_tokenize(text.lower())
        except:
            # Fallback tokenization if NLTK fails
            tokens = re.findall(r'\b\w+\b', text.lower())
        
        # Remove punctuation and short words
        tokens = [token for token in tokens if token.isalnum() and len(token) > 2]
        
        # Remove stop words
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # POS tagging to keep only nouns, adjectives, and verbs
        try:
            pos_tags = pos_tag(tokens)
            keywords = []
            
            for word, pos in pos_tags:
                if pos.startswith(('NN', 'JJ', 'VB')):  # Nouns, adjectives, verbs
                    keywords.append(word)
        except:
            # Fallback: use all tokens if POS tagging fails
            print("Warning: POS tagging failed, using all tokens")
            keywords = tokens
        
        # Extract multi-word phrases (bigrams)
        bigrams = self._extract_bigrams(text)
        keywords.extend(bigrams)
        
        return list(set(keywords))  # Remove duplicates
    
    def _extract_bigrams(self, text: str) -> List[str]:
        """Extract meaningful two-word phrases"""
        # Simple regex for common academic/technical phrases
        patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Title Case Phrases
            r'\b\w+ learning\b',              # "machine learning", "deep learning"
            r'\b\w+ analysis\b',              # "data analysis", "statistical analysis"
            r'\b\w+ discovery\b',             # "drug discovery", "knowledge discovery"
            r'\b\w+ networks?\b',             # "neural networks", "social network"
        ]
        
        bigrams = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            bigrams.extend([match.lower() for match in matches])
        
        return list(set(bigrams))


