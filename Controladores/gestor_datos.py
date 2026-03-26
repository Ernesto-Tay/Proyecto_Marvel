# Las siguientes clases funcionan como cache del sistema para optimizar procesos.
from Modelos.__init__ import Creador, Comic, Evento, Personaje
from Estructuras_Listas.init import ListaDoble
import json
from PyQt6.QtCore import pyqtSignal, QObject
import urllib.request
import os
import traceback
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder = os.path.join(BASE_DIR, "Datos_json")
IMGS_DIR = os.path.join(BASE_DIR, "imgs")
MAX_CACHE_COMICS = 60
MAX_CACHE_PERSONAJES = 400
MAX_CACHE_CREADORES = 400
MAX_CACHE_EVENTOS = 400


def _limitar_diccionario(diccionario, max_items):
    if not isinstance(diccionario, dict) or len(diccionario) <= max_items:
        return diccionario
    # Conserva los elementos mas recientes segun orden de insercion.
    return dict(list(diccionario.items())[-max_items:])


class DescargadorImagenes:
    """
    Clase dedicada a descargar imagenes de URLs y guardarlas localmente.
    """

    def __init__(self, carpeta_destino=IMGS_DIR):
        self.carpeta_destino = carpeta_destino
        self.headers = {"User-Agent": "Proyecto_Marvel/1.0 (Proyecto Universitario)"}
        os.makedirs(self.carpeta_destino, exist_ok=True)

    def descargar(self, url):
        """
        Descarga la imagen de la URL y la guarda.
        Retorna una tupla: (URL_ComicVine, Ruta_Local)
        """
        if not url:
            return (None, None)

        nombre_archivo = url.split("/")[-1]
        ruta_local = os.path.join(self.carpeta_destino, nombre_archivo)
        if not os.path.exists(ruta_local):
            try:
                req = urllib.request.Request(url, headers=self.headers)
                with urllib.request.urlopen(req) as response:
                    with open(ruta_local, "wb") as f:
                        f.write(response.read())
            except Exception as e:
                print(f"Hubo un error al descargar la imagen {url}: {e}")
                return (url, None)

        return (url, ruta_local)


class DataComics:
    def __init__(self):
        self.datos = {}
        self.max_items = MAX_CACHE_COMICS

    def _normalizar_comic(self, comic):
        if not isinstance(comic, dict):
            return comic

        def _min_creditos(lista):
            if not isinstance(lista, list):
                return []
            salida = []
            for item in lista:
                if not isinstance(item, dict):
                    continue
                i = item.get("id")
                n = item.get("name")
                if i is None and n is None:
                    continue
                salida.append({"id": i, "name": n})
            return salida

        return {
            "id": comic.get("id"),
            "isbn": comic.get("isbn"),
            "name": comic.get("name"),
            "issue_number": comic.get("issue_number"),
            "cover_date": comic.get("cover_date"),
            "image": comic.get("image"),
            "character_credits": _min_creditos(comic.get("character_credits")),
            "person_credits": _min_creditos(comic.get("person_credits")),
            "event_credits": _min_creditos(comic.get("event_credits")),
            "publisher": comic.get("publisher"),
        }

    def obtener(self, api, id=None):
        if id:
            cache_key = str(id)
            if id in self.datos:
                return self.datos[id]
            if cache_key in self.datos:
                return self.datos[cache_key]
            data = api.obtener_comics(id)
            if data:
                comic = self._normalizar_comic(data[0])
                if not comic.get("publisher") or comic["publisher"].get("name") == "Marvel":
                    self.datos[id] = comic
                    self.datos[cache_key] = comic
                    self.guardar()
                    return comic
            return False

        try:
            data = api.obtener_comics()
        except Exception:
            return self.datos if self.datos else False

        r_data = {}
        if data is not None:
            for comic in data:
                comic = self._normalizar_comic(comic)
                if not comic.get("publisher") or comic["publisher"].get("name") == "Marvel":
                    self.datos[comic["id"]] = comic
                    r_data[comic["id"]] = comic
            if r_data:
                self.guardar()
            return r_data
        return self.datos if self.datos else False

    def cargar(self):
        ruta = os.path.join(folder, "comics.json")
        recortado = False
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.datos = json.load(f)
        except FileNotFoundError:
            self.datos = {}
        if isinstance(self.datos, dict) and len(self.datos) > self.max_items:
            self.datos = _limitar_diccionario(self.datos, self.max_items)
            recortado = True
        if recortado:
            self.guardar()

    def guardar(self):
        os.makedirs(folder, exist_ok=True)
        ruta = os.path.join(folder, "comics.json")
        self.datos = _limitar_diccionario(self.datos, self.max_items)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)


