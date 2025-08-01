#!/usr/bin/env python3
"""
Test script for the Simple RAG System
"""

import asyncio
import json
import requests
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_upload_documents():
    """Test uploading documents"""
    print("\nTesting document upload...")
    
    # Sample documents
    documents = [
        "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines.",
        "Machine Learning is a subset of AI that focuses on algorithms and statistical models.",
        "Deep Learning uses neural networks with multiple layers to understand complex patterns.",
        "Natural Language Processing (NLP) focuses on interaction between computers and human language.",
        "Computer Vision enables computers to interpret and understand visual information."
    ]
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/upload-text",
            json=documents,
            headers={"Content-Type": "application/json"}
        )
        print(f"Upload response: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Upload failed: {e}")
        return False

def test_query(question, top_k=3):
    """Test querying the RAG system"""
    print(f"\nTesting query: '{question}'")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/query",
            json={"question": question, "top_k": top_k},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Question: {question}")
            print(f"Answer: {result['answer'][:200]}...")
            print(f"Sources: {result['sources']}")
            print(f"Confidence: {result['confidence']:.3f}")
            return True
        else:
            print(f"Query failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Query failed: {e}")
        return False

def test_get_documents():
    """Test getting document information"""
    print("\nTesting get documents...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/documents")
        if response.status_code == 200:
            result = response.json()
            print(f"Total documents: {result['total_documents']}")
            return True
        else:
            print(f"Get documents failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Get documents failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Simple RAG System Test ===\n")
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(5)
    
    # Test health
    if not test_health():
        print("Server is not running. Please start the server first.")
        return
    
    # Test upload
    if test_upload_documents():
        print("✓ Document upload successful")
    else:
        print("✗ Document upload failed")
        return
    
    # Test queries
    test_questions = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "What is deep learning?",
        "Explain natural language processing",
        "What is computer vision?"
    ]
    
    for question in test_questions:
        test_query(question)
    
    # Test get documents
    test_get_documents()
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    main() 