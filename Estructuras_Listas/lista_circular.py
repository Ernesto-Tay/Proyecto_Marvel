from Modelos.nodo import Nodo

class ListaCircular: #La usaremos para navegar entre las secciones
    def __init__(self):
        self.actual = None
        self.tamanio = 0

    def esta_vacia(self):
        return self.actual is None

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.actual = nuevo
            nuevo.siguiente = nuevo
        else:
            nuevo.siguiente = self.actual.siguiente
            self.actual.siguiente = nuevo

