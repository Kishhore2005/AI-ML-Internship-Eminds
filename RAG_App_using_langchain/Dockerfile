# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p data database

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Starting RAG LangChain Application..."\n\
echo "Starting FastAPI backend..."\n\
python fastapi_main.py &\n\
BACKEND_PID=$!\n\
echo "Waiting for backend to start..."\n\
sleep 10\n\
echo "Starting Streamlit frontend..."\n\
streamlit run main.py --server.port 8501 --server.address 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Set the default command
CMD ["/app/start.sh"]
