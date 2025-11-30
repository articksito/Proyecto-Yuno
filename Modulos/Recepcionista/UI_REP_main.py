import sys
import os

from datetime import datetime
from functools import partial 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap

# --- AJUSTE DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path: sys.path.append(current_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)

# --- IMPORTACIÓN DE LA VENTANA DE LOGIN ---
try:
    from UI_inicio_de_sesion import MainWindow as LoginWindow
except ImportError:
    LoginWindow = None  

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        
        self.nombre_usuario = nombre_usuario
        self.ventana = None 

        self.setWindowTitle(f"Sistema Veterinario Yuno - Menú Principal ({self.nombre_usuario})")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600) # Evitar modo miniatura

        # Datos visuales
        self.user_data = {
            "nombre": self.nombre_usuario,
            "puesto": "Recepcionista",
        }

        # Widget Central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS (ESTANDARIZADOS) ---
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
            /* Botones del Menú Lateral (Igual que en las otras vistas) */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px;
                color: white; font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF;
            }
            /* Botones del Submenú */
            QPushButton.sub-btn {
                text-align: left; padding-left: 40px; font-size: 16px;
                border-radius: 10px; color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05);
                height: 35px; margin: 2px 10px;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
        """)

        # 1. Sidebar
        self.setup_sidebar()

        # 2. Panel Contenido
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        
        self.content_layout = QVBoxLayout(self.white_panel)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.setSpacing(20)

        self.setup_central_info()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        # Márgenes idénticos a las otras vistas para consistencia visual
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50) 
        self.sidebar_layout.setSpacing(5)

        # Logo
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_logo = os.path.join(parent_dir, "FILES", "logo_yuno.png")
        
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                lbl_logo.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")

        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)
        
        # Menús
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])

        self.sidebar_layout.addStretch()

        # Botón Cerrar Sesión (Estilo unificado)
        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("""
            QPushButton {
                border: 2px solid white; 
                border-radius: 15px; 
                padding: 10px; 
                margin-top: 20px;
                font-size: 14px; 
                color: white; 
                font-weight: bold; 
                background-color: transparent;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.2); }
        """)
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        
        btn_logout.clicked.connect(self.logout_to_login) 
        
        self.sidebar_layout.addWidget(btn_logout)

    def logout_to_login(self):
        """Cierra el menú y abre la ventana de inicio de sesión."""
        if LoginWindow:
            try:
                self.ventana = LoginWindow()
                self.ventana.show()
                self.close()
            except Exception as e:
                print(f"Error al abrir Login: {e}")
                self.close()
        else:
            self.close()

    def setup_accordion_group(self, title, options):
        btn_main = QPushButton(title)
        btn_main.setProperty("class", "menu-btn")
        btn_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebar_layout.addWidget(btn_main)

        frame_options = QFrame()
        layout_options = QVBoxLayout(frame_options)
        layout_options.setContentsMargins(0, 0, 0, 10)
        layout_options.setSpacing(5)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            # Router
            btn_sub.clicked.connect(partial(self.router_ventanas, title, opt_text))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def setup_central_info(self):
        info_container = QFrame()
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(15)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_title = QLabel("Bienvenid@")
        lbl_title.setStyleSheet("color: #888; font-size: 24px; letter-spacing: 2px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_name = QLabel(self.user_data['nombre'])
        lbl_name.setStyleSheet("color: #5f2c82; font-size: 56px; font-weight: bold;")
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_role = QLabel(self.user_data['puesto'])
        lbl_role.setStyleSheet("color: #FC7CE2; font-size: 20px; font-weight: 600;")
        lbl_role.setAlignment(Qt.AlignmentFlag.AlignCenter)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedWidth(120)
        line.setStyleSheet("background-color: #DDD; margin: 25px 0;")
        
        self.lbl_time = QLabel()
        self.lbl_time.setStyleSheet("color: #555; font-size: 80px; font-weight: 300; font-family: 'Segoe UI Light';")
        self.lbl_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.lbl_time.setText(current_time)

    def router_ventanas(self, categoria, opcion):
        print(f"Abriendo: {categoria} -> {opcion}") 
        
        # Mapeo de Nombres de Archivos
        mapa_ventanas = {
            "Citas": {
                "Agendar": "UI_REP_Crear_cita",
                "Visualizar": "UI_REP_Revisar_Cita",
                "Modificar": "UI_REP_Modificar_cita"
            },
            "Mascotas": {
                "Registrar": "UI_REP_Registrar_mascota",
                "Visualizar": "UI_Revisar_Mascota",
                "Modificar": "UI_REP_Modificar_Mascota"
            },
            "Clientes": {
                "Registrar": "UI_REP_Registra_cliente",
                "Visualizar": "UI_Revisar_cliente",
                "Modificar": "UI_REP_Modificar_cliente"
            }
        }

        nombre_archivo = mapa_ventanas.get(categoria, {}).get(opcion)

        if nombre_archivo:
            try:
                module = __import__(nombre_archivo, fromlist=['MainWindow'])
                self.ventana = module.MainWindow(self.nombre_usuario)
                self.ventana.show()
                self.close()
            except ImportError as e:
                QMessageBox.critical(self, "Error de Archivo", f"No se encuentra el archivo: {nombre_archivo}.py\n\nDetalle: {e}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al abrir la ventana:\n{e}")
        else:
            QMessageBox.warning(self, "En construcción", f"La opción '{opcion}' aún no está vinculada.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow("Recepcionista TEST")
    window.show()
    sys.exit(app.exec())