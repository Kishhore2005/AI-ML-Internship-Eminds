#!/usr/bin/env python3
"""
Setup script for configuring API keys for the Movie Recommendation System
"""

import os
import sys
from config import Config, ENV_SETUP_INSTRUCTIONS

def setup_api_keys():
    """
    Interactive setup for API keys
    """
    print("🎬 Movie Recommendation System - API Setup")
    print("=" * 50)
    
    # Check current configuration
    print("\n📋 Current Configuration:")
    print(f"TMDB API Key: {'✅ Configured' if Config.is_tmdb_configured() else '❌ Not configured'}")
    print(f"IMDb API: {'✅ Enabled' if Config.USE_IMDB_API else '❌ Disabled'}")
    print(f"Groq API Key: {'✅ Configured' if Config.is_groq_configured() else '❌ Not configured'}")
    
    print("\n🔧 Setup Options:")
    print("1. Set up TMDB API key (for real movie data)")
    print("2. Enable IMDb API (no API key required)")
    print("3. Set up Groq API key (for AI responses)")
    print("4. Set up all APIs")
    print("5. Switch between TMDB and IMDb")
    print("6. View setup instructions")
    print("7. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                setup_tmdb_key()
            elif choice == "2":
                setup_imdb_api()
            elif choice == "3":
                setup_groq_key()
            elif choice == "4":
                setup_tmdb_key()
                setup_imdb_api()
                setup_groq_key()
            elif choice == "5":
                switch_api()
            elif choice == "6":
                print("\n📖 Setup Instructions:")
                print(ENV_SETUP_INSTRUCTIONS)
            elif choice == "7":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Setup cancelled. Goodbye!")
            break

def setup_tmdb_key():
    """
    Set up TMDB API key
    """
    print("\n🎬 TMDB API Key Setup")
    print("-" * 30)
    print("1. Go to https://www.themoviedb.org/settings/api")
    print("2. Create a free account if you don't have one")
    print("3. Generate an API key")
    print("4. Copy the API key")
    
    api_key = input("\nEnter your TMDB API key: ").strip()
    
    if api_key:
        # Update config
        Config.TMDB_API_KEY = api_key
        print("✅ TMDB API key configured successfully!")
        
        # Test the API
        print("🧪 Testing API connection...")
        try:
            from src.services.movie_service import get_movies_by_genre
            movies = get_movies_by_genre("action")
            if movies:
                print(f"✅ API test successful! Found {len(movies)} action movies.")
            else:
                print("⚠️ API test completed but no movies found.")
        except Exception as e:
            print(f"❌ API test failed: {e}")
    else:
        print("❌ No API key provided.")

def setup_imdb_api():
    """
    Set up IMDb API (no API key required)
    """
    print("\n🎭 IMDb API Setup")
    print("-" * 30)
    print("IMDb API from https://imdb.iamidiotareyoutoo.com")
    print("No API key required - this is a free service!")
    
    enable = input("\nEnable IMDb API? (y/n): ").strip().lower()
    
    if enable == 'y':
        Config.USE_IMDB_API = True
        print("✅ IMDb API enabled successfully!")
        
        # Test the API
        print("🧪 Testing IMDb API connection...")
        try:
            from src.services.imdb_api_service import imdb_service
            movie = imdb_service.search_movie_by_imdb_id("tt2250912")  # Spider-Man: Homecoming
            if movie:
                print(f"✅ IMDb API test successful! Found: {movie['title']}")
            else:
                print("⚠️ IMDb API test completed but no movie found.")
        except Exception as e:
            print(f"❌ IMDb API test failed: {e}")
    else:
        Config.USE_IMDB_API = False
        print("❌ IMDb API disabled.")

def setup_groq_key():
    """
    Set up Groq API key
    """
    print("\n🤖 Groq API Key Setup")
    print("-" * 30)
    print("1. Go to https://console.groq.com/")
    print("2. Create a free account if you don't have one")
    print("3. Generate an API key")
    print("4. Copy the API key")
    
    api_key = input("\nEnter your Groq API key: ").strip()
    
    if api_key:
        # Update config
        Config.GROQ_API_KEY = api_key
        print("✅ Groq API key configured successfully!")
        
        # Test the API
        print("🧪 Testing API connection...")
        try:
            from groq import Groq
            llm = Groq(api_key=api_key)
            response = llm.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": "Hello"}]
            )
            print("✅ Groq API test successful!")
        except Exception as e:
            print(f"❌ Groq API test failed: {e}")
    else:
        print("❌ No API key provided.")

def switch_api():
    """
    Switch between TMDB and IMDb APIs
    """
    print("\n🔄 API Selection")
    print("-" * 30)
    print(f"Current API: {'IMDb' if Config.USE_IMDB_API else 'TMDB'}")
    print("1. Use TMDB API (requires API key)")
    print("2. Use IMDb API (no API key required)")
    
    choice = input("\nSelect API (1-2): ").strip()
    
    if choice == "1":
        Config.USE_IMDB_API = False
        print("✅ Switched to TMDB API")
    elif choice == "2":
        Config.USE_IMDB_API = True
        print("✅ Switched to IMDb API")
    else:
        print("❌ Invalid choice.")

def create_env_file():
    """
    Create a .env file with the current configuration
    """
    env_content = f"""# Movie Recommendation System Environment Variables
TMDB_API_KEY={Config.TMDB_API_KEY}
IMDB_API_KEY={Config.IMDB_API_KEY}
GROQ_API_KEY={Config.GROQ_API_KEY}
USE_IMDB_API={str(Config.USE_IMDB_API).lower()}
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")

if __name__ == "__main__":
    setup_api_keys()
    
    # Offer to create .env file
    if Config.is_tmdb_configured() or Config.is_groq_configured() or Config.USE_IMDB_API:
        create_env = input("\n📝 Create .env file with current configuration? (y/n): ").strip().lower()
        if create_env == 'y':
            create_env_file()
    
    print("\n🎉 Setup complete! You can now run: streamlit run main.py") 