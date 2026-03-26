import math
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from Estructuras_Listas.Lista_simple import ListaSimple

MAX_AUTOR_IMAGENES_ASYNC = 10


class AutorImagenWorker(QObject):
    finalizado = pyqtSignal(int, object)

    def __init__(self, token, gestor, api, creadores_ids, creadores_nombres):
        super().__init__()
        self.token = token
        self.gestor = gestor
        self.api = api
        self.creadores_ids = list(creadores_ids or [])
        self.creadores_nombres = list(creadores_nombres or [])

    def ejecutar(self):
        detalles = []
        for idx, nombre in enumerate(self.creadores_nombres):
            ruta_imagen = None
            if idx < MAX_AUTOR_IMAGENES_ASYNC and idx < len(self.creadores_ids):
                try:
                    creador = self.gestor.buscador("creador", self.api, self.creadores_ids[idx])
                except Exception:
                    creador = None
                if creador:
                    imagen = getattr(creador, "imagen", None)
                    if isinstance(imagen, tuple) and len(imagen) > 1:
                        ruta_imagen = imagen[1]
            detalles.append({"texto": nombre, "imagen": ruta_imagen})
        self.finalizado.emit(self.token, detalles)


class DetallesPersonaje(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212; border: none;")
        self._autor_worker_thread = None
        self._autor_worker = None
        self._token_autores = 0

        self.tamanio_pagina_detalles = 10
        self.estado_listas = {
            "autores": {"lista": ListaSimple(), "pagina": 0, "layout": None, "lbl_pag": None, "btn_prev": None, "btn_next": None},
            "comics": {"lista": ListaSimple(), "pagina": 0, "layout": None, "lbl_pag": None, "btn_prev": None, "btn_next": None},
            "eventos": {"lista": ListaSimple(), "pagina": 0, "layout": None, "lbl_pag": None, "btn_prev": None, "btn_next": None},
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

        self.foto_perfil = QLabel()
        self.foto_perfil.setFixedSize(320, 320)
        self.foto_perfil.setStyleSheet("""
            border: 3px solid #e62429;
            border-radius: 12px;
            background-color: #1a1a1a;
            color: #666666;
        """)
        self.foto_perfil.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.foto_perfil.setText("No Image")
        fila_superior.addWidget(self.foto_perfil)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(15)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.lbl_nombre = QLabel("NOMBRE DEL PERSONAJE")
        self.lbl_nombre.setStyleSheet("font-size: 38px; font-weight: bold; color: #ffffff; background: transparent;")
        info_layout.addWidget(self.lbl_nombre)

        layout_superior_detalles = QHBoxLayout()
        layout_superior_detalles.setSpacing(30)
        layout_superior_detalles.setAlignment(Qt.AlignmentFlag.AlignTop)

        desc_container = QVBoxLayout()
        lbl_t_desc = QLabel("Descripcion")
        lbl_t_desc.setStyleSheet("color: #e62429; font-size: 18px; font-weight: bold; background: transparent;")

        self.lbl_descripcion = QLabel("Selecciona un personaje...")
        self.lbl_descripcion.setWordWrap(True)
        self.lbl_descripcion.setStyleSheet("color: #cccccc; font-size: 14px; line-height: 150%; background: transparent;")

        desc_container.addWidget(lbl_t_desc)
        desc_container.addWidget(self.lbl_descripcion)
        desc_container.addStretch()
        layout_superior_detalles.addLayout(desc_container, 1)

        self.lista_autores_widget = self.crear_cuadro_creadores("Autores", "autores")
        self.lista_autores_widget.setFixedWidth(280)
        layout_superior_detalles.addWidget(self.lista_autores_widget)

        info_layout.addLayout(layout_superior_detalles)
        fila_superior.addLayout(info_layout, 1)
        layout_principal.addLayout(fila_superior)

        tablas_layout = QHBoxLayout()
        tablas_layout.setSpacing(30)
        tablas_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.lista_comics = self.crear_lista_marvel("Comics", "comics")
        tablas_layout.addWidget(self.lista_comics)

        self.lista_eventos = self.crear_lista_marvel("Eventos", "eventos")
        tablas_layout.addWidget(self.lista_eventos)

        layout_principal.addLayout(tablas_layout)

    def crear_cuadro_creadores(self, titulo, clave):
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
        ly_autores = QVBoxLayout(contenedor_scroll)
        ly_autores.setSpacing(10)
        ly_autores.setContentsMargins(10, 10, 10, 10)
        ly_autores.addWidget(self.crear_label_vacio("Sin autores disponibles"))
        ly_autores.addStretch()
        scroll.setWidget(contenedor_scroll)
        ly_frame.addWidget(scroll)
        self.estado_listas[clave]["layout"] = ly_autores

        ly_frame.addWidget(self.crear_controles_paginacion(clave, oscuro=True))

        return frame

    def _normalizar_item_visual(self, item):
        if isinstance(item, dict):
            return str(item.get("texto", "")), item.get("imagen")
        return str(item), None

    def crear_item_autor(self, nombre):
        nombre, ruta_imagen = self._normalizar_item_visual(nombre)
        item_w = QWidget()
        item_w.setFixedHeight(50)
        ly = QHBoxLayout(item_w)
        ly.setContentsMargins(6, 4, 6, 4)
        ly.setSpacing(8)
        img = QLabel()
        img.setFixedSize(28, 28)
        img.setStyleSheet("background: #333; border: 1px solid #444; border-radius: 14px;")
        if ruta_imagen and os.path.exists(ruta_imagen):
            pixmap = QPixmap(ruta_imagen)
            img.setPixmap(
                pixmap.scaled(
                    img.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        lbl = QLabel(nombre)
        lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #eee; border: none; background: transparent;")
        lbl.setWordWrap(True)

        ly.addWidget(img)
        ly.addWidget(lbl)
        ly.addStretch()
        item_w.setStyleSheet("QWidget:hover { background: #222; border-radius: 4px; }")
        return item_w

    def crear_controles_paginacion(self, clave, oscuro=True):
        widget_pag = QWidget()
        ly = QHBoxLayout(widget_pag)
        ly.setContentsMargins(0, 5, 0, 5)
        ly.setAlignment(Qt.AlignmentFlag.AlignCenter)

        color = "white" if oscuro else "black"
        estilo_flecha = f"color: {color}; font-size: 18px; font-weight: bold; border: none; background: transparent;"

        btn_prev = QPushButton("<")
        btn_prev.setStyleSheet(estilo_flecha)
        btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_prev.clicked.connect(lambda: self.cambiar_pagina(clave, -1))

        lbl_pag = QLabel("1/1")
        lbl_pag.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 16px; padding: 0 10px; background: transparent;")

        btn_next = QPushButton(">")
        btn_next.setStyleSheet(estilo_flecha)
        btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_next.clicked.connect(lambda: self.cambiar_pagina(clave, 1))

        self.estado_listas[clave]["lbl_pag"] = lbl_pag
        self.estado_listas[clave]["btn_prev"] = btn_prev
        self.estado_listas[clave]["btn_next"] = btn_next

        ly.addWidget(btn_prev)
        ly.addWidget(lbl_pag)
        ly.addWidget(btn_next)
        return widget_pag

    def crear_lista_marvel(self, titulo, clave):
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
        ly_scroll.addWidget(self.crear_label_vacio("Sin elementos disponibles"))
        ly_scroll.addStretch()
        scroll.setWidget(contenedor_scroll)
        ly_frame.addWidget(scroll)

        self.estado_listas[clave]["layout"] = ly_scroll

        ly_frame.addWidget(self.crear_controles_paginacion(clave, oscuro=True))
        return frame

    def crear_label_vacio(self, texto):
        label = QLabel(texto)
        label.setStyleSheet("color: #999; font-size: 13px; border: none; background: transparent; padding: 12px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def crear_item_lista(self, texto):
        texto, ruta_imagen = self._normalizar_item_visual(texto)
        item_w = QWidget()
        item_w.setFixedHeight(55)
        item_ly = QHBoxLayout(item_w)
        item_ly.setContentsMargins(6, 4, 6, 4)
        item_ly.setSpacing(8)

        img_m = QLabel()
        img_m.setFixedSize(28, 28)
        img_m.setStyleSheet("background: #333; border-radius: 4px;")
        if ruta_imagen and os.path.exists(ruta_imagen):
            pixmap = QPixmap(ruta_imagen)
            img_m.setPixmap(
                pixmap.scaled(
                    img_m.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        txt = QLabel(texto)
        txt.setStyleSheet("color: #ddd; font-size: 13px; border: none; background: transparent;")
        txt.setWordWrap(True)

        flecha = QLabel(">")
        flecha.setStyleSheet("color: #444; font-weight: bold; border: none; background: transparent;")

        item_ly.addWidget(img_m)
        item_ly.addWidget(txt, 1)
        item_ly.addWidget(flecha)
        item_w.setStyleSheet("QWidget:hover { background: #222; border-radius: 4px; }")
        return item_w

    def limpiar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self.limpiar_layout(child_layout)

    def poblar_lista_simple(self, clave, elementos):
        estado = self.estado_listas[clave]
        nueva_lista = ListaSimple()
        for elemento in elementos or []:
            nueva_lista.agregar(elemento)
        estado["lista"] = nueva_lista
        estado["pagina"] = 0
        self.renderizar_lista(clave)

    def cambiar_pagina(self, clave, delta):
        estado = self.estado_listas[clave]
        lista = estado["lista"]
        if lista.tamanio == 0:
            return
        paginas_totales = max(1, math.ceil(lista.tamanio / self.tamanio_pagina_detalles))
        nueva = estado["pagina"] + delta
        if 0 <= nueva < paginas_totales:
            estado["pagina"] = nueva
            self.renderizar_lista(clave)

    def actualizar_controles_paginacion(self, clave):
        estado = self.estado_listas[clave]
        lista = estado["lista"]
        pagina = estado["pagina"]
        paginas_totales = max(1, math.ceil(lista.tamanio / self.tamanio_pagina_detalles))
        if estado["lbl_pag"] is not None:
            estado["lbl_pag"].setText(f"{pagina + 1}/{paginas_totales}")
        if estado["btn_prev"] is not None:
            estado["btn_prev"].setEnabled(pagina > 0)
        if estado["btn_next"] is not None:
            estado["btn_next"].setEnabled(pagina < paginas_totales - 1)

    def renderizar_lista(self, clave):
        estado = self.estado_listas[clave]
        layout = estado["layout"]
        if layout is None:
            return

        self.limpiar_layout(layout)

        lista = estado["lista"]
        pagina = estado["pagina"]
        items = lista.obtener_pagina(pagina, self.tamanio_pagina_detalles)
        if not items:
            placeholder = {
                "autores": "Sin autores disponibles",
                "comics": "Sin comics asociados",
                "eventos": "Sin eventos asociados",
            }[clave]
            layout.addWidget(self.crear_label_vacio(placeholder))
        else:
            for item in items:
                if clave == "autores":
                    layout.addWidget(self.crear_item_autor(item))
                else:
                    layout.addWidget(self.crear_item_lista(item))
        layout.addStretch()
        self.actualizar_controles_paginacion(clave)

    def _cancelar_worker_autores(self):
        self._token_autores += 1
        if self._autor_worker_thread is not None:
            self._autor_worker_thread.quit()
            self._autor_worker_thread.wait(100)
        self._autor_worker_thread = None
        self._autor_worker = None

    def _iniciar_worker_autores(self, personaje, gestor, api):
        if not gestor or not api or not getattr(personaje, "creadores_ids", None) or not getattr(personaje, "creadores", None):
            return

        self._cancelar_worker_autores()
        token = self._token_autores
        thread = QThread(self)
        worker = AutorImagenWorker(token, gestor, api, personaje.creadores_ids, personaje.creadores)
        worker.moveToThread(thread)
        worker.finalizado.connect(self._aplicar_autores_async)
        thread.started.connect(worker.ejecutar)
        worker.finalizado.connect(thread.quit)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        self._autor_worker_thread = thread
        self._autor_worker = worker
        thread.start()

    def _aplicar_autores_async(self, token, detalles):
        if token != self._token_autores:
            return
        self.estado_listas["autores"]["pagina"] = 0
        self.poblar_lista_simple("autores", detalles)

    def actualizar_datos(self, personaje, gestor=None, api=None):
        self.lbl_nombre.setText(personaje.nombre)
        self.lbl_descripcion.setText(personaje.descripcion or "Este personaje no tiene descripcion disponible.")

        url_remota, ruta_local = personaje.imagen if personaje.imagen else (None, None)
        if ruta_local and os.path.exists(ruta_local):
            pixmap = QPixmap(ruta_local)
            self.foto_perfil.setPixmap(
                pixmap.scaled(
                    self.foto_perfil.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.foto_perfil.setText("")
        else:
            self.foto_perfil.setPixmap(QPixmap())
            self.foto_perfil.setText("No Image")

        self._cancelar_worker_autores()
        self.poblar_lista_simple("autores", getattr(personaje, "detalles_creadores", None) or personaje.creadores)
        self.poblar_lista_simple("comics", getattr(personaje, "detalles_comics", None) or personaje.comics)
        self.poblar_lista_simple("eventos", getattr(personaje, "detalles_eventos", None) or personaje.eventos)
        self._iniciar_worker_autores(personaje, gestor, api)

    def volver(self):
        v = self.window()
        if hasattr(v, "stack"):
            v.stack.setCurrentIndex(2)

    def closeEvent(self, event):
        self._cancelar_worker_autores()
        super().closeEvent(event)
