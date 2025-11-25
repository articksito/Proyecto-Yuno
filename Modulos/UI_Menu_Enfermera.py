import sys
import os
# Aseguramos que Python busque módulos en la carpeta actual
sys.path.append(os.getcwd())

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QGridLayout, QMessageBox, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Veterinario Yuno - Panel de Enfermería")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES ---
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC);
            }
            QWidget#WhitePanel {
                background-color: white;
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                margin: 20px 20px 20px 0px; 
            }
            QWidget#Sidebar {
                background-color: transparent;
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                color: #333;
            }
            /* ESTILOS DEL MENÚ LATERAL */
            QPushButton.menu-btn {
                text-align: left;
                padding-left: 20px;
                border: none;
                background-color: transparent;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 24px;
                height: 50px;
                margin-top: 10px;
            }
            QPushButton.menu-btn:hover {
                color: #EEE;
            }
            QPushButton.sub-btn {
                text-align: left;
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px;
                font-weight: normal;
                padding-left: 40px;
                border: none;
                color: #F0F0F0;
                background-color: transparent;
                height: 35px;
            }
            QPushButton.sub-btn:hover {
                color: white;
                font-weight: bold;
            }
        """)

        # --- 1. BARRA LATERAL (Izquierda) ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO (Derecha - Contenido Principal) ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header con Botón de Salir
        header_layout = QHBoxLayout()
        header_layout.addStretch() # Empuja el botón a la derecha
        
        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.setStyleSheet("""
            QPushButton { background-color: #ff6b6b; color: white; border-radius: 15px; padding: 8px 15px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #ff5252; }
        """)
        btn_logout.clicked.connect(self.close)

        header_layout.addWidget(btn_logout)
        self.white_layout.addLayout(header_layout)

        # --- CONTENIDO CENTRAL (BIENVENIDA) ---
        self.white_layout.addStretch()
        
        lbl_welcome = QLabel("Bienvenido al Panel de Enfermería")
        lbl_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_welcome.setStyleSheet("font-size: 48px; font-weight: bold; color: #444;")
        self.white_layout.addWidget(lbl_welcome)

        lbl_instructions = QLabel("Seleccione una opción del menú lateral para comenzar.")
        lbl_instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_instructions.setStyleSheet("font-size: 24px; color: #777; margin-top: 10px;")
        self.white_layout.addWidget(lbl_instructions)

        self.white_layout.addStretch()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # LÓGICA DEL MENÚ LATERAL (SIDEBAR)
    # ==========================================
    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)
        
        # Logo o Título Superior
        lbl_logo = QLabel("YUNO VET")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lbl_logo.setStyleSheet("color: white; font-size: 32px; font-weight: bold; margin-bottom: 20px; margin-left: 10px;")
        self.sidebar_layout.addWidget(lbl_logo)

        # Grupos de Menú (Acordeón) - ACTUALIZADO CON TUS REQUISITOS
        self.setup_accordion_group("Citas", ["Visualizar"]) # Solo visualizar
        self.setup_accordion_group("Mascotas", ["Visualizar"]) # Solo visualizar
        # Clientes ELIMINADO por completo
        self.setup_accordion_group("Inventario", ["Farmacia", "Hospitalización"]) # Completo
        self.setup_accordion_group("Expediente", ["Diagnóstico"]) # Agregué Diagnóstico aquí para acceso rápido

        self.sidebar_layout.addStretch()

    def setup_accordion_group(self, title, options):
        # Botón Principal (Categoría)
        btn_main = QPushButton(title)
        btn_main.setProperty("class", "menu-btn")
        btn_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebar_layout.addWidget(btn_main)

        # Contenedor de Opciones (Oculto por defecto)
        frame_options = QFrame()
        layout_options = QVBoxLayout(frame_options)
        layout_options.setContentsMargins(10, 0, 0, 10)
        layout_options.setSpacing(2)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            # Conectar click del sub-botón
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.navegar_desde_sidebar(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide() # Empiezan ocultos
        self.sidebar_layout.addWidget(frame_options)
        
        # Funcionalidad de colapsar/expandir
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def navegar_desde_sidebar(self, categoria, opcion):
        """Redirige las opciones del sidebar a las funciones correspondientes"""
        print(f"Navegando Sidebar: {categoria} - {opcion}")
        
        # Mapeo de opciones del Sidebar a funciones
        if categoria == "Citas" and opcion == "Visualizar":
            self.abrir_citas()
        elif categoria == "Mascotas" and opcion == "Visualizar":
            self.abrir_pacientes()
        elif categoria == "Inventario" and opcion == "Farmacia":
            self.abrir_farmacia()
        elif categoria == "Inventario" and opcion == "Hospitalización":
            self.abrir_hospitalizacion()
        elif categoria == "Expediente" and opcion == "Diagnóstico":
            self.abrir_diagnostico()
        else:
            QMessageBox.warning(self, "Opción no vinculada", f"La opción '{opcion}' de '{categoria}' no tiene una función asignada aún.")

    # ==========================================
    # FUNCIONES DE APERTURA DE VENTANAS
    # ==========================================
    def abrir_citas(self):
        try:
            from UI_Revisar_Cita import MainWindow as VentanaCitas
            self.ventana_citas = VentanaCitas()
            self.ventana_citas.show()
        except Exception as e:
            self.mostrar_error("UI_Revisar_Cita.py", e)

    def abrir_pacientes(self):
        try:
            from UI_Revisar_Mascota import MainWindow as VentanaPacientes
            self.ventana_pacientes = VentanaPacientes()
            self.ventana_pacientes.show()
        except Exception as e:
            self.mostrar_error("UI_Revisar_Mascota.py", e)

    def abrir_diagnostico(self):
        try:
            from UI_Diagnostico import MainWindow as VentanaDiagnostico
            self.ventana_diag = VentanaDiagnostico()
            self.ventana_diag.show()
        except Exception as e:
            self.mostrar_error("UI_Diagnostico.py", e)

    def abrir_farmacia(self):
        try:
            from UI_Farmacia import MainWindow as VentanaFarmacia
            self.ventana_farmacia = VentanaFarmacia()
            self.ventana_farmacia.show()
        except Exception as e:
            self.mostrar_error("UI_Farmacia.py", e)

    def abrir_hospitalizacion(self):
        try:
            from UI_Hospitalizacion import MainWindow as VentanaHosp
            self.ventana_hosp = VentanaHosp()
            self.ventana_hosp.show()
        except Exception as e:
            self.mostrar_error("UI_Hospitalizacion.py", e)

    def mostrar_error(self, archivo, error):
        msg = f"Error al abrir {archivo}.\n\nDetalle: {error}"
        if isinstance(error, ImportError):
            msg += "\n\nPOSIBLES CAUSAS:\n1. El archivo no está en la misma carpeta.\n2. El nombre del archivo es diferente.\n3. Falta 'db_connection.py' en la carpeta."
        QMessageBox.critical(self, "Error de Módulo", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())