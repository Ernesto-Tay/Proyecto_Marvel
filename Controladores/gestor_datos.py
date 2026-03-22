# Las siguientes clases funcionarán como el Cache del sistema para optimizar procesos
from Modelos.__init__ import Creador, Comic, Evento, Personaje
from init import ComicVineAPI
class DataComics:
    def __init__(self):
        self.datos = {}
    def obtener(self, id, api):
        if id in self.datos:
            return self.datos[id]
        data = api.obtener_comics(id)
        if data is not None:
            self.datos[id] = data
            return data
        return False


class DataCreadores:
    def __init__(self):
        self.datos = {}

    def obtener(self, id, api):
        if id in self.datos:
            return self.datos[id]
        data = api.obtener_creadores(id)
        if data is not None:
            self.datos[id] = data
            return data
        return False


class DataEventos:
    def __init__(self):
        self.datos = {}
    def obtener(self, id, api):
        if id in self.datos:
            return self.datos[id]
        data = api.obtener_eventos(id)
        if data is not None:
            self.datos[id] = data
            return data
        return False


class DataPersonajes:
    def __init__(self):
        self.datos = {}

    def obtener(self, id, api):
        if id in self.datos:
            return self.datos[id]
        data = api.obtener_personajes(id)
        if data is not None:
            self.datos[id] = data
            return data
        return False


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
    def convertir_a_comic(self, datos): #crea una lista de datos con instancias de cómics
        try:
            c_id = datos.get("id")
            nombre = datos.get("name")
            isbn = datos.get("issue_number")
            personajes = datos.get("character_credits")
            lanzamiento = datos.get("cover_date")
            p_ids = [p.get("id") for p in personajes]
            autores = datos.get("person_credits")
            a_ids = [a.get("id") for a in autores]
            imagen = datos.get("image")

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
            imagen = datos.get("image")
            autor = Creador(c_id, nombre, imagen)
            return autor
        except:
            return None

    def convertir_a_evento(self, datos): # retorna una lista de datos con instancias de eventos
        try:
            e_id = datos.get("id")
            nombre = datos.get("name")
            descripcion = datos.get("deck")
            imagen = datos.get("image")
            evento = Evento(e_id, nombre, descripcion, imagen)
            return evento
        except:
            return None

    def convertir_a_personaje(self, datos): # retorna una lista de datos con istancias de personaejs
        try:
            p_id = datos.get("id")
            nombre = datos.get("name")
            imagen = datos.get("image")
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
        if type not in types.keys(): #si se solicita un tipo que no  existe
            return False

        type_dict = types[type][0]
        if not type_dict[id]: #si el valor buscado por ID no existe en los diccionarios de instancias convertidas
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