import math
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from Estructuras_Listas.Lista_simple import ListaSimple


class DetallesComic(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212; border: none;")

        self.tamanio_pagina = 10
        self.estado_listas = {
            "autores": {"lista": ListaSimple(), "pagina": 0, "layout": None, "lbl_pag": None, "btn_prev": None, "btn_next": None},
            "personajes": {"lista": ListaSimple(), "pagina": 0, "layout": None, "lbl_pag": None, "btn_prev": None, "btn_next": None},
        }

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(60, 20, 60, 20)
        layout_principal.setSpacing(25)

        self.btn_regresar = QPushButton("VOLVER AL LISTADO")
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

        fila_superior = QHBoxLayout()
        fila_superior.setSpacing(50)
        fila_superior.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.foto_portada = QLabel()
        self.foto_portada.setFixedSize(280, 380)
        self.foto_portada.setStyleSheet("""
            border: 3px solid #e62429;
            border-radius: 12px;
            background-color: #1a1a1a;
            color: #666666;
        """)
        self.foto_portada.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.foto_portada.setText("No Image")
        fila_superior.addWidget(self.foto_portada)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(12)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.lbl_titulo = QLabel("TITULO DEL COMIC")
        self.lbl_titulo.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffffff; background: transparent;")
        self.lbl_titulo.setWordWrap(True)
        info_layout.addWidget(self.lbl_titulo)

        self.lbl_fecha = QLabel("")
        self.lbl_fecha.setStyleSheet("color: #e62429; font-size: 16px; font-weight: bold; background: transparent;")
        info_layout.addWidget(self.lbl_fecha)

        self.lbl_isbn = QLabel("")
        self.lbl_isbn.setStyleSheet("color: #aaaaaa; font-size: 13px; background: transparent;")
        info_layout.addWidget(self.lbl_isbn)

        lbl_t_desc = QLabel("Descripcion")
        lbl_t_desc.setStyleSheet("color: #e62429; font-size: 16px; font-weight: bold; background: transparent; margin-top: 8px;")
        info_layout.addWidget(lbl_t_desc)

        self.lbl_descripcion = QLabel("Selecciona un comic...")
        self.lbl_descripcion.setWordWrap(True)
        self.lbl_descripcion.setStyleSheet("color: #cccccc; font-size: 13px; line-height: 150%; background: transparent;")
        info_layout.addWidget(self.lbl_descripcion)
        info_layout.addStretch()

        fila_superior.addLayout(info_layout, 1)
        layout_principal.addLayout(fila_superior)

        tablas_layout = QHBoxLayout()
        tablas_layout.setSpacing(30)
        tablas_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.lista_autores_widget = self._crear_lista("Autores", "autores")
        tablas_layout.addWidget(self.lista_autores_widget)

        self.lista_personajes_widget = self._crear_lista("Personajes que Aparecen", "personajes")
        tablas_layout.addWidget(self.lista_personajes_widget)

        layout_principal.addLayout(tablas_layout)

    def _crear_lista(self, titulo, clave):
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
        scroll.setFixedHeight(220)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none; background: #111; width: 8px; border-radius: 4px;
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
        ly_scroll.addWidget(self._crear_label_vacio("Sin elementos disponibles"))
        ly_scroll.addStretch()
        scroll.setWidget(contenedor_scroll)
        ly_frame.addWidget(scroll)

        self.estado_listas[clave]["layout"] = ly_scroll
        ly_frame.addWidget(self._crear_controles_paginacion(clave))
        return frame

    def _crear_label_vacio(self, texto):
        label = QLabel(texto)
        label.setStyleSheet("color: #999; font-size: 13px; border: none; background: transparent; padding: 12px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _normalizar_item_visual(self, item):
        if isinstance(item, dict):
            return str(item.get("texto", "")), item.get("imagen")
        return str(item), None

    def _crear_item(self, texto):
        texto, ruta_imagen = self._normalizar_item_visual(texto)
        item_w = QWidget()
        item_w.setFixedHeight(45)
        item_ly = QHBoxLayout(item_w)
        item_ly.setContentsMargins(6, 4, 6, 4)
        item_ly.setSpacing(8)

        img = QLabel()
        img.setFixedSize(24, 24)
        img.setStyleSheet("background: #333; border: 1px solid #444; border-radius: 12px;")
        if ruta_imagen and os.path.exists(ruta_imagen):
            pixmap = QPixmap(ruta_imagen)
            img.setPixmap(
                pixmap.scaled(
                    img.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        txt = QLabel(texto)
        txt.setStyleSheet("color: #ddd; font-size: 13px; border: none; background: transparent;")
        txt.setWordWrap(True)

        item_ly.addWidget(img)
        item_ly.addWidget(txt, 1)
        item_w.setStyleSheet("QWidget:hover { background: #222; border-radius: 4px; }")
        return item_w

    def _crear_controles_paginacion(self, clave):
        widget_pag = QWidget()
        ly = QHBoxLayout(widget_pag)
        ly.setContentsMargins(0, 5, 0, 5)
        ly.setAlignment(Qt.AlignmentFlag.AlignCenter)

        estilo_flecha = "color: white; font-size: 18px; font-weight: bold; border: none; background: transparent;"

        btn_prev = QPushButton("<")
        btn_prev.setStyleSheet(estilo_flecha)
        btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_prev.clicked.connect(lambda: self._cambiar_pagina(clave, -1))

        lbl_pag = QLabel("1/1")
        lbl_pag.setStyleSheet("color: white; font-weight: bold; font-size: 14px; padding: 0 10px; background: transparent;")

        btn_next = QPushButton(">")
        btn_next.setStyleSheet(estilo_flecha)
        btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_next.clicked.connect(lambda: self._cambiar_pagina(clave, 1))

        self.estado_listas[clave]["lbl_pag"] = lbl_pag
        self.estado_listas[clave]["btn_prev"] = btn_prev
        self.estado_listas[clave]["btn_next"] = btn_next

        ly.addWidget(btn_prev)
        ly.addWidget(lbl_pag)
        ly.addWidget(btn_next)
        return widget_pag

    def _poblar_lista(self, clave, elementos):
        estado = self.estado_listas[clave]
        nueva_lista = ListaSimple()
        for elemento in elementos or []:
            nueva_lista.agregar(elemento)
        estado["lista"] = nueva_lista
        estado["pagina"] = 0
        self._renderizar_lista(clave)

    def _cambiar_pagina(self, clave, delta):
        estado = self.estado_listas[clave]
        lista = estado["lista"]
        if lista.tamanio == 0:
            return
        paginas_totales = max(1, math.ceil(lista.tamanio / self.tamanio_pagina))
        nueva = estado["pagina"] + delta
        if 0 <= nueva < paginas_totales:
            estado["pagina"] = nueva
            self._renderizar_lista(clave)

    def _actualizar_controles(self, clave):
        estado = self.estado_listas[clave]
        lista = estado["lista"]
        pagina = estado["pagina"]
        paginas_totales = max(1, math.ceil(lista.tamanio / self.tamanio_pagina))
        if estado["lbl_pag"] is not None:
            estado["lbl_pag"].setText(f"{pagina + 1}/{paginas_totales}")
        if estado["btn_prev"] is not None:
            estado["btn_prev"].setEnabled(pagina > 0)
        if estado["btn_next"] is not None:
            estado["btn_next"].setEnabled(pagina < paginas_totales - 1)

    def _limpiar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self._limpiar_layout(child_layout)

    def _renderizar_lista(self, clave):
        estado = self.estado_listas[clave]
        layout = estado["layout"]
        if layout is None:
            return

        self._limpiar_layout(layout)

        lista = estado["lista"]
        pagina = estado["pagina"]
        items = lista.obtener_pagina(pagina, self.tamanio_pagina)

        placeholders = {
            "autores": "Sin autores disponibles",
            "personajes": "Sin personajes asociados",
        }
        if not items:
            layout.addWidget(self._crear_label_vacio(placeholders[clave]))
        else:
            for item in items:
                layout.addWidget(self._crear_item(item))
        layout.addStretch()
        self._actualizar_controles(clave)

    def actualizar_datos(self, comic):
        self.lbl_titulo.setText(comic.titulo or "Sin titulo")
        fecha = comic.fecha_lanzamiento or ""
        self.lbl_fecha.setText(f"Fecha: {fecha}" if fecha else "")
        isbn = comic.isbn or ""
        self.lbl_isbn.setText(f"ISBN: {isbn}" if isbn else "")

        desc = comic.descripcion or "Este comic no tiene descripcion disponible."
        import re
        desc = re.sub(r"<[^>]+>", "", desc)
        self.lbl_descripcion.setText(desc[:500] + ("..." if len(desc) > 500 else ""))

        url_remota, ruta_local = comic.imagen if comic.imagen else (None, None)
        if ruta_local and os.path.exists(ruta_local):
            pixmap = QPixmap(ruta_local)
            self.foto_portada.setPixmap(
                pixmap.scaled(
                    self.foto_portada.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.foto_portada.setText("")
        else:
            self.foto_portada.setPixmap(QPixmap())
            self.foto_portada.setText("No Image")

        self._poblar_lista("autores", getattr(comic, "detalles_creadores", None) or getattr(comic, "nombres_creadores", []))
        self._poblar_lista("personajes", getattr(comic, "detalles_personajes", None) or getattr(comic, "nombres_personajes", []))

    def volver(self):
        v = self.window()
        if hasattr(v, "stack"):
            v.stack.setCurrentIndex(1)
            if hasattr(v, "actualizar_estilo_boton"):
                v.actualizar_estilo_boton(v.btn_home, False)
                v.actualizar_estilo_boton(v.btn_comics, True)
                v.actualizar_estilo_boton(v.btn_personajes, False)
