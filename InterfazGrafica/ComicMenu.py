import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QScrollArea, QFrame, QLineEdit,
                             QComboBox, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap


class ComicMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white; border: none;")

        # Layout exterior
        layout_exterior = QVBoxLayout(self)
        layout_exterior.setContentsMargins(0, 0, 0, 0)

        # Contenedor principal
        self.lienzo = QFrame()
        self.lienzo.setStyleSheet("background-color: white;")
        layout_principal = QVBoxLayout(self.lienzo)
        layout_principal.setContentsMargins(25, 20, 25, 10)

        # cabecera
        contenedor_cabecera = QVBoxLayout()
        contenedor_cabecera.setSpacing(15)

        # Título Centrado
        fila_titulo = QHBoxLayout()
        titulo = QLabel("Buscador de comics")
        titulo.setStyleSheet("color: black; font-size: 28px; font-weight: bold;")
        fila_titulo.addStretch()
        fila_titulo.addWidget(titulo)
        fila_titulo.addStretch()
        contenedor_cabecera.addLayout(fila_titulo)

        # buscador
        fila_busqueda = QHBoxLayout()

        # BARRA DE BÚSQUEDA
        self.buscador_oval = QLineEdit()
        self.buscador_oval.setPlaceholderText(" Buscar comics por nombre...")
        self.buscador_oval.setFixedWidth(500)
        self.buscador_oval.setStyleSheet("""
            QLineEdit {
                background-color: white; border: 3px solid #800000;
                border-radius: 20px; padding: 10px 15px; color: black;
                font-size: 15px;
            }
        """)

        # BOTÓN FECHA
        self.btn_fecha = QPushButton("Fecha\nAAAA MM")
        self.btn_fecha.setFixedSize(110, 60)
        self.btn_fecha.setStyleSheet("""
            QPushButton {
                background-color: #ff3333; color: white; border-radius: 12px; 
                font-weight: bold; border-bottom: 5px solid #ffcccc;
            }
        """)

        fila_busqueda.addStretch()
        fila_busqueda.addWidget(self.buscador_oval)
        fila_busqueda.addSpacing(20)
        fila_busqueda.addWidget(self.btn_fecha)
        fila_busqueda.addStretch()
        contenedor_cabecera.addLayout(fila_busqueda)

        layout_principal.addLayout(contenedor_cabecera)

        fila_filtros = QHBoxLayout()
        fila_filtros.setContentsMargins(10, 20, 20, 20)

        estilo_cb = """
            QComboBox { 
                background: #f8f8f8; border: 1px solid #ddd; border-radius: 6px; 
                padding: 6px; color: black; min-width: 140px;
            }
            QComboBox QAbstractItemView {
                background-color: white; color: black;
                selection-background-color: #e62429; selection-color: white;
            }
        """

        self.cb_tipo = QComboBox();
        self.cb_tipo.addItems(["Nombre", "ID"]);
        self.cb_tipo.setStyleSheet(estilo_cb)
        self.cb_lanz = QComboBox();
        self.cb_lanz.addItem("Fecha Lanzamiento");
        self.cb_lanz.setStyleSheet(estilo_cb)
        self.cb_orden = QComboBox();
        self.cb_orden.addItems(["A - Z", "Z - A"]);
        self.cb_orden.setStyleSheet(estilo_cb)
        self.cb_anio = QComboBox();
        self.cb_anio.addItem("Año");
        self.cb_anio.setStyleSheet(estilo_cb)

        fila_filtros.addWidget(self.cb_tipo)
        fila_filtros.addStretch()
        fila_filtros.addWidget(self.cb_lanz)
        fila_filtros.addWidget(self.cb_orden)
        fila_filtros.addWidget(self.cb_anio)
        layout_principal.addLayout(fila_filtros)

        #listado de comic
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        # Barra de desplazamiento
        self.scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: white; }
            QScrollBar:vertical {
                border: none; background: #f0f0f0; width: 10px; border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #e62429; border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        self.contenedor_items = QWidget()
        self.contenedor_items.setStyleSheet("background-color: white;")
        self.layout_lista = QVBoxLayout(self.contenedor_items)
        self.layout_lista.setSpacing(0)
        self.layout_lista.setContentsMargins(10, 15, 20, 15)

        for i in range(5):
            self.layout_lista.addWidget(self.crear_item_lista(f"NOmbre Cmic{i + 1}", 2020 + i))
        #Aqi es estatico, por ahora, despues se modificara porque aun no recibe datos de la api :,D
        self.scroll.setWidget(self.contenedor_items)
        layout_principal.addWidget(self.scroll)

        # paginacion
        footer_layout = QHBoxLayout()
        self.lbl_paginacion = QLabel("1")
        self.lbl_paginacion.setFixedSize(60, 35)
        self.lbl_paginacion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_paginacion.setStyleSheet("""
            QLabel {
                background-color: white; color: #e62429; font-weight: bold;
                font-size: 16px; border: 2px solid #e62429; border-radius: 8px;
            }
        """)

        footer_layout.addStretch()
        footer_layout.addWidget(self.lbl_paginacion)
        footer_layout.addStretch()
        layout_principal.addLayout(footer_layout)

        layout_exterior.addWidget(self.lienzo)

    def crear_item_lista(self, nombre, anio):
        item_frame = QFrame()
        # Línea divisoria roja superior
        item_frame.setStyleSheet("QFrame { border-top: 1px solid #800000; background-color: white; }")

        ly_h = QHBoxLayout(item_frame)
        ly_h.setContentsMargins(0, 20, 0, 20)

        img = QLabel()
        img.setFixedSize(110, 160)

        ruta_foto = os.path.join(os.path.dirname(__file__), "Recursos", "portada.jpg")
        pixmap = QPixmap(ruta_foto)

        if not pixmap.isNull():
            img.setPixmap(pixmap.scaled(110, 160, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                        Qt.TransformationMode.SmoothTransformation))
            img.setStyleSheet("border: none; border-radius: 4px;")
        else:
            img.setStyleSheet("background-color: #f0f0f0; border: 1px solid #800000; border-radius: 4px;")
            img.setText("Sin Foto")
            img.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Información
        info = QVBoxLayout()
        # Texto negro y grande, como en la imagen
        lbl_n = QLabel(f"Nombre: {nombre}");
        lbl_n.setStyleSheet("color: black; font-size: 20px; font-weight: bold; border: none;")
        lbl_f = QLabel(f"Lanzamiento: {anio}");
        lbl_f.setStyleSheet("color: black; font-size: 20px; border: none;")
        btn = QPushButton("Detalles");
        btn.setFixedSize(110, 35);
        btn.setStyleSheet("background: #ff3333; color: white; border-radius: 12px; font-weight: bold; border: none;")

        info.addWidget(lbl_n);
        info.addSpacing(5);
        info.addWidget(lbl_f);
        info.addSpacing(10);
        info.addWidget(btn);
        info.addStretch()
        ly_h.addWidget(img);
        ly_h.addSpacing(25);
        ly_h.addLayout(info);
        ly_h.addStretch()

        return item_frame