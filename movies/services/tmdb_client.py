import requests
from django.conf import settings

TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_BASE_URL = settings.TMDB_API_BASE_URL

class TMDBClient:
    def __init__(self, api_key: str = TMDB_API_KEY, base_url: str = TMDB_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
    
    def _get(self, endpoint: str, params: dict = None):
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        params.setdefault('language', 'en-US')

        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_movie_detail(self, tmdb_id: int):
        return self._get(f"/movie/{tmdb_id}")
    
    def get_popular_movies(self, page: int = 1):
        return self._get("/movie/popular", params={"page": page})
    
    def search_movies(self, query: str, page: int = 1):
        return self._get('/search/movie', params={"query": query, "page": page})
    