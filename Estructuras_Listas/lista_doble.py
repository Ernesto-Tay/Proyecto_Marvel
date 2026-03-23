from Modelos.modo_doble import NodoDoble

#Usamos la lista doblemente enlazada para guardar a los personajes
class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamanio=0

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

    def buscar_por_nombre(self, texto):
        resultados = []
        actual = self.cabeza

        while actual:
            if texto.lower() in actual.dato.nombre.lower():
                resultados.append(actual.dato)
            actual = actual.siguiente
        return resultados

    def buscar(self, dato):
        actual = self.cabeza
        while actual:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

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

    def eliminar(self, dato):
        if self.esta_vacia():
            return False

        actual = self.cabeza

        while actual:
            if actual.dato == dato:
                if actual == self.cabeza:
                    self.cabeza = actual.siguiente
                    if self.cabeza:
                        self.cabeza.anterior = None
                    else:
                        self.cola = None

                elif actual == self.cola:
                    self.cola = actual.anterior
                    self.cola.siguiente = None

                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                self.tamanio -= 1
                return True
            actual = actual.siguiente
        return False

    def ordenar_por_nombre(self, ascendente=True):
        if self.tamanio <= 1:
            return

        for i in range(self.tamanio):
            actual = self.cabeza
            for j in range(self.tamanio - 1):
                siguiente = actual.siguiente

                nombre_a = actual.dato.obtener_nombre().lower()
                nombre_b = siguiente.dato.obtener_nombre().lower()

                if (ascendente and nombre_a > nombre_b) or (not ascendente and nombre_a < nombre_b):
                    auxi = actual.dato
                    actual.dato = siguiente.dato
                    siguiente.dato = auxi

                actual = actual.siguiente


lisa= ListaDoble()

lisa.agregar("mono")
lisa.agregar("jirafa")
lisa.recorrer_atras()
print(lisa.recorrer_adelante())
print(lisa.recorrer_atras())