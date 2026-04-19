FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for PyMuPDF and python-docx)
RUN apt-get update && apt-get install -y \
    build-essential \
    libmupdf-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose Streamlit default port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.fileWatcherType=none", \
    "--browser.gatherUsageStats=false"]
