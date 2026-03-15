from Modelos.nodo import Nodo

class NodoDoble(Nodo):
    def __init__(self, dato):
        super().__init__(dato)
        self.anterior = None