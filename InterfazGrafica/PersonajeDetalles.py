import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QScrollArea, QFrame, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class DetallesPersonaje(QWidget):
    def __init__(self):
        super().__init__()
        # Fondo blanco para la ventana principal
        self.setStyleSheet("background-color: white; border: none;")

        # Layout Principal (Controla el espaciado global)
        layout_principal = QVBoxLayout(self)
        # --- CAMBIO CLAVE 1: Añadimos márgenes laterales para que nada se corte ---
        layout_principal.setContentsMargins(60, 20, 60, 20)
        layout_principal.setSpacing(25)

        # --- BOTÓN REGRESAR ---
        self.btn_regresar = QPushButton("← VOLVER AL LISTADO")
        self.btn_regresar.setFixedWidth(200)
        self.btn_regresar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_regresar.setStyleSheet("""
            QPushButton {
                background-color: transparent; color: #e62429;
                font-weight: bold; font-size: 13px; text-align: left;
            }
            QPushButton:hover { color: #ff3333; text-decoration: underline; }
        """)
        self.btn_regresar.clicked.connect(self.volver)
        layout_principal.addWidget(self.btn_regresar)

        # =========================================================================
        # --- SECCIÓN SUPERIOR: IMAGEN + DESCRIPCIÓN ---
        # =========================================================================
        fila_superior = QHBoxLayout()
        # Espacio fijo entre foto y descripción
        fila_superior.setSpacing(50)
        # Alineación superior para que la descripción empiece al nivel de la foto
        fila_superior.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Imagen Principal
        self.foto_perfil = QLabel()
        self.foto_perfil.setFixedSize(320, 320)
        self.foto_perfil.setStyleSheet("""
            border: 3px solid #e62429; 
            border-radius: 12px; 
            background-color: #f0f0f0;
        """)
        self.foto_perfil.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fila_superior.addWidget(self.foto_perfil)

        # ... (Mantener igual hasta la creación de info_layout)

        # Contenedor de Información (Nombre arriba, luego Desc y Creadores lado a lado)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(15)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.lbl_nombre = QLabel("NOMBRE DEL PERSONAJE")
        self.lbl_nombre.setStyleSheet("font-size: 38px; font-weight: bold; color: black; background: transparent;")
        info_layout.addWidget(self.lbl_nombre)

        # --- NUEVO LAYOUT HORIZONTAL PARA DESC + CREADORES ---
        layout_superior_detalles = QHBoxLayout()
        layout_superior_detalles.setSpacing(30)
        layout_superior_detalles.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Bloque de Descripción
        desc_container = QVBoxLayout()
        lbl_t_desc = QLabel("Descripción")
        lbl_t_desc.setStyleSheet("color: #e62429; font-size: 18px; font-weight: bold; background: transparent;")

        self.lbl_descripcion = QLabel("Selecciona un personaje...")
        self.lbl_descripcion.setWordWrap(True)
        self.lbl_descripcion.setStyleSheet("color: #333; font-size: 14px; line-height: 150%; background: transparent;")

        desc_container.addWidget(lbl_t_desc)
        desc_container.addWidget(self.lbl_descripcion)
        desc_container.addStretch()

        # Añadimos descripción al layout horizontal
        layout_superior_detalles.addLayout(desc_container, 1)

        # --- CUADRO DE CREADORES (Movid de abajo hacia aquí) ---
        self.lista_autores_widget = self.crear_cuadro_creadores("Autres", ["Stan Lee", "Steve Ditko"])
        self.lista_autores_widget.setFixedWidth(280)  # Ancho fijo para que no baile
        layout_superior_detalles.addWidget(self.lista_autores_widget)

        # Añadimos este layout horizontal al vertical principal de info
        info_layout.addLayout(layout_superior_detalles)

        fila_superior.addLayout(info_layout, 1)
        layout_principal.addLayout(fila_superior)

        # =========================================================================
        # --- SECCIÓN INFERIOR: SOLO CÓMICS Y EVENTOS ---
        # =========================================================================
        tablas_layout = QHBoxLayout()
        tablas_layout.setSpacing(30)
        tablas_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        items_demo = ["Amazing Fantasy #15", "Civil War", "Spider-Verse", "Secret Wars", "Avengers #1"]

        self.lista_comics = self.crear_lista_marvel("Cómics", items_demo)
        tablas_layout.addWidget(self.lista_comics)

        self.lista_eventos = self.crear_lista_marvel("Eventos", items_demo)
        tablas_layout.addWidget(self.lista_eventos)

        layout_principal.addLayout(tablas_layout)

        # ... (Resto de funciones de ayuda igual)

    # --- FUNCIONES DE AYUDA ---

    def crear_cuadro_creadores(self, titulo, nombres):
        frame = QFrame()
        # --- CAMBIO CLAVE 4: Quitamos ancho fijo para que se alinee con los otros ---
        frame.setStyleSheet("background: #161616; border-radius: 8px; border: 1px solid #222;")
        ly_frame = QVBoxLayout(frame)
        ly_frame.setContentsMargins(0, 0, 0, 0)

        # Header oscuro igual a los otros
        header = QLabel(f"  {titulo}")
        header.setFixedHeight(40)
        header.setStyleSheet("""
            background: #222; color: white; font-weight: bold; 
            border-bottom: 2px solid #e62429; 
            border-top-left-radius: 8px; border-top-right-radius: 8px;
            background-color: #222;
        """)
        ly_frame.addWidget(header)

        # Contenedor de la lista de autores
        contenedor = QWidget()
        contenedor.setStyleSheet("background: transparent; border: none;")
        ly_autores = QVBoxLayout(contenedor)
        ly_autores.setSpacing(10)
        ly_autores.setContentsMargins(10, 10, 10, 10)

        for nombre in nombres:
            ly_autores.addLayout(self.crear_item_autor(nombre))

        ly_autores.addStretch()
        ly_frame.addWidget(contenedor)

        # Paginación interna
        ly_frame.addWidget(self.crear_controles_paginacion(oscuro=True))

        return frame

    def crear_item_autor(self, nombre):
        ly = QHBoxLayout()
        img = QLabel()
        img.setFixedSize(40, 40)
        # Foto circular gris sobre fondo negro
        img.setStyleSheet("background: #333; border: 1px solid #444; border-radius: 20px;")

        lbl = QLabel(nombre)
        lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #eee; border: none; background: transparent;")

        ly.addWidget(img)
        ly.addWidget(lbl)
        ly.addStretch()
        return ly

    def crear_controles_paginacion(self, oscuro=True):
        widget_pag = QWidget()
        ly = QHBoxLayout(widget_pag)
        ly.setContentsMargins(0, 5, 0, 5)
        ly.setAlignment(Qt.AlignmentFlag.AlignCenter)

        color = "white" if oscuro else "black"
        estilo_flecha = f"color: {color}; font-size: 18px; font-weight: bold; border: none; background: transparent;"

        btn_prev = QPushButton("◀")
        btn_prev.setStyleSheet(estilo_flecha)
        btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)

        lbl_pag = QLabel("1")
        lbl_pag.setStyleSheet(
            f"color: {color}; font-weight: bold; font-size: 16px; padding: 0 10px; background: transparent;")

        btn_next = QPushButton("▶")
        btn_next.setStyleSheet(estilo_flecha)
        btn_next.setCursor(Qt.CursorShape.PointingHandCursor)

        ly.addWidget(btn_prev)
        ly.addWidget(lbl_pag)
        ly.addWidget(btn_next)
        return widget_pag

    def crear_lista_marvel(self, titulo, items):
        frame = QFrame()
        frame.setStyleSheet("background: #161616; border-radius: 8px; border: 1px solid #222;")
        ly_frame = QVBoxLayout(frame)
        ly_frame.setContentsMargins(0, 0, 0, 0)

        header = QLabel(f"  {titulo}")
        header.setFixedHeight(40)
        header.setStyleSheet("""
            background: #222; color: white; font-weight: bold; 
            border-bottom: 2px solid #e62429; 
            border-top-left-radius: 8px; border-top-right-radius: 8px;
            background-color: #222;
        """)
        ly_frame.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        # --- CAMBIO CLAVE 5: Ajustamos la altura del scroll para que todos terminen igual ---
        scroll.setFixedHeight(240)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none; background: #111; width: 8px; margin: 0px; border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #555; min-height: 20px; border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover { background: #e62429; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        contenedor_scroll = QWidget()
        contenedor_scroll.setStyleSheet("background: #161616;")
        ly_scroll = QVBoxLayout(contenedor_scroll)
        ly_scroll.setSpacing(0)
        ly_scroll.setContentsMargins(5, 5, 10, 5)

        for nombre in items:
            item_w = QWidget();
            item_w.setFixedHeight(55)
            item_ly = QHBoxLayout(item_w)

            img_m = QLabel();
            img_m.setFixedSize(35, 35)
            img_m.setStyleSheet("background: #333; border-radius: 4px;")
            txt = QLabel(nombre);
            txt.setStyleSheet("color: #ddd; font-size: 13px; border: none; background: transparent;")
            flecha = QLabel(">");
            flecha.setStyleSheet("color: #444; font-weight: bold; border: none; background: transparent;")

            item_ly.addWidget(img_m);
            item_ly.addWidget(txt, 1);
            item_ly.addWidget(flecha)
            item_w.setStyleSheet("QWidget:hover { background: #222; border-radius: 4px; }")
            ly_scroll.addWidget(item_w)

        ly_scroll.addStretch()
        scroll.setWidget(contenedor_scroll)
        ly_frame.addWidget(scroll)

        # Paginación
        ly_frame.addWidget(self.crear_controles_paginacion(oscuro=True))

        return frame

    def actualizar_datos(self, nombre):
        self.lbl_nombre.setText(f"Nombre: {nombre.upper()}")
        self.lbl_descripcion.setText(f"Información detallada sobre {nombre}. "
                                     f"Explora sus apariciones más importantes.")

    def volver(self):
        v = self.window()
        if hasattr(v, 'stack'):
            v.stack.setCurrentIndex(2)  # Regresa a la lista de personajes