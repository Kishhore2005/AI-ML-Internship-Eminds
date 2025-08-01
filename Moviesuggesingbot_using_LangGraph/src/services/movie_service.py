import requests
import random
import os
from typing import List, Dict, Any
from config import Config
from src.services.imdb_api_service import imdb_service

# Genre mapping for TMDB API
GENRE_MAPPING = {
    "action": 28,
    "comedy": 35,
    "drama": 18,
    "horror": 27,
    "romance": 10749,
    "sci-fi": 878,
    "thriller": 53,
    "adventure": 12,
    "animation": 16,
    "crime": 80,
    "documentary": 99,
    "family": 10751,
    "fantasy": 14,
    "history": 36,
    "music": 10402,
    "mystery": 9648,
    "war": 10752,
    "western": 37
}

def get_movies_by_genre(genre: str) -> List[Dict[str, Any]]:
    """
    Fetches movie recommendations for a given genre using TMDB or IMDb API.
    Returns a list of movie recommendations or empty list if not found.
    """
    # Normalize genre input
    genre_lower = genre.lower().strip()
    
    # Check which API to use
    if Config.USE_IMDB_API:
        return get_movies_from_imdb_api(genre_lower)
    else:
        return get_movies_from_tmdb_api(genre_lower)

def get_movies_from_imdb_api(genre: str) -> List[Dict[str, Any]]:
    """
    Get movies using IMDb API
    """
    try:
        movies = imdb_service.get_movies_by_genre(genre)
        
        # If IMDb API returns no movies, fall back to mock database
        if not movies:
            print(f"No movies found for genre '{genre}' in IMDb API, using fallback database")
            return get_movies_from_mock_database(genre)
        
        return movies
        
    except Exception as e:
        print(f"IMDb API Error: {e}")
        print("Falling back to mock database...")
        return get_movies_from_mock_database(genre)

def get_movies_from_tmdb_api(genre: str) -> List[Dict[str, Any]]:
    """
    Get movies using TMDB API
    """
    # Check if we have a valid API key
    if not Config.is_tmdb_configured():
        # Fallback to mock database if no API key is provided
        return get_movies_from_mock_database(genre)
    
    # Get genre ID from mapping
    genre_id = GENRE_MAPPING.get(genre)
    if not genre_id:
        return []
    
    try:
        # Fetch movies by genre from TMDB API
        url = f"{Config.TMDB_BASE_URL}/discover/movie"
        params = {
            "api_key": Config.TMDB_API_KEY,
            "with_genres": genre_id,
            "sort_by": "popularity.desc",
            "language": "en-US",
            "page": 1
        }
        
        response = requests.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        movies = data.get("results", [])
        
        # Format movies for our application
        formatted_movies = []
        for movie in movies[:Config.MAX_MOVIES_PER_GENRE]:  # Get top movies
            formatted_movie = {
                "title": movie.get("title", "Unknown"),
                "year": movie.get("release_date", "")[:4] if movie.get("release_date") else "Unknown",
                "rating": round(movie.get("vote_average", 0), 1),
                "description": movie.get("overview", "No description available."),
                "poster_path": movie.get("poster_path"),
                "tmdb_id": movie.get("id"),
                "source": "TMDB API"
            }
            formatted_movies.append(formatted_movie)
        
        return formatted_movies
        
    except requests.RequestException as e:
        print(f"TMDB API Error: {e}")
        # Fallback to mock database on API error
        return get_movies_from_mock_database(genre)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return get_movies_from_mock_database(genre)

