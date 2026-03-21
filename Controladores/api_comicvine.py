# Aqui vaos a controlar la API de Comic Vine, quiere decir
#aqui vamos a hacer las consultas, obtener datos, procesar los comics y asi,
#para esto cada uhno debe solicitar su API en comic vine :D
import urllib.request
import json
import time

class ComicVineAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://comicvine.gamespot.com/api"
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 5 peticiones por segundo para que nos nos vanee comic vine xd

        # Headers para que Comic Vine nos acepte
        self.headers = {"User-Agent": "Proyecto_Marvel/1.0 (Proyecto Universitario)"}

    def control_tiempo(self):
        lapso = time.time() -  self.last_request_time
        if lapso < self.min_request_interval:
            time.sleep(self.min_request_interval-lapso)

    def extraccion(self, endpoint):  #el endpoint refiere al tipo de dato a extraer: "issues" = cómics; "characters" = personajes, "events" = eventos
        self.control_tiempo()
        req = urllib.request.Request(f"{self.base_url}/{endpoint}/?api_key={self.api_key}&format=json&filter=publisher:Marvel", headers=self.headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        self.last_request_time = time.time()
        return data