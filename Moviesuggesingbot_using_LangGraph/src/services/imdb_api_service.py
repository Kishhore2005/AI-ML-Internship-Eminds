import requests
import json
from typing import List, Dict, Any, Optional
from config import Config

class IMDBAPIService:
    """
    Service to interact with the IMDb API
    """
    
    def __init__(self):
        self.base_url = "https://imdb.iamidiotareyoutoo.com"
        self.api_key = Config.IMDB_API_KEY if hasattr(Config, 'IMDB_API_KEY') else None
    
    def search_movie_by_imdb_id(self, imdb_id: str) -> Optional[Dict[str, Any]]:
        """
        Search for a movie by IMDb ID (e.g., tt2250912)
        """
        try:
            url = f"{self.base_url}/search"
            params = {"tt": imdb_id}
            
            response = requests.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("ok") and data.get("short"):
                movie_data = data["short"]
                return self._format_movie_data(movie_data)
            
            return None
            
        except Exception as e:
            print(f"IMDb API Error: {e}")
            return None
    
    def search_movies_by_title(self, title: str) -> List[Dict[str, Any]]:
        """
        Search for movies by title
        """
        try:
            url = f"{self.base_url}/search"
            params = {"q": title}
            
            response = requests.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            movies = []
            
            if data.get("ok") and data.get("short"):
                movie_data = data["short"]
                formatted_movie = self._format_movie_data(movie_data)
                if formatted_movie:
                    movies.append(formatted_movie)
            
            return movies
            
        except Exception as e:
            print(f"IMDb API Error: {e}")
            return []
    
    def get_movies_by_genre(self, genre: str) -> List[Dict[str, Any]]:
        """
        Get movies by genre using IMDb API
        Note: This API doesn't support direct genre search, so we'll use a curated list
        """
        # Expanded list of movies by genre
        genre_movies = {
            "action": [
                "tt2250912",  # Spider-Man: Homecoming
                "tt0468569",  # The Dark Knight
                "tt0133093",  # The Matrix
                "tt0111161",  # The Shawshank Redemption (has action elements)
                "tt0110912",  # Pulp Fiction
            ],
            "comedy": [
                "tt0110912",  # Pulp Fiction
                "tt0137523",  # Fight Club
                "tt0109830",  # Forrest Gump
                "tt0111161",  # The Shawshank Redemption
                "tt0068646",  # The Godfather
            ],
            "drama": [
                "tt0111161",  # The Shawshank Redemption
                "tt0109830",  # Forrest Gump
                "tt0108052",  # Schindler's List
                "tt0068646",  # The Godfather
                "tt0137523",  # Fight Club
            ],
            "horror": [
                "tt0114369",  # Se7en
                "tt0137523",  # Fight Club (psychological horror elements)
                "tt0110912",  # Pulp Fiction (thriller elements)
                "tt0468569",  # The Dark Knight (dark elements)
                "tt0108052",  # Schindler's List (dramatic)
            ],
            "romance": [
                "tt0109830",  # Forrest Gump (romantic elements)
                "tt0111161",  # The Shawshank Redemption (friendship)
                "tt0108052",  # Schindler's List (love story)
                "tt0068646",  # The Godfather (family love)
                "tt0137523",  # Fight Club (relationships)
            ],
            "sci-fi": [
                "tt0133093",  # The Matrix
                "tt2250912",  # Spider-Man: Homecoming (superhero sci-fi)
                "tt0468569",  # The Dark Knight (tech elements)
                "tt0114369",  # Se7en (crime investigation)
                "tt0110912",  # Pulp Fiction (modern setting)
            ],
            "thriller": [
                "tt0114369",  # Se7en
                "tt0137523",  # Fight Club
                "tt0110912",  # Pulp Fiction
                "tt0468569",  # The Dark Knight
                "tt0068646",  # The Godfather
            ],
            "crime": [
                "tt0114369",  # Se7en
                "tt0110912",  # Pulp Fiction
                "tt0068646",  # The Godfather
                "tt0468569",  # The Dark Knight
                "tt0137523",  # Fight Club
            ],
            "documentary": [
                "tt0108052",  # Schindler's List (historical drama)
                "tt0111161",  # The Shawshank Redemption (prison life)
                "tt0109830",  # Forrest Gump (historical events)
                "tt0068646",  # The Godfather (mafia life)
                "tt0137523",  # Fight Club (social commentary)
            ],
            "family": [
                "tt0109830",  # Forrest Gump (family-friendly)
                "tt2250912",  # Spider-Man: Homecoming (superhero family)
                "tt0111161",  # The Shawshank Redemption (friendship)
                "tt0108052",  # Schindler's List (family survival)
                "tt0068646",  # The Godfather (family drama)
            ],
            "adventure": [
                "tt2250912",  # Spider-Man: Homecoming
                "tt0109830",  # Forrest Gump
                "tt0133093",  # The Matrix
                "tt0468569",  # The Dark Knight
                "tt0111161",  # The Shawshank Redemption
            ],
            "animation": [
                "tt2250912",  # Spider-Man: Homecoming (CGI elements)
                "tt0133093",  # The Matrix (special effects)
                "tt0468569",  # The Dark Knight (visual effects)
                "tt0114369",  # Se7en (cinematography)
                "tt0110912",  # Pulp Fiction (stylized)
            ],
            "fantasy": [
                "tt0133093",  # The Matrix (virtual reality)
                "tt2250912",  # Spider-Man: Homecoming (superhero fantasy)
                "tt0468569",  # The Dark Knight (superhero)
                "tt0109830",  # Forrest Gump (magical realism)
                "tt0068646",  # The Godfather (dramatic fantasy)
            ],
            "history": [
                "tt0108052",  # Schindler's List
                "tt0109830",  # Forrest Gump
                "tt0068646",  # The Godfather
                "tt0111161",  # The Shawshank Redemption
                "tt0137523",  # Fight Club
            ],
            "music": [
                "tt0109830",  # Forrest Gump (soundtrack)
                "tt0110912",  # Pulp Fiction (music)
                "tt0137523",  # Fight Club (soundtrack)
                "tt0468569",  # The Dark Knight (score)
                "tt0108052",  # Schindler's List (score)
            ],
            "mystery": [
                "tt0114369",  # Se7en
                "tt0110912",  # Pulp Fiction
                "tt0468569",  # The Dark Knight
                "tt0068646",  # The Godfather
                "tt0137523",  # Fight Club
            ],
            "war": [
                "tt0108052",  # Schindler's List
                "tt0109830",  # Forrest Gump
                "tt0068646",  # The Godfather
                "tt0111161",  # The Shawshank Redemption
                "tt0137523",  # Fight Club
            ],
            "western": [
                "tt0109830",  # Forrest Gump (American journey)
                "tt0111161",  # The Shawshank Redemption (prison)
                "tt0068646",  # The Godfather (family saga)
                "tt0108052",  # Schindler's List (survival)
                "tt0137523",  # Fight Club (modern western)
            ]
        }
        
        # Get movies for the requested genre
        movie_ids = genre_movies.get(genre.lower(), [])
        
        movies = []
        for imdb_id in movie_ids[:5]:  # Get first 5 movies
            movie_data = self.search_movie_by_imdb_id(imdb_id)
            if movie_data:
                movies.append(movie_data)
        
        return movies
    
    def _format_movie_data(self, movie_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Format IMDb API response to our standard format
        """
        try:
            # Extract basic information
            title = movie_data.get("name", "Unknown")
            description = movie_data.get("description", "No description available.")
            
            # Extract year from datePublished
            date_published = movie_data.get("datePublished", "")
            year = date_published[:4] if date_published else "Unknown"
            
            # Extract rating
            aggregate_rating = movie_data.get("aggregateRating", {})
            rating = aggregate_rating.get("ratingValue", 0)
            
            # Extract genres
            genres = movie_data.get("genre", [])
            
            # Extract actors
            actors = movie_data.get("actor", [])
            actor_names = [actor.get("name", "") for actor in actors if actor.get("name")]
            
            # Extract director
            directors = movie_data.get("director", [])
            director_names = [director.get("name", "") for director in directors if director.get("name")]
            
            # Extract runtime
            duration = movie_data.get("duration", "")
            runtime = self._parse_duration(duration)
            
            # Extract poster image
            image = movie_data.get("image", "")
            
            return {
                "title": title,
                "year": year,
                "rating": float(rating) if rating else 0.0,
                "description": description,
                "genres": genres,
                "actors": actor_names,
                "directors": director_names,
                "runtime": runtime,
                "poster_path": image,
                "imdb_id": movie_data.get("imdbId", ""),
                "source": "IMDb API"
            }
            
        except Exception as e:
            print(f"Error formatting movie data: {e}")
            return None
    
    def _parse_duration(self, duration: str) -> str:
        """
        Parse ISO 8601 duration format (PT2H13M) to readable format
        """
        if not duration:
            return "Unknown"
        
        try:
            # Remove PT prefix
            duration = duration.replace("PT", "")
            
            hours = 0
            minutes = 0
            
            if "H" in duration:
                hours_part = duration.split("H")[0]
                hours = int(hours_part)
                duration = duration.split("H")[1]
            
            if "M" in duration:
                minutes_part = duration.split("M")[0]
                minutes = int(minutes_part)
            
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
                
        except:
            return "Unknown"
    
    def _matches_genre(self, movie_data: Dict[str, Any], target_genre: str) -> bool:
        """
        Check if movie matches the target genre
        """
        movie_genres = movie_data.get("genres", [])
        target_genre_lower = target_genre.lower()
        
        for genre in movie_genres:
            if target_genre_lower in genre.lower():
                return True
        
        return False

# Create a global instance
imdb_service = IMDBAPIService() 