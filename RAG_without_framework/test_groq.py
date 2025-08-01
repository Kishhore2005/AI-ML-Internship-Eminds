#!/usr/bin/env python3
"""
Test Groq API key
"""

import os
from dotenv import load_dotenv
from groq import Groq

def test_groq():
    """Test Groq API"""
    print("🧪 Testing Groq API...")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    print(f"🔑 Found API key: {api_key[:10]}...")
    
    try:
        client = Groq(api_key=api_key)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Say hello"}
            ],
            max_tokens=20
        )
        
        print("✅ API key works!")
        print(f"✅ Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        
        if "401" in str(e):
            print("💡 This is an authentication error. Please check:")
            print("   1. Your API key is correct")
            print("   2. Your API key starts with 'gsk_'")
            print("   3. Your API key is not expired")
            print("   4. You have credits in your Groq account")
        
        return False

if __name__ == "__main__":
    success = test_groq()
    if success:
        print("\n🎉 Your Groq API is working! You can now run the RAG app.")
    else:
        print("\n❌ Please fix the API key issue before running the RAG app.") 