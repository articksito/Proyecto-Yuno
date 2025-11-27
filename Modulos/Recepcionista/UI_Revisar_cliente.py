import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Revisar Cliente")
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
            /* Estilos para datos de revisión */
            QLabel.label-key {
                font-size: 20px;
                color: #666;
                font-weight: normal;
            }
            QLabel.label-value {
                font-size: 24px;
                color: #000;
                font-weight: bold;
                padding-bottom: 15px;
                border-bottom: 1px solid #EEE;
            }
        """)

        # --- 1. BARRA LATERAL (Izquierda) ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO (Derecha - Revisión Cliente) ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header con Título y Botón Volver
        header_layout = QHBoxLayout()
        
        lbl_header = QLabel("Revisar cliente")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver") 
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                color: #555;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
                color: #333;
            }
        """)
        btn_back.clicked.connect(self.close)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_back)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(40)

        # Contenedor Principal de Datos
        content_layout = QHBoxLayout()
        content_layout.setSpacing(50)

        # --- A. COLUMNA DE DATOS DEL CLIENTE (Izquierda) ---
        self.setup_client_data(content_layout)

        # --- B. PANEL DE INFORMACIÓN Y FOTO (Derecha) ---
        self.setup_info_board(content_layout)

        self.white_layout.addLayout(content_layout)
        self.white_layout.addStretch()

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

    def setup_client_data(self, parent_layout):
        # Contenedor de datos estilo lista/ficha
        data_widget = QWidget()
        data_layout = QVBoxLayout(data_widget)
        data_layout.setSpacing(20)
        data_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Datos simulados del cliente
        client_data = [
            ("ID Cliente:", "CLI-8832"),
            ("Nombre:", "Juan"),
            ("Apellido:", "Pérez"),
            ("Correo:", "juan.perez@email.com"),
            ("Dirección:", "Av. Siempre Viva 123"),
            ("Teléfono:", "555-0199")
        ]

        for key, value in client_data:
            row_widget = QWidget()
            row_layout = QVBoxLayout(row_widget)
            row_layout.setContentsMargins(0,0,0,0)
            row_layout.setSpacing(5)

            lbl_key = QLabel(key)
            lbl_key.setProperty("class", "label-key")
            
            lbl_value = QLabel(value)
            lbl_value.setProperty("class", "label-value")
            # Permitir seleccionar texto para copiar
            lbl_value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            row_layout.addWidget(lbl_key)
            row_layout.addWidget(lbl_value)
            
            data_layout.addWidget(row_widget)

        parent_layout.addWidget(data_widget, stretch=3)

    def setup_info_board(self, parent_layout):
        # Panel derecho contenedor
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(30)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- 1. Foto de Perfil (Placeholder) ---
        profile_container = QWidget()
        profile_layout = QVBoxLayout(profile_container)
        profile_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_photo = QLabel("👤")
        lbl_photo.setFixedSize(150, 150)
        lbl_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_photo.setStyleSheet("""
            background-color: #F0F0F0;
            border: 3px solid #FC7CE2;
            border-radius: 75px; /* Círculo perfecto */
            font-size: 60px;
            color: #AAA;
        """)
        
        lbl_photo_caption = QLabel("Foto de Perfil")
        lbl_photo_caption.setStyleSheet("color: #888; font-size: 14px; margin-top: 10px;")
        lbl_photo_caption.setAlignment(Qt.AlignmentFlag.AlignCenter)

        profile_layout.addWidget(lbl_photo)
        profile_layout.addWidget(lbl_photo_caption)
        right_layout.addWidget(profile_container)

        # --- 2. Board de Información ---
        board_container = QFrame()
        board_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #CCC;
                border-radius: 10px;
            }
        """)
        
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(0)

        # Header degradado
        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8));
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom: none;
        """)
        header_layout = QVBoxLayout(header_frame)
        lbl_info_title = QLabel("Información")
        lbl_info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info_title.setStyleSheet("color: white; font-size: 22px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(lbl_info_title)

        # Contenido (Motivo/Notas)
        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(30, 30, 30, 30)
        
        lbl_motivo_title = QLabel("Historial / Notas:")
        lbl_motivo_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333; margin-bottom: 10px;")
        
        lbl_motivo_text = QLabel(
            "Cliente frecuente desde 2021. \n"
            "Mascotas registradas: 2 (Firulais, Michi). \n"
            "Pagos al día. Prefiere contacto por WhatsApp."
        )
        lbl_motivo_text.setWordWrap(True)
        lbl_motivo_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        lbl_motivo_text.setStyleSheet("color: #555; font-size: 16px; border: none; line-height: 1.5;")
        
        content_layout.addWidget(lbl_motivo_title)
        content_layout.addWidget(lbl_motivo_text)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)

        right_layout.addWidget(board_container)

        parent_layout.addWidget(right_container, stretch=2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())