from Modelos.nodo import Nodo

#La lista simplemente enlazada servira pra almacenar los comics
class ListaSimple:

    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None
