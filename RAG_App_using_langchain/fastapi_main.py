from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import sys
import uvicorn

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.services.pdf_service import PDFService
from src.services.vector_service import VectorService
from src.services.llm_service import LLMService

# Initialize FastAPI app
app = FastAPI(
    title="RAG PDF Chatbot API",
    description="A FastAPI-based RAG system for PDF document processing and querying",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    question: str
    k: Optional[int] = 4
    model_name: Optional[str] = "llama3-8b-8192"

class UploadResponse(BaseModel):
    message: str
    chunks_count: int
    vector_store_info: dict
    filename: str

class QueryResponse(BaseModel):
    answer: str
    model_info: dict
    sources: List[str]

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

# Global variables for services
vector_service = None
llm_service = None
current_model = "llama3-8b-8192"

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global vector_service, llm_service
    try:
        # Initialize vector service
        vector_service = VectorService()
        
        # Initialize LLM service
        llm_service = LLMService(model_name=current_model)
        
        print("✅ RAG API services initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing services: {e}")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API documentation"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RAG PDF Chatbot API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #0066cc; }
        </style>
    </head>
    <body>
        <h1>📄 RAG PDF Chatbot API</h1>
        <p>Welcome to the RAG-based PDF processing and querying API!</p>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/health</code> - Health check
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/upload</code> - Upload and process PDF
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/query</code> - Query processed documents
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/docs</code> - Interactive API documentation
        </div>
        
        <h2>Quick Start:</h2>
        <ol>
            <li>Upload a PDF using <code>POST /upload</code></li>
            <li>Query the document using <code>POST /query</code></li>
            <li>Check the interactive docs at <code>/docs</code></li>
        </ol>
        
        <p><a href="/docs">📖 View Interactive API Documentation</a></p>
    </body>
    </html>
    """

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        service="RAG PDF Chatbot API",
        version="1.0.0"
    )

@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    global vector_service
    
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save uploaded file
        temp_path = PDFService.save_uploaded_file(file.file, f"data/{file.filename}")
        
        # Extract text
        raw_text = PDFService.extract_text_from_pdf(temp_path)
        text_chunks = PDFService.get_text_chunks(raw_text)
        
        # Create vector store
        vector_service = VectorService()
        vector_store = vector_service.create_vector_store(text_chunks)
        
        # Save vector store
        save_path = vector_service.save_vector_store()
        
        # Cleanup temp file
        PDFService.cleanup_temp_file(temp_path)
        
        return UploadResponse(
            message="PDF processed successfully",
            chunks_count=len(text_chunks),
            vector_store_info=vector_service.get_vector_store_info(),
            filename=file.filename
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """Query the uploaded document"""
    global vector_service, llm_service, current_model
    
    try:
        # Check if vector service is available
        if vector_service is None:
            raise HTTPException(status_code=400, detail="No documents uploaded. Please upload a PDF first.")
        
        # Update model if different
        if request.model_name != current_model:
            try:
                llm_service = LLMService(model_name=request.model_name)
                current_model = request.model_name
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error switching model: {str(e)}")
        
        # Load vector store if needed
        if not vector_service.is_loaded():
            vector_service.load_vector_store()
        
        # Perform similarity search
        docs = vector_service.similarity_search(request.question, request.k)
        
        # Get LLM response
        response = llm_service.get_response(docs, request.question)
        
        # Extract sources from documents
        sources = [doc.page_content[:100] + "..." for doc in docs]
        
        return QueryResponse(
            answer=response,
            model_info=llm_service.get_model_info(),
            sources=sources
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/vector-store-info")
async def get_vector_store_info():
    """Get information about the current vector store"""
    global vector_service
    
    try:
        if vector_service is None:
            return {"message": "No vector store available"}
        
        info = vector_service.get_vector_store_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def get_available_models():
    """Get list of available models"""
    models = [
        {"name": "llama3-8b-8192", "description": "Llama 3 8B model"},
        {"name": "mixtral-8x7b-32768", "description": "Mixtral 8x7B model"},
        {"name": "llama3-70b-8192", "description": "Llama 3 70B model"}
    ]
    return {"models": models, "current_model": current_model}

@app.post("/change-model")
async def change_model(model_name: str):
    """Change the current LLM model"""
    global llm_service, current_model
    
    try:
        llm_service = LLMService(model_name=model_name)
        current_model = model_name
        return {"message": f"Model changed to {model_name}", "current_model": current_model}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error changing model: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "fastapi_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 