# Las siguientes clases funcionarán como el Cache del sistema para optimizar procesos
from Modelos.__init__ import Creador, Comic, Evento, Personaje
import json
folder = "Datos_json"
import urllib.request
import os

class DescargadorImagenes:
    """
    Clase dedicada a descargar imágenes de URLs y guardarlas localmente.
    """
    def __init__(self, carpeta_destino="imgs"):
        self.carpeta_destino = carpeta_destino
        self.headers = {"User-Agent": "Proyecto_Marvel/1.0 (Proyecto Universitario)"}
        os.makedirs(self.carpeta_destino, exist_ok=True)

    def descargar(self, url):
        """
        Descarga la imagen de la URL y la guarda.
        Retorna una tupla: (URL_ComicVine, Ruta_Local)
        """
        # Validar que la URL exista
        if not url:
            return (None, None)

        # Extraer el nombre de la imagen al final de la URL (ej: "batman_portada.jpg")
        nombre_archivo = url.split("/")[-1]

        # Crear la ruta completa donde se guardará (ej: "Imagenes_ComicVine/batman_portada.jpg")
        ruta_local = os.path.join(self.carpeta_destino, nombre_archivo)

        # Verificar si la imagen ya fue descargada antes para ahorrar tiempo y recursos
        if not os.path.exists(ruta_local):
            try:
                req = urllib.request.Request(url, headers=self.headers)
                with urllib.request.urlopen(req) as response:
                    # Guardamos la imagen en modo binario ("wb" = write binary)
                    with open(ruta_local, "wb") as f:
                        f.write(response.read())
            except Exception as e:
                print(f"Hubo un error al descargar la imagen {url}: {e}")
                return (url, None)

        # Retornamos la tupla solicitada
        return (url, ruta_local)



