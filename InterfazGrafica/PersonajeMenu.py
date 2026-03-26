import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,QPushButton, QScrollArea, QFrame, QLineEdit,QComboBox, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QPixmap
from Controladores.init import gestor, PageOrderer
from Controladores.api_comicvine import ComicVineAPI

class PersonajesMenu(QWidget):
    def __init__(self, perfil, controlador=None):
        super().__init__()
        self.perfil = perfil
        self.controlador = controlador
        self.pagina_actual = 0
        self.gestor = gestor
        self.lista_personajes = None
        self.thread = None
        self.trabajador = None
        self.api = ComicVineAPI(self.perfil.clave) if getattr(self.perfil, "clave", None) else None
        self.modo_carga = "ucm"

        # Contenedor principal
        self.setStyleSheet("background-color: #121212; border: none;")
        layout_exterior = QVBoxLayout(self)
        layout_exterior.setContentsMargins(0, 0, 0, 0)

        self.lienzo = QFrame()
        self.lienzo.setStyleSheet("background-color: #121212;")
        layout_principal = QVBoxLayout(self.lienzo)
        layout_principal.setContentsMargins(25, 20, 25, 10)

        # cabecera
        contenedor_cabecera = QVBoxLayout()
        contenedor_cabecera.setSpacing(15)

        fila_titulo = QHBoxLayout()
        titulo = QLabel("Buscador de Personajes")
        titulo.setStyleSheet("color: #ffffff; font-size: 28px; font-weight: bold;")
        fila_titulo.addStretch()
        fila_titulo.addWidget(titulo)
        fila_titulo.addStretch()
        contenedor_cabecera.addLayout(fila_titulo)

        self.lbl_estado = QLabel("Cargando personajes...")
        self.lbl_estado.setStyleSheet("color: #aaaaaa; font-size: 13px;")
        self.lbl_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contenedor_cabecera.addWidget(self.lbl_estado)

        fila_busqueda = QHBoxLayout()
        self.buscador_oval = QLineEdit()
        self.buscador_oval.setPlaceholderText(" Buscar por nombre o creador...")
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

        #busqueda/orden
        fila_filtros = QHBoxLayout()
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
        # Ordenameinto
        self.cb_orden = QComboBox()
        self.cb_orden.addItems(["Ordenar por nombre"])
        self.cb_orden.setStyleSheet(estilo_cb)

        self.cb_lanz = QComboBox()
        self.cb_lanz.addItems(["Relevantes UCM", "Catalogo general"])
        self.cb_lanz.setStyleSheet(estilo_cb)

        fila_filtros.addWidget(self.cb_orden)
        fila_filtros.addStretch()
        fila_filtros.addWidget(self.cb_lanz)
        layout_principal.addLayout(fila_filtros)

        self.cb_orden.clear()  # Limpiamos lo anterior
        self.cb_orden.addItems(["Nombre (A-Z)", "Nombre (Z-A)","Creador"])
        self.cb_orden.currentIndexChanged.connect(self.manejar_ordenamiento)
        self.cb_lanz.currentIndexChanged.connect(self.manejar_modo_carga)

        # area de caudros
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

        #Esto es solo para probar, aun no se debe conectar la api x,d
        # Generación de 10 personajes
        self.scroll.setWidget(self.contenedor_grid)
        layout_principal.addWidget(self.scroll)

        #paginacion
        #Son estaticos por ahora, cuando se integre la lista doble con la api ya no lo sera :D
        footer = QHBoxLayout()
        self.btn_ant = QPushButton("<")
        self.btn_sig = QPushButton(">")

        # Estilos
        self.btn_ant.setStyleSheet(
            "background: #252525; color: #aaaaaa; padding: 8px 16px; border-radius: 5px; "
            "font-weight: bold; border: 1px solid #333333; font-size: 13px;")
        self.btn_sig.setStyleSheet(
            "background: #e62429; color: white; padding: 8px 16px; border-radius: 5px; "
            "font-weight: bold; border: none; font-size: 13px;")

        self.lbl_pag = QLabel(f"{self.pagina_actual}")
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
        texto = self.buscador_oval.text().strip().lower()

        if not texto:
            self.mostrar_pagina()
            return

        resultados = []

        if self.lista_personajes:
            personajes = self.lista_personajes.obtener_pagina(0, self.lista_personajes.tamanio)

            for p in personajes:
                # 🔥 ASEGURAR CREADORES (igual que en detalles)
                if not p.creadores and getattr(p, "creadores_ids", []):
                    nombres = []
                    for cid in p.creadores_ids[:3]:  # limitamos para rendimiento
                        creador_obj = self.gestor.buscador("creador", self.api, cid)
                        if creador_obj and getattr(creador_obj, "nombre_completo", None):
                            nombres.append(creador_obj.nombre_completo)
                    if nombres:
                        p.creadores = nombres

                nombre_match = texto in p.nombre.lower()

                creador_match = any(
                    texto in c.lower() for c in (p.creadores or [])
                )

                if nombre_match or creador_match:
                    resultados.append(p)

        self.mostrar_resultados_filtrados(resultados)


    def mostrar_resultados_filtrados(self, lista_resultados):
        for i in reversed(range(self.layout_grid.count())):
            widget = self.layout_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        for i, personaje in enumerate(lista_resultados[:15]):
            fila = i // 5
            columna = i % 5
            tarjeta = self.crear_tarjeta_personaje(personaje)
            self.layout_grid.addWidget(tarjeta, fila, columna)

    def manejar_ordenamiento(self):
        if not self.lista_personajes or self.lista_personajes.esta_vacia():
            return

        texto = self.cb_orden.currentText()

        personajes = self.lista_personajes.obtener_pagina(0, self.lista_personajes.tamanio)

        if texto == "Nombre (A-Z)":
            personajes.sort(key=lambda p: p.nombre.lower())

        elif texto == "Nombre (Z-A)":
            personajes.sort(key=lambda p: p.nombre.lower(), reverse=True)

        elif texto == "Creador":
            personajes.sort(
                key=lambda p: (p.creadores[0].lower() if p.creadores else "zzz")
            )

        # 🔥 guardamos lista ordenada temporal
        self._lista_filtrada = personajes
        self.pagina_actual = 0
        self.mostrar_pagina()

    def ordenar_por_creador(self):
        if not self.lista_personajes:
            return

        try:
            personajes = self.lista_personajes.obtener_pagina(0, self.lista_personajes.tamanio)

            personajes.sort(
                key=lambda p: (p.creadores[0].lower() if p.creadores else "zzz")
            )

            # 🔥 guardamos temporalmente
            self._lista_ordenada_temp = personajes

        except Exception as e:
            print("Error ordenando:", e)


    def carga_datos(self):
        if not self.api:
            self.mostrar_error_carga("No hay una clave de API configurada para cargar personajes.")
            return

        if self._thread_activo():
            return

        self.thread = QThread()
        self.trabajador = PageOrderer(self.gestor, self.api, self.modo_carga)
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

    def manejar_modo_carga(self):
        nuevo_modo = "ucm" if self.cb_lanz.currentIndex() == 0 else "general"
        if nuevo_modo == self.modo_carga:
            return
        self.modo_carga = nuevo_modo
        self.pagina_actual = 0
        self.lbl_estado.setText("Cargando personajes...")
        self.lista_personajes = None
        self.carga_datos()


    def recibir_lista(self, lista):
        self.lista_personajes = lista
        # CORRECCION: limpiar el estado de error/carga cuando ya hay datos disponibles.
        self.lbl_estado.setText("")
        self.mostrar_pagina()

    def mostrar_error_carga(self, mensaje):
        # CORRECCION: dejar el error visible dentro de la pantalla y tambien en una ventana emergente.
        self.lbl_estado.setText("Error al cargar personajes. Revisa el detalle mostrado.")
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
        if not self.lista_personajes:
            return

        for i in reversed(range(self.layout_grid.count())):
            self.layout_grid.itemAt(i).widget().setParent(None)

        if hasattr(self, "_lista_filtrada"):
            inicio = self.pagina_actual * 10
            fin = inicio + 10
            personajes_pagina = self._lista_filtrada[inicio:fin]
        else:
            personajes_pagina = self.lista_personajes.obtener_pagina(self.pagina_actual, 10)
        for i, personaje in enumerate(personajes_pagina):
            fila = i // 5
            columna = i % 5
            tarjeta = self.crear_tarjeta_personaje(personaje)
            self.layout_grid.addWidget(tarjeta, fila, columna)
        self.lbl_pag.setText(f"{self.pagina_actual + 1}")


    def pagina_siguiente(self):
        if self.lista_personajes and (self.pagina_actual + 1) * 10 < self.lista_personajes.tamanio:
            self.pagina_actual += 1
            self.mostrar_pagina()


    def pagina_anterior(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.mostrar_pagina()


    def crear_tarjeta_personaje(self, nombre):
        tarjeta = QFrame()
        tarjeta.setFixedSize(180, 260)
        tarjeta.setStyleSheet("""
            QFrame { 
                background-color: #1a1a1a; 
                border-radius: 10px;
            }
            QFrame:hover { border: 2px solid #e62429; }
        """)

        ly = QVBoxLayout(tarjeta)
        ly.setContentsMargins(10, 10, 10, 10)

        url_remota, ruta_local = nombre.imagen

        img_label = QLabel()
        img_label.setFixedSize(160, 160)
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_label.setStyleSheet("background-color: #222; border-radius: 8px;")

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

        # Nombre
        lbl_n = QLabel(nombre.nombre)
        lbl_n.setStyleSheet("color: white; font-weight: bold; font-size: 14px; border: none; background: transparent;")
        lbl_n.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botón Detalles
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
        ly.addWidget(lbl_n)
        ly.addStretch()
        ly.addWidget(btn)

        btn.clicked.connect(lambda: self.enviar_a_detalles(nombre))
        return tarjeta

    def enviar_a_detalles(self, nombre):
        """Navega a la vista de detalles del personaje """
        ventana = self.window()
        if hasattr(ventana, 'stack') and hasattr(ventana, 'vista_detalles_per'):
            personaje_detallado = self._cargar_detalles_personaje(nombre)
            ventana.vista_detalles_per.actualizar_datos(personaje_detallado)
            ventana.stack.setCurrentIndex(3) #detalles indice 3

            # Limpia estilos de botones laterales
            if hasattr(ventana, 'actualizar_estilo_boton'):
                ventana.actualizar_estilo_boton(ventana.btn_home, False)
                ventana.actualizar_estilo_boton(ventana.btn_comics, False)
                ventana.actualizar_estilo_boton(ventana.btn_personajes, False)

    def _cargar_detalles_personaje(self, personaje_base):
        """
        Carga detalle real del personaje y fuerza cacheo de comics/creadores/eventos asociados.
        """
        personaje = personaje_base
        if not self.api:
            return personaje

        # 1) Traer ficha detallada del personaje por id.
        try:
            detalle_raw = self.api.obtener_personajes(personaje_base.id)
            if detalle_raw and isinstance(detalle_raw, list):
                convertido = self.gestor.converter.convertir_a_personaje(detalle_raw[0])
                if convertido is not None:
                    personaje = convertido
                    self.gestor.personajes[personaje.id] = personaje
                    # Actualizar cache raw para que los datos enriquecidos persistan
                    self.gestor.raw_data.d_personajes.datos[personaje.id] = detalle_raw[0]
                    self.gestor.raw_data.d_personajes.datos[str(personaje.id)] = detalle_raw[0]
                    self.gestor.raw_data.d_personajes.guardar()
        except Exception:
            # Si falla el detalle remoto, seguimos con la info base en vez de cortar la hidratacion.
            pass

        # 1b) Resolver IDs directamente si tenemos IDs pero no nombres
        if not personaje.creadores and getattr(personaje, "creadores_ids", []):
            nombres = []
            for cid in personaje.creadores_ids[:5]:
                creador_obj = self.gestor.buscador("creador", self.api, cid)
                if creador_obj and getattr(creador_obj, "nombre_completo", None):
                    nombres.append(creador_obj.nombre_completo)
            if nombres:
                personaje.creadores = nombres

        if not personaje.eventos and getattr(personaje, "eventos_ids", []):
            nombres = []
            for eid in personaje.eventos_ids[:5]:
                evento_obj = self.gestor.buscador("evento", self.api, eid)
                if evento_obj and getattr(evento_obj, "titulo", None):
                    nombres.append(evento_obj.titulo)
            if nombres:
                personaje.eventos = nombres

        # 2) Solo si faltan datos visibles, hidratar relaciones y con limite para evitar esperas largas.
        if personaje.comics and personaje.creadores and personaje.eventos:
            return personaje

        max_relaciones = 3
        nombres_comics = list(personaje.comics or [])
        nombres_creadores = list(personaje.creadores or [])
        nombres_eventos = list(personaje.eventos or [])
        ids_creadores = list(getattr(personaje, "creadores_ids", []) or [])
        ids_eventos = list(getattr(personaje, "eventos_ids", []) or [])

        for comic_id in getattr(personaje, "comics_ids", [])[:max_relaciones]:
            comic_obj = self.gestor.buscador("comic", self.api, comic_id)
            if comic_obj and getattr(comic_obj, "titulo", None):
                nombres_comics.append(comic_obj.titulo)
                # Extraer nombres directamente del comic (evita lookups adicionales)
                nombres_creadores.extend(getattr(comic_obj, "nombres_creadores", []) or [])
                # Mantener IDs para lookups adicionales si necesario
                ids_creadores.extend(getattr(comic_obj, "creadores", []) or [])
                ids_eventos.extend(getattr(comic_obj, "eventos", []) or [])

        ids_creadores = list(dict.fromkeys([x for x in ids_creadores if x]))
        for creador_id in ids_creadores[:max_relaciones]:
            creador_obj = self.gestor.buscador("creador", self.api, creador_id)
            if creador_obj and getattr(creador_obj, "nombre_completo", None):
                nombres_creadores.append(creador_obj.nombre_completo)

        ids_eventos = list(dict.fromkeys([x for x in ids_eventos if x]))
        for evento_id in ids_eventos[:max_relaciones]:
            evento_obj = self.gestor.buscador("evento", self.api, evento_id)
            if evento_obj and getattr(evento_obj, "titulo", None):
                nombres_eventos.append(evento_obj.titulo)

        # Deduplicar conservando orden para mostrar limpio.
        personaje.comics = list(dict.fromkeys([x for x in nombres_comics if x]))
        personaje.creadores = list(dict.fromkeys([x for x in nombres_creadores if x]))
        personaje.eventos = list(dict.fromkeys([x for x in nombres_eventos if x]))
        return personaje
