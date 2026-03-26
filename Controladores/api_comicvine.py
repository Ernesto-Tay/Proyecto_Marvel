# Aqui vaos a controlar la API de Comic Vine, quiere decir
# aqui vamos a hacer las consultas, obtener datos, procesar los comics y asi,
# para esto cada uhno debe solicitar su API en comic vine :D
import urllib.request
import urllib.parse
import json
import time


class ComicVineAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://comicvine.gamespot.com/api"
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 5 peticiones por segundo
        self.last_error = None

        # Headers para que Comic Vine nos acepte
        self.headers = {"User-Agent": "Proyecto_Marvel/1.0 (Proyecto Universitario)"}

    def control_tiempo(self):
        lapso = time.time() - self.last_request_time
        if lapso < self.min_request_interval:
            time.sleep(self.min_request_interval - lapso)

    def _extraccion(self, endpoint, filtro):
        self.control_tiempo()
        self.last_error = None
        req = urllib.request.Request(f"{self.base_url}/{endpoint}/?api_key={self.api_key}&format=json{filtro}",headers=self.headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        self.last_request_time = time.time()

        status = data.get("status_code")
        if status not in (None, 1):
            api_error = data.get("error", "Error desconocido de ComicVine")
            self.last_error = f"ComicVine status_code={status}: {api_error}"
            raise RuntimeError(self.last_error)

        results = data.get("results")
        if isinstance(results, list):
            return results
        if isinstance(results, dict):
            return [results]
        return []

    def obtener_comics(self, c_id=None):
        ep = "issues"
        if c_id:
            ep = f"issue/4000-{c_id}"
        return self._extraccion(
            ep,
            "&filter=publisher:Marvel&field_list=id,isbn,name,issue_number,character_credits,person_credits,event_credits,cover_date,image&limit=60",
        )

    def _buscar_personajes_por_nombre(self, nombre):
        nombre_q = urllib.parse.quote(str(nombre))
        return self._extraccion(
            "search",
            f"&resources=character&query={nombre_q}"
            "&field_list=id,name,image,deck,description,creator_credits,event_credits,issue_credits,publisher"
            "&limit=10",
        )

    def obtener_personajes(self, p_id=None, modo="general"):
        ep = "characters"
        if p_id:
            ep = f"character/4005-{p_id}"
            return self._extraccion(
                ep,
                "&field_list=id,name,image,deck,description,creator_credits,event_credits,issue_credits,publisher",
            )

        if modo == "ucm":
            # Priorizacion por personajes populares del UCM/Marvel para evitar listados aleatorios.
            favoritos = [
                "Spider-Man",
                "Iron Man",
                "Captain America",
                "Thor",
                "Hulk",
                "Black Widow",
                "Doctor Strange",
                "Scarlet Witch",
                "Loki",
                "Black Panther",
                "Captain Marvel",
                "Ant-Man",
                "Wasp",
                "Hawkeye",
                "Vision",
                "Winter Soldier",
                "Star-Lord",
                "Gamora",
                "Rocket Raccoon",
                "Groot",
            ]
            salida = []
            vistos = set()
            for nombre in favoritos:
                try:
                    resultados = self._buscar_personajes_por_nombre(nombre)
                except Exception:
                    continue
                for item in resultados:
                    pid = item.get("id")
                    if not pid or pid in vistos:
                        continue
                    pub = (item.get("publisher") or {}).get("name")
                    if pub and pub != "Marvel":
                        continue
                    salida.append(item)
                    vistos.add(pid)
                    break
            if salida:
                return salida

        # Traer paginas para no quedarnos en un solo bloque.
        acumulado = []
        page_size = 100
        max_pages = 2
        for pagina in range(max_pages):
            offset = pagina * page_size
            lote = self._extraccion(
                ep,
                f"&field_list=id,name,image,deck,description,creator_credits,event_credits,issue_credits,publisher"
                f"&sort=name:asc&limit={page_size}&offset={offset}",
            )
            if not lote:
                break
            acumulado.extend(lote)
            if len(lote) < page_size:
                break
        return acumulado

    def obtener_eventos(self, e_id=None):
        ep = "events"
        if e_id:
            ep = f"event/4045-{e_id}"
        return self._extraccion(ep, "&field_list=id,name,image,deck,start_year")

    def obtener_creadores(self, a_id=None):
        ep = "persons"
        if a_id:
            ep = f"person/4040-{a_id}"
        return self._extraccion(ep, "&field_list=id,name,image")
