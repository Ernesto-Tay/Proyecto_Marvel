class Personaje: # Trabajaremos con clase para representar a cada personaje de Marvel

    def __init__(self, id_marvel, nombre, imagen):
        self.id = id_marvel
        self.nombre = nombre
        self.imagen = imagen
        self.descripcion = ""
        self.creadores = []  #lista de ids de creadores
        self.comics = []  # Lista de isd de comics donde aparece
        self.eventos = []  # Lista de ids de eventos

    def __str__(self):
        return f"Personaje: {self.nombre}"

    def obtener_nombre(self):
        return self.nombre

    def obtener_fecha(self):
        return ""
