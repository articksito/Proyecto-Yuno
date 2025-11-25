import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QListWidget, 
                             QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from UI_Realizar_consulta import *
from UI_Revisar_consulta import *
from db_connection import Conexion 

class VeterinarioMenu(QMainWindow):
    def __init__(self, nombre_usuario):
        super().__init__()
        
        # 1. Base de Datos
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error BD: {e}")

        # 2. Datos del Usuario
        self.nombre_usuario = nombre_usuario
        self.user_data = {
            "nombre": f"{self.nombre_usuario}",
            "puesto": "Médico Veterinario",
            "id": "MED-001"
        }

        self.setWindowTitle("Sistema Veterinario Yuno - Panel Médico")
        self.resize(1366, 768)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS ACTUALIZADOS ---
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
            QLabel { font-family: 'Segoe UI', sans-serif; }
            
            /* ESTILO BOTÓN PRINCIPAL (ACORDEÓN) */
            QPushButton[class="menu-btn"] {
                text-align: left; padding-left: 20px; border: none; color: white;
                font-family: 'Segoe UI', sans-serif; font-size: 18px; font-weight: bold;
                background-color: transparent; height: 45px; border-radius: 10px;
            }
            QPushButton[class="menu-btn"]:hover { 
                background-color: rgba(255, 255, 255, 0.2); 
            }

            /* ESTILO SUB-BOTONES (DESPLEGABLES) */
            QPushButton[class="sub-btn"] {
                text-align: left; padding-left: 40px; border: none; color: #EEE;
                font-family: 'Segoe UI', sans-serif; font-size: 15px;
                background-color: transparent; height: 35px; border-radius: 10px;
            }
            QPushButton[class="sub-btn"]:hover { 
                color: #333; background-color: rgba(255, 255, 255, 0.4); font-weight: bold;
            }
            
            /* Botón Logout */
            QPushButton.logout-btn {
                border: 2px solid white; color: white; border-radius: 15px;
                padding: 10px; font-weight: bold; background: transparent;
            }
            QPushButton.logout-btn:hover { background-color: rgba(255, 255, 255, 0.1); }
            
            /* Lista */
            QListWidget {
                border: 1px solid #E0E0E0; border-radius: 10px;
                background-color: #F9F9F9; padding: 10px; font-size: 15px; color: #333;
            }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

    # ============================================================
    #  BARRA LATERAL CON ACORDEÓN
    # ============================================================
    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(280)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 40, 20, 40)
        self.sidebar_layout.setSpacing(5)

        lbl_logo = QLabel("YUNO VET\nMÉDICO")
        lbl_logo.setStyleSheet("color: white; font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(lbl_logo)

        # --- AQUI CREAMOS LOS GRUPOS DESPLEGABLES ---
        
        # Grupo 1: Consultas
        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        
        # Grupo 2: Recetas
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setProperty("class", "logout-btn")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)

        self.main_layout.addWidget(self.sidebar)

    def setup_accordion_group(self, title, options):
        """Crea un grupo de botones tipo acordeón"""
        btn_main = QPushButton(title)
        btn_main.setProperty("class", "menu-btn") # Estilo CSS
        btn_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebar_layout.addWidget(btn_main)

        frame_options = QFrame()
        layout_options = QVBoxLayout(frame_options)
        layout_options.setContentsMargins(0, 0, 0, 10)
        layout_options.setSpacing(2) 
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn") # Estilo CSS
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # CONEXIÓN AL ENRUTADOR
            # Usamos lambda para pasar los argumentos específicos
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.router_ventanas(t, o))
            
            layout_options.addWidget(btn_sub)

        frame_options.hide() # Empiezan ocultos
        self.sidebar_layout.addWidget(frame_options)
        
        # Lógica de mostrar/ocultar
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    # ============================================================
    #  ENRUTADOR (ROUTER) DE VENTANAS
    # ============================================================
    def router_ventanas(self, categoria, opcion):
        """
        Recibe la categoría (Consultas/Recetas) y la opción seleccionada.
        Aquí es donde abres tus clases nuevas.
        """
        print(f"Navegando a: {categoria} -> {opcion}")

        # --- LÓGICA DE CONSULTAS ---
        if categoria == "Consultas":
            if opcion == "Crear Consulta":
                self.ventana = VentanaConsulta()
                self.ventana.show()
                self.close()
                QMessageBox.information(self, "Sistema", "Abriendo: Crear Consulta")
                
            elif opcion == "Ver Registro":
                self.ventana = VentanaRevisarConsulta()
                self.ventana.show()
                self.close()
                QMessageBox.information(self, "Sistema", "Abriendo: Historial de Consultas")

        # --- LÓGICA DE RECETAS ---
        elif categoria == "Recetas":
            if opcion == "Crear Receta":
                # self.ventana = ClaseCrearReceta()
                # self.ventana.show()
                # self.close()
                QMessageBox.information(self, "Sistema", "Abriendo: Crear Receta")
                
            elif opcion == "Ver Registro":
                # self.ventana = ClaseVerRegistroRecetas()
                # self.ventana.show()
                # self.close()
                QMessageBox.information(self, "Sistema", "Abriendo: Historial de Recetas")

    # ============================================================
    #  PANEL CENTRAL (RELOJ + DB) - SIN CAMBIOS
    # ============================================================
    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        
        panel_layout = QHBoxLayout(self.white_panel)
        panel_layout.setContentsMargins(40, 40, 40, 40)
        panel_layout.setSpacing(40)

        # IZQUIERDA: Reloj
        left_container = QFrame()
        info_layout = QVBoxLayout(left_container)
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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        # DERECHA: Lista DB
        right_container = QFrame()
        list_layout = QVBoxLayout(right_container)
        list_layout.setContentsMargins(0, 0, 0, 0)

        lbl_info = QLabel("Pacientes en espera:")
        lbl_info.setStyleSheet("font-size: 18px; color: #666; font-weight: bold; margin-bottom: 10px;")
        list_layout.addWidget(lbl_info)

        self.lista_espera = QListWidget()
        try:
            datos_citas = self.conexion.Select_users('cita') 
            if datos_citas:
                citas_recientes = datos_citas[::-1][:15]

                for fila in citas_recientes:
                    paciente = fila[1]  
                    motivo = fila[2]    
                    hora = fila[3]      
                    self.lista_espera.addItem(f"{hora} - {paciente} ({motivo})")
            else:
                self.lista_espera.addItem("No hay citas pendientes.")
        except Exception as e:
            print(f"Error UI Citas: {e}")
            self.lista_espera.addItem("Sin conexión a Base de Datos.")

        list_layout.addWidget(self.lista_espera)

        panel_layout.addWidget(left_container, 60)
        panel_layout.addWidget(right_container, 40)

        self.main_layout.addWidget(self.white_panel)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.lbl_time.setText(current_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = VeterinarioMenu("jose")
    window.show()
    sys.exit(app.exec())