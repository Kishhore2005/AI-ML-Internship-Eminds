from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.routers.router import router
from src.services.service1 import RAGService
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Simple RAG API",
    description="A simple RAG (Retrieval-Augmented Generation) API without frameworks",
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

# Include routers
app.include_router(router, prefix="/api/v1")

# Initialize RAG service
rag_service = RAGService()

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG service on startup"""
    try:
        await rag_service.initialize()
        print("RAG service initialized successfully!")
    except Exception as e:
        print(f"Error initializing RAG service: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Simple RAG API",
        "version": "1.0.0",
        "endpoints": {
            "query": "/api/v1/query",
            "upload": "/api/v1/upload",
            "health": "/api/v1/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RAG API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
