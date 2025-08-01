from langgraph.graph import StateGraph, END
from typing import TypedDict
from typing import Optional, Dict, Any
from src.services.movie_service import get_movies_by_genre, get_available_genres, format_movie_recommendations
from src.memory import memory
from config import Config

# --- GROQ LLM Integration ---
from groq import Groq

# Use config for API key
llm = Groq(api_key=Config.GROQ_API_KEY)

# Define state schema
class MovieState(TypedDict):
    user_input: Optional[str]
    message: Optional[str]
    next: Optional[str]

def ask_genre_node(state: MovieState) -> MovieState:
    available_genres = get_available_genres()
    genre_list = ", ".join(available_genres)
    return {
        "user_input": state.get("user_input"),
        "message": f"Enter a movie genre (e.g., {genre_list}):",
        "next": "validate_genre"
    }

def validate_genre_node(state: MovieState) -> MovieState:
    genre = state.get("user_input", "").strip()
    if not genre:
        return {
            "user_input": state.get("user_input"),
            "message": "Genre cannot be empty.",
            "next": "retry"
        }
    
    movies = get_movies_by_genre(genre)
    if not movies:
        return {
            "user_input": state.get("user_input"),
            "message": f"Sorry, no movies found for genre '{genre}'.",
            "next": "retry"
        }
    
    memory.set("last_genre", genre.title())
    memory.set("last_movies", movies)
    return {
        "user_input": state.get("user_input"),
        "message": genre,
        "next": "respond"
    }

def retry_node(state: MovieState) -> MovieState:
    available_genres = get_available_genres()
    genre_list = ", ".join(available_genres)
    return {
        "user_input": state.get("user_input"),
        "message": f"Please enter a valid genre (e.g., {genre_list}):",
        "next": "validate_genre"
    }

def respond_node(state: MovieState) -> MovieState:
    last_genre = memory.get("last_genre", "Unknown")
    last_movies = memory.get("last_movies", [])
    
    # Format the movie recommendations
    formatted_recommendations = format_movie_recommendations(last_movies)
    
    # Use Groq LLM to enhance the response
    prompt = f"Enhance this movie recommendation response to be more engaging and personalized: {formatted_recommendations} (Genre: {last_genre})"
    try:
        llm_response = llm.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        enhanced_message = llm_response.choices[0].message.content
    except Exception as e:
        enhanced_message = f"{formatted_recommendations}\n\n(Genre: {last_genre})\n[LLM error: {e}]"
    
    return {
        "user_input": state.get("user_input"),
        "message": enhanced_message,
        "next": END
    }

# Build the graph
workflow = StateGraph(MovieState)

# Add nodes
workflow.add_node("ask_genre", ask_genre_node)
workflow.add_node("validate_genre", validate_genre_node)
workflow.add_node("retry", retry_node)
workflow.add_node("respond", respond_node)

# Set entry point
workflow.set_entry_point("ask_genre")

# Compile the graph
graph = workflow.compile()

# Helper functions for Streamlit
def validate_genre_and_get_movies(genre: str) -> tuple[bool, str]:
    """
    Validate genre and get movie recommendations. Returns (is_valid, message)
    """
    if not genre.strip():
        return False, "Genre cannot be empty."
    
    movies = get_movies_by_genre(genre)
    if not movies:
        return False, f"Sorry, no movies found for genre '{genre}'."
    
    memory.set("last_genre", genre.title())
    memory.set("last_movies", movies)
    return True, format_movie_recommendations(movies)

def get_enhanced_movie_response(genre: str, recommendations: str) -> str:
    """
    Use Groq LLM to enhance the movie recommendation response
    """
    prompt = f"Enhance this movie recommendation response to be more engaging and personalized: {recommendations} (Genre: {genre})"
    try:
        llm_response = llm.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return llm_response.choices[0].message.content
    except Exception as e:
        return f"{recommendations}\n\n(Genre: {genre})\n[LLM error: {e}]"