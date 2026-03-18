# Aqui vaos a controlar la API de Comic Vine, quiere decir
#aqui vamos a hacer las consultas, obtener datos, procesar los comics y asi,
#para esto cada uhno debe solicitar su API en comic vine :D

class ComicVineAPI:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://comicvine.gamespot.com/api"
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 5 peticiones por segundo para que nos nos vanee comic vine xd

        # Headers para que Comic Vine nos acepte
        self.headers = {"User-Agent': 'Proyecto_Marvel/1.0 (Proyecto Universitario)"}