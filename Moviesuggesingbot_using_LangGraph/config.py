import os
from typing import Optional

class Config:
    """
    Configuration class for API keys and settings
    """
    
    # TMDB API Configuration
    TMDB_API_KEY: str = os.getenv("TMDB_API_KEY", "YOUR_TMDB_API_KEY_HERE")
    TMDB_BASE_URL: str = "ur tmdb api key here"
    
    # IMDb API Configuration
    IMDB_API_KEY: str = os.getenv("IMDB_API_KEY", "YOUR_IMDB_API_KEY_HERE")
    IMDB_BASE_URL: str = "movie free open source api key here"
    
    # Groq API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "ur api key here")
    
    # Application Settings
    MAX_MOVIES_PER_GENRE: int = 5
    REQUEST_TIMEOUT: int = 10
    
    # API Selection (TMDB or IMDb)
    USE_IMDB_API: bool = os.getenv("USE_IMDB_API", "false").lower() == "true"
    
    @classmethod
    def is_tmdb_configured(cls) -> bool:
        """Check if TMDB API is properly configured"""
        return cls.TMDB_API_KEY != "YOUR_TMDB_API_KEY_HERE"
    
    @classmethod
    def is_imdb_configured(cls) -> bool:
        """Check if IMDb API is properly configured"""
        return cls.IMDB_API_KEY != "YOUR_IMDB_API_KEY_HERE"
    
    @classmethod
    def is_groq_configured(cls) -> bool:
        """Check if Groq API is properly configured"""
        return cls.GROQ_API_KEY != "YOUR_GROQ_API_KEY_HERE"
    
    @classmethod
    def get_tmdb_api_key(cls) -> Optional[str]:
        """Get TMDB API key if configured"""
        return cls.TMDB_API_KEY if cls.is_tmdb_configured() else None
    
    @classmethod
    def get_imdb_api_key(cls) -> Optional[str]:
        """Get IMDb API key if configured"""
        return cls.IMDB_API_KEY if cls.is_imdb_configured() else None
    
    @classmethod
    def get_groq_api_key(cls) -> Optional[str]:
        """Get Groq API key if configured"""
        return cls.GROQ_API_KEY if cls.is_groq_configured() else None

# Environment variable setup instructions
ENV_SETUP_INSTRUCTIONS = """
To set up your API keys, you can either:

1. Set environment variables:
   export TMDB_API_KEY="your_tmdb_api_key_here"
   export IMDB_API_KEY="your_imdb_api_key_here"
   export GROQ_API_KEY="your_groq_api_key_here"
   export USE_IMDB_API="true"  # Set to "true" to use IMDb API instead of TMDB

2. Or create a .env file in the project root:
   TMDB_API_KEY=your_tmdb_api_key_here
   IMDB_API_KEY=your_imdb_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   USE_IMDB_API=true

3. Or update the config.py file directly with your keys.

Get your free TMDB API key from: https://www.themoviedb.org/settings/api
Get your free Groq API key from: https://console.groq.com/
IMDb API: https://imdb.iamidiotareyoutoo.com (no API key required)
""" 
