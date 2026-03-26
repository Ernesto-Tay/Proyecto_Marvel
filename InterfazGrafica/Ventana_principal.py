import sys
import os
from collections import Counter
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTreeWidget, QTreeWidgetItem, QHeaderView, 
                             QPushButton, QLabel, QLineEdit, QComboBox, 
                             QTextEdit, QMessageBox, QMenuBar, QMenu, 
                             QFrame, QApplication, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QIcon
from PIL import Image, ImageQt
import os

# Asegurarse de que la ruta esté configurada
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controladores.gestor_datos import Instancias
# Importar desde el __init__ de Modelos
from Modelos import Comic, ListaDoble

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurar ventana principal
        self.setWindowTitle("Biblioteca de Cómics Marvel")
        self.setGeometry(100, 100, 1200, 700)
        self.setMinimumSize(1000, 600)
        
        # Controlador
        self.controlador = Instancias()
        
        # Variables para filtros
        self.filtro_autor = ""
        self.filtro_anio = ""
        self.busqueda = ""
        self.orden = "Nombre"
        
        # Configurar estilo CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a2e;
            }
            QWidget {
                background-color: #1a1a2e;
            }
            QLabel {
                color: white;
            }
            QLabel#titulo {
                color: #e94560;
                font-size: 20px;
                font-weight: bold;
            }
            QLabel#subtitulo {
                color: #e94560;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #0f3460;
                color: white;
                border: 1px solid #e94560;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 2px solid #e94560;
            }
            QPushButton {
                font-weight: bold;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                color: white;
            }
            QPushButton#btnAgregar {
                background-color: #e94560;
            }
            QPushButton#btnAgregar:hover {
                background-color: #ff6b8b;
            }
            QPushButton#btnEditar {
                background-color: #0f3460;
            }
            QPushButton#btnEditar:hover {
                background-color: #1a4a7a;
            }
            QPushButton#btnEliminar {
                background-color: #dc3545;
            }
            QPushButton#btnEliminar:hover {
                background-color: #ff4757;
            }
            QTreeWidget {
                background-color: #16213e;
                color: white;
                alternate-background-color: #0f3460;
                gridline-color: #e94560;
                selection-background-color: #e94560;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:hover {
                background-color: #0f3460;
            }
            QHeaderView::section {
                background-color: #e94560;
                color: white;
                padding: 5px;
                border: none;
            }
            QMenuBar {
                background-color: #16213e;
                color: white;
            }
            QMenuBar::item {
                background-color: #16213e;
                color: white;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #e94560;
            }
            QMenu {
                background-color: #16213e;
                color: white;
                border: 1px solid #e94560;
            }
            QMenu::item:selected {
                background-color: #e94560;
            }
        """)
        
        # Crear interfaz
        self.crear_barra_menu()
        self.crear_barra_herramientas()
        self.crear_panel_principal()
        
        # Cargar datos iniciales
        self.cargar_comics()
        
    def crear_barra_menu(self):
        """Crear menú superior"""
        menubar = self.menuBar()
        
        # Menú Archivo
        archivo_menu = menubar.addMenu("Archivo")
        
        agregar_action = QAction("Agregar Comic", self)
        agregar_action.triggered.connect(self.abrir_agregar_comic)
        archivo_menu.addAction(agregar_action)
        
        estadisticas_action = QAction("Estadísticas", self)
        estadisticas_action.triggered.connect(self.mostrar_estadisticas)
        archivo_menu.addAction(estadisticas_action)
        
        archivo_menu.addSeparator()
        
        salir_action = QAction("Salir", self)
        salir_action.triggered.connect(self.close)
        archivo_menu.addAction(salir_action)
        
        # Menú Ayuda
        ayuda_menu = menubar.addMenu("Ayuda")
        
        acerca_action = QAction("Acerca de", self)
        acerca_action.triggered.connect(self.mostrar_acerca_de)
        ayuda_menu.addAction(acerca_action)
        
    def crear_barra_herramientas(self):
        """Crear barra de herramientas con búsqueda y filtros"""
        toolbar = QWidget()
        toolbar.setFixedHeight(80)
        toolbar.setStyleSheet("background-color: #16213e;")
        
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        # Título
        titulo = QLabel("MARVEL COMICS")
        titulo.setObjectName("titulo")
        toolbar_layout.addWidget(titulo)
        
        # Buscador
        frame_busqueda = QWidget()
        frame_busqueda.setStyleSheet("background-color: #16213e;")
        busqueda_layout = QHBoxLayout(frame_busqueda)
        busqueda_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_buscar = QLabel("🔍 Buscar:")
        lbl_buscar.setStyleSheet("background-color: #16213e; color: white;")
        self.busqueda_entry = QLineEdit()
        self.busqueda_entry.setPlaceholderText("Buscar por título o autor...")
        self.busqueda_entry.setMinimumWidth(250)
        self.busqueda_entry.textChanged.connect(self.cargar_comics)
        
        busqueda_layout.addWidget(lbl_buscar)
        busqueda_layout.addWidget(self.busqueda_entry)
        toolbar_layout.addWidget(frame_busqueda)
        
        # Filtros
        frame_filtros = QWidget()
        frame_filtros.setStyleSheet("background-color: #16213e;")
        filtros_layout = QHBoxLayout(frame_filtros)
        filtros_layout.setContentsMargins(0, 0, 0, 0)
        
        # Filtro autor
        lbl_autor = QLabel("Autor:")
        lbl_autor.setStyleSheet("background-color: #16213e; color: white;")
        self.autor_combo = QComboBox()
        self.autor_combo.addItem("Todos")
        self.autor_combo.currentTextChanged.connect(self.cargar_comics)
        self.autor_combo.setMinimumWidth(150)
        
        # Filtro año
        lbl_anio = QLabel("Año:")
        lbl_anio.setStyleSheet("background-color: #16213e; color: white;")
        self.anio_combo = QComboBox()
        self.anio_combo.addItem("Todos")
        self.anio_combo.currentTextChanged.connect(self.cargar_comics)
        self.anio_combo.setMinimumWidth(100)
        
        filtros_layout.addWidget(lbl_autor)
        filtros_layout.addWidget(self.autor_combo)
        filtros_layout.addSpacing(10)
        filtros_layout.addWidget(lbl_anio)
        filtros_layout.addWidget(self.anio_combo)
        
        toolbar_layout.addWidget(frame_filtros)
        
        # Ordenamiento
        frame_orden = QWidget()
        frame_orden.setStyleSheet("background-color: #16213e;")
        orden_layout = QHBoxLayout(frame_orden)
        orden_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_orden = QLabel("Ordenar por:")
        lbl_orden.setStyleSheet("background-color: #16213e; color: white;")
        self.orden_combo = QComboBox()
        self.orden_combo.addItems(["Nombre", "Año", "Autor"])
        self.orden_combo.currentTextChanged.connect(self.cargar_comics)
        self.orden_combo.setMinimumWidth(120)
        
        orden_layout.addWidget(lbl_orden)
        orden_layout.addWidget(self.orden_combo)
        
        toolbar_layout.addWidget(frame_orden)
        toolbar_layout.addStretch()
        
        # Agregar toolbar al layout principal
        self.setMenuWidget(toolbar)
        
    def crear_panel_principal(self):
        """Crear panel principal con TreeWidget y panel de detalles"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Panel izquierdo (lista de cómics)
        panel_izquierdo = QWidget()
        panel_izquierdo.setStyleSheet("background-color: #1a1a2e;")
        izquierdo_layout = QVBoxLayout(panel_izquierdo)
        
        # TreeWidget
        self.tree = QTreeWidget()
        self.tree.setAlternatingRowColors(True)
        self.tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.tree.setColumnCount(5)
        self.tree.setHeaderLabels(["ID", "Título", "Autor", "Año", "Editorial"])
        
        # Configurar columnas
        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.tree.itemSelectionChanged.connect(self.mostrar_detalles)
        
        izquierdo_layout.addWidget(self.tree)
        
        # Botones de acción
        frame_botones = QWidget()
        frame_botones.setStyleSheet("background-color: #1a1a2e;")
        botones_layout = QHBoxLayout(frame_botones)
        botones_layout.setSpacing(10)
        
        self.btn_agregar = QPushButton("Agregar Comic")
        self.btn_agregar.setObjectName("btnAgregar")
        self.btn_agregar.clicked.connect(self.abrir_agregar_comic)
        
        self.btn_editar = QPushButton("Editar")
        self.btn_editar.setObjectName("btnEditar")
        self.btn_editar.clicked.connect(self.editar_comic)
        
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setObjectName("btnEliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_comic)
        
        botones_layout.addWidget(self.btn_agregar)
        botones_layout.addWidget(self.btn_editar)
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addStretch()
        
        izquierdo_layout.addWidget(frame_botones)
        
        # Panel derecho (detalles)
        panel_derecho = QWidget()
        panel_derecho.setFixedWidth(350)
        panel_derecho.setStyleSheet("background-color: #16213e;")
        derecho_layout = QVBoxLayout(panel_derecho)
        derecho_layout.setContentsMargins(10, 10, 10, 10)
        
        # Título detalles
        lbl_detalles = QLabel("DETALLES DEL CÓMIC")
        lbl_detalles.setObjectName("subtitulo")
        lbl_detalles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        derecho_layout.addWidget(lbl_detalles)
        
        # Área de texto para detalles
        self.txt_detalles = QTextEdit()
        self.txt_detalles.setReadOnly(True)
        self.txt_detalles.setStyleSheet("""
            QTextEdit {
                background-color: #0f3460;
                color: white;
                border: 1px solid #e94560;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        derecho_layout.addWidget(self.txt_detalles)
        
        # Agregar paneles al layout principal
        main_layout.addWidget(panel_izquierdo, 1)
        main_layout.addWidget(panel_derecho)
        
    def cargar_comics(self):
        """Cargar comics en el TreeWidget con filtros y ordenamiento"""
        # Limpiar tree
        self.tree.clear()
        
        # Obtener comics filtrados
        comics = self.controlador.obtener_todos_comics()
        
        # Aplicar filtros
        self.busqueda = self.busqueda_entry.text().lower()
        self.filtro_autor = self.autor_combo.currentText()
        self.filtro_anio = self.anio_combo.currentText()
        
        if self.filtro_autor != "Todos":
            comics = [c for c in comics if c.autor == self.filtro_autor]
        if self.filtro_anio != "Todos":
            comics = [c for c in comics if str(c.anio) == self.filtro_anio]
        if self.busqueda:
            comics = [c for c in comics if self.busqueda in c.titulo.lower() or 
                     self.busqueda in c.autor.lower()]
        
        # Ordenar
        self.orden = self.orden_combo.currentText()
        if self.orden == "Nombre":
            comics.sort(key=lambda x: x.titulo)
        elif self.orden == "Año":
            comics.sort(key=lambda x: x.anio)
        elif self.orden == "Autor":
            comics.sort(key=lambda x: x.autor)
        
        # Insertar en tree
        for comic in comics:
            item = QTreeWidgetItem(self.tree)
            item.setText(0, str(comic.id))
            item.setText(1, comic.titulo)
            item.setText(2, comic.autor)
            item.setText(3, str(comic.anio))
            item.setText(4, comic.editorial)
            # Guardar el objeto comic para usarlo después
            item.setData(0, Qt.ItemDataRole.UserRole, comic)
        
        # Actualizar filtros
        self.actualizar_filtros(comics)
        
    def actualizar_filtros(self, comics):
        """Actualizar opciones de filtros"""
        # Guardar selección actual
        autor_actual = self.autor_combo.currentText()
        anio_actual = self.anio_combo.currentText()
        
        # Actualizar autores
        autores = sorted(set(c.autor for c in comics))
        self.autor_combo.clear()
        self.autor_combo.addItem("Todos")
        self.autor_combo.addItems(autores)
        
        # Restaurar selección si existe
        index = self.autor_combo.findText(autor_actual)
        if index >= 0:
            self.autor_combo.setCurrentIndex(index)
        
        # Actualizar años
        anios = sorted(set(c.anio for c in comics))
        self.anio_combo.clear()
        self.anio_combo.addItem("Todos")
        self.anio_combo.addItems([str(anio) for anio in anios])
        
        # Restaurar selección si existe
        index = self.anio_combo.findText(anio_actual)
        if index >= 0:
            self.anio_combo.setCurrentIndex(index)
        
    def mostrar_detalles(self):
        """Mostrar detalles del comic seleccionado"""
        items = self.tree.selectedItems()
        if not items:
            return
            
        item = items[0]
        comic = item.data(0, Qt.ItemDataRole.UserRole)
        
        if comic:
            detalles = f"""
            TÍTULO: {comic.titulo}
            
            AUTOR: {comic.autor}
            
            AÑO: {comic.anio}
            
            EDITORIAL: {comic.editorial}
            
            DESCRIPCIÓN:
            {comic.descripcion if hasattr(comic, 'descripcion') else 'No disponible'}
            
            PERSONAJES:
            {', '.join(comic.personajes) if hasattr(comic, 'personajes') else 'No disponible'}
            """
            
            self.txt_detalles.setText(detalles)
            
    def abrir_agregar_comic(self):
        """Abrir ventana para agregar comic"""
        # Importar aquí para evitar importación circular
        from .ventana_comic import VentanaComic
        ventana_comic = VentanaComic(self.controlador, self.cargar_comics, parent=self)
        ventana_comic.exec()
        
    def editar_comic(self):
        """Editar comic seleccionado"""
        items = self.tree.selectedItems()
        if not items:
            QMessageBox.warning(self, "Advertencia", "Selecciona un comic para editar")
            return
            
        item = items[0]
        comic = item.data(0, Qt.ItemDataRole.UserRole)
        
        if comic:
            from .ventana_comic import VentanaComic
            ventana_comic = VentanaComic(self.controlador, self.cargar_comics, comic, self)
            ventana_comic.exec()
            
    def eliminar_comic(self):
        """Eliminar comic seleccionado"""
        items = self.tree.selectedItems()
        if not items:
            QMessageBox.warning(self, "Advertencia", "Selecciona un comic para eliminar")
            return
            
        reply = QMessageBox.question(self, "Confirmar", 
                                    "¿Estás seguro de eliminar este comic?",
                                    QMessageBox.StandardButton.Yes | 
                                    QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            item = items[0]
            comic = item.data(0, Qt.ItemDataRole.UserRole)
            self.controlador.eliminar_comic(comic.id)
            self.cargar_comics()
            self.txt_detalles.clear()
            QMessageBox.information(self, "Éxito", "Comic eliminado correctamente")
            
    def mostrar_estadisticas(self):
        """Mostrar estadísticas de la colección"""
        comics = self.controlador.obtener_todos_comics()
        
        total = len(comics)
        autores = len(set(c.autor for c in comics))
        anios = len(set(c.anio for c in comics))
        editoriales = len(set(c.editorial for c in comics))
        
        stats = f"""
        ESTADÍSTICAS DE LA COLECCIÓN
        
        Total de cómics: {total}
        Autores distintos: {autores}
        Años diferentes: {anios}
        Editoriales: {editoriales}
        
        TOP 5 AUTORES:
        """
        
        contador_autores = Counter(c.autor for c in comics)
        for autor, count in contador_autores.most_common(5):
            stats += f"\n   • {autor}: {count} cómic(s)"
            
        QMessageBox.information(self, "Estadísticas", stats)
        
    def mostrar_acerca_de(self):
        """Mostrar información del programa"""
        info = """
        SISTEMA DE GESTIÓN DE CÓMICS MARVEL
        
        Versión: 1.0
        Desarrollado para Proyecto Marvel
        
        Características:
        Gestión completa de cómics
        Búsqueda y filtros avanzados
        Ordenamiento por nombre, año o autor
        Interfaz moderna y fácil de usar
        
        © 2026 - Todos los derechos reservados
        """
        QMessageBox.about(self, "Acerca de", info)
        
    def iniciar(self):
        """Iniciar la aplicación"""
        self.show()