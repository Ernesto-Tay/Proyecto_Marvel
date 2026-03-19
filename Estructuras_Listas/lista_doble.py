from Modelos.modo_doble import NodoDoble

#Usamos la lista doblemente enlazada para guardar a los personajes
class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def esta_vacia(self):
        return self.cabeza is None