class DataCreadores:
    def __init__(self):
        self.datos = {}
        self.max_items = MAX_CACHE_CREADORES

    def obtener(self, id, api):
        cache_key = str(id)
        if id in self.datos:
            return self.datos[id]
        if cache_key in self.datos:
            return self.datos[cache_key]
        data = api.obtener_creadores(id)
        if data:
            self.datos[id] = data[0]
            self.datos[cache_key] = data[0]
            self.guardar()
            return data[0]
        return False

    def cargar(self):
        ruta = os.path.join(folder, "creadores.json")
        recortado = False
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.datos = json.load(f)
        except FileNotFoundError:
            self.datos = {}
        if isinstance(self.datos, dict) and len(self.datos) > self.max_items:
            self.datos = _limitar_diccionario(self.datos, self.max_items)
            recortado = True
        if recortado:
            self.guardar()

    def guardar(self):
        os.makedirs(folder, exist_ok=True)
        ruta = os.path.join(folder, "creadores.json")
        self.datos = _limitar_diccionario(self.datos, self.max_items)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)


class DataEventos:
    def __init__(self):
        self.datos = {}
        self.max_items = MAX_CACHE_EVENTOS

    def obtener(self, id, api):
        cache_key = str(id)
        if id in self.datos:
            return self.datos[id]
        if cache_key in self.datos:
            return self.datos[cache_key]
        data = api.obtener_eventos(id)
        if data:
            self.datos[id] = data[0]
            self.datos[cache_key] = data[0]
            self.guardar()
            return data[0]
        return False

    def cargar(self):
        ruta = os.path.join(folder, "eventos.json")
        recortado = False
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.datos = json.load(f)
        except FileNotFoundError:
            self.datos = {}
        if isinstance(self.datos, dict) and len(self.datos) > self.max_items:
            self.datos = _limitar_diccionario(self.datos, self.max_items)
            recortado = True
        if recortado:
            self.guardar()

    def guardar(self):
        os.makedirs(folder, exist_ok=True)
        ruta = os.path.join(folder, "eventos.json")
        self.datos = _limitar_diccionario(self.datos, self.max_items)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)


class DataPersonajes:
    def __init__(self):
        self.datos = {}
        self.max_items = MAX_CACHE_PERSONAJES

    def obtener(self, api, id=None, modo="general"):
        if id:
            cache_key = str(id)
            if id in self.datos:
                return self.datos[id]
            if cache_key in self.datos:
                return self.datos[cache_key]
            data = api.obtener_personajes(id)
            if data:
                personaje = data[0]
                if not personaje.get("publisher") or personaje["publisher"].get("name") == "Marvel":
                    self.datos[id] = personaje
                    self.datos[cache_key] = personaje
                    self.guardar()
                    return personaje
            return False

        try:
            data = api.obtener_personajes(modo=modo)
        except Exception:
            # Si hay cache, seguimos en modo offline. si no hay cache, propagamos el error
            if self.datos:
                return self.datos
            raise

        r_data = {}
        if data is not None:
            for val in data:
                if not val.get("publisher") or val["publisher"].get("name") == "Marvel":
                    self.datos[val["id"]] = val
                    r_data[val["id"]] = val
            if r_data:
                self.guardar()
            return r_data
        return self.datos if self.datos else False

    def cargar(self):
        ruta = os.path.join(folder, "personajes.json")
        recortado = False
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.datos = json.load(f)
        except FileNotFoundError:
            self.datos = {}
        if isinstance(self.datos, dict) and len(self.datos) > self.max_items:
            self.datos = _limitar_diccionario(self.datos, self.max_items)
            recortado = True
        if recortado:
            self.guardar()

    def guardar(self):
        os.makedirs(folder, exist_ok=True)
        ruta = os.path.join(folder, "personajes.json")
        self.datos = _limitar_diccionario(self.datos, self.max_items)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)


class DataBank:
    def __init__(self):
        self.d_comics = DataComics()
        self.d_creadores = DataCreadores()
        self.d_eventos = DataEventos()
        self.d_personajes = DataPersonajes()
        self.cargar_todos()

    def cargar_todos(self):
        self.d_comics.cargar()
        self.d_eventos.cargar()
        self.d_creadores.cargar()
        self.d_personajes.cargar()

    def guardar_todos(self):
        self.d_comics.guardar()
        self.d_eventos.guardar()
        self.d_creadores.guardar()
        self.d_personajes.guardar()


