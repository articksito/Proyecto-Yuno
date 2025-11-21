import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from db_connection import Conexion

from UI_Crear_cita import MainWindow as AgendarCita
from UI_Revisar_Cita import MainWindow as Visualizar

class MainWindow(QMainWindow):
    def __init__(self, nombre):
        self.nombre = nombre
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Recepción")
        self.resize(1280, 720)

        # Datos simulados (Aquí conectarías tu BD)
        self.user_data = {
            "nombre": f"{self.nombre}",
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
        
        # Menús Desplegables (Configurados igual que antes)
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
            # Aquí conectamos al enrutador
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

        lbl_title = QLabel("Recepcionista")
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
        """
        Esta función recibe el clic y decide qué función específica ejecutar
        basándose en la categoría y la opción seleccionada.
        """
        print(f"Abriendo: {categoria} -> {opcion}") # Para depuración en consola

        # --- RUTA: CITAS ---
        if categoria == "Citas":
            if opcion == "Agendar": self.abrir_citas_agendar()
            elif opcion == "Visualizar": self.abrir_citas_visualizar()
            elif opcion == "Modificar": self.abrir_citas_modificar()
            elif opcion == "Eliminar": self.abrir_citas_eliminar()

        # --- RUTA: MASCOTAS ---
        elif categoria == "Mascotas":
            if opcion == "Registrar": self.abrir_mascotas_registrar()
            elif opcion == "Visualizar": self.abrir_mascotas_visualizar()
            elif opcion == "Modificar": self.abrir_mascotas_modificar()
            elif opcion == "Eliminar": self.abrir_mascotas_eliminar()

        # --- RUTA: CLIENTES ---
        elif categoria == "Clientes":
            if opcion == "Registrar": self.abrir_clientes_registrar()
            elif opcion == "Visualizar": self.abrir_clientes_visualizar()
            elif opcion == "Modificar": self.abrir_clientes_modificar()
            elif opcion == "Eliminar": self.abrir_clientes_eliminar()

    def placeholder_temporal(self, titulo):
        """BORRA ESTA FUNCION CUANDO TENGAS TUS VENTANAS LISTAS"""
        d = QDialog(self)
        d.setWindowTitle(titulo)
        l = QLabel(f"Aquí iría la ventana de:\n{titulo}", d)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        d.resize(300, 200)
        d.exec()

    # ---------------------------------------------------------
    # BOTONES PARA ABRIR VENTANAS
    # ---------------------------------------------------------

    # --- SECCIÓN CITAS ---
    def abrir_citas_agendar(self):
        self.agendar = AgendarCita()
        self.agendar.show()
        self.close()

    def abrir_citas_visualizar(self):
        self.visualizar = Visualizar()
        self.visualizar.show()
        self.close()

    def abrir_citas_modificar(self):
        self.placeholder_temporal("Modificar Cita") # <-- AQUI CONECTAS TU VENTANA

    def abrir_citas_eliminar(self):
        self.placeholder_temporal("Eliminar Cita") # <-- AQUI CONECTAS TU VENTANA


    # --- SECCIÓN MASCOTAS ---
    def abrir_mascotas_registrar(self):
        self.placeholder_temporal("Registrar Mascota") # <-- AQUI CONECTAS TU VENTANA

    def abrir_mascotas_visualizar(self):
        self.placeholder_temporal("Visualizar Mascotas") # <-- AQUI CONECTAS TU VENTANA

    def abrir_mascotas_modificar(self):
        self.placeholder_temporal("Modificar Mascota") # <-- AQUI CONECTAS TU VENTANA

    def abrir_mascotas_eliminar(self):
        self.placeholder_temporal("Eliminar Mascota") # <-- AQUI CONECTAS TU VENTANA


    # --- SECCIÓN CLIENTES ---
    def abrir_clientes_registrar(self):
        self.placeholder_temporal("Registrar Cliente") # <-- AQUI CONECTAS TU VENTANA

    def abrir_clientes_visualizar(self):
        self.placeholder_temporal("Visualizar Clientes") # <-- AQUI CONECTAS TU VENTANA

    def abrir_clientes_modificar(self):
        self.placeholder_temporal("Modificar Cliente") # <-- AQUI CONECTAS TU VENTANA

    def abrir_clientes_eliminar(self):
        self.placeholder_temporal("Eliminar Cliente") # <-- AQUI CONECTAS TU VENTANA

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())