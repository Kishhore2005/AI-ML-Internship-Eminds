# Movie recommendation functions have been moved to src/services/movie_service.py
# This file maintains consistency with the original project structure

from src.services.movie_service import get_movies_by_genre, get_available_genres, format_movie_recommendations

def get_movie_recommendations(genre: str) -> str:
    """
    Get movie recommendations for a given genre.
    This is a wrapper function for the movie service.
    """
    movies = get_movies_by_genre(genre)
    return format_movie_recommendations(movies) 