# Cada instancia de esta clase va a representar a un creador ya sea escritor etc

class Creador:
    def __init__(self, id_marvel, nombre_completo, imagen):
        self.id = id_marvel
        self.nombre_completo = nombre_completo
        self.imagen= imagen
        self.rol = ""  # Aqui se puede poner cualquier rol: escritor, artista, autor, etc

    def __str__(self):
        return f"Creador: {self.nombre_completo}"
