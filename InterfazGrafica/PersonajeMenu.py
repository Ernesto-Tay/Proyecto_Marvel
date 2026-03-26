import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,QPushButton, QScrollArea, QFrame, QLineEdit,QComboBox, QGridLayout)
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QPixmap
from Controladores.init import gestor, PageOrderer
from Estructuras_Listas.init import ListaDoble

class PersonajesMenu(QWidget):
    def __init__(self, perfil, controlador=None):
        super().__init__()
        self.perfil = perfil
        self.controlador = controlador
        self.pagina_actual = 0
        self.gestor = gestor
        self.lista_personajes = None
        self.thread = None
        self.trabajador = None
        self.carga_datos()



        # Contenedor principal
        self.setStyleSheet("background-color: white; border: none;")
        layout_exterior = QVBoxLayout(self)
        layout_exterior.setContentsMargins(0, 0, 0, 0)

        self.lienzo = QFrame()
        self.lienzo.setStyleSheet("background-color: white;")
        layout_principal = QVBoxLayout(self.lienzo)
        layout_principal.setContentsMargins(25, 20, 25, 10)

        # cabecera
        contenedor_cabecera = QVBoxLayout()
        contenedor_cabecera.setSpacing(15)

        fila_titulo = QHBoxLayout()
        titulo = QLabel("Buscador de Personajes")
        titulo.setStyleSheet("color: black; font-size: 28px; font-weight: bold;")
        fila_titulo.addStretch()
        fila_titulo.addWidget(titulo)
        fila_titulo.addStretch()
        contenedor_cabecera.addLayout(fila_titulo)

        fila_busqueda = QHBoxLayout()
        self.buscador_oval = QLineEdit()
        self.buscador_oval.setPlaceholderText(" Buscar por nombre o creador...")
        self.buscador_oval.setFixedWidth(500)
        self.buscador_oval.setStyleSheet("""
            QLineEdit {
                background-color: white; border: 3px solid #800000;
                border-radius: 20px; padding: 10px 15px; color: black;
                font-size: 15px;
            }
        """)

        fila_busqueda.addStretch()
        fila_busqueda.addWidget(self.buscador_oval)
        fila_busqueda.addStretch()
        contenedor_cabecera.addLayout(fila_busqueda)
        layout_principal.addLayout(contenedor_cabecera)

        #busqueda/orden
        fila_filtros = QHBoxLayout()
        estilo_cb = """
            QComboBox { 
                background: #e62429; border: 1px solid red; border-radius: 6px; 
                padding: 6px; color: black; min-width: 160px;
            }
            QComboBox QAbstractItemView {
                background-color: #ffa6a6 ; color: black;
                selection-background-color: red; selection-color: red;
            }
        """
        # Ordenameinto
        self.cb_orden = QComboBox()
        self.cb_orden.addItems(["Ordenar por nombre"])
        self.cb_orden.setStyleSheet(estilo_cb)

        self.cb_lanz = QComboBox()
        self.cb_lanz.addItem("Lanzamiento")
        self.cb_lanz.setStyleSheet(estilo_cb)

        fila_filtros.addWidget(self.cb_orden)
        fila_filtros.addStretch()
        fila_filtros.addWidget(self.cb_lanz)
        layout_principal.addLayout(fila_filtros)

        self.cb_orden.clear()  # Limpiamos lo anterior
        self.cb_orden.addItems(["Nombre (A-Z)", "Nombre (Z-A)"])
        self.cb_orden.currentIndexChanged.connect(self.manejar_ordenamiento)

        # area de caudros
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: white; }")

        self.contenedor_grid = QWidget()
        self.contenedor_grid.setStyleSheet("background-color: white;")
        self.layout_grid = QGridLayout(self.contenedor_grid)
        self.layout_grid.setSpacing(20)
        self.layout_grid.setContentsMargins(10, 10, 10, 10)

        #Esto es solo para probar, aun no se debe conectar la api x,d
        # Generación de 10 personajes
        self.scroll.setWidget(self.contenedor_grid)
        layout_principal.addWidget(self.scroll)

        #paginacion
        #Son estaticos por ahora, cuando se integre la lista doble con la api ya no lo sera :D
        footer = QHBoxLayout()
        self.btn_ant = QPushButton("<")
        self.btn_sig = QPushButton(">")

        # Estilos
        self.btn_ant.setStyleSheet(
            "background: #333; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        self.btn_sig.setStyleSheet(
            "background: #e62429; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")

        self.lbl_pag = QLabel(f"{self.pagina_actual}")
        self.lbl_pag.setStyleSheet("color: black; font-weight: bold; font-size: 14px;")
        self.btn_sig.clicked.connect(self.pagina_siguiente)
        self.btn_ant.clicked.connect(self.pagina_anterior)
        footer.addStretch()
        footer.addWidget(self.btn_ant)
        footer.addSpacing(15)
        footer.addWidget(self.lbl_pag)
        footer.addSpacing(15)
        footer.addWidget(self.btn_sig)
        footer.addStretch()
        layout_principal.addLayout(footer)
        layout_exterior.addWidget(self.lienzo)


    def manejar_ordenamiento(self):
        if not self.lista_personajes or self.lista_personajes.esta_vacia():
            return

        texto_seleccionado = self.cb_orden.currentText()
        ascendente = (texto_seleccionado == "Nombre (A-Z)")
        self.lista_personajes.ordenar_por_nombre(ascendente=ascendente)
        self.pagina_actual = 0
        self.mostrar_pagina()

    def carga_datos(self):
        self.thread = QThread()
        self.trabajador = PageOrderer(self.gestor, self.perfil.clave)
        self.trabajador.moveToThread(self.thread)
        self.trabajador.finalizado.connect(self.recibir_lista)
        self.thread.started.connect(self.trabajador.dump_list)
        self.thread.start()


    def recibir_lista(self, lista):
        self.lista_personajes = lista
        self.mostrar_pagina()


    def mostrar_pagina(self):
        if not self.lista_personajes:
            return

        for i in reversed(range(self.layout_grid.count())):
            self.layout_grid.itemAt(i).widget().setParent(None)

        personajes_pagina = self.lista_personajes.obtener_pagina(self.pagina_actual, 10)
        for i, personaje in enumerate(personajes_pagina):
            fila = i // 5
            columna = i % 5
            tarjeta = self.crear_tarjeta_personaje(personaje)
            self.layout_grid.addWidget(tarjeta, fila, columna)
        self.lbl_pag.setText(f"{self.pagina_actual + 1}")


    def pagina_siguiente(self):
        if self.lista_personajes and (self.pagina_actual + 1) * 10 < self.lista_personajes.tamanio:
            self.pagina_actual += 1
            self.mostrar_pagina()


    def pagina_anterior(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.mostrar_pagina()


    def crear_tarjeta_personaje(self, nombre):
        tarjeta = QFrame()
        tarjeta.setFixedSize(180, 260)
        tarjeta.setStyleSheet("""
            QFrame { 
                background-color: #1a1a1a; 
                border-radius: 10px;
            }
            QFrame:hover { border: 2px solid #e62429; }
        """)

        ly = QVBoxLayout(tarjeta)
        ly.setContentsMargins(10, 10, 10, 10)

        # Imagen de referencia
        img = QLabel()
        img.setFixedSize(160, 160)
        img.setStyleSheet("background-color: #333; border-radius: 8px;")
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Nombre
        lbl_n = QLabel(nombre.nombre)
        lbl_n.setStyleSheet("color: white; font-weight: bold; font-size: 14px; border: none; background: transparent;")
        lbl_n.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botón Detalles
        btn = QPushButton("Ver Detalles")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton { 
                background: #e62429; color: white; border-radius: 4px; 
                font-size: 11px; font-weight: bold; padding: 5px;
            }
            QPushButton:hover { background: white; color: #e62429; }
        """)

        ly.addWidget(img)
        ly.addWidget(lbl_n)
        ly.addStretch()
        ly.addWidget(btn)

        btn.clicked.connect(lambda: self.enviar_a_detalles(nombre))
        return tarjeta

    def enviar_a_detalles(self, nombre):
        """Navega a la vista de detalles del personaje """
        ventana = self.window()
        if hasattr(ventana, 'stack') and hasattr(ventana, 'vista_detalles_per'):
            ventana.vista_detalles_per.actualizar_datos(nombre)
            ventana.stack.setCurrentIndex(3) #detalles indice 3

            # Limpia estilos de botones laterales
            if hasattr(ventana, 'actualizar_estilo_boton'):
                ventana.actualizar_estilo_boton(ventana.btn_home, False)
                ventana.actualizar_estilo_boton(ventana.btn_comics, False)
                ventana.actualizar_estilo_boton(ventana.btn_personajes, False)