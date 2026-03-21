class Conversor:
    """
    Esta clase es la encargada de convertir diccionarios a instancias de clase que se encuentran en "modelos".
    Si quiere datos filtrados, se debe filtrar el diccionario o la serie de datos antes de que entre aquí.
    "datos" recibe un diccionario (se maneja como tal), así que tomar en cuenta eso en el filtrado.
    """
    def __init__(self, datos):
        self.datos = datos

    def convertir_a_comic(self): pass#crea una lista de datos con instancias de cómics

    def convertir_a_creador(self): pass #retorna una lista de datos con instancias de creadores

    def convertir_a_evento(self): pass # retorna una lista de datos con instancias de eventos

    def convertir_a_personaje(self): pass # retorna una lista de datos con istancias de personaejs