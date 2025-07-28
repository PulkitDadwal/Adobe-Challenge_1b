# Persona-Driven Document Intelligence System

## Pre-built Image
Available on Docker Hub: `parzivl/document-intelligence:latest`

## Quick Start (Using Pre-built Image)
```bash
mkdir -p output
docker run --rm -v $(pwd)/Challenge_1b:/app/input -v $(pwd)/output:/app/output --network none parzivl/document-intelligence:latest
```

## Build from Source
If you want to build locally:
```bash
docker build --platform linux/amd64 -t document-intelligence:latest .
docker run --rm -v $(pwd)/Challenge_1b:/app/input -v $(pwd)/output:/app/output --network none document-intelligence:latest
```

## For Windows PowerShell
```powershell
mkdir -p output
docker run --rm -v "${PWD}/Challenge_1b:/app/input" -v "${PWD}/output:/app/output" --network none parzivl/document-intelligence:latest
```

## Approach

This system processes PDF documents and extracts relevant sections based on user persona and job requirements using a multi-stage approach:

1. **PDF Text Extraction**: Uses PyMuPDF to extract text from PDFs page by page
2. **Keyword Analysis**: Extracts relevant keywords from persona and job descriptions using NLTK
3. **Section Ranking**: Ranks document sections by keyword relevance and frequency
4. **Subsection Analysis**: Generates refined summaries of top-ranked sections
5. **Output Formatting**: Structures results into JSON format with metadata

The system processes documents through multiple stages:
- Page-by-page text extraction with cleaning and filtering
- Natural language processing for keyword extraction and POS tagging
- Relevance scoring using keyword frequency and positioning
- Extractive summarization of the most important sections

## Models and Libraries Used

### Core Libraries
- **PyMuPDF (1.22.5)**: PDF text extraction and processing
- **NLTK (3.8.1)**: Natural language processing, tokenization, POS tagging, and stopwords
- **NumPy (1.24.3)**: Numerical computations for scoring algorithms
- **Python Standard Library**: JSON processing, file handling, regex

### No External Models
- No pre-trained ML models (stays under 1GB limit)
- No network dependencies (works offline after NLTK data download)
- Custom keyword-based relevance scoring system

## Architecture

- `main.py`: Main orchestrator with DocumentIntelligenceSystem class
- `pdf_extractor.py`: PDF text extraction using PyMuPDF
- `keyword_analyzer.py`: NLTK-based keyword extraction and analysis
- `section_ranker.py`: Relevance scoring and section ranking
- `subsection_analyzer.py`: Extractive summarization of top sections
- `output_formatter.py`: JSON output formatting
- `challenge1b_processor.py`: Batch processor for Challenge 1b collections
- Supports AMD64 architecture explicitly
- Containerized for consistent execution

## How to Build and Run

### Build the Docker Image
```bash
docker build --platform linux/amd64 -t document-intelligence:latest .
```

### Run the Solution
```bash
docker run --rm -v $(pwd)/Challenge_1b:/app/input -v $(pwd)/output:/app/output --network none document-intelligence:latest
```

### Expected Behavior
- Processes all collections from `/app/input` directory
- Generates corresponding `collection_X_output.json` files in `/app/output`
- Each JSON contains extracted sections and refined summaries
- Works completely offline with no network calls
- Processing time under 60 seconds for 3-5 PDFs

### Input/Output Format
**Input**: Challenge 1b directory structure with collections containing PDFs and input JSON
**Output**: JSON files with structure:
```json
{
  "metadata": {
    "input_documents": ["list of PDF files"],
    "persona": "User Persona",
    "job_to_be_done": "Task description"
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Content",
      "page_number": 1
    }
  ]
}
```

## Performance

- CPU-only processing
- Handles 3-5 PDFs in under 60 seconds
- Memory efficient with page-by-page processing
- Model size under 1GB (NLTK data only)

## Usage Examples

### Process all collections:
```bash
docker run --rm -v $(pwd)/Challenge_1b:/app/input -v $(pwd)/output:/app/output --network none parzivl/document-intelligence:latest
```

### Process specific collection:
```bash
docker run --rm -v $(pwd)/Challenge_1b:/app/input -v $(pwd)/output:/app/output --network none parzivl/document-intelligence:latest python challenge1b_processor.py --collection "/app/input/Collection 1"
```

### Direct usage with main.py:
```bash
python main.py --pdfs doc1.pdf doc2.pdf doc3.pdf \
               --persona "PhD Researcher in Computational Biology" \
               --job "Prepare literature review on GNNs for drug discovery"
```



