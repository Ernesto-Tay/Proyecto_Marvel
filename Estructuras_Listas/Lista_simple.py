from Modelos.nodo import Nodo

#La lista simplemente enlazada servira pra almacenar los comics
class ListaSimple:

    def __init__(self):
        self.cabeza = None
        self.tamanio= 0

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
        self.tamanio+= 1

    def agregar_al_inicio(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
        self.tamanio +=1

    def eliminar(self, dato):
        if self.esta_vacia():
            return False

        if self.cabeza.dato == dato:
            self.cabeza = self.cabeza.siguiente
            self.tamanio -=1
            return True

        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self.tamanio -=1
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

    def ordenar_por_nombre(self, ascendente=True):
        if self.tamanio <= 1:
            return

        for i in range(self.tamanio - 1):
            actual = self.cabeza
            for j in range(self.tamanio - i - 1):
                siguiente = actual.siguiente

                nombre_a = actual.dato.obtener_nombre().lower()
                nombre_b = siguiente.dato.obtener_nombre().lower()

                if (ascendente and nombre_a > nombre_b) or (not ascendente and nombre_a < nombre_b):
                    # Intercambiamos solo los adtos de los nodos, no los nodos en sí
                    auxiliar= actual.dato
                    actual.dato = siguiente.dato
                    siguiente.dato= auxiliar

                actual = actual.siguiente


    def ordenar_por_fecha(self, ascendente=True):
        if self.tamanio <= 1:
            return

        for i in range(self.tamanio - 1):
            actual = self.cabeza
            for j in range(self.tamanio - i - 1):
                siguiente = actual.siguiente

                fecha_a = actual.dato.obtener_fecha()
                fecha_b = siguiente.dato.obtener_fecha()

                if (ascendente and fecha_a > fecha_b) or (not ascendente and fecha_a < fecha_b):
                    auxi= actual.dato
                    actual.dato= siguiente.dato
                    siguiente.dato = auxi

                actual = actual.siguiente

    def obtener_pagina(self, numero_pagina, elementos_por_pagina=10):
        inicio = numero_pagina * elementos_por_pagina

        if inicio >= self.tamanio:
            return []
        resultados = []
        actual = self.cabeza

        # Saltaremos hasta el inicio
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

    def obtener_todos(self):
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos