import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from Controladores.init import gestor


class HomeMenu(QWidget):
    def __init__(self, parent_principal=None):
        super().__init__()
        self.parent_principal = parent_principal
        self._lbl_stats = {}
        self.setStyleSheet("background-color: #121212;")

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(40, 30, 40, 30)
        root_layout.setSpacing(30)

        # ── Header ──────────────────────────────────────────────────────────
        header = QHBoxLayout()
        header.setSpacing(30)

        ruta_recursos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Recursos")
        ruta_marvel = os.path.join(ruta_recursos, "marvel.png")
        lbl_logo = QLabel()
        lbl_logo.setStyleSheet("border: none; background: transparent;")
        if os.path.exists(ruta_marvel):
            lbl_logo.setPixmap(QPixmap(ruta_marvel).scaled(
                320, 110,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        header.addWidget(lbl_logo)

        header.addStretch()

        bienvenida = QVBoxLayout()
        bienvenida.setSpacing(4)
        bienvenida.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

        lbl_hola = QLabel("Bienvenido,")
        lbl_hola.setStyleSheet("color: #aaaaaa; font-size: 16px; background: transparent;")
        lbl_hola.setAlignment(Qt.AlignmentFlag.AlignRight)
        bienvenida.addWidget(lbl_hola)

        perfil = getattr(parent_principal, 'perfil', None)
        nombre = (getattr(perfil, 'nombre', None) or getattr(perfil, 'usuario', 'Administrador')) if perfil else 'Administrador'
        lbl_nombre = QLabel(nombre)
        lbl_nombre.setStyleSheet("color: #ffffff; font-size: 26px; font-weight: bold; background: transparent;")
        lbl_nombre.setAlignment(Qt.AlignmentFlag.AlignRight)
        bienvenida.addWidget(lbl_nombre)

        header.addLayout(bienvenida)
        root_layout.addLayout(header)

        # ── Separador + subtítulo ────────────────────────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: #2a2a2a; border: none; max-height: 1px;")
        root_layout.addWidget(sep)

        lbl_panel = QLabel("Panel de Administración")
        lbl_panel.setStyleSheet("color: #aaaaaa; font-size: 14px; background: transparent;")
        root_layout.addWidget(lbl_panel)

        # ── Stats ────────────────────────────────────────────────────────────
        stats_row = QHBoxLayout()
        stats_row.setSpacing(20)

        raw = gestor.raw_data
        stats = [
            ("Cómics",     "comics",      len(raw.d_comics.datos)),
            ("Personajes", "personajes", len(raw.d_personajes.datos)),
            ("Creadores",  "creadores",   len(raw.d_creadores.datos)),
            ("Eventos",    "eventos",    len(raw.d_eventos.datos)),
        ]
        for titulo, clave, icono, valor in stats:
            stats_row.addWidget(self._crear_stat_card(titulo, clave, icono, valor))

        root_layout.addLayout(stats_row)

        # ── Accesos rápidos ──────────────────────────────────────────────────
        lbl_accesos = QLabel("Accesos rápidos")
        lbl_accesos.setStyleSheet("color: #aaaaaa; font-size: 14px; background: transparent;")
        root_layout.addWidget(lbl_accesos)

        accesos_row = QHBoxLayout()
        accesos_row.setSpacing(20)

        self.btn_ir_comics = QPushButton("  Explorar Cómics")
        self.btn_ir_comics.setFixedHeight(52)
        self.btn_ir_comics.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ir_comics.setStyleSheet("""
            QPushButton {
                background-color: #e62429; color: white; border-radius: 8px;
                font-weight: bold; font-size: 15px; text-align: left; padding-left: 20px;
                border: none;
            }
            QPushButton:hover { background-color: #ff3333; }
        """)
        self.btn_ir_comics.clicked.connect(self._ir_a_comics)

        self.btn_explorar = QPushButton("  Explorar Personajes")
        self.btn_explorar.setFixedHeight(52)
        self.btn_explorar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_explorar.setStyleSheet("""
            QPushButton {
                background-color: #252525; color: #ffffff; border-radius: 8px;
                font-weight: bold; font-size: 15px; text-align: left; padding-left: 20px;
                border: 1px solid #e62429;
            }
            QPushButton:hover { background-color: #2d2d2d; }
        """)
        self.btn_explorar.clicked.connect(self.ir_a_personajes)

        accesos_row.addWidget(self.btn_ir_comics)
        accesos_row.addWidget(self.btn_explorar)
        root_layout.addLayout(accesos_row)

        root_layout.addStretch()

    def _crear_stat_card(self, titulo, clave, icono, valor):
        card = QFrame()
        card.setMinimumHeight(110)
        card.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 12px;
                border-top: 3px solid #e62429;
                border-left: 1px solid #2a2a2a;
                border-right: 1px solid #2a2a2a;
                border-bottom: 1px solid #2a2a2a;
            }
        """)

        ly = QVBoxLayout(card)
        ly.setContentsMargins(20, 16, 20, 16)
        ly.setSpacing(6)
        ly.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        lbl_icono_valor = QHBoxLayout()
        lbl_icono_valor.setSpacing(10)

        lbl_icono = QLabel(icono)
        lbl_icono.setStyleSheet("font-size: 22px; background: transparent; border: none;")
        lbl_icono_valor.addWidget(lbl_icono)

        lbl_valor = QLabel(str(valor))
        lbl_valor.setStyleSheet(
            "font-size: 36px; font-weight: bold; color: #e62429; background: transparent; border: none;"
        )
        lbl_icono_valor.addWidget(lbl_valor)
        lbl_icono_valor.addStretch()
        ly.addLayout(lbl_icono_valor)

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet(
            "font-size: 13px; color: #aaaaaa; background: transparent; border: none;"
        )
        ly.addWidget(lbl_titulo)

        self._lbl_stats[clave] = lbl_valor
        return card

    def actualizar_stats(self):
        raw = gestor.raw_data
        counts = {
            "comics":     len(raw.d_comics.datos),
            "personajes": len(raw.d_personajes.datos),
            "creadores":  len(raw.d_creadores.datos),
            "eventos":    len(raw.d_eventos.datos),
        }
        for clave, lbl in self._lbl_stats.items():
            lbl.setText(str(counts[clave]))

    def _ir_a_comics(self):
        if self.parent_principal:
            self.parent_principal.cambiar_pestana(1, self.parent_principal.btn_comics)

    def ir_a_personajes(self):
        if self.parent_principal:
            self.parent_principal.cambiar_pestana(2, self.parent_principal.btn_personajes)
