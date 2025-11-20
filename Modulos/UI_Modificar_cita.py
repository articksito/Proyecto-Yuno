import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QDateEdit, QTimeEdit, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Modificar Cita")
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

        # --- 2. PANEL BLANCO (Derecha - Modificar) ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header con Título y Botón Cerrar
        header_layout = QHBoxLayout()
        
        lbl_header = QLabel("Modificar cita")
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
        btn_close_view.clicked.connect(lambda: print("Cerrar vista")) 

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close_view)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # Contenedor Horizontal para Formulario + Panel Info
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        # --- A. FORMULARIO DE EDICIÓN (Izquierda) ---
        self.setup_edit_form(content_layout)

        # --- B. PANEL DE INFORMACIÓN (Derecha) ---
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        
        # Botón Guardar
        self.setup_save_button()

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

    def setup_edit_form(self, parent_layout):
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Estilo de Inputs (Fondo Lila Transparente)
        input_style = """
            QLineEdit, QDateEdit, QTimeEdit, QComboBox {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 18px;
                color: #333;
                height: 45px;
            }
            QComboBox::drop-down { border: 0px; }
        """
        
        # Estilo especial para campos NO modificables
        readonly_style = """
            QLineEdit {
                background-color: #E0E0E0;
                border: 1px solid #CCC;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 18px;
                color: #777;
                height: 45px;
            }
        """
        
        label_style = "font-size: 24px; color: black; font-weight: 400;"

        # --- Campos ---
        
        # 1. ID de la cita (NO MODIFICABLE)
        lbl_id = QLabel("ID de la cita:")
        lbl_id.setStyleSheet(label_style)
        inp_id = QLineEdit("C-2024-089") # Valor precargado
        inp_id.setReadOnly(True)
        inp_id.setStyleSheet(readonly_style)
        inp_id.setToolTip("Este campo no es modificable")

        # 2. Fecha
        lbl_fecha = QLabel("Fecha de la cita:")
        lbl_fecha.setStyleSheet(label_style)
        inp_fecha = QDateEdit()
        inp_fecha.setCalendarPopup(True)
        inp_fecha.setDate(datetime.now().date())
        inp_fecha.setStyleSheet(input_style)

        # 3. Hora
        lbl_hora = QLabel("Hora de la cita:")
        lbl_hora.setStyleSheet(label_style)
        inp_hora = QTimeEdit()
        inp_hora.setTime(datetime.now().time())
        inp_hora.setStyleSheet(input_style)

        # 4. Motivo
        lbl_motivo = QLabel("Motivo:")
        lbl_motivo.setStyleSheet(label_style)
        inp_motivo = QLineEdit("Revisión general")
        inp_motivo.setStyleSheet(input_style)

        # 5. Estado
        lbl_estado = QLabel("Estado:")
        lbl_estado.setStyleSheet(label_style)
        inp_estado = QComboBox()
        inp_estado.addItems(["Pendiente", "Confirmada", "Cancelada", "Completada"])
        inp_estado.setCurrentText("Confirmada")
        inp_estado.setStyleSheet(input_style)

        # 6. ID Mascota
        lbl_mascota = QLabel("Id de la mascota:")
        lbl_mascota.setStyleSheet(label_style)
        inp_mascota = QLineEdit("PET-452")
        inp_mascota.setStyleSheet(input_style)

        # 7. ID Veterinario
        lbl_vet = QLabel("Id del veterinario:")
        lbl_vet.setStyleSheet(label_style)
        inp_vet = QLineEdit("VET-004")
        inp_vet.setStyleSheet(input_style)

        # Añadir al Grid
        grid_layout.addWidget(lbl_id, 0, 0)
        grid_layout.addWidget(inp_id, 0, 1)

        grid_layout.addWidget(lbl_fecha, 1, 0)
        grid_layout.addWidget(inp_fecha, 1, 1)

        grid_layout.addWidget(lbl_hora, 2, 0)
        grid_layout.addWidget(inp_hora, 2, 1)

        grid_layout.addWidget(lbl_motivo, 3, 0)
        grid_layout.addWidget(inp_motivo, 3, 1)

        grid_layout.addWidget(lbl_estado, 4, 0)
        grid_layout.addWidget(inp_estado, 4, 1)

        grid_layout.addWidget(lbl_mascota, 5, 0)
        grid_layout.addWidget(inp_mascota, 5, 1)

        grid_layout.addWidget(lbl_vet, 6, 0)
        grid_layout.addWidget(inp_vet, 6, 1)

        # Label extra de "No modificable" (opcional, visual)
        lbl_warning = QLabel("(No modificable)")
        lbl_warning.setStyleSheet("font-size: 12px; color: #888;")
        grid_layout.addWidget(lbl_warning, 0, 2)

        grid_layout.setRowStretch(7, 1)
        parent_layout.addWidget(form_widget, stretch=2)

    def setup_info_board(self, parent_layout):
        board_container = QFrame()
        board_container.setFixedWidth(300)
        board_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DDD;
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
        lbl_info_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(lbl_info_title)

        # Contenido
        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_motivo = QLabel("<b>Motivo actual:</b><br>Revisión general")
        lbl_motivo.setWordWrap(True)
        lbl_motivo.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        lbl_motivo.setStyleSheet("color: #555; font-size: 16px; border: none;")
        
        content_layout.addWidget(lbl_motivo)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)

        parent_layout.addWidget(board_container, stretch=1)

    def setup_save_button(self):
        btn_save = QPushButton("Guardar")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedSize(250, 60)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #b67cfc;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #a060e8;
            }
            QPushButton:pressed {
                background-color: #8a4cd0;
            }
        """)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_save)
        btn_container.addStretch()
        
        self.white_layout.addLayout(btn_container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())