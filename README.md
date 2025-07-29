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

## Execution Instructions

### Prerequisites
- Docker installed on your system
- Input data in `Challenge_1b` directory structure

### Step-by-Step Execution

1. **Prepare your input directory**:
   ```bash
   # Ensure your Challenge_1b directory contains collections like:
   # Challenge_1b/
   #   ├── Collection 1/
   #   ├── Collection 2/
   #   └── Collection 3/
   ```

2. **Create output directory**:
   ```bash
   mkdir -p output
   ```

3. **Run the system** (choose one method):

   **Option A: Using pre-built image (recommended)**:
   ```bash
   docker run --rm \
     -v $(pwd)/Challenge_1b:/app/input \
     -v $(pwd)/output:/app/output \
     --network none \
     parzivl/document-intelligence:latest
   ```

   **Option B: Build and run locally**:
   ```bash
   docker build --platform linux/amd64 -t document-intelligence:latest .
   docker run --rm \
     -v $(pwd)/Challenge_1b:/app/input \
     -v $(pwd)/output:/app/output \
     --network none \
     document-intelligence:latest
   ```

   **Option C: Windows PowerShell**:
   ```powershell
   docker run --rm `
     -v "${PWD}/Challenge_1b:/app/input" `
     -v "${PWD}/output:/app/output" `
     --network none `
     parzivl/document-intelligence:latest
   ```

4. **Verify results**:
   ```bash
   ls output/
   # Should show: collection_1_output.json, collection_2_output.json, etc.
   ```

### Processing Individual Collections

To process a specific collection:
```bash
docker run --rm \
  -v $(pwd)/Challenge_1b:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  parzivl/document-intelligence:latest \
  python challenge1b_processor.py --collection "/app/input/Collection 1"
```

### Direct Usage (Development)

For development or custom usage:
```bash
python main.py \
  --pdfs doc1.pdf doc2.pdf doc3.pdf \
  --persona "PhD Researcher in Computational Biology" \
  --job "Prepare literature review on GNNs for drug discovery" \
  --output results.json
```

### Troubleshooting

- **Permission issues**: Ensure Docker has access to your directories
- **Network disabled**: The `--network none` flag ensures offline operation
- **Platform compatibility**: Use `--platform linux/amd64` for consistent results
- **Memory issues**: System processes documents page-by-page to minimize memory usage

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