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

    def _extraccion(self, endpoint, filtro):  #el endpoint refiere al tipo de dato a extraer: "issues" = cómics; "characters" = personajes, "events" = eventos
        self.control_tiempo()
        req = urllib.request.Request(f"{self.base_url}/{endpoint}/?api_key={self.api_key}&format=json{filtro}", headers=self.headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        self.last_request_time = time.time()
        return data

    def obtener_comics(self, c_id = None):
        ep = "issues"
        if c_id:
            ep = f"issue/4000-{c_id}"
        return self._extraccion(ep, "&filter=publisher:Marvel&field_list=id,isbn,name,issue_number,character_credits,person_credits,event_credits,image")

    def obtener_personajes(self, p_id = None):
        ep = "characters"
        if p_id:
            ep = f"character/4005-{p_id}"
        return self._extraccion(ep, "&field_list=id,name,image,deck,description, ")

    def obtener_eventos(self, e_id = None):
        ep = "events"
        if e_id:
            ep = f"event/4045-{e_id}"
        return self._extraccion(ep, "&field_list=id,name,image,start_year")

    def obtener_autores(self, a_id = None):
        ep = "persons"
        if a_id:
            ep = f"person/4040-{a_id}"
        return self._extraccion(ep, "&field_list=id,name,image")