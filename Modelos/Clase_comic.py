class Comic: # vamos a usar la calse comic para representar lso comics de la tienda
    def __init__(self, id_marvel, titulo, imagen, fecha_lanzamiento):
        self.id = id_marvel
        self.titulo = titulo
        self.imagen = imagen
        self.fecha_lanzamiento = fecha_lanzamiento
        self.isbn = ""
        self.descripcion = ""
        self.personajes = []  # esta es la lista de ids de personajes
        self.creadores = []  # esta es la lista de ids de creadores
        self.eventos = []  # lista de ids de eventos relacionados

    def obtener_nombre_busqueda(self):
        return self.titulo

    def obtener_fecha(self):
        return self.fecha_lanzamiento
