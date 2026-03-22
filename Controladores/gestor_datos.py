# Las siguientes clases funcionarán como el Cache del sistema para optimizar procesos
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



class Instancias:
    """
    Esta es la DataBank de la información ya instanciada
    """
    def __init__(self):
        self.comics = {}
        self.creadores = {}
        self.eventos = {}
        self.personajes = {}

    def buscador(self, id, type, inst, api):
        """
        :param id: Es el ID de referencia para la búsqueda. Debe ser de 4 dígitos.
        :param type: Es el tipo de dato
        :param inst: Es el nombre de la variable con la cual está definido el instanciador
        :param api: Es la variable que refiere a la clase que controla la conexión con ComicVine
        """
        types = {"comic":self.comics, "creador":self.creadores, "evento":self.eventos, "personaje":self.personajes}
        if type not in types.keys():
            return False

        if not types[type][id]:
            return False




class Instanciador:
    """
    Esta clase es la encargada de convertir diccionarios a instancias de clase que se encuentran en los modelos de abajo.
    Si quiere datos filtrados, se debe filtrar el diccionario o la serie de datos antes de que entre aquí.
    "datos" recibe un diccionario (se maneja como tal), así que tomar en cuenta eso en el filtrado.
    """
    def convertir_a_comic(self, datos): pass #crea una lista de datos con instancias de cómics

    def convertir_a_creador(self, datos): pass #retorna una lista de datos con instancias de creadores

    def convertir_a_evento(self, datos): pass # retorna una lista de datos con instancias de eventos

    def convertir_a_personaje(self, datos): pass # retorna una lista de datos con istancias de personaejs