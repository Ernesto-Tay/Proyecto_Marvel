from Modelos.nodo import Nodo


class ListaCircular: #La usaremos para navegar entre las secciones
    def __init__(self):
        self.actual = None
        self.tamanio = 0

    def esta_vacia(self):
        return self.actual is None
