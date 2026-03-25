import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from PersonajeMenu import PersonajesMenu
from PersonajeDetalles import DetallesPersonaje
from HomeMenu import HomeMenu


class MenuPrincipal(QMainWindow):
    def __init__(self, nombre_usuario="Admin"):
        super().__init__()
        self.setWindowTitle("MUNDO COMIC - Catálogo Virtual")
        self.showMaximized()
        # Fondo blanco para el área de contenido
        self.setStyleSheet("background-color: white; color: white; font-family: 'Segoe UI', Arial;")

        self.ruta_recursos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Recursos")

        # Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        #
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet("background-color: #161616; border-right: 1px solid #222;")
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        # Icono
        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_avatar = os.path.join(self.ruta_recursos, "icono.png")
        if os.path.exists(ruta_avatar):
            self.avatar_label.setPixmap(QPixmap(ruta_avatar).scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio,
                                                                    Qt.TransformationMode.SmoothTransformation))
        self.sidebar_layout.addWidget(self.avatar_label)

        self.lbl_logo = QLabel("MUNDO COMIC")
        self.lbl_logo.setStyleSheet("color: #e62429; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(self.lbl_logo)

        # Botones de Menú
        self.btn_home = self.crear_boton_menu("HOME", True)
        self.btn_comics = self.crear_boton_menu("COMICS", False)
        self.btn_personajes = self.crear_boton_menu("PERSONAJES", False)

        self.sidebar_layout.addWidget(self.btn_home)
        self.sidebar_layout.addWidget(self.btn_comics)
        self.sidebar_layout.addWidget(self.btn_personajes)
        self.sidebar_layout.addStretch()

        # --- STACKED WIDGET (CONTENEDOR) ---
        self.stack = QStackedWidget()
        self.vista_home_vacia = HomeMenu(self)

        # Comic, solo llamen al modulo, no colocar logica :D
        self.vista_comics_vacia = QWidget()

        # perosnjae
        self.vista_personajes = PersonajesMenu()

        #detalles personaje
        self.vista_detalles_per = DetallesPersonaje()


        self.stack.addWidget(self.vista_home_vacia)  #0
        self.stack.addWidget(self.vista_comics_vacia)  #1
        self.stack.addWidget(self.vista_personajes)  #2
        self.stack.addWidget(self.vista_detalles_per)  # 3

        # Conectar botones a sus índices
        self.btn_home.clicked.connect(lambda: self.cambiar_pestana(0, self.btn_home))
        self.btn_comics.clicked.connect(lambda: self.cambiar_pestana(1, self.btn_comics))
        self.btn_personajes.clicked.connect(lambda: self.cambiar_pestana(2, self.btn_personajes))

        self.stack.setCurrentIndex(0)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.stack)

    def cambiar_pestana(self, indice, boton):
        self.stack.setCurrentIndex(indice)
        for b in [self.btn_home, self.btn_comics, self.btn_personajes]:
            self.actualizar_estilo_boton(b, b == boton)

    def actualizar_estilo_boton(self, btn, activo):
        if activo:
            btn.setStyleSheet(
                "background-color: #252525; color: #e62429; border-left: 5px solid #e62429; text-align: left; font-weight: bold; font-size: 14px; height: 55px; border-right: none;")
        else:
            btn.setStyleSheet(
                "background-color: transparent; color: #888; border-left: 5px solid transparent; text-align: left; font-size: 14px; border: none; height: 55px;")

    def crear_boton_menu(self, texto, activo):
        btn = QPushButton(f"  {texto}")
        self.actualizar_estilo_boton(btn, activo)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def mostrar_detalles(self, nombre):
        #Función para saltar a la pantalla de detalles
        self.stack.setCurrentIndex(3)  # Índice de la vista de detalles