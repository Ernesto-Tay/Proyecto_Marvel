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

    def eliminar(self, dato):
        if self.esta_vacia():
            return False
        actual = self.actual

        while True:
            if actual.siguiente.dato == dato:
                nodo_a_borrar = actual.siguiente

                if self.tamanio == 1:
                    self.actual = None
                else:
                    actual.siguiente = nodo_a_borrar.siguiente
                    # Si borramos el dato actual, actual ahora es el siguiente, lo movemos
                    if nodo_a_borrar == self.actual:
                        self.actual = actual

                self.tamanio -= 1
                return True
            actual = actual.siguiente
            if actual == self.cabeza:
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

        auxiliar = self.actual

        while True:
            datos_lista.append(auxiliar.dato)
            auxiliar = auxiliar.siguiente

            if auxiliar == self.cabeza:
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

