from Modelos.nodo import Nodo

#La lista simplemente enlazada servira pra almacenar los comics
class ListaSimple:

    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1

    def agregar_al_inicio(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo

    def eliminar(self, dato):
        if self.esta_vacia():
            return False

        if self.cabeza.dato == dato:
            self.cabeza = self.cabeza.siguiente
            return True

        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                return True
            actual = actual.siguiente
        return False

    def buscar(self, dato):
        actual = self.cabeza
        while actual:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    #Nota: comprobar que funciones correctamente cuando se extrangan datos reales de API!
    def buscar_por_nombre(self, texto):
        resultados = []
        actual = self.cabeza
        texto = texto.lower()

        while actual:
            try:
                nombre = actual.dato.obtener_nombre()
                if texto in nombre.lower():
                    resultados.append(actual.dato)
            except AttributeError:
                pass
            actual = actual.siguiente
        return resultados



