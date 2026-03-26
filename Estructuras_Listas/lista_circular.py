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
            aux = self.actual
            while aux.siguiente != self.actual:
                aux = aux.siguiente

            aux.siguiente = nuevo
            nuevo.siguiente = self.actual  # Cierra el círculo
        self.tamanio += 1

    def eliminar(self, dato):
        if self.esta_vacia():
            return False
        inicio = self.actual
        actual = self.actual
        while True:
            if actual.siguiente.dato == dato:
                nodo_a_borrar = actual.siguiente
                if self.tamanio == 1:
                    self.actual = None
                else:
                    actual.siguiente = nodo_a_borrar.siguiente
                    if nodo_a_borrar == self.actual:
                        self.actual = actual.siguiente
                self.tamanio -= 1
                return True
            actual = actual.siguiente
            if actual == inicio:
                break
        return False

    def buscar(self, dato):
        if self.esta_vacia():
            return False

        actual = self.actual
        for i in range(self.tamanio):
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        datos_lista = []
        if self.esta_vacia():
            return datos_lista

        inicio = self.actual
        auxiliar = self.actual

        while True:
            datos_lista.append(auxiliar.dato)
            auxiliar = auxiliar.siguiente
            if auxiliar == inicio:
                break
        return datos_lista

    def siguiente(self):
        if not self.esta_vacia():
            self.actual = self.actual.siguiente
            return self.actual.dato
        return None

    def anterior(self):
        if self.esta_vacia():
            return None

        # Como es circular simple, para ir al de atrás hay que dar toda la vuelta
        auxiliar = self.actual
        while auxiliar.siguiente != self.actual:
            auxiliar = auxiliar.siguiente

        self.actual = auxiliar
        return self.actual.dato

    def obtener_pagina(self, numero_pagina, elementos_por_pagina=10):
        inicio = numero_pagina * elementos_por_pagina

        if inicio >= self.tamanio:
            return []

        resultados = []
        actual = self.actual

        # Saltar hasta el inicio
        for i in range(inicio):
            if actual:
                actual = actual.siguiente

        # Recoger página
        for i in range(elementos_por_pagina):
            if actual:
                resultados.append(actual.dato)
                actual = actual.siguiente
            else:
                break
        return resultados