def get_movies_from_mock_database(genre: str) -> List[Dict[str, Any]]:
    """
    Fallback mock database for when API is unavailable
    """
    movie_database = {
        "action": [
            {"title": "Mad Max: Fury Road", "year": 2015, "rating": 8.1, "description": "A post-apocalyptic action film with stunning visuals and non-stop action sequences."},
            {"title": "John Wick", "year": 2014, "rating": 7.4, "description": "A retired hitman seeks revenge after his dog is killed."},
            {"title": "Mission: Impossible - Fallout", "year": 2018, "rating": 7.7, "description": "Ethan Hunt and his team race against time to prevent a global catastrophe."},
            {"title": "The Dark Knight", "year": 2008, "rating": 9.0, "description": "Batman faces his greatest challenge when the Joker wreaks havoc on Gotham City."},
            {"title": "Die Hard", "year": 1988, "rating": 8.2, "description": "An action classic where a cop battles terrorists in a skyscraper."}
        ],
        "comedy": [
            {"title": "The Grand Budapest Hotel", "year": 2014, "rating": 8.1, "description": "A whimsical comedy about a legendary concierge and his young protégé."},
            {"title": "Superbad", "year": 2007, "rating": 7.6, "description": "Two high school friends try to score alcohol for a party."},
            {"title": "Shaun of the Dead", "year": 2004, "rating": 7.9, "description": "A comedy horror about a man trying to survive a zombie apocalypse."},
            {"title": "The Hangover", "year": 2009, "rating": 7.7, "description": "Three friends wake up from a bachelor party with no memory of the night before."},
            {"title": "Bridesmaids", "year": 2011, "rating": 6.8, "description": "A comedy about a maid of honor who tries to keep her best friend's wedding on track."}
        ],
        "drama": [
            {"title": "The Shawshank Redemption", "year": 1994, "rating": 9.3, "description": "A powerful drama about hope and friendship in prison."},
            {"title": "Forrest Gump", "year": 1994, "rating": 8.8, "description": "The life story of a simple man who witnesses and influences major events in American history."},
            {"title": "The Green Mile", "year": 1999, "rating": 8.6, "description": "A touching drama about a death row guard and a special inmate."},
            {"title": "Schindler's List", "year": 1993, "rating": 8.9, "description": "A powerful true story about a man who saved thousands of Jews during the Holocaust."},
            {"title": "12 Angry Men", "year": 1957, "rating": 8.9, "description": "A jury deliberates the fate of a young man accused of murder."}
        ],
        "horror": [
            {"title": "The Shining", "year": 1980, "rating": 8.4, "description": "A psychological horror about a family isolated in a haunted hotel."},
            {"title": "A Quiet Place", "year": 2018, "rating": 7.5, "description": "A family must live in silence to avoid creatures that hunt by sound."},
            {"title": "Get Out", "year": 2017, "rating": 7.7, "description": "A social thriller about a young black man meeting his white girlfriend's family."},
            {"title": "Hereditary", "year": 2018, "rating": 7.3, "description": "A family tragedy leads to terrifying supernatural events."},
            {"title": "The Conjuring", "year": 2013, "rating": 7.5, "description": "Paranormal investigators help a family terrorized by a dark presence."}
        ],
        "romance": [
            {"title": "The Notebook", "year": 2004, "rating": 7.8, "description": "A romantic story about a couple whose love spans decades."},
            {"title": "La La Land", "year": 2016, "rating": 8.0, "description": "A musical romance about an aspiring actress and a jazz musician."},
            {"title": "Eternal Sunshine of the Spotless Mind", "year": 2004, "rating": 8.3, "description": "A unique love story about erasing memories of a relationship."},
            {"title": "Before Sunrise", "year": 1995, "rating": 8.1, "description": "Two strangers spend one magical night together in Vienna."},
            {"title": "500 Days of Summer", "year": 2009, "rating": 7.7, "description": "A non-linear romantic comedy about the ups and downs of a relationship."}
        ],
        "sci-fi": [
            {"title": "Inception", "year": 2010, "rating": 8.8, "description": "A thief who steals corporate secrets through dream-sharing technology."},
            {"title": "Interstellar", "year": 2014, "rating": 8.6, "description": "A team of explorers travel through a wormhole in space."},
            {"title": "The Matrix", "year": 1999, "rating": 8.7, "description": "A computer programmer discovers a mysterious world of digital reality."},
            {"title": "Blade Runner", "year": 1982, "rating": 8.1, "description": "A detective hunts down replicants in a dystopian future."},
            {"title": "Arrival", "year": 2016, "rating": 7.9, "description": "A linguist works with the military to communicate with alien visitors."}
        ],
        "thriller": [
            {"title": "Gone Girl", "year": 2014, "rating": 8.1, "description": "A psychological thriller about a woman who disappears on her fifth wedding anniversary."},
            {"title": "The Silence of the Lambs", "year": 1991, "rating": 8.6, "description": "An FBI trainee seeks the help of a cannibal killer to catch another serial killer."},
            {"title": "Se7en", "year": 1995, "rating": 8.6, "description": "Two detectives hunt a serial killer who uses the seven deadly sins as his motives."},
            {"title": "Fight Club", "year": 1999, "rating": 8.8, "description": "An insomniac office worker forms an underground fight club."},
            {"title": "Prisoners", "year": 2013, "rating": 8.1, "description": "A father takes matters into his own hands when his daughter goes missing."}
        ],
        "crime": [
            {"title": "The Godfather", "year": 1972, "rating": 9.2, "description": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son."},
            {"title": "Goodfellas", "year": 1990, "rating": 8.7, "description": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen."},
            {"title": "Pulp Fiction", "year": 1994, "rating": 8.9, "description": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption."},
            {"title": "The Departed", "year": 2006, "rating": 8.5, "description": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang."},
            {"title": "Heat", "year": 1995, "rating": 8.2, "description": "A group of professional bank robbers start to feel the heat from police when they unknowingly leave a clue."}
        ],
        "documentary": [
            {"title": "Planet Earth", "year": 2006, "rating": 9.4, "description": "A documentary series about the planet's most beautiful and awe-inspiring natural wonders."},
            {"title": "The Last Dance", "year": 2020, "rating": 9.1, "description": "Charting the rise of the 1990's Chicago Bulls, led by Michael Jordan."},
            {"title": "Making a Murderer", "year": 2015, "rating": 8.5, "description": "Filmed over a 10-year period, Steven Avery, a DNA exoneree who, while in the midst of exposing corruption."},
            {"title": "The Act of Killing", "year": 2012, "rating": 8.2, "description": "A documentary which challenges former Indonesian death-squad leaders to reenact their mass-killings."},
            {"title": "Citizenfour", "year": 2014, "rating": 8.0, "description": "A documentarian and a reporter travel to Hong Kong for the first of many meetings with Edward Snowden."}
        ],
        "family": [
            {"title": "Toy Story", "year": 1995, "rating": 8.3, "description": "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy."},
            {"title": "Finding Nemo", "year": 2003, "rating": 8.1, "description": "After his son is captured in the Great Barrier Reef and taken to Sydney, a timid clownfish sets out on a journey to bring him home."},
            {"title": "The Lion King", "year": 1994, "rating": 8.5, "description": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself."},
            {"title": "Up", "year": 2009, "rating": 8.2, "description": "78-year-old Carl Fredricksen travels to Paradise Falls in his house equipped with balloons."},
            {"title": "Inside Out", "year": 2015, "rating": 8.1, "description": "After young Riley is uprooted from her Midwest life and moved to San Francisco, her emotions conflict on how to adapt."}
        ],
        "adventure": [
            {"title": "Indiana Jones and the Raiders of the Lost Ark", "year": 1981, "rating": 8.4, "description": "Archaeologist and adventurer Indiana Jones is hired by the U.S. government to find the Ark of the Covenant."},
            {"title": "The Lord of the Rings: The Fellowship of the Ring", "year": 2001, "rating": 8.8, "description": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring."},
            {"title": "Jurassic Park", "year": 1993, "rating": 8.5, "description": "A pragmatic paleontologist touring an almost complete theme park on an island in Central America."},
            {"title": "Pirates of the Caribbean: The Curse of the Black Pearl", "year": 2003, "rating": 8.0, "description": "Blacksmith Will Turner teams up with eccentric pirate Captain Jack Sparrow to save his love."},
            {"title": "The Princess Bride", "year": 1987, "rating": 8.0, "description": "While home sick in bed, a young boy's grandfather reads him the story of a farmboy-turned-pirate."}
        ],
        "animation": [
            {"title": "Spirited Away", "year": 2001, "rating": 8.6, "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods."},
            {"title": "Spider-Man: Into the Spider-Verse", "year": 2018, "rating": 8.4, "description": "Teen Miles Morales becomes Spider-Man of his reality, crossing his path with five counterparts."},
            {"title": "Coco", "year": 2017, "rating": 8.4, "description": "Aspiring musician Miguel, confronted with his family's ancestral ban on music, enters the Land of the Dead."},
            {"title": "Zootopia", "year": 2016, "rating": 8.0, "description": "In a city of anthropomorphic animals, a rookie bunny cop and a cynical con artist fox must work together."},
            {"title": "Moana", "year": 2016, "rating": 7.6, "description": "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches an impetuous Chieftain's daughter's island."}
        ],
        "fantasy": [
            {"title": "The Lord of the Rings: The Return of the King", "year": 2003, "rating": 8.9, "description": "Gandalf and Aragorn lead the World of Men against evil Sauron to aid Frodo's quest to destroy the One Ring."},
            {"title": "Harry Potter and the Sorcerer's Stone", "year": 2001, "rating": 7.6, "description": "An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself."},
            {"title": "The Wizard of Oz", "year": 1939, "rating": 8.0, "description": "Dorothy Gale is swept away from a farm in Kansas to a magical land of Oz in a tornado."},
            {"title": "Pan's Labyrinth", "year": 2006, "rating": 8.2, "description": "In the falangist Spain of 1944, the bookish young stepdaughter of a sadistic army officer escapes into an eerie but captivating fantasy world."},
            {"title": "The Princess Bride", "year": 1987, "rating": 8.0, "description": "While home sick in bed, a young boy's grandfather reads him the story of a farmboy-turned-pirate."}
        ],
        "history": [
            {"title": "Schindler's List", "year": 1993, "rating": 8.9, "description": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce."},
            {"title": "Saving Private Ryan", "year": 1998, "rating": 8.6, "description": "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper."},
            {"title": "The Pianist", "year": 2002, "rating": 8.5, "description": "A Polish Jewish musician struggles to survive the destruction of the Warsaw ghetto of World War II."},
            {"title": "Apollo 13", "year": 1995, "rating": 7.6, "description": "NASA must devise a strategy to return Apollo 13 to Earth safely after the spacecraft undergoes massive internal damage."},
            {"title": "Lincoln", "year": 2012, "rating": 7.3, "description": "As the Civil War continues to rage, America's president struggles with continuing carnage on the battlefield."}
        ],
        "music": [
            {"title": "La La Land", "year": 2016, "rating": 8.0, "description": "A jazz pianist falls for an aspiring actress in Los Angeles."},
            {"title": "The Sound of Music", "year": 1965, "rating": 8.0, "description": "A woman leaves an Austrian convent to become a governess to the children of a Naval officer widower."},
            {"title": "Bohemian Rhapsody", "year": 2018, "rating": 7.9, "description": "The story of the legendary British rock band Queen and lead singer Freddie Mercury."},
            {"title": "A Star Is Born", "year": 2018, "rating": 7.6, "description": "A seasoned musician discovers and falls in love with a struggling artist."},
            {"title": "Moulin Rouge!", "year": 2001, "rating": 7.6, "description": "A poet falls for a beautiful courtesan whom a jealous duke covets."}
        ],
        "mystery": [
            {"title": "The Sixth Sense", "year": 1999, "rating": 8.1, "description": "A boy who communicates with spirits seeks the help of a disheartened child psychologist."},
            {"title": "Gone Girl", "year": 2014, "rating": 8.1, "description": "A woman disappears on the day of her fifth wedding anniversary."},
            {"title": "The Usual Suspects", "year": 1995, "rating": 8.5, "description": "A sole survivor tells of the twisty events leading up to a horrific gun battle on a boat."},
            {"title": "Memento", "year": 2000, "rating": 8.4, "description": "A man with short-term memory loss attempts to track down his wife's murderer."},
            {"title": "The Prestige", "year": 2006, "rating": 8.2, "description": "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion."}
        ],
        "war": [
            {"title": "Saving Private Ryan", "year": 1998, "rating": 8.6, "description": "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper."},
            {"title": "Full Metal Jacket", "year": 1987, "rating": 8.3, "description": "A pragmatic U.S. Marine observes the dehumanizing effects the Vietnam War has on his fellow recruits."},
            {"title": "Apocalypse Now", "year": 1979, "rating": 8.4, "description": "A U.S. Army officer serving in Vietnam is tasked with assassinating a renegade Special Forces Colonel."},
            {"title": "Platoon", "year": 1986, "rating": 8.1, "description": "A young soldier in Vietnam faces a moral crisis when confronted with the horrors of war."},
            {"title": "The Hurt Locker", "year": 2008, "rating": 7.5, "description": "During the Iraq War, a Sergeant recently assigned to an army bomb squad is put at odds with his squad mates."}
        ],
        "western": [
            {"title": "The Good, the Bad and the Ugly", "year": 1966, "rating": 8.8, "description": "A bounty hunting scam joins two men in an uneasy alliance against a third in a race to find a fortune in gold buried in a remote cemetery."},
            {"title": "Unforgiven", "year": 1992, "rating": 8.2, "description": "Retired Old West gunslinger William Munny reluctantly takes on one last job."},
            {"title": "Django Unchained", "year": 2012, "rating": 8.4, "description": "With the help of a German bounty hunter, a freed slave sets out to rescue his wife from a brutal Mississippi plantation owner."},
            {"title": "True Grit", "year": 2010, "rating": 7.6, "description": "A stubborn teenager enlists the help of a tough U.S. Marshal to track down her father's murderer."},
            {"title": "3:10 to Yuma", "year": 2007, "rating": 7.7, "description": "A small-time rancher agrees to hold a captured outlaw who's awaiting a train to go to court."}
        ]
    }
    
    if genre in movie_database:
        return random.sample(movie_database[genre], min(3, len(movie_database[genre])))
    else:
        return []

def get_available_genres() -> List[str]:
    """
    Returns a list of available movie genres
    """
    return list(GENRE_MAPPING.keys())

def format_movie_recommendations(movies: List[Dict[str, Any]]) -> str:
    """
    Formats a list of movies into a readable string
    """
    if not movies:
        return "No movies found for this genre."
    
    result = "Here are some great movie recommendations:\n\n"
    for i, movie in enumerate(movies, 1):
        # Handle different movie data formats
        title = movie.get("title", "Unknown")
        year = movie.get("year", "Unknown")
        rating = movie.get("rating", 0)
        description = movie.get("description", "No description available.")
        source = movie.get("source", "Unknown")
        
        # Format rating
        if isinstance(rating, (int, float)):
            rating_str = f"⭐ {rating}/10"
        else:
            rating_str = "⭐ N/A"
        
        result += f"{i}. **{title}** ({year}) - {rating_str}\n"
        result += f"   {description}\n"
        
        # Add additional info if available
        if movie.get("actors"):
            actors = ", ".join(movie["actors"][:3])  # Show first 3 actors
            result += f"   **Cast:** {actors}\n"
        
        if movie.get("runtime") and movie["runtime"] != "Unknown":
            result += f"   **Runtime:** {movie['runtime']}\n"
        
        result += f"   **Source:** {source}\n\n"
    
    return result

def search_movies_by_title(title: str) -> List[Dict[str, Any]]:
    """
    Search for movies by title using the configured API
    """
    if Config.USE_IMDB_API:
        return imdb_service.search_movies_by_title(title)
    else:
        return search_movies_by_title_tmdb(title)

def search_movies_by_title_tmdb(title: str) -> List[Dict[str, Any]]:
    """
    Search for movies by title using TMDB API
    """
    if not Config.is_tmdb_configured():
        return []
    
    try:
        url = f"{Config.TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": Config.TMDB_API_KEY,
            "query": title,
            "language": "en-US",
            "page": 1
        }
        
        response = requests.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        movies = data.get("results", [])
        
        formatted_movies = []
        for movie in movies[:5]:
            formatted_movie = {
                "title": movie.get("title", "Unknown"),
                "year": movie.get("release_date", "")[:4] if movie.get("release_date") else "Unknown",
                "rating": round(movie.get("vote_average", 0), 1),
                "description": movie.get("overview", "No description available."),
                "poster_path": movie.get("poster_path"),
                "tmdb_id": movie.get("id"),
                "source": "TMDB API"
            }
            formatted_movies.append(formatted_movie)
        
        return formatted_movies
        
    except Exception as e:
        print(f"Search error: {e}")
        return []

def get_movie_details(movie_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific movie
    """
    if not Config.is_tmdb_configured():
        return {}
    
    try:
        url = f"{Config.TMDB_BASE_URL}/movie/{movie_id}"
        params = {
            "api_key": Config.TMDB_API_KEY,
            "language": "en-US"
        }
        
        response = requests.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        
        movie = response.json()
        
        return {
            "title": movie.get("title", "Unknown"),
            "year": movie.get("release_date", "")[:4] if movie.get("release_date") else "Unknown",
            "rating": round(movie.get("vote_average", 0), 1),
            "description": movie.get("overview", "No description available."),
            "runtime": movie.get("runtime", 0),
            "genres": [genre["name"] for genre in movie.get("genres", [])],
            "poster_path": movie.get("poster_path"),
            "backdrop_path": movie.get("backdrop_path"),
            "budget": movie.get("budget", 0),
            "revenue": movie.get("revenue", 0),
            "source": "TMDB API"
        }
        
    except Exception as e:
        print(f"Movie details error: {e}")
        return {} 