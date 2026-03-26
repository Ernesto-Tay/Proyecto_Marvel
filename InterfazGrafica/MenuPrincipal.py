import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from ComicMenu import ComicsMenu
from ComicDetalles import DetallesComic
from PersonajeMenu import PersonajesMenu
from PersonajeDetalles import DetallesPersonaje
from HomeMenu import HomeMenu
from Estructuras_Listas.lista_circular import ListaCircular


class MenuPrincipal(QMainWindow):
    def __init__(self, perfil):
        super().__init__()
        # Lista circular para navegar entre secciones principales
        self.nav_circular = ListaCircular()
        self.nav_circular.agregar(0)  # Home
        self.nav_circular.agregar(1)  # Comics
        self.nav_circular.agregar(2)  # Personajes

        self.perfil = perfil
        self.setWindowTitle("MUNDO COMIC - Catálogo Virtual")
        self.showMaximized()
        self.setStyleSheet("background-color: #121212; color: white; font-family: 'Segoe UI', Arial;")

        self.ruta_recursos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Recursos")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sidebar
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
        self.lbl_logo.setStyleSheet("color: #e62429; font-size: 24px; font-weight: bold; margin-bottom: 4px;")
        self.lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(self.lbl_logo)

        nombre_admin = getattr(perfil, 'nombre', None) or getattr(perfil, 'usuario', 'Admin')
        self.lbl_admin = QLabel(f"Admin: {nombre_admin}")
        self.lbl_admin.setStyleSheet("color: #666666; font-size: 11px; background: transparent;")
        self.lbl_admin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(self.lbl_admin)

        sep_top = QFrame()
        sep_top.setFrameShape(QFrame.Shape.HLine)
        sep_top.setStyleSheet("background: #2a2a2a; border: none; max-height: 1px; margin: 8px 0px;")
        self.sidebar_layout.addWidget(sep_top)

        # Navegación Circular
        fila_flechas = QHBoxLayout()
        self.btn_atras_circ = QPushButton("◀")
        self.btn_sig_circ = QPushButton("▶")

        estilo_flecha = """
            QPushButton {
                background-color: #252525; color: #e62429; border-radius: 15px;
                font-weight: bold; font-size: 13px; min-width: 45px; height: 30px;
                border: 1px solid #333333;
            }
            QPushButton:hover { background-color: #e62429; color: white; border: 1px solid #e62429; }
        """
        self.btn_atras_circ.setStyleSheet(estilo_flecha)
        self.btn_sig_circ.setStyleSheet(estilo_flecha)

        fila_flechas.addStretch()
        fila_flechas.addWidget(self.btn_atras_circ)
        fila_flechas.addSpacing(10)
        fila_flechas.addWidget(self.btn_sig_circ)
        fila_flechas.addStretch()

        self.sidebar_layout.addLayout(fila_flechas)
        self.sidebar_layout.addSpacing(15)

        # Botones de Menú
        self.btn_home = self.crear_boton_menu("HOME", True)
        self.btn_comics = self.crear_boton_menu("COMICS", False)
        self.btn_personajes = self.crear_boton_menu("PERSONAJES", False)

        self.sidebar_layout.addWidget(self.btn_home)
        self.sidebar_layout.addWidget(self.btn_comics)
        self.sidebar_layout.addWidget(self.btn_personajes)
        self.sidebar_layout.addStretch()

        sep_bottom = QFrame()
        sep_bottom.setFrameShape(QFrame.Shape.HLine)
        sep_bottom.setStyleSheet("background: #2a2a2a; border: none; max-height: 1px;")
        self.sidebar_layout.addWidget(sep_bottom)

        lbl_version = QLabel("v1.0 — Mundo Comic")
        lbl_version.setStyleSheet("color: #444444; font-size: 10px; padding: 8px; background: transparent;")
        lbl_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(lbl_version)

        # Stacked Widget (contenedor de vistas)
        self.stack = QStackedWidget()

        self.vista_home = HomeMenu(self)              # índice 0
        self.vista_comics = ComicsMenu(perfil)        # índice 1
        self.vista_personajes = PersonajesMenu(perfil) # índice 2
        self.vista_detalles_per = DetallesPersonaje() # índice 3
        self.vista_detalles_comic = DetallesComic()   # índice 4

        self.stack.addWidget(self.vista_home)
        self.stack.addWidget(self.vista_comics)
        self.stack.addWidget(self.vista_personajes)
        self.stack.addWidget(self.vista_detalles_per)
        self.stack.addWidget(self.vista_detalles_comic)

        # Conexiones
        self.btn_sig_circ.clicked.connect(self.mover_siguiente_circular)
        self.btn_atras_circ.clicked.connect(self.mover_anterior_circular)

        self.btn_home.clicked.connect(lambda: self.cambiar_pestana(0, self.btn_home))
        self.btn_comics.clicked.connect(lambda: self.cambiar_pestana(1, self.btn_comics))
        self.btn_personajes.clicked.connect(lambda: self.cambiar_pestana(2, self.btn_personajes))

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.stack)
        self.stack.setCurrentIndex(0)

    def mover_siguiente_circular(self):
        indice = self.nav_circular.siguiente()
        self.sincronizar_ui_circular(indice)

    def mover_anterior_circular(self):
        indice = self.nav_circular.anterior()
        self.sincronizar_ui_circular(indice)

    def sincronizar_ui_circular(self, indice):
        self.stack.setCurrentIndex(indice)
        botones = {0: self.btn_home, 1: self.btn_comics, 2: self.btn_personajes}
        for i, btn in botones.items():
            self.actualizar_estilo_boton(btn, i == indice)
        if indice == 0:
            self.vista_home.actualizar_stats()

    def cambiar_pestana(self, indice, boton):
        self.stack.setCurrentIndex(indice)
        # Sincronizamos el puntero de la lista circular
        while self.nav_circular.actual.dato != indice:
            self.nav_circular.siguiente()

        for b in [self.btn_home, self.btn_comics, self.btn_personajes]:
            self.actualizar_estilo_boton(b, b == boton)
        if indice == 0:
            self.vista_home.actualizar_stats()

    def actualizar_estilo_boton(self, btn, activo):
        if activo:
            btn.setStyleSheet(
                "background-color: #252525; color: #e62429; "
                "border-left: 4px solid #e62429; border-top: none; border-right: none; border-bottom: none; "
                "text-align: left; padding-left: 16px; font-weight: bold; font-size: 14px; height: 55px;")
        else:
            btn.setStyleSheet(
                "background-color: transparent; color: #888888; "
                "border-left: 4px solid transparent; border-top: none; border-right: none; border-bottom: none; "
                "text-align: left; padding-left: 16px; font-size: 14px; height: 55px;")

    def crear_boton_menu(self, texto, activo):
        btn = QPushButton(f"  {texto}")
        self.actualizar_estilo_boton(btn, activo)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn
