#!/usr/bin/env python3
"""
Setup script for Groq API key configuration
"""

import os
import getpass

def setup_groq_api():
    """Setup Groq API key"""
    print("🔑 Groq API Key Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = ".env"
    
    if os.path.exists(env_file):
        print("📄 .env file already exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if "GROQ_API_KEY" in content:
                print("✅ GROQ_API_KEY found in .env file")
                return True
    
    print("📝 Creating .env file...")
    
    # Get API key from user
    print("\n🔑 Please enter your Groq API key:")
    print("💡 Get it from: https://console.groq.com/")
    print("💡 It should start with 'gsk_'")
    
    api_key = getpass.getpass("API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    if not api_key.startswith("gsk_"):
        print("⚠️ Warning: API key should start with 'gsk_'")
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            return False
    
    # Write to .env file
    env_content = f"""# Groq API Key
GROQ_API_KEY={api_key}
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_groq_connection():
    """Test Groq API connection"""
    print("\n🧪 Testing Groq API connection...")
    
    try:
        from dotenv import load_dotenv
        from groq import Groq
        
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            print("❌ GROQ_API_KEY not found in environment")
            return False
        
        client = Groq(api_key=api_key)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Hello, this is a test."}
            ],
            max_tokens=10
        )
        
        print("✅ Groq API connection successful!")
        print(f"✅ Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Groq API test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Groq API Setup for Simple RAG")
    print("=" * 50)
    
    # Setup API key
    if setup_groq_api():
        print("\n✅ API key configured successfully!")
        
        # Test connection
        if test_groq_connection():
            print("\n🎉 Setup complete! You can now run the RAG application.")
            print("\n📋 Next steps:")
            print("1. Start the RAG API: python main.py")
            print("2. Start the Streamlit app: streamlit run simple_rag.py")
        else:
            print("\n❌ API key test failed. Please check your API key.")
    else:
        print("\n❌ Setup failed. Please try again.")

if __name__ == "__main__":
    main() 