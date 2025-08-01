from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
import os

# Import services
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
from services.pdf_service import PDFService
from services.vector_service import VectorService
from services.llm_service import LLMService

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    k: Optional[int] = 4

class UploadResponse(BaseModel):
    message: str
    chunks_count: int
    vector_store_info: dict

class QueryResponse(BaseModel):
    answer: str
    model_info: dict

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    try:
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
            vector_store_info=vector_service.get_vector_store_info()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """Query the uploaded document"""
    try:
        # Load vector store
        vector_service = VectorService()
        vector_service.load_vector_store()
        
        # Perform similarity search
        docs = vector_service.similarity_search(request.question, request.k)
        
        # Get LLM response
        llm_service = LLMService()
        response = llm_service.get_response(docs, request.question)
        
        return QueryResponse(
            answer=response,
            model_info=llm_service.get_model_info()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RAG API"}

@router.get("/vector-store-info")
async def get_vector_store_info():
    """Get information about the current vector store"""
    try:
        vector_service = VectorService()
        info = vector_service.get_vector_store_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
