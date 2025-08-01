import requests
import json

# Base URL for the FastAPI server
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("✅ Health check:", response.json())
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_models():
    """Test the models endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/models")
        print("✅ Models:", response.json())
        return True
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def test_vector_store_info():
    """Test the vector store info endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/vector-store-info")
        print("✅ Vector store info:", response.json())
        return True
    except Exception as e:
        print(f"❌ Vector store info test failed: {e}")
        return False

def test_query_without_upload():
    """Test querying without uploading a document first"""
    try:
        data = {
            "question": "What is this document about?",
            "k": 4,
            "model_name": "llama3-8b-8192"
        }
        response = requests.post(f"{BASE_URL}/query", json=data)
        print("✅ Query without upload (expected error):", response.json())
        return True
    except Exception as e:
        print(f"❌ Query test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing FastAPI RAG Application")
    print("=" * 50)
    
    # Test health endpoint
    test_health()
    
    # Test models endpoint
    test_models()
    
    # Test vector store info
    test_vector_store_info()
    
    # Test query without upload
    test_query_without_upload()
    
    print("\n" + "=" * 50)
    print("📖 To test file upload, use the interactive docs at:")
    print(f"   {BASE_URL}/docs")
    print("\n🚀 To run the server:")
    print("   python fastapi_main.py")

if __name__ == "__main__":
    main() 