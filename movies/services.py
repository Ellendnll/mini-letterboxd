import os
import requests

class TMDBService:
    def __init__(self):
        # Busca a chave da API diretamente do arquivo .env protegido
        self.api_key = os.getenv('TMDB_API_KEY')
        # URL base para todas as consultas da API do TMDB
        self.base_url = 'https://api.themoviedb.org/3'
        # Define o idioma das respostas para Português do Brasil
        self.language = 'pt-BR'

    def search_movies(self, query):
        """Busca filmes pelo título com base no que o usuário digitou"""
        url = f"{self.base_url}/search/movie"
        params = {
            'api_key': self.api_key,
            'query': query,
            'language': self.language
        }
        
        try:
            response = requests.get(url, params=params)
            # Transforma a resposta em JSON
            data = response.json()
            # Retorna apenas a lista de filmes ('results'), ou uma lista vazia se der erro
            return data.get('results', [])
        except requests.RequestException:
            return []

    def get_movie_details(self, movie_id):
        """Busca as informações detalhadas de um filme específico usando o ID dele"""
        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            'api_key': self.api_key,
            'language': self.language
        }
        
        try:
            response = requests.get(url, params=params)
            # Retorna o dicionário com todos os detalhes do filme (sinopse, nota, etc.)
            return response.json()
        except requests.RequestException:
            return None