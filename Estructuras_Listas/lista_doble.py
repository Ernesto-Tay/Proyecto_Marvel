from Modelos.modo_doble import NodoDoble

#Usamos la lista doblemente enlazada para guardar a los personajes
class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, dato):
        nuevo = NodoDoble(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo

    def agregar_al_inicio(self, dato):
        nuevo = NodoDoble(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo

    def recorrer_adelante(self):
        datos = []  #aqui vamos a guardar datos
        actual = self.cabeza

        while actual:
            datos.append(actual.dato)
            actual = actual.siguiente

        return datos

    def recorrer_atras(self):
        datos_reversa = []
        actual = self.cola

        while actual:
            datos_reversa.append(actual.dato)
            actual = actual.anterior

        return datos_reversa

lisa= ListaDoble()

lisa.agregar("mono")
lisa.agregar("jirafa")
lisa.recorrer_atras()
print(lisa.recorrer_adelante())
print(lisa.recorrer_atras())