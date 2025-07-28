FROM python:3.9-bullseye

WORKDIR /app

# Install system dependencies for PyMuPDF
RUN apt-get update && apt-get install -y \
    libfontconfig1 \
    libfreetype6 \
    libjpeg62-turbo \
    libopenjp2-7 \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir PyMuPDF==1.22.5
RUN pip install --no-cache-dir nltk==3.8.1
RUN pip install --no-cache-dir numpy==1.24.3

# Verify PyMuPDF installation
RUN python -c "import fitz; print('PyMuPDF installed successfully')"

# Download NLTK data (required for offline operation)
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng')"

# Copy application code
COPY . .

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set the default command to process all collections in input folder
CMD ["python", "challenge1b_processor.py", "--all", "--base", "/app/input", "--output", "/app/output"]












