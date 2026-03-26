class Personaje: # Trabajaremos con clase para representar a cada personaje de Marvel

    def __init__(self, id_marvel, nombre, imagen):
        self.id = id_marvel
        self.nombre = nombre
        self.imagen = imagen
        self.descripcion = ""
        self.creadores = []  # Lista de nombres de creadores
        self.comics = []  # Lista de nombres de comics donde aparece
        self.eventos = []  # Lista de nombres de eventos
        self.creadores_ids = []  # Lista de ids de creadores
        self.comics_ids = []  # Lista de ids de comics
        self.eventos_ids = []  # Lista de ids de eventos
        self.detalles_creadores = []
        self.detalles_comics = []
        self.detalles_eventos = []

    def __str__(self):
        return f"Personaje: {self.nombre}"

    def obtener_nombre(self):
        return self.nombre

    def obtener_fecha(self):
        return ""
