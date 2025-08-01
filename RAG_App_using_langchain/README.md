# RAG PDF Chatbot - Streamlit Frontend + FastAPI Backend

A comprehensive RAG (Retrieval-Augmented Generation) system with two deployment options:
- **Streamlit Frontend**: User-friendly web interface for end users
- **FastAPI Backend**: RESTful API for developers and integrations

## 🚀 Features

- **PDF Processing**: Upload and extract text from PDF documents
- **Vector Search**: FAISS-based similarity search for document retrieval
- **LLM Integration**: Support for multiple Groq models (Llama 3, Mixtral)
- **Dual Interface**: Streamlit UI + FastAPI REST API
- **Interactive Docs**: Auto-generated API documentation
- **CORS Support**: Cross-origin request handling

## 📋 Prerequisites

- Python 3.8+
- Groq API key
- Required Python packages (see requirements.txt)

## 🛠️ Installation

1. **Clone the repository** (if not already done)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🚀 Running the Application

### Option 1: Streamlit Frontend (Recommended for End Users)
```bash
streamlit run main.py
```
- **URL**: `http://localhost:8501`
- **Best for**: End users, quick testing, interactive experience
- **Features**: Upload PDFs, chat interface, model selection

### Option 2: FastAPI Backend (Recommended for Developers)
```bash
python fastapi_main.py
```
- **URL**: `http://localhost:8000`
- **Docs**: `http://localhost:8000/docs`
- **Best for**: API integrations, custom frontends, programmatic access

### Option 3: Both (Full Stack)
```bash
# Terminal 1: Start FastAPI backend
python fastapi_main.py

# Terminal 2: Start Streamlit frontend
streamlit run main.py
```

## 📖 Architecture Overview

### Streamlit Frontend (`main.py`)
- **Purpose**: User-friendly web interface
- **Features**: 
  - PDF upload and processing
  - Real-time chat interface
  - Model selection and configuration
  - Visual feedback and progress indicators

### FastAPI Backend (`fastapi_main.py`)
- **Purpose**: RESTful API server
- **Features**:
  - REST API endpoints
  - PDF processing and storage
  - Document querying
  - Model management
  - Interactive API documentation

### Shared Services
Both frontend and backend use the same underlying services:
- `pdf_service.py`: PDF text extraction and processing
- `vector_service.py`: FAISS vector store operations
- `llm_service.py`: Groq LLM integration

## 📖 API Endpoints (FastAPI Backend)

### Health Check
```bash
GET /health
```

### Upload PDF
```bash
POST /upload
Content-Type: multipart/form-data
Body: file (PDF file)
```

### Query Documents
```bash
POST /query
Content-Type: application/json
Body: {
  "question": "What is this document about?",
  "k": 4,
  "model_name": "llama3-8b-8192"
}
```

### Get Available Models
```bash
GET /models
```

### Change Model
```bash
POST /change-model
Content-Type: application/json
Body: "llama3-70b-8192"
```

### Get Vector Store Info
```bash
GET /vector-store-info
```

## 🧪 Testing

### Test FastAPI Backend
```bash
python test_fastapi.py
```

### Interactive API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

## 📁 Project Structure

```
RAG_App_using_langchain/
├── main.py                  # Streamlit frontend application
├── fastapi_main.py          # FastAPI backend application
├── test_fastapi.py          # API testing script
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── data/                   # PDF storage directory
├── database/               # Vector store storage
└── src/
    ├── services/
    │   ├── pdf_service.py      # PDF processing
    │   ├── vector_service.py   # Vector operations
    │   └── llm_service.py      # LLM integration
    └── routers/
        └── router.py           # API routes (legacy)
```

## 🔧 Configuration

### Available Models
- `llama3-8b-8192` (default)
- `mixtral-8x7b-32768`
- `llama3-70b-8192`

### Vector Store Settings
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- Storage: FAISS index in `database/faiss_index/`

## 💡 Usage Examples

### Using Streamlit Frontend
1. Run `streamlit run main.py`
2. Upload a PDF file
3. Start chatting with the document

### Using FastAPI Backend with curl

1. **Upload a PDF**:
   ```bash
   curl -X POST "http://localhost:8000/upload" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@your_document.pdf"
   ```

2. **Query the document**:
   ```bash
   curl -X POST "http://localhost:8000/query" \
        -H "accept: application/json" \
        -H "Content-Type: application/json" \
        -d '{
          "question": "What are the main points?",
          "k": 4,
          "model_name": "llama3-8b-8192"
        }'
   ```

### Using Python requests

```python
import requests

# Upload PDF
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/upload', files=files)
    print(response.json())

# Query document
data = {
    "question": "What is this about?",
    "k": 4,
    "model_name": "llama3-8b-8192"
}
response = requests.post('http://localhost:8000/query', json=data)
print(response.json())
```

## 🎯 When to Use Which?

### Use Streamlit Frontend When:
- ✅ You want a user-friendly interface
- ✅ You're demonstrating to end users
- ✅ You need quick setup and testing
- ✅ You want interactive features (chat, file upload)

### Use FastAPI Backend When:
- ✅ You're building custom applications
- ✅ You need API integration
- ✅ You're developing mobile apps
- ✅ You want programmatic access
- ✅ You need to scale the backend

## 🔍 Troubleshooting

### Common Issues

1. **API Key Error**:
   - Ensure `GROQ_API_KEY` is set in `.env` file
   - Verify the key is valid and has sufficient credits

2. **Port Already in Use**:
   - Streamlit: Change port with `streamlit run main.py --server.port 8502`
   - FastAPI: Change port in `fastapi_main.py` or use `--port 8001`

3. **Memory Issues**:
   - Use smaller models for large documents
   - Reduce chunk size in PDF processing

4. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path and virtual environment

## 📊 Performance Tips

- Use smaller models for faster responses
- Adjust chunk size based on document complexity
- Monitor memory usage with large documents
- Consider using async operations for better performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes.

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Groq API Documentation](https://console.groq.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
