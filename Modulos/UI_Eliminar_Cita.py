import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Eliminar Cita")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal (Horizontal)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES ---
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC);
            }
            QWidget#Sidebar {
                background-color: transparent;
            }
            QWidget#WhitePanel {
                background-color: white;
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                margin: 20px 20px 20px 0px; 
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                color: #333;
            }
            /* Estilos del Sidebar */
            QLabel#Logo {
                color: white; 
                font-size: 36px; 
                font-weight: bold; 
                margin-bottom: 30px;
            }
            QPushButton.menu-btn {
                text-align: left;
                padding-left: 20px;
                border: none;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 18px;
                background-color: transparent;
                height: 40px;
            }
            QPushButton.menu-btn:hover {
                color: #E0E0E0;
                background-color: rgba(255, 255, 255, 0.1);
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
            QPushButton.sub-btn {
                text-align: left;
                border: none;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: normal;
                padding-left: 50px;
                color: #F0F0F0;
                background-color: transparent;
                height: 30px;
            }
            QPushButton.sub-btn:hover {
                color: #333;
                background-color: rgba(255, 255, 255, 0.2);
                font-weight: bold;
            }
        """)

        # --- 1. BARRA LATERAL (Izquierda) ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO (Derecha - Eliminar) ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header con Título y Botón Cerrar
        header_layout = QHBoxLayout()
        
        lbl_header = QLabel("Eliminar citas")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_close_view = QPushButton("✕")
        btn_close_view.setFixedSize(40, 40)
        btn_close_view.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close_view.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border-radius: 20px;
                font-size: 20px;
                color: #666;
                border: none;
            }
            QPushButton:hover {
                background-color: #ffcccc;
                color: #cc0000;
            }
        """)
        btn_close_view.clicked.connect(self.close) 

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close_view)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(30)

        # --- CONTENIDO DE ELIMINACIÓN ---
        self.setup_delete_content(self.white_layout)

        # Agregar al layout principal
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        lbl_logo = QLabel("YUNO VET")
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(lbl_logo)
        
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar", "Eliminar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar", "Eliminar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar", "Eliminar"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("""
            QPushButton {
                text-align: center; border: 2px solid white; 
                border-radius: 15px; padding: 10px; margin-top: 20px;
                font-size: 14px; color: white; font-weight: bold;
                background-color: transparent;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.2); }
        """)
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)

    def setup_accordion_group(self, title, options):
        btn_main = QPushButton(title)
        btn_main.setProperty("class", "menu-btn")
        btn_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebar_layout.addWidget(btn_main)

        frame_options = QFrame()
        layout_options = QVBoxLayout(frame_options)
        layout_options.setContentsMargins(0, 0, 0, 10)
        layout_options.setSpacing(2)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def setup_delete_content(self, parent_layout):
        # --- 1. Barra de Búsqueda ---
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(15)

        # Input de búsqueda
        inp_search = QLineEdit()
        inp_search.setPlaceholderText("Buscar paciente (Nombre o ID)...")
        inp_search.setFixedHeight(50)
        inp_search.setStyleSheet("""
            QLineEdit {
                background-color: #F0F2F5;
                border: 1px solid #DDD;
                border-radius: 10px;
                padding: 5px 20px;
                font-size: 18px;
                color: #333;
            }
        """)
        
        btn_search = QPushButton("🔍")
        btn_search.setFixedSize(50, 50)
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("""
            QPushButton {
                background-color: #5f2c82;
                color: white;
                border-radius: 10px;
                font-size: 20px;
            }
            QPushButton:hover { background-color: #4a2366; }
        """)

        search_layout.addWidget(inp_search)
        search_layout.addWidget(btn_search)
        
        parent_layout.addWidget(search_container)
        parent_layout.addSpacing(30)

        # --- 2. Tarjeta de Detalles (Solo Lectura) ---
        # Simulamos que se encontró un registro para mostrar los campos del diseño
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(241, 131, 227, 0.1); 
                border: 1px solid #E1BEE7;
                border-radius: 15px;
            }
            QLabel {
                background-color: transparent;
                border: none;
                color: #444;
                font-size: 18px;
            }
            QLabel.value {
                font-weight: bold;
                color: #000;
            }
        """)
        
        details_layout = QGridLayout(details_frame)
        details_layout.setContentsMargins(30, 30, 30, 30)
        details_layout.setVerticalSpacing(20)
        details_layout.setHorizontalSpacing(40)

        # Datos de ejemplo
        labels = [
            ("ID de la cita:", "C-2024-089"),
            ("Fecha:", "24/11/2025"),
            ("Hora:", "10:30 AM"),
            ("Estado:", "Pendiente"),
            ("Id mascota:", "PET-452"),
            ("ID veterinario:", "VET-004")
        ]

        # Crear Grid
        for i, (label_text, value_text) in enumerate(labels):
            lbl = QLabel(label_text)
            val = QLabel(value_text)
            val.setProperty("class", "value") # Aplica el estilo negrita
            
            # Columna 0: Label, Columna 1: Valor
            # Si es par va a la izquierda, impar a la derecha (efecto 2 columnas)
            row = i // 2
            col_start = (i % 2) * 2
            
            details_layout.addWidget(lbl, row, col_start)
            details_layout.addWidget(val, row, col_start + 1)

        parent_layout.addWidget(details_frame)
        parent_layout.addStretch()

        # --- 3. Botón Eliminar ---
        btn_delete = QPushButton("Eliminar cita")
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.setFixedSize(250, 60)
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #b67cfc;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #ff4d4d; /* Rojo al pasar el mouse para indicar peligro */
            }
            QPushButton:pressed {
                background-color: #cc0000;
            }
        """)
        
        # Conectar a una función de confirmación
        btn_delete.clicked.connect(self.confirm_delete)

        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_delete)
        btn_container.addStretch()
        
        parent_layout.addLayout(btn_container)
        parent_layout.addSpacing(20)

    def confirm_delete(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirmar Eliminación")
        msg.setText("¿Está seguro que desea eliminar esta cita?")
        msg.setInformativeText("Esta acción no se puede deshacer.")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        
        # Estilo simple para el popup
        msg.setStyleSheet("background-color: white; color: #333;")
        
        ret = msg.exec()
        if ret == QMessageBox.StandardButton.Yes:
            print("Cita eliminada")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())