class Instanciador:
    """
    Convierte diccionarios crudos en instancias de los modelos.
    """

    def __init__(self, carpeta_imgs=IMGS_DIR):
        self.descargador = DescargadorImagenes(carpeta_destino=carpeta_imgs)

    def _extraer_id_credito(self, item):
        """
        Extrae id numerico desde un credito de ComicVine.
        Prioriza el campo 'id', pero soporta 'api_detail_url' cuando no viene id.
        """
        if not isinstance(item, dict):
            return None
        val = item.get("id")
        if val:
            return val
        detalle = item.get("api_detail_url") or ""
        match = re.search(r"/\d+-([0-9]+)/?$", str(detalle))
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None

    def _procesar_imagen(self, datos_imagen):
        if isinstance(datos_imagen, dict):
            url = datos_imagen.get("medium_url") or datos_imagen.get("icon_url")
            if url:
                return self.descargador.descargar(url)
        elif isinstance(datos_imagen, str):
            return self.descargador.descargar(datos_imagen)
        return (None, None)

    def convertir_a_comic(self, datos):
        try:
            c_id = datos.get("id")
            nombre = datos.get("name")
            isbn = datos.get("isbn")
            personajes = datos.get("character_credits") or []
            lanzamiento = datos.get("cover_date")
            p_ids = [self._extraer_id_credito(p) for p in personajes if isinstance(p, dict)]
            p_ids = [pid for pid in p_ids if pid is not None]
            autores = datos.get("person_credits") or []
            a_ids = [self._extraer_id_credito(a) for a in autores if isinstance(a, dict)]
            a_ids = [aid for aid in a_ids if aid is not None]
            r_eventos = datos.get("event_credits") or []
            e_ids = [self._extraer_id_credito(e) for e in r_eventos if isinstance(e, dict)]
            e_ids = [eid for eid in e_ids if eid is not None]
            imagen = self._procesar_imagen(datos.get("image"))

            comic = Comic(c_id, nombre, imagen, lanzamiento)
            comic.creadores = a_ids
            comic.personajes = p_ids
            comic.eventos = e_ids
            comic.isbn = isbn
            comic.descripcion = datos.get("description")
            return comic
        except Exception:
            return None

    def convertir_a_creador(self, datos):
        try:
            c_id = datos.get("id")
            nombre = datos.get("name")
            imagen = self._procesar_imagen(datos.get("image"))
            return Creador(c_id, nombre, imagen)
        except Exception:
            return None

    def convertir_a_evento(self, datos):
        try:
            e_id = datos.get("id")
            nombre = datos.get("name")
            descripcion = datos.get("deck")
            imagen = self._procesar_imagen(datos.get("image"))
            return Evento(e_id, nombre, descripcion, imagen)
        except Exception:
            return None

    def convertir_a_personaje(self, datos):
        try:
            p_id = datos.get("id")
            nombre = datos.get("name")
            imagen = self._procesar_imagen(datos.get("image"))
            descripcion = datos.get("deck") or datos.get("description") or ""
            r_creadores = datos.get("creator_credits") or []
            creadores = [c.get("name") for c in r_creadores if isinstance(c, dict) and c.get("name")]
            creadores_ids = [self._extraer_id_credito(c) for c in r_creadores if isinstance(c, dict)]
            creadores_ids = [cid for cid in creadores_ids if cid is not None]
            r_eventos = datos.get("event_credits") or []
            eventos = [e.get("name") for e in r_eventos if isinstance(e, dict) and e.get("name")]
            eventos_ids = [self._extraer_id_credito(e) for e in r_eventos if isinstance(e, dict)]
            eventos_ids = [eid for eid in eventos_ids if eid is not None]
            r_comics = datos.get("issue_credits") or []
            comics = [cm.get("name") for cm in r_comics if isinstance(cm, dict) and cm.get("name")]
            comics_ids = [self._extraer_id_credito(cm) for cm in r_comics if isinstance(cm, dict)]
            comics_ids = [coid for coid in comics_ids if coid is not None]

            personaje = Personaje(p_id, nombre, imagen)
            personaje.descripcion = descripcion
            personaje.creadores = creadores
            personaje.eventos = eventos
            personaje.comics = comics
            personaje.creadores_ids = creadores_ids
            personaje.eventos_ids = eventos_ids
            personaje.comics_ids = comics_ids
            return personaje
        except Exception:
            return None


class Instancias:
    """
    DataBank de la informacion ya instanciada.
    """

    def __init__(self):
        self.comics = {}
        self.creadores = {}
        self.eventos = {}
        self.personajes = {}
        self.raw_data = DataBank()
        self.converter = Instanciador()

    def buscador(self, type, api, id=None):
        types = {
            "comic": [self.comics, self.raw_data.d_comics],
            "creador": [self.creadores, self.raw_data.d_creadores],
            "evento": [self.eventos, self.raw_data.d_eventos],
            "personaje": [self.personajes, self.raw_data.d_personajes],
        }
        if type not in types:
            return False

        type_dict = types[type][0]
        retrieval = types[type][1]
        if id and id not in type_dict:
            data = retrieval.obtener(id=id, api=api)
            if data is not None:
                match type:
                    case "comic":
                        c_data = self.converter.convertir_a_comic(data)
                    case "creador":
                        c_data = self.converter.convertir_a_creador(data)
                    case "evento":
                        c_data = self.converter.convertir_a_evento(data)
                    case "personaje":
                        c_data = self.converter.convertir_a_personaje(data)
                        if c_data is not None:
                            if not c_data.comics:
                                com_list = [comic.titulo for comic in self.comics.values() if c_data.id in comic.personajes]
                                c_data.comics = com_list
                if c_data is None:
                    return False
                type_dict[c_data.id] = c_data
                return c_data
            return False
        return type_dict.get(id, False)

    def dumper(self, type, api, modo="general"):
        types = {"comic": [self.comics, self.raw_data.d_comics], "personaje": [self.personajes, self.raw_data.d_personajes]}
        if type not in types:
            return False

        type_dict = types[type][0]
        retrieval = types[type][1]
        data = retrieval.obtener(api=api, modo=modo)
        if data and isinstance(data, dict):
            conv = {}
            for val in data.values():
                match type:
                    case "comic":
                        c_data = self.converter.convertir_a_comic(val)
                    case "personaje":
                        c_data = self.converter.convertir_a_personaje(val)
                        if c_data is not None:
                            if not c_data.comics:
                                com_list = [comic.titulo for comic in self.comics.values() if c_data.id in comic.personajes]
                                c_data.comics = com_list
                # CORRECCION: ignorar conversiones invalidas en lugar de romper toda la carga.
                if c_data is None:
                    continue
                type_dict[c_data.id] = c_data
                conv[c_data.id] = c_data
            return conv
        return False


gestor = Instancias()


class PageOrderer(QObject):
    finalizado = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, g_data, perfil_clave, modo_carga="general"):
        super().__init__()
        self.gestor = g_data
        self.perfil_clave = perfil_clave
        self.modo_carga = modo_carga

    def _cargar_personajes_desde_cache_local(self):
        """
        Intenta reconstruir personajes usando solo el cache local en memoria/disco.
        """
        cache = self.gestor.raw_data.d_personajes.datos
        if not cache:
            self.gestor.raw_data.d_personajes.cargar()
            cache = self.gestor.raw_data.d_personajes.datos

        if not cache or not isinstance(cache, dict):
            return {}

        conv = {}
        for val in cache.values():
            c_data = self.gestor.converter.convertir_a_personaje(val)
            if c_data is None:
                continue
            self.gestor.personajes[c_data.id] = c_data
            conv[c_data.id] = c_data
        return conv

    def dump_list(self):
        try:
            if not hasattr(self.perfil_clave, "obtener_personajes"):
                raise ValueError("La API de ComicVine no fue inicializada correctamente.")

            personajes_dict = self.gestor.dumper("personaje", self.perfil_clave, modo=self.modo_carga)
            if not personajes_dict:
                personajes_dict = self._cargar_personajes_desde_cache_local()

            if not personajes_dict:
                ruta_cache = os.path.join(folder, "personajes.json")
                en_memoria = len(self.gestor.raw_data.d_personajes.datos or {})
                raise ValueError(
                    "No se pudieron cargar personajes desde ComicVine ni desde cache local.\n"
                    f"Cache esperada: {ruta_cache}\n"
                    f"Registros disponibles en memoria: {en_memoria}"
                )

            lista_marvel = ListaDoble()
            for personaje_obj in personajes_dict.values():
                if personaje_obj is None:
                    continue
                lista_marvel.agregar(personaje_obj)

            if lista_marvel.tamanio == 0:
                raise ValueError("La carga termino sin personajes validos para mostrar.")

            self.finalizado.emit(lista_marvel)
        except Exception as e:
            self.error.emit(f"{e}\n\n{traceback.format_exc()}")
