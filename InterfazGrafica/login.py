import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,QPushButton, QLabel, QLineEdit, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QBrush, QImage, QPixmap

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controladores.auth import Auth


class MundoComicLogin(QWidget):
    def __init__(self, auth, on_login_exitoso):
        super().__init__()
        self.auth = auth
        self.on_login_exitoso = on_login_exitoso

        self.setWindowTitle("Mundo Comic - Catálogo Virtual")

        # --- CONFIGURACIÓN DE RUTAS ---
        self.ruta_script = os.path.dirname(os.path.abspath(__file__))
        self.carpeta_recursos = os.path.join(self.ruta_script, "Recursos")

        # Configucion el tamaño inicial
        self.setMinimumSize(1000, 700)
        self.showMaximized()

        self.setup_ui()

    def resizeEvent(self, event):
        self.actualizar_fondo()
        super().resizeEvent(event)

    def actualizar_fondo(self):
        ruta_fondo = os.path.join(self.carpeta_recursos, "img_1.png")
        if os.path.exists(ruta_fondo):
            oImage = QImage(ruta_fondo)
            # Usamos self.rect().size() para obtener el tamaño real de la pantalla actual, porque antes no dejaba
            #y se miraba feo >:(
            sImage = oImage.scaled(self.size(),Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)
            palette = QPalette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
            self.setPalette(palette)

    def setup_ui(self):
        self.setStyleSheet("color: white; font-family: 'Segoe UI', Arial;")

        # Ccentrado de la pagina :D
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- TARJETA DE LOGIN--- Esto ayuda a mantener tamaño
        container = QFrame()
        container.setFixedSize(400, 580)
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(20, 20, 20, 235); 
                border: 2px solid #e62429;
                border-radius: 30px;}""")

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 30, 40, 30)
        container_layout.setSpacing(10)

        # --- SECCIÓN DONDE IRA EL LOGO DE SPIDERMAN :D ---
        ruta_logo = os.path.join(self.carpeta_recursos, "UWU-PNG-Image.png")
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("border: none; background: transparent;")

        if os.path.exists(ruta_logo):
            img_logo = QImage(ruta_logo)
            scaled_logo = img_logo.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(QPixmap.fromImage(scaled_logo))
        else:
            logo_label.setText("")

        container_layout.addWidget(logo_label)

        # Titulos
        titulo = QLabel("MUNDO COMIC")
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; border: none; background: transparent;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(titulo)

        sub_titulo = QLabel("- Catálogo Virtual -")
        sub_titulo.setStyleSheet("color: #888; border: none; font-size: 13px; background: transparent;")
        sub_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(sub_titulo)

        container_layout.addSpacing(20)

        #INPUTS
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("USUARIO")
        self.apply_input_style(self.user_input)
        container_layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("CONTRASEÑA")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.apply_input_style(self.pass_input)
        container_layout.addWidget(self.pass_input)

        container_layout.addSpacing(20)

        # Botón Entrar
        btn_entrar = QPushButton("ENTRAR")
        btn_entrar.setMinimumHeight(55)
        btn_entrar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_entrar.setStyleSheet("""
            QPushButton {
                background-color: #e62429;
                color: white;
                border-radius: 27px;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover { background-color: #ff2b31; }""")
        btn_entrar.clicked.connect(self.intentar_login)
        container_layout.addWidget(btn_entrar)

        # Links
        links = QLabel("¿Olvidó su contraseña?")
        links.setAlignment(Qt.AlignmentFlag.AlignCenter)
        links.setStyleSheet("background: transparent; border: none; color: #666; font-size: 11px; margin-top: 10px;")
        container_layout.addWidget(links)

        main_layout.addWidget(container)

    def apply_input_style(self, widget):
        widget.setMinimumHeight(48)
        widget.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 12px;
                padding-left: 15px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #e62429; }""")

    def intentar_login(self):
        usuario = self.user_input.text().strip()
        contra = self.pass_input.text()
        exito, mensaje = self.auth.login(usuario, contra)

        if exito:
            QMessageBox.information(self, "Confirmación", f"Bienvenido {self.auth.admin.nombre}")
            self.on_login_exitoso()
        else:
            QMessageBox.critical(self, "Error", mensaje)



app = QApplication(sys.argv)
auth_service = Auth()

