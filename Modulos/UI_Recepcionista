import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Recepción")
        self.resize(1280, 720)

        # Datos simulados (Aquí conectarías tu BD)
        self.user_data = {
            "nombre": "Ana García",
            "puesto": "Recepcionista Senior",
            "id": "REC-001"
        }

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal (Horizontal)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS (Copiados del diseño de Login) ---
        # Degradado: Rosa (#FC7CE2) arriba -> Azul (#7CEBFC) abajo
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
            }
            /* Estilo Botones Menú (Transparentes y blancos) */
            QPushButton {
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
            QPushButton:hover {
                color: #E0E0E0;
                background-color: rgba(255, 255, 255, 0.1);
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
            /* Estilo Botones Sub-menú */
            QPushButton.sub-btn {
                font-size: 16px;
                font-weight: normal;
                padding-left: 50px;
                color: #F0F0F0;
            }
            QPushButton.sub-btn:hover {
                color: #333;
                background-color: rgba(255, 255, 255, 0.2);
                font-weight: bold;
            }
        """)

        # --- 1. BARRA LATERAL (Izquierda) ---
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        # Logo
        lbl_logo = QLabel("YUNO VET")
        lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(lbl_logo)
        
        # Menús Desplegables
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar", "Eliminar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar", "Eliminar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar", "Eliminar"])

        self.sidebar_layout.addStretch()

        # Botón Cerrar Sesión
        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("""
            text-align: center; border: 2px solid white; 
            border-radius: 15px; padding: 10px; margin-top: 20px;
            font-size: 14px;
        """)
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)

        # --- 2. PANEL BLANCO (Derecha) ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        
        self.content_layout = QVBoxLayout(self.white_panel)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.setSpacing(20)

        # Información Centralizada
        self.setup_central_info()

        # Agregar a la ventana
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_accordion_group(self, title, options):
        """Crea un grupo de botones tipo acordeón"""
        btn_main = QPushButton(title)
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
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.open_option_window(t, o))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def setup_central_info(self):
        """Configura la información centrada en el panel blanco"""
        
        info_container = QFrame()
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(15)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título "Recepcionista"
        lbl_title = QLabel("Recepcionista")
        lbl_title.setStyleSheet("color: #888; font-size: 24px; letter-spacing: 2px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Nombre (Grande)
        lbl_name = QLabel(self.user_data['nombre'])
        lbl_name.setStyleSheet("color: #5f2c82; font-size: 56px; font-weight: bold;") # Color morado del login
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Puesto
        lbl_role = QLabel(self.user_data['puesto'])
        lbl_role.setStyleSheet("color: #FC7CE2; font-size: 20px; font-weight: 600;")
        lbl_role.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedWidth(120)
        line.setStyleSheet("background-color: #DDD; margin: 25px 0;")
        
        # Hora actual
        self.lbl_time = QLabel()
        self.lbl_time.setStyleSheet("""
            color: #555; 
            font-size: 80px; 
            font-weight: 300; 
            font-family: 'Segoe UI Light';
        """)
        self.lbl_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Armado del layout central
        info_layout.addWidget(lbl_title)
        info_layout.addWidget(lbl_name)
        info_layout.addWidget(lbl_role)
        
        line_layout = QHBoxLayout()
        line_layout.addStretch()
        line_layout.addWidget(line)
        line_layout.addStretch()
        info_layout.addLayout(line_layout)
        
        info_layout.addWidget(self.lbl_time)

        self.content_layout.addWidget(info_container)

        # Timer para el reloj en tiempo real
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) # 1000 ms = 1 segundo
        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.lbl_time.setText(current_time)

    def open_option_window(self, category, option):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{category} - {option}")
        dialog.resize(400, 300)
        dialog.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout(dialog)
        label = QLabel(f"Sección: {category}\nAcción: {option}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #333; font-size: 20px; font-family: 'Segoe UI';")
        layout.addWidget(label)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Fuente global
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())