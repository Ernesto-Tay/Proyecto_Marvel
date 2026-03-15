class Evento: # esta clase va a representar un evento en Marvel

    def __init__(self, id_marvel, titulo, descripcion, imagen):
        self.id = id_marvel
        self.titulo = titulo
        self.descripcion = descripcion
        self.imagen= imagen

    def __str__(self):
        return f"Evento: {self.titulo}"
