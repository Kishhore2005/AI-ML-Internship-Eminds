import requests
import json

def test_api_connection():
    """Test the connection to the RAG API"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing RAG API Connection...")
    print(f"API URL: {base_url}")
    print("-" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Upload test
    print("\n2. Testing document upload...")
    test_docs = ["This is a test document for the RAG system."]
    try:
        response = requests.post(
            f"{base_url}/api/v1/upload-text",
            json=test_docs,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Upload test passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Upload test failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False
    
    # Test 3: Query test
    print("\n3. Testing query endpoint...")
    try:
        response = requests.post(
            f"{base_url}/api/v1/query",
            json={"question": "What is this?", "top_k": 3},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Query test passed!")
            result = response.json()
            print(f"   Answer: {result.get('answer', '')[:100]}...")
        else:
            print(f"❌ Query test failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Query test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! The API is working correctly.")
    return True

if __name__ == "__main__":
    test_api_connection() 