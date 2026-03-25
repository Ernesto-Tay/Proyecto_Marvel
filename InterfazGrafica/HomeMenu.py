import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class HomeMenu(QWidget):
    def __init__(self, parent_principal=None):
        super().__init__()
        self.parent_principal = parent_principal
        self.setStyleSheet("background-color: #1a1a1a;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Logo / Imagen
        self.lbl_logo = QLabel()
        ruta_recursos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Recursos")
        ruta_marvel = os.path.join(ruta_recursos, "marvel.png")

        if os.path.exists(ruta_marvel):
            pixmap = QPixmap(ruta_marvel).scaled(600, 400,
                                                 Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation)
            self.lbl_logo.setPixmap(pixmap)
        else:
            self.lbl_logo.setText("BIENVENIDO A MUNDO COMIC")
            self.lbl_logo.setStyleSheet("color: white; font-size: 40px; font-weight: bold;")

        self.lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_logo)

        # Botón de Bienvenido
        self.btn_explorar = QPushButton("¡BIENVENIDO!")
        self.btn_explorar.setFixedWidth(250)
        self.btn_explorar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_explorar.setStyleSheet("""
            QPushButton {
                background-color: #e62429; color: white; border-radius: 5px;
                padding: 12px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #ff3333; }
        """)

        #Aqui fue el error, la funcion se debe pasar sin parentesis x,d
        self.btn_explorar.clicked.connect(self.ir_a_personajes)
        layout.addWidget(self.btn_explorar, 0, Qt.AlignmentFlag.AlignCenter)

    def ir_a_personajes(self):
        if self.parent_principal:
            self.parent_principal.cambiar_pestana(2, self.parent_principal.btn_personajes)