class DataComics:
    def __init__(self):
        self.datos = {}
    def obtener(self, id, api):
        if id in self.datos:
            return self.datos[id]
        data = api.obtener_comics(id)
        if data is not None:
            self.datos[id] = data[0]
            return data[0]
        return False

    def cargar(self):
        ruta = os.path.join(folder, "comics.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.datos = json.load(f)
        except FileNotFoundError:
            self.datos = {}

    def guardar(self):
        os.makedirs(folder, exist_ok=True)
        ruta = os.path.join(folder, "comics.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)


class DataCreadores:
    def __init__(self):
        self.datos = {}

    def obtener(self, id, api):
        if id in self.datos:
            return self.datos[id]
        data = api.obtener_creadores(id)
        if data is not None:
            self.datos[id] = data[0]
            return data[0]
        return False

    def cargar(self):
        ruta = os.path.join(folder, "creadores.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.datos = json.load(f)
        except FileNotFoundError:
            self.datos = {}

    def guardar(self):
        os.makedirs(folder, exist_ok=True)
        ruta = os.path.join(folder, "creadores.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)


class DataEventos:
    def __init__(self):
        self.datos = {}
    def obtener(self, id, api):
        if id in self.datos:
            return self.datos[id]
        data = api.obtener_eventos(id)
        if data is not None:
            self.datos[id] = data[0]
            return data[0]
        return False

    def cargar(self):
        ruta = os.path.join(folder, "eventos.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.datos = json.load(f)
        except FileNotFoundError:
            self.datos = {}

    def guardar(self):
        os.makedirs(folder, exist_ok=True)
        ruta = os.path.join(folder, "eventos.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)


class DataPersonajes:
    def __init__(self):
        self.datos = {}

    def obtener(self, id, api):
        if id in self.datos:
            return self.datos[id]
        data = api.obtener_personajes(id)
        if data is not None:
            self.datos[id] = data[0]
            return data[0]
        return False

    def cargar(self):
        ruta = os.path.join(folder, "personajes.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.datos = json.load(f)
        except FileNotFoundError:
            self.datos = {}
    def guardar(self):
        os.makedirs(folder, exist_ok=True)
        ruta = os.path.join(folder, "personajes.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)


class DataBank:
    def __init__(self):
        self.d_comics = DataComics()
        self.d_creadores = DataCreadores()
        self.d_eventos = DataEventos()
        self.d_personajes = DataPersonajes()


class Instanciador:
    """
    Esta clase es la encargada de convertir diccionarios a instancias de clase que se encuentran en los modelos de abajo.
    Si quiere datos filtrados, se debe filtrar el diccionario o la serie de datos antes de que entre aquí.
    "datos" recibe un diccionario (se maneja como tal), así que tomar en cuenta eso en el filtrado.
    """
    def __init__(self, carpeta_imgs = "imgs"):
        self.descargador = DescargadorImagenes(carpeta_destino = carpeta_imgs)

    def _procesar_imagen(self, datos_imagen):
        if isinstance(datos_imagen, dict):
            # ComicVine suele tener varios tamaños, así que especificamos cuál queremos
            url = datos_imagen.get("medium_url") or datos_imagen.get("icon_url")
            if url:
                return self.descargador.descargar(url)
        elif isinstance(datos_imagen, str):
            # Por si en algún caso la API se pone humilde y da la URL directa como texto
            return self.descargador.descargar(datos_imagen)
        return (None, None)

    def convertir_a_comic(self, datos): #crea una lista de datos con instancias de cómics
        try:
            c_id = datos.get("id")
            nombre = datos.get("name")
            isbn = datos.get("isbn")
            personajes = datos.get("character_credits")
            lanzamiento = datos.get("cover_date")
            p_ids = [p.get("id") for p in personajes]
            autores = datos.get("person_credits")
            a_ids = [a.get("id") for a in autores]
            imagen = self._procesar_imagen(datos.get("image")) # GUARDA UNA TUPLA (url, ruta_local)

            comic = Comic(c_id, nombre, imagen, lanzamiento)
            comic.creadores = a_ids
            comic.personajes = p_ids
            comic.isbn = isbn
            comic.descripcion = datos.get("description")
            return comic
        except:
            return None

    def convertir_a_creador(self, datos): #retorna una lista de datos con instancias de creadores
        try:
            c_id = datos.get("id")
            nombre = datos.get("name")
            imagen = self._procesar_imagen(datos.get("image"))
            autor = Creador(c_id, nombre, imagen)
            return autor
        except:
            return None

    def convertir_a_evento(self, datos): # retorna una lista de datos con instancias de eventos
        try:
            e_id = datos.get("id")
            nombre = datos.get("name")
            descripcion = datos.get("deck")
            imagen = self._procesar_imagen(datos.get("image"))
            evento = Evento(e_id, nombre, descripcion, imagen)
            return evento
        except:
            return None

    def convertir_a_personaje(self, datos): # retorna una lista de datos con istancias de personaejs
        try:
            p_id = datos.get("id")
            nombre = datos.get("name")
            imagen = self._procesar_imagen(datos.get("image"))
            descripcion = datos.get("deck")
            r_creadores = datos.get("creator_credits")
            c_ids = [c.get("id") for c in r_creadores]
            r_eventos = datos.get("event_credits")
            e_ids = [e.get("id") for e in r_eventos]

            personaje = Personaje(p_id, nombre, imagen)
            personaje.descripcion = descripcion
            personaje.creadores = c_ids
            personaje.eventos = e_ids
            return personaje
            # falta la lista de cómics relacionados con el personaje, hacerlo en el Instanciador
        except:
            return None


class Instancias:
    """
    Esta es la DataBank de la información ya instanciada.
    SOLO DEBE HABER UNA INSTANCIA DE ESTA CLASE, DE LO CONTRARIO LA INFORMACIÓN PUEDE DUPLICARSE Y ESO LLEVARÍA A ERRORES.
    """
    def __init__(self):
        self.comics = {}
        self.creadores = {}
        self.eventos = {}
        self.personajes = {}
        self.raw_data = DataBank()
        self.converter = Instanciador()


    def buscador(self, id, type, api):
        """
        :param id: Es el ID de referencia para la búsqueda. Debe ser de 4 dígitos.
        :param type: Es el tipo de dato (comic, creador, evento, personaje).
        :param api: Es la variable que refiere a la clase que controla la conexión con ComicVine
        """
        types = {"comic":[self.comics, self.raw_data.d_comics], "creador": [self.creadores, self.raw_data.d_creadores], "evento":[self.eventos,self.raw_data.d_eventos], "personaje":[self.personajes, self.raw_data.d_personajes]}
        if type not in types.keys(): #si se solicita un tipo que no existe
            return False

        type_dict = types[type][0]
        if id not in type_dict.keys(): #si el valor buscado por ID no existe en los diccionarios de instancias convertidas
            retrieval = types[type][1]
            data = retrieval.obtener(id, api) #se busca en los diccionarios de instancias crudas, o se solicita de la API
            if data is not None: #ahora toca relacionar "data" con la función respectiva del convertidor (si se obtuvo algún dato)
                match type:
                    case "comic":
                        c_data = self.converter.convertir_a_comic(data)
                    case "creador":
                        c_data = self.converter.convertir_a_creador(data)
                    case "evento":
                        c_data = self.converter.convertir_a_evento(data)
                    case "personaje":
                        c_data = self.converter.convertir_a_personaje(data)
                        com_list = [comic.id for comic in self.comics.values() if c_data.id in comic.personajes]
                        c_data.comics = com_list
                type_dict[c_data.id] = c_data
                return c_data
            return False
        return type_dict[id]