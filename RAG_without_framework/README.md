# Simple RAG (Retrieval-Augmented Generation) System

A simple RAG implementation without frameworks, built with FastAPI, sentence transformers, and FAISS for efficient similarity search.

## Features

- **Document Upload**: Upload text documents to build a knowledge base
- **Semantic Search**: Find relevant documents using sentence embeddings
- **Question Answering**: Generate answers based on retrieved documents
- **Persistent Storage**: Documents and embeddings are saved to disk
- **RESTful API**: Easy-to-use HTTP endpoints
- **No Framework Dependencies**: Built from scratch without LangChain or similar frameworks

## Project Structure

```
RAG_without_framework/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── data/                  # Sample documents and data
│   └── sample_documents.txt
├── database/              # Persistent storage for documents and embeddings
├── src/
│   ├── routers/
│   │   └── router.py      # API endpoints
│   └── services/
│       └── service1.py    # RAG service implementation
```

## Installation

1. **Clone the repository** (if not already done):
```bash
git clone <repository-url>
cd AI-ML-Internship-Eminds/RAG_without_framework
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/health` - Check if the service is running

### Query
- **POST** `/api/v1/query` - Ask questions to the RAG system
  ```json
  {
    "question": "What is machine learning?",
    "top_k": 3
  }
  ```

### Document Upload
- **POST** `/api/v1/upload` - Upload text files
- **POST** `/api/v1/upload-text` - Upload text directly
  ```json
  ["Text document 1", "Text document 2"]
  ```

### Document Management
- **GET** `/api/v1/documents` - Get information about stored documents
- **DELETE** `/api/v1/documents` - Clear all documents

## Usage Examples

### 1. Start the server
```bash
python main.py
```

### 2. Upload documents
```bash
curl -X POST "http://localhost:8000/api/v1/upload-text" \
     -H "Content-Type: application/json" \
     -d '["Artificial Intelligence is a branch of computer science..."]'
```

### 3. Ask questions
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is AI?", "top_k": 3}'
```

### 4. Check health
```bash
curl http://localhost:8000/api/v1/health
```

## How It Works

1. **Document Processing**: Text documents are cleaned, chunked, and stored
2. **Embedding Generation**: Sentence transformers create vector embeddings for each chunk
3. **Indexing**: FAISS creates an efficient similarity search index
4. **Retrieval**: When a question is asked, it's embedded and similar documents are retrieved
5. **Answer Generation**: A simple template-based approach generates answers using retrieved context

## Technical Details

- **Embedding Model**: `all-MiniLM-L6-v2` (lightweight and fast)
- **Vector Database**: FAISS for efficient similarity search
- **Chunking**: 512-word chunks with 50-word overlap
- **Storage**: JSON for documents, pickle for embeddings, FAISS binary for index

## Configuration

You can modify the following parameters in `src/services/service1.py`:

- `chunk_size`: Number of words per chunk (default: 512)
- `chunk_overlap`: Overlap between chunks (default: 50)
- `model_name`: Sentence transformer model (default: "all-MiniLM-L6-v2")

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Sample Data

The `data/sample_documents.txt` file contains sample text about AI and machine learning that you can use for testing.

## Troubleshooting

1. **Memory Issues**: Reduce `chunk_size` for large documents
2. **Slow Performance**: The first run will download the embedding model (~80MB)
3. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

## License

This project is for educational purposes.
