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
                             QHBoxLayout, QPushButton, QLabel, QFrame, QDialog, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap

from db_connection import Conexion

class MainWindow(QMainWindow):
    def __init__(self, nombre="Recepcionista"):
        self.nombre = nombre
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Recepción")
        self.resize(1280, 720)

        # Datos simulados
        self.user_data = {
            "nombre": f"{self.nombre}",
            "puesto": "Recepcionista",
            "id": "REC-001"
        }

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal (Horizontal)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS ---
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
            /* Estilo Botones Menú Principal */
            QPushButton.menu-btn {
                text-align: left;
                padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1);
                height: 50px;
                margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid white;
                color: #FFF;
            }
            /* Estilo Sub-botones */
            QPushButton.sub-btn {
                text-align: left;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: normal;
                padding-left: 40px;
                border-radius: 10px;
                color: #F0F0F0;
                background-color: rgba(0, 0, 0, 0.05);
                height: 35px;
                margin-bottom: 2px;
                margin-left: 10px;
                margin-right: 10px;
            }
            QPushButton.sub-btn:hover {
                color: white;
                background-color: rgba(255, 255, 255, 0.3);
                font-weight: bold;
            }
        """)

        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # --- LOGO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))

        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                # Escalar logo para que se vea bien en el sidebar
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")

        self.sidebar_layout.addWidget(lbl_logo)
        
        # Menús Desplegables (Solo opciones existentes)
        self.setup_accordion_group("Citas", ["Agendar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Modificar"])

        self.sidebar_layout.addStretch()

        # Botón Cerrar Sesión
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
        btn_main.setProperty("class", "menu-btn") # Para aplicar estilo CSS
        btn_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebar_layout.addWidget(btn_main)

        frame_options = QFrame()
        layout_options = QVBoxLayout(frame_options)
        layout_options.setContentsMargins(0, 0, 0, 10)
        layout_options.setSpacing(5) # Un poco de espacio entre sub-botones
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn") # Para aplicar estilo CSS
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            # Conexión al enrutador
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.router_ventanas(t, o))
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

    # =========================================================================
    #                    ZONA DE LÓGICA Y APERTURA DE VENTANAS
    # =========================================================================

    def router_ventanas(self, categoria, opcion):
        print(f"Abriendo: {categoria} -> {opcion}") 

        try:
            # --- RUTA: CITAS ---
            if categoria == "Citas":
                if opcion == "Agendar":
                    from UI_REP_Crear_cita import MainWindow as AgendarCita
                    self.ventana = AgendarCita()
                    self.ventana.show()
                    self.close()

                elif opcion == "Modificar":
                    from UI_REP_Modificar_cita import MainWindow as ModificarCita
                    self.ventana = ModificarCita()
                    self.ventana.show()
                    self.close()

            # --- RUTA: MASCOTAS ---
            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    from UI_REP_Registrar_mascota import MainWindow as RegistrarMascota
                    self.ventana = RegistrarMascota()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_REP_Modificar_Mascota import MainWindow as ModificarMascota
                    self.ventana = ModificarMascota()
                    self.ventana.show()
                    self.close()

            # --- RUTA: CLIENTES ---
            elif categoria == "Clientes":
                if opcion == "Registrar":
                    from UI_REP_Registra_cliente import MainWindow as RegistrarCliente
                    self.ventana = RegistrarCliente()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cliente import MainWindow as ModificarCliente
                    self.ventana = ModificarCliente()
                    self.ventana.show()
                    self.close()
                    
        except ImportError as e:
            QMessageBox.warning(self, "Error de Archivo", f"No se encuentra el archivo de la ventana:\n{e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la ventana: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())