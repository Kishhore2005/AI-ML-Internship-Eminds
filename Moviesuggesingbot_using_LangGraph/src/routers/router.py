# This file defines API routes for the Movie Recommendation System.
# It provides endpoints for movie recommendations and related functionality.

from typing import List, Dict, Any
from src.services.movie_service import (
    get_movies_by_genre, 
    get_available_genres, 
    format_movie_recommendations,
    search_movies_by_title,
    get_movie_details
)

def get_movie_recommendations_by_genre(genre: str) -> Dict[str, Any]:
    """
    Get movie recommendations for a given genre.
    Returns a dictionary with recommendations and metadata.
    """
    try:
        movies = get_movies_by_genre(genre)
        formatted_response = format_movie_recommendations(movies)
        
        return {
            "success": True,
            "genre": genre,
            "recommendations": movies,
            "formatted_response": formatted_response,
            "count": len(movies)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "genre": genre,
            "recommendations": [],
            "formatted_response": f"Sorry, I couldn't find movie recommendations for {genre}.",
            "count": 0
        }

def get_available_movie_genres() -> Dict[str, Any]:
    """
    Get list of available movie genres.
    Returns a dictionary with available genres.
    """
    try:
        genres = get_available_genres()
        return {
            "success": True,
            "genres": genres,
            "count": len(genres)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "genres": [],
            "count": 0
        }

def search_movies_by_title_api(title: str) -> Dict[str, Any]:
    """
    Search for movies by title.
    Returns a dictionary with search results.
    """
    try:
        movies = search_movies_by_title(title)
        return {
            "success": True,
            "search_term": title,
            "results": movies,
            "count": len(movies)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "search_term": title,
            "results": [],
            "count": 0
        }

def get_movie_details_api(movie_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific movie.
    Returns a dictionary with movie details.
    """
    try:
        movie_details = get_movie_details(movie_id)
        return {
            "success": True,
            "movie_id": movie_id,
            "details": movie_details
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "movie_id": movie_id,
            "details": {}
        }

# Example usage for FastAPI integration:
# from fastapi import FastAPI, HTTPException
# 
# app = FastAPI()
# 
# @app.get("/movies/genre/{genre}")
# async def get_movies_by_genre_endpoint(genre: str):
#     result = get_movie_recommendations_by_genre(genre)
#     if not result["success"]:
#         raise HTTPException(status_code=500, detail=result["error"])
#     return result
# 
# @app.get("/movies/genres")
# async def get_genres_endpoint():
#     return get_available_movie_genres()
# 
# @app.get("/movies/search")
# async def search_movies_endpoint(title: str):
#     return search_movies_by_title_api(title)
# 
# @app.get("/movies/{movie_id}")
# async def get_movie_details_endpoint(movie_id: int):
#     return get_movie_details_api(movie_id)
