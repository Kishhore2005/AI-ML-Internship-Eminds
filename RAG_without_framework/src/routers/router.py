from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import json
from src.services.service1 import RAGService

router = APIRouter()

# Initialize RAG service
rag_service = RAGService()

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

class UploadResponse(BaseModel):
    message: str
    documents_processed: int

@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system with a question
    """
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Get answer from RAG service
        answer, sources, confidence = await rag_service.query(request.question, request.top_k)
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(
    file: UploadFile = File(...),
    document_type: str = Form("text")
):
    """
    Upload documents to the RAG system
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content
        content = await file.read()
        
        if document_type == "text":
            text_content = content.decode("utf-8")
            documents_processed = await rag_service.add_documents([text_content])
        else:
            raise HTTPException(status_code=400, detail="Unsupported document type")
        
        return UploadResponse(
            message=f"Successfully uploaded {file.filename}",
            documents_processed=documents_processed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@router.post("/upload-text")
async def upload_text_documents(texts: List[str]):
    """
    Upload text documents directly
    """
    try:
        if not texts:
            raise HTTPException(status_code=400, detail="No texts provided")
        
        documents_processed = await rag_service.add_documents(texts)
        
        return {
            "message": f"Successfully uploaded {documents_processed} documents",
            "documents_processed": documents_processed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading texts: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check for the RAG service
    """
    try:
        status = await rag_service.get_status()
        return {
            "status": "healthy",
            "documents_count": status.get("documents_count", 0),
            "index_status": status.get("index_status", "unknown")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")

@router.get("/documents")
async def get_documents():
    """
    Get information about stored documents
    """
    try:
        documents_info = await rag_service.get_documents_info()
        return documents_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")

@router.delete("/documents")
async def clear_documents():
    """
    Clear all documents from the RAG system
    """
    try:
        await rag_service.clear_documents()
        return {"message": "All documents cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing documents: {str(e)}")
