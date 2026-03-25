import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QScrollArea, QFrame, QLineEdit,
                             QComboBox, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class PersonajesMenu(QWidget):
    def __init__(self):
        super().__init__()
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
        self.buscador_oval.setPlaceholderText(" Buscar personajes...")
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

        # filtros de busqueda/orden
        fila_filtros = QHBoxLayout()
        estilo_cb = """
            QComboBox { 
                background: #f8f8f8; border: 1px solid #ddd; border-radius: 6px; 
                padding: 6px; color: black; min-width: 160px;
            }
            QComboBox QAbstractItemView {
                background-color: white; color: black;
                selection-background-color: #e62429; selection-color: white;
            }
        """
        self.cb_orden = QComboBox();
        self.cb_orden.addItems(["Ordenar por nombre", "Creador"]);
        self.cb_orden.setStyleSheet(estilo_cb)
        self.cb_lanz = QComboBox();
        self.cb_lanz.addItem("Lanzamiento");
        self.cb_lanz.setStyleSheet(estilo_cb)

        fila_filtros.addWidget(self.cb_orden)
        fila_filtros.addStretch()
        fila_filtros.addWidget(self.cb_lanz)
        layout_principal.addLayout(fila_filtros)

        # cuadros para mostrar a personajes
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: white; }")

        self.contenedor_grid = QWidget()
        self.contenedor_grid.setStyleSheet("background-color: white;")
        self.layout_grid = QGridLayout(self.contenedor_grid)
        self.layout_grid.setSpacing(20)
        self.layout_grid.setContentsMargins(10, 10, 10, 10)

        # Generacion de personajes de prueba en cuadrícula
        personajes = ["Spider-Man", "Iron Man", "Black Panther", "Thor", "Storm",
                      "Deadpool", "Black Widow", "Falcon", "Captain Marvel", "She-Hulk"]

        for i, nombre in enumerate(personajes):
            fila = i // 5
            columna = i % 5
            self.layout_grid.addWidget(self.crear_tarjeta_personaje(nombre), fila, columna)

        self.scroll.setWidget(self.contenedor_grid)
        layout_principal.addWidget(self.scroll)

        # pahinacion
        footer = QHBoxLayout()
        btn_ant = QPushButton("< Anterior")
        btn_sig = QPushButton("Siguiente >")
        estilo_btn_pag = "QPushButton { background: #333; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold; }"
        btn_ant.setStyleSheet(estilo_btn_pag)
        btn_sig.setStyleSheet(
            "background: #e62429; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")

        footer.addStretch()
        footer.addWidget(btn_ant)
        footer.addSpacing(10)
        footer.addWidget(btn_sig)
        footer.addStretch()
        layout_principal.addLayout(footer)

        layout_exterior.addWidget(self.lienzo)

    def crear_tarjeta_personaje(self, nombre):
        tarjeta = QFrame()
        tarjeta.setFixedSize(180, 260)
        # Diseño de tarjeta
        tarjeta.setStyleSheet("""
            QFrame { 
                background-color: #1a1a1a; 
                border-radius: 10px;
            }
        """)

        ly = QVBoxLayout(tarjeta)
        ly.setContentsMargins(10, 10, 10, 10)

        # Imagen del personaje
        img = QLabel()
        img.setFixedSize(160, 160)
        img.setStyleSheet("background-color: #333; border-radius: 8px;")  # Simula la imagen de ref
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Nombre
        lbl_n = QLabel(nombre)
        lbl_n.setStyleSheet("color: white; font-weight: bold; font-size: 14px; border: none;")
        lbl_n.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botón Detalles
        btn = QPushButton("Ver Detalles")
        btn.setStyleSheet("""
            QPushButton { 
                background: #e62429; color: white; border-radius: 4px; 
                font-size: 11px; font-weight: bold; padding: 5px;
            }
        """)

        ly.addWidget(img)
        ly.addWidget(lbl_n)
        ly.addWidget(btn)

        btn.clicked.connect(lambda: self.enviar_a_detalles(nombre))

        return tarjeta

    def enviar_a_detalles(self, nombre):
        #Obtenemos la ventana principal
        ventana = self.window()

        if hasattr(ventana, 'stack') and hasattr(ventana, 'vista_detalles_per'):
            ventana.vista_detalles_per.actualizar_datos(nombre)

            ventana.stack.setCurrentIndex(3) #el indice 3 es detalles de personaje

            #Desactive los botones del sidebar para que ninguno parezca como seleccionado (ya paso y se miraba mal xd)
            if hasattr(ventana, 'btn_personajes'):
                ventana.actualizar_estilo_boton(ventana.btn_home, False)
                ventana.actualizar_estilo_boton(ventana.btn_comics, False)
                ventana.actualizar_estilo_boton(ventana.btn_personajes, False)