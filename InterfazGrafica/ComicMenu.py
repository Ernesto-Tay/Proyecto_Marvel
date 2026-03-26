import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QScrollArea, QFrame, QLineEdit, QComboBox, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QPixmap

from Controladores.init import gestor, ComicOrderer
from Controladores.api_comicvine import ComicVineAPI


class ComicsMenu(QWidget):
    def __init__(self, perfil, controlador=None):
        super().__init__()
        self.perfil = perfil
        self.controlador = controlador
        self.pagina_actual = 0
        self.gestor = gestor
        self.lista_comics = None
        self.thread = None
        self.trabajador = None
        self.api = ComicVineAPI(self.perfil.clave) if getattr(self.perfil, "clave", None) else None

        self.setStyleSheet("background-color: #121212; border: none;")
        layout_exterior = QVBoxLayout(self)
        layout_exterior.setContentsMargins(0, 0, 0, 0)

        self.lienzo = QFrame()
        self.lienzo.setStyleSheet("background-color: #121212;")
        layout_principal = QVBoxLayout(self.lienzo)
        layout_principal.setContentsMargins(25, 20, 25, 10)

        # Cabecera
        contenedor_cabecera = QVBoxLayout()
        contenedor_cabecera.setSpacing(15)

        fila_titulo = QHBoxLayout()
        titulo = QLabel("Buscador de Cómics")
        titulo.setStyleSheet("color: #ffffff; font-size: 28px; font-weight: bold;")
        fila_titulo.addStretch()
        fila_titulo.addWidget(titulo)
        fila_titulo.addStretch()
        contenedor_cabecera.addLayout(fila_titulo)

        self.lbl_estado = QLabel("Cargando cómics...")
        self.lbl_estado.setStyleSheet("color: #aaaaaa; font-size: 13px;")
        self.lbl_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contenedor_cabecera.addWidget(self.lbl_estado)

        fila_busqueda = QHBoxLayout()
        self.buscador_oval = QLineEdit()
        self.buscador_oval.setPlaceholderText(" Buscar por título...")
        self.buscador_oval.setFixedWidth(500)
        self.buscador_oval.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d; border: 2px solid #333333;
                border-radius: 20px; padding: 10px 15px; color: #ffffff;
                font-size: 15px;
            }
            QLineEdit:focus { border: 2px solid #e62429; }
        """)
        fila_busqueda.addStretch()
        fila_busqueda.addWidget(self.buscador_oval)
        fila_busqueda.addStretch()
        contenedor_cabecera.addLayout(fila_busqueda)
        layout_principal.addLayout(contenedor_cabecera)
        self.buscador_oval.textChanged.connect(self.manejar_busqueda)

        # Filtros y orden
        estilo_cb = """
            QComboBox {
                background: #2d2d2d; border: 1px solid #444444; border-radius: 6px;
                padding: 6px 10px; color: #ffffff; min-width: 160px; font-size: 13px;
            }
            QComboBox:hover { border: 1px solid #e62429; }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d; color: #ffffff;
                selection-background-color: #e62429; selection-color: white;
                border: 1px solid #444444;
            }
        """
        fila_filtros = QHBoxLayout()
        self.cb_orden = QComboBox()
        self.cb_orden.addItems(["Título (A-Z)", "Título (Z-A)", "Fecha (más reciente)", "Fecha (más antigua)"])
        self.cb_orden.setStyleSheet(estilo_cb)
        self.cb_orden.currentIndexChanged.connect(self.manejar_ordenamiento)

        fila_filtros.addWidget(self.cb_orden)
        fila_filtros.addStretch()
        layout_principal.addLayout(fila_filtros)

        # Área de tarjetas
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: #121212; }
            QScrollBar:vertical { background: #1a1a1a; width: 8px; border-radius: 4px; border: none; }
            QScrollBar::handle:vertical { background: #444444; min-height: 20px; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #e62429; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        self.contenedor_grid = QWidget()
        self.contenedor_grid.setStyleSheet("background-color: #121212;")
        self.layout_grid = QGridLayout(self.contenedor_grid)
        self.layout_grid.setSpacing(20)
        self.layout_grid.setContentsMargins(10, 10, 10, 10)

        self.scroll.setWidget(self.contenedor_grid)
        layout_principal.addWidget(self.scroll)

        # Paginación
        footer = QHBoxLayout()
        self.btn_ant = QPushButton("<")
        self.btn_sig = QPushButton(">")

        self.btn_ant.setStyleSheet(
            "background: #252525; color: #aaaaaa; padding: 8px 16px; border-radius: 5px; "
            "font-weight: bold; border: 1px solid #333333; font-size: 13px;")
        self.btn_sig.setStyleSheet(
            "background: #e62429; color: white; padding: 8px 16px; border-radius: 5px; "
            "font-weight: bold; border: none; font-size: 13px;")

        self.lbl_pag = QLabel("1")
        self.lbl_pag.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        self.btn_sig.clicked.connect(self.pagina_siguiente)
        self.btn_ant.clicked.connect(self.pagina_anterior)
        footer.addStretch()
        footer.addWidget(self.btn_ant)
        footer.addSpacing(15)
        footer.addWidget(self.lbl_pag)
        footer.addSpacing(15)
        footer.addWidget(self.btn_sig)
        footer.addStretch()
        layout_principal.addLayout(footer)
        layout_exterior.addWidget(self.lienzo)
        self.carga_datos()

    def manejar_busqueda(self):
        texto = self.buscador_oval.text().strip()
        if not texto:
            self.mostrar_pagina()
            return
        if self.lista_comics:
            resultados = self.lista_comics.buscar_por_nombre(texto)
            self.mostrar_resultados_filtrados(resultados)

    def mostrar_resultados_filtrados(self, lista_resultados):
        for i in reversed(range(self.layout_grid.count())):
            widget = self.layout_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        for i, comic in enumerate(lista_resultados[:15]):
            fila = i // 5
            columna = i % 5
            tarjeta = self.crear_tarjeta_comic(comic)
            self.layout_grid.addWidget(tarjeta, fila, columna)

    def manejar_ordenamiento(self):
        if not self.lista_comics or self.lista_comics.esta_vacia():
            return
        idx = self.cb_orden.currentIndex()
        if idx == 0:
            self.lista_comics.ordenar_por_nombre(ascendente=True)
        elif idx == 1:
            self.lista_comics.ordenar_por_nombre(ascendente=False)
        elif idx == 2:
            self.lista_comics.ordenar_por_fecha(ascendente=False)
        elif idx == 3:
            self.lista_comics.ordenar_por_fecha(ascendente=True)
        self.pagina_actual = 0
        self.mostrar_pagina()

    def carga_datos(self):
        if not self.api:
            self.mostrar_error_carga("No hay una clave de API configurada para cargar cómics.")
            return
        if self._thread_activo():
            return

        self.thread = QThread()
        self.trabajador = ComicOrderer(self.gestor, self.api)
        self.trabajador.moveToThread(self.thread)
        self.trabajador.finalizado.connect(self.recibir_lista)
        self.trabajador.error.connect(self.mostrar_error_carga)
        self.trabajador.finalizado.connect(self.thread.quit)
        self.trabajador.error.connect(self.thread.quit)
        self.thread.finished.connect(self._on_thread_finished)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.trabajador.dump_list)
        self.thread.start()

    def _thread_activo(self):
        if not self.thread:
            return False
        try:
            return self.thread.isRunning()
        except RuntimeError:
            self.thread = None
            self.trabajador = None
            return False

    def _on_thread_finished(self):
        self.thread = None
        self.trabajador = None

    def recibir_lista(self, lista):
        self.lista_comics = lista
        self.lbl_estado.setText("")
        self.mostrar_pagina()

    def mostrar_error_carga(self, mensaje):
        self.lbl_estado.setText("Error al cargar cómics. Revisa el detalle mostrado.")
        self.lbl_estado.setStyleSheet("color: #e62429; font-size: 13px; font-weight: bold;")
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Error de carga")
        msg_box.setText(mensaje)
        msg_box.setStyleSheet("""
            QMessageBox { background-color: #1a1a1a; }
            QMessageBox QLabel { color: #ffffff; background-color: #1a1a1a; }
            QMessageBox QPushButton {
                color: white; background-color: #e62429;
                padding: 6px 12px; min-width: 80px; border-radius: 4px;
            }
        """)
        msg_box.exec()

    def mostrar_pagina(self):
        if not self.lista_comics:
            return
        for i in reversed(range(self.layout_grid.count())):
            widget = self.layout_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        comics_pagina = self.lista_comics.obtener_pagina(self.pagina_actual, 10)
        for i, comic in enumerate(comics_pagina):
            fila = i // 5
            columna = i % 5
            tarjeta = self.crear_tarjeta_comic(comic)
            self.layout_grid.addWidget(tarjeta, fila, columna)
        self.lbl_pag.setText(f"{self.pagina_actual + 1}")

    def pagina_siguiente(self):
        if self.lista_comics and (self.pagina_actual + 1) * 10 < self.lista_comics.tamanio:
            self.pagina_actual += 1
            self.mostrar_pagina()

    def pagina_anterior(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.mostrar_pagina()

    def crear_tarjeta_comic(self, comic):
        tarjeta = QFrame()
        tarjeta.setFixedSize(180, 280)
        tarjeta.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 10px;
            }
            QFrame:hover { border: 2px solid #e62429; }
        """)

        ly = QVBoxLayout(tarjeta)
        ly.setContentsMargins(10, 10, 10, 10)

        img_label = QLabel()
        img_label.setFixedSize(160, 170)
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_label.setStyleSheet("background-color: #222; border-radius: 8px;")

        url_remota, ruta_local = comic.imagen if comic.imagen else (None, None)
        if ruta_local and os.path.exists(ruta_local):
            pixmap = QPixmap(ruta_local)
            img_label.setPixmap(pixmap.scaled(
                img_label.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            img_label.setText("No Image")
            img_label.setStyleSheet("color: #555; background-color: #333; border-radius: 8px;")

        # Título (recortar si es muy largo)
        titulo_texto = comic.titulo or "Sin título"
        if len(titulo_texto) > 22:
            titulo_texto = titulo_texto[:20] + "..."
        lbl_titulo = QLabel(titulo_texto)
        lbl_titulo.setStyleSheet("color: white; font-weight: bold; font-size: 11px; border: none; background: transparent;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_titulo.setWordWrap(True)

        # Fecha ya en formato MM-AAAA
        fecha = comic.fecha_lanzamiento or ""
        lbl_fecha = QLabel(fecha)
        lbl_fecha.setStyleSheet("color: #aaa; font-size: 10px; border: none; background: transparent;")
        lbl_fecha.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn = QPushButton("Ver Detalles")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: #e62429; color: white; border-radius: 4px;
                font-size: 11px; font-weight: bold; padding: 5px;
            }
            QPushButton:hover { background: white; color: #e62429; }
        """)

        ly.addWidget(img_label)
        ly.addWidget(lbl_titulo)
        ly.addWidget(lbl_fecha)
        ly.addStretch()
        ly.addWidget(btn)

        btn.clicked.connect(lambda: self.enviar_a_detalles(comic))
        return tarjeta

    def enviar_a_detalles(self, comic):
        ventana = self.window()
        if hasattr(ventana, 'stack') and hasattr(ventana, 'vista_detalles_comic'):
            comic_detallado = self._cargar_detalles_comic(comic)
            ventana.vista_detalles_comic.actualizar_datos(comic_detallado)
            ventana.stack.setCurrentIndex(4)  # índice de DetallesComic

            if hasattr(ventana, 'actualizar_estilo_boton'):
                ventana.actualizar_estilo_boton(ventana.btn_home, False)
                ventana.actualizar_estilo_boton(ventana.btn_comics, False)
                ventana.actualizar_estilo_boton(ventana.btn_personajes, False)

    def _cargar_detalles_comic(self, comic_base):
        comic = comic_base
        if not self.api:
            return comic

        # Traer ficha detallada del comic por id (tiene más datos que el listado)
        try:
            detalle_raw = self.api.obtener_comics(comic_base.id)
            if detalle_raw and isinstance(detalle_raw, list):
                convertido = self.gestor.converter.convertir_a_comic(detalle_raw[0])
                if convertido is not None:
                    comic = convertido
                    self.gestor.comics[comic.id] = comic
                    self.gestor.raw_data.d_comics.datos[comic.id] = self.gestor.raw_data.d_comics._normalizar_comic(detalle_raw[0])
                    self.gestor.raw_data.d_comics.datos[str(comic.id)] = self.gestor.raw_data.d_comics.datos[comic.id]
                    self.gestor.raw_data.d_comics.guardar()
        except Exception:
            pass

        # Usar nombres ya incluidos en los créditos (vienen directo de la API sin llamadas extra)
        nombres_creadores = list(getattr(comic, "nombres_creadores", []) or [])
        nombres_personajes = list(getattr(comic, "nombres_personajes", []) or [])

        # Solo si faltan nombres, intentar resolver por ID (máximo 5 para no tardar)
        max_rel = 5
        if not nombres_creadores:
            for creador_id in (getattr(comic, "creadores", []) or [])[:max_rel]:
                try:
                    obj = self.gestor.buscador("creador", self.api, creador_id)
                    if obj and getattr(obj, "nombre_completo", None):
                        nombres_creadores.append(obj.nombre_completo)
                except Exception:
                    pass

        if not nombres_personajes:
            for personaje_id in (getattr(comic, "personajes", []) or [])[:max_rel]:
                try:
                    obj = self.gestor.buscador("personaje", self.api, personaje_id)
                    if obj and getattr(obj, "nombre", None):
                        nombres_personajes.append(obj.nombre)
                except Exception:
                    pass

        comic.nombres_creadores = list(dict.fromkeys([x for x in nombres_creadores if x]))
        comic.nombres_personajes = list(dict.fromkeys([x for x in nombres_personajes if x]))
        return comic
