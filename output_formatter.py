"""
Output Formatting Module
========================
Formats results into structured JSON output.
"""

from datetime import datetime
from typing import List, Dict, Any


class OutputFormatter:
    def format_output(self, pdf_files: List[str], persona: str, job_to_be_done: str,
                     ranked_sections: List[Dict], subsection_summaries: List[Dict]) -> Dict[str, Any]:
        """Format all results into structured JSON"""
        
        # Extract document names
        doc_names = [pdf_file.split('/')[-1] for pdf_file in pdf_files]
        
        # Format extracted sections (remove full text for cleaner output)
        extracted_sections = []
        for section in ranked_sections:
            extracted_sections.append({
                'document': section['document'],
                'section_title': section['section_title'],
                'importance_rank': section['importance_rank'],
                'page_number': section['page_number']
            })
        
        # Format subsection analysis
        subsection_analysis = []
        for summary in subsection_summaries:
            subsection_analysis.append({
                'document': summary['document'],
                'refined_text': summary['refined_text'],
                'page_number': summary['page_number']
            })
        
        # Create final output structure
        output = {
            'metadata': {
                'input_documents': doc_names,
                'persona': persona,
                'job_to_be_done': job_to_be_done
            },
            'extracted_sections': extracted_sections,
            'subsection_analysis': subsection_analysis
        }
        
        return output
