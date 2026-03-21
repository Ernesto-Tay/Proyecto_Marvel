"""
Este arvhivo solo vamos a usarlo para hacer importaciones en otros archivos y que
el codigo no sea tan extenso al moemnto de hacer importaciones, quiere decir no estar llamando
en cada carpeta a las clases una por una y asi :D
"""

from Modelos.Clase_comic import Comic
from Modelos.Clase_personaje import Personaje
from Modelos.Clase_creador import Creador
from Modelos.Clase_evento import Evento
from Modelos.nodo import Nodo
from Modelos.modo_doble import NodoDoble

__all__ = ["Comic","Personaje", "Creador","Evento","Nodo", "NodoDoble"]