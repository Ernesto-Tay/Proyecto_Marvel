import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from ComicMenu import ComicMenu


class MenuPrincipal(QMainWindow):
    def __init__(self, nombre_usuario="Admin"):
        super().__init__()
        self.setWindowTitle("MUNDO COMIC - Catálogo Virtual")
        self.showMaximized()

        # rutas
        self.ruta_script = os.path.dirname(os.path.abspath(__file__))
        self.carpeta_recursos = os.path.join(self.ruta_script, "Recursos")
        self.setStyleSheet("background-color: #0f0f0f; color: white; font-family: 'Segoe UI', Arial;")

        # Layout Principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Barra lateral :D, aqui vamos a poder movernos entre las secciones de comic y menu
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet("background-color: #161616; border-right: 1px solid #222;")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(10)

        #el icono del spiderman :D
        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_avatar = os.path.join(self.carpeta_recursos, "icono.png")

        if os.path.exists(ruta_avatar):
            pixmap = QPixmap(ruta_avatar)
            self.avatar_label.setPixmap(
                pixmap.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.avatar_label.setText("👤")
            self.avatar_label.setStyleSheet("font-size: 60px; color: #444; margin-bottom: 10px;")

        self.sidebar_layout.addWidget(self.avatar_label)


        self.lbl_logo = QLabel("MUNDO COMIC")
        self.lbl_logo.setStyleSheet("color: #e62429; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(self.lbl_logo)

        #botones de navegacion
        self.btn_home = self.crear_boton_menu("HOME", False)
        self.btn_comics = self.crear_boton_menu("COMICS", True)
        self.btn_personajes = self.crear_boton_menu("PERSONAJES", False)

        self.sidebar_layout.addWidget(self.btn_home)
        self.sidebar_layout.addWidget(self.btn_comics)
        self.sidebar_layout.addWidget(self.btn_personajes)
        self.sidebar_layout.addStretch()

        self.stack = QStackedWidget()
        self.vista_comics = ComicMenu()
        self.stack.addWidget(self.vista_comics)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.stack)

    def crear_boton_menu(self, texto, activo):
        btn = QPushButton(f"  {texto}")
        btn.setFixedHeight(55)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if activo:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #252525; color: #e62429; border-left: 5px solid #e62429;
                    text-align: left; font-weight: bold; font-size: 14px; border-radius: 0;
                } """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent; color: #888; border-left: 5px solid transparent;
                    text-align: left; font-size: 14px; border: none;
                }
                QPushButton:hover { background-color: #202020; color: white; }
            """)
        return btn