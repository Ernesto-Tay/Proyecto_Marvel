from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QTextEdit, QPushButton, 
                             QMessageBox, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
# Importar desde el __init__ de Modelos
from Modelos import Comic

class VentanaComic(QDialog):
    def __init__(self, controlador, callback_actualizar, comic=None, parent=None):
        super().__init__(parent)
        self.controlador = controlador
        self.callback = callback_actualizar
        self.comic = comic
        
        # Configurar la ventana
        if comic:
            self.setWindowTitle("Editar Comic")
        else:
            self.setWindowTitle("Agregar Comic")
            
        self.setGeometry(200, 200, 500, 600)
        self.setMinimumSize(500, 600)
        self.setMaximumSize(500, 600)
        self.setModal(True)
        
        # Aplicar estilo CSS
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
            }
            QWidget#mainWidget {
                background-color: #16213e;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
            QLabel#titulo {
                color: #e94560;
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit {
                background-color: #0f3460;
                color: white;
                border: 1px solid #e94560;
                border-radius: 3px;
                padding: 5px;
                font-size: 10px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #e94560;
            }
            QPushButton {
                font-weight: bold;
                padding: 5px 20px;
                border: none;
                border-radius: 3px;
            }
            QPushButton#btnGuardar {
                background-color: #e94560;
                color: white;
            }
            QPushButton#btnGuardar:hover {
                background-color: #ff6b8b;
            }
            QPushButton#btnCancelar {
                background-color: #6c757d;
                color: white;
            }
            QPushButton#btnCancelar:hover {
                background-color: #8c959d;
            }
        """)
        
        self.crear_formulario()
        
        if comic:
            self.cargar_datos()
            
    def crear_formulario(self):
        """Crear formulario de ingreso"""
        # Widget principal
        main_widget = QWidget()
        main_widget.setObjectName("mainWidget")
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Título
        titulo = QLabel("DATOS DEL CÓMIC")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Campos
        self.entries = {}
        
        # Título
        self.titulo_entry = QLineEdit()
        self.titulo_entry.setPlaceholderText("Ingrese el título del cómic")
        form_layout.addRow(QLabel("Título:"), self.titulo_entry)
        self.entries['titulo'] = self.titulo_entry
        
        # Autor
        self.autor_entry = QLineEdit()
        self.autor_entry.setPlaceholderText("Ingrese el autor del cómic")
        form_layout.addRow(QLabel("Autor:"), self.autor_entry)
        self.entries['autor'] = self.autor_entry
        
        # Año
        self.anio_entry = QLineEdit()
        self.anio_entry.setPlaceholderText("Ingrese el año de publicación")
        form_layout.addRow(QLabel("Año:"), self.anio_entry)
        self.entries['anio'] = self.anio_entry
        
        # Editorial
        self.editorial_entry = QLineEdit()
        self.editorial_entry.setPlaceholderText("Ingrese la editorial")
        form_layout.addRow(QLabel("Editorial:"), self.editorial_entry)
        self.entries['editorial'] = self.editorial_entry
        
        # Descripción
        self.descripcion_text = QTextEdit()
        self.descripcion_text.setMaximumHeight(100)
        self.descripcion_text.setPlaceholderText("Ingrese la descripción del cómic")
        form_layout.addRow(QLabel("Descripción:"), self.descripcion_text)
        self.entries['descripcion'] = self.descripcion_text
        
        # Personajes
        self.personajes_entry = QLineEdit()
        self.personajes_entry.setPlaceholderText("Ingrese los personajes separados por coma")
        form_layout.addRow(QLabel("Personajes (separados por coma):"), self.personajes_entry)
        
        layout.addLayout(form_layout)
        
        # Espaciador
        layout.addStretch()
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setObjectName("btnGuardar")
        self.btn_guardar.clicked.connect(self.guardar)
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("btnCancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.btn_guardar)
        btn_layout.addWidget(self.btn_cancelar)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Establecer el layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_widget)
        
    def cargar_datos(self):
        """Cargar datos del comic a editar"""
        self.titulo_entry.setText(self.comic.titulo)
        self.autor_entry.setText(self.comic.autor)
        self.anio_entry.setText(str(self.comic.anio))
        self.editorial_entry.setText(self.comic.editorial)
        
        if hasattr(self.comic, 'descripcion'):
            self.descripcion_text.setPlainText(self.comic.descripcion)
            
        if hasattr(self.comic, 'personajes'):
            # Asegurarse de que personajes es una lista
            if isinstance(self.comic.personajes, list):
                self.personajes_entry.setText(', '.join(self.comic.personajes))
            else:
                self.personajes_entry.setText(str(self.comic.personajes))
            
    def guardar(self):
        """Guardar comic"""
        try:
            # Obtener datos
            titulo = self.titulo_entry.text().strip()
            autor = self.autor_entry.text().strip()
            anio = int(self.anio_entry.text().strip())
            editorial = self.editorial_entry.text().strip()
            descripcion = self.descripcion_text.toPlainText().strip()
            
            # Procesar personajes - eliminar prints de debug si los hay
            personajes_text = self.personajes_entry.text().strip()
            if personajes_text:
                personajes = [p.strip() for p in personajes_text.split(',') if p.strip()]
            else:
                personajes = []
            
            # Validar
            if not all([titulo, autor, anio, editorial]):
                QMessageBox.warning(self, "Campos incompletos", 
                                  "Todos los campos son obligatorios")
                return
                
            if self.comic:
                # Editar
                self.comic.titulo = titulo
                self.comic.autor = autor
                self.comic.anio = anio
                self.comic.editorial = editorial
                self.comic.descripcion = descripcion
                self.comic.personajes = personajes
                self.controlador.actualizar_comic(self.comic)
                QMessageBox.information(self, "Éxito", 
                                      "Comic actualizado correctamente")
            else:
                # Crear nuevo
                nuevo_id = self.controlador.generar_id()
                comic = Comic(nuevo_id, titulo, autor, anio, editorial)
                comic.descripcion = descripcion
                comic.personajes = personajes
                self.controlador.agregar_comic(comic)
                QMessageBox.information(self, "Éxito", 
                                      "Comic agregado correctamente")
                
            self.callback()
            self.accept()
            
        except ValueError:
            QMessageBox.critical(self, "Error", 
                               "El año debe ser un número válido")
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"Error al guardar: {str(e)}")