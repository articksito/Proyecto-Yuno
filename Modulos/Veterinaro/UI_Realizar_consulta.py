import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QComboBox, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from UI_Revisar_consulta import *
from db_connection import Conexion

class VentanaConsulta(QMainWindow):
    def __init__(self, nombre_usuario):
        super().__init__()
        
        # 1. Inicializar conexión
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error BD: {e}")

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Sistema Veterinario Yuno - Nueva Consulta")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal (Horizontal)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS VISUALES ---
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
            /* Inputs Estilo Yuno (Rosados y translúcidos) */
            QLineEdit, QComboBox, QTextEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 16px;
                color: #333;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                background-color: rgba(241, 131, 227, 0.5);
            }
            QComboBox::drop-down { border: 0px; }
            
            /* Botones Menú Lateral (Acordeón) */
            QPushButton[class="menu-btn"] {
                text-align: left; padding-left: 20px; border: none; color: white;
                font-family: 'Segoe UI', sans-serif; font-size: 18px; font-weight: bold;
                background-color: transparent; height: 45px; border-radius: 10px;
            }
            QPushButton[class="menu-btn"]:hover { 
                background-color: rgba(255, 255, 255, 0.2); 
            }

            /* Sub-Botones (Desplegables) */
            QPushButton[class="sub-btn"] {
                text-align: left; padding-left: 40px; border: none; color: #EEE;
                font-family: 'Segoe UI', sans-serif; font-size: 15px;
                background-color: transparent; height: 35px; border-radius: 10px;
            }
            QPushButton[class="sub-btn"]:hover { 
                color: #333; background-color: rgba(255, 255, 255, 0.4); font-weight: bold;
            }

            /* Botón X */
            QPushButton#CloseBtn {
                background-color: #f0f0f0; border-radius: 20px;
                font-size: 20px; color: #666; border: none;
            }
            QPushButton#CloseBtn:hover { background-color: #ffcccc; color: #cc0000; }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

    # ============================================================
    #  BARRA LATERAL CON MENÚ DESPLEGABLE
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

        # --- GRUPOS ACORDEÓN ---
        # Aquí definimos las categorías y sus opciones
        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("""
            border: 2px solid white; color: white; border-radius: 15px; 
            padding: 10px; font-weight: bold; background: transparent;
        """)
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)

        self.main_layout.addWidget(self.sidebar)

    def setup_accordion_group(self, title, options):
        """Crea el botón principal y el área desplegable con sub-botones"""
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
            
            # CONEXIÓN AL ENRUTADOR (Router)
            # Usamos lambda para capturar qué botón fue presionado
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.router_ventanas(t, o))
            
            layout_options.addWidget(btn_sub)

        frame_options.hide() # Por defecto oculto
        self.sidebar_layout.addWidget(frame_options)
        
        # Conectar el clic del botón principal para mostrar/ocultar
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    # ============================================================
    #  ENRUTADOR DE VENTANAS (Navegación)
    # ============================================================
    def router_ventanas(self, categoria, opcion):
        print(f"Navegando desde Consulta a: {categoria} -> {opcion}")
        
        # Lógica de navegación. 
        # IMPORTANTE: Realiza los imports DENTRO de los if para evitar errores circulares.
        
        try:
            if categoria == "Consultas":
                if opcion == "Crear Consulta":
                    QMessageBox.information(self, "Sistema", "Ya te encuentras en 'Crear Consulta'.")
                
                elif opcion == "Ver Registro":
                    self.ventana = VentanaRevisarConsulta(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                    QMessageBox.information(self, "Navegación", "Ir a: Ver Registro de Consultas")

            elif categoria == "Recetas":
                if opcion == "Crear Receta":
                    from UI_Registrar_receta import VentanaReceta
                    self.ventana = VentanaReceta()
                    self.ventana.show()
                    self.close()
                    QMessageBox.information(self, "Navegación", "Ir a: Crear Receta")
                
                elif opcion == "Ver Registro":
                    from UI_Revisar_recetas import VentanaRevisarReceta
                    self.ventana = VentanaRevisarReceta()
                    self.ventana.show()
                    self.close()
                    QMessageBox.information(self, "Navegación", "Ir a: Ver Registro de Recetas")
        
        except Exception as e:
            QMessageBox.critical(self, "Error de Navegación", f"No se pudo abrir la ventana: {e}")

    # ============================================================
    #  PANEL CENTRAL (Formulario)
    # ============================================================
    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # --- HEADER ---
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Realizar Consulta")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_close = QPushButton("✕")
        btn_close.setObjectName("CloseBtn")
        btn_close.setFixedSize(40, 40)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.volver_al_menu)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close)
        self.white_layout.addLayout(header_layout)

        # Espaciador
        self.white_layout.addSpacing(20)

        # --- FORMULARIO GRID ---
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(30)
        grid.setContentsMargins(0, 0, 0, 0)

        lbl_style = "font-size: 20px; color: black; font-weight: 400;"
        input_height = "height: 45px;"

        # 1. ID Veterinario
        lbl_vet = QLabel("ID Veterinario:")
        lbl_vet.setStyleSheet(lbl_style)
        self.inp_vet = QLineEdit()
        self.inp_vet.setPlaceholderText("ID Médico")
        self.inp_vet.setStyleSheet(input_height)

        # 2. ID Mascota
        lbl_mascota = QLabel("ID Mascota:")
        lbl_mascota.setStyleSheet(lbl_style)
        self.inp_mascota = QLineEdit()
        self.inp_mascota.setPlaceholderText("ID Paciente")
        self.inp_mascota.setStyleSheet(input_height)

        # 3. Consultorio
        lbl_cons = QLabel("Consultorio:")
        lbl_cons.setStyleSheet(lbl_style)
        self.inp_cons = QComboBox()
        self.inp_cons.addItems(["Sala 1", "Sala 2", "Quirófano", "Triaje"])
        self.inp_cons.setEditable(True)
        self.inp_cons.setStyleSheet(input_height)

        # 4. Método Pago
        lbl_pago = QLabel("Método Pago:")
        lbl_pago.setStyleSheet(lbl_style)
        self.inp_pago = QComboBox()
        self.inp_pago.addItems(["Efectivo", "Tarjeta", "Transferencia", "Seguro"])
        self.inp_pago.setStyleSheet(input_height)

        # 5. ID Cita
        lbl_cita = QLabel("ID Cita (Opcional):")
        lbl_cita.setStyleSheet(lbl_style)
        self.inp_cita = QLineEdit()
        self.inp_cita.setPlaceholderText("ID Cita")
        self.inp_cita.setStyleSheet(input_height)

        # 6. Fecha (Solo lectura)
        lbl_fecha = QLabel("Fecha:")
        lbl_fecha.setStyleSheet(lbl_style)
        self.inp_fecha = QLineEdit()
        self.inp_fecha.setText(datetime.now().strftime("%Y-%m-%d"))
        self.inp_fecha.setReadOnly(True)
        self.inp_fecha.setStyleSheet(input_height + "background-color: rgba(200, 200, 200, 0.3);")

        # AGREGAR AL GRID
        grid.addWidget(lbl_vet, 0, 0)
        grid.addWidget(self.inp_vet, 0, 1)

        grid.addWidget(lbl_mascota, 1, 0)
        grid.addWidget(self.inp_mascota, 1, 1)

        grid.addWidget(lbl_cons, 2, 0)
        grid.addWidget(self.inp_cons, 2, 1)

        grid.addWidget(lbl_pago, 3, 0)
        grid.addWidget(self.inp_pago, 3, 1)

        grid.addWidget(lbl_cita, 4, 0)
        grid.addWidget(self.inp_cita, 4, 1)

        grid.addWidget(lbl_fecha, 5, 0)
        grid.addWidget(self.inp_fecha, 5, 1)

        self.white_layout.addWidget(form_widget)
        self.white_layout.addSpacing(20)

        # --- MOTIVO ---
        lbl_motivo = QLabel("Motivo de Consulta / Diagnóstico:")
        lbl_motivo.setStyleSheet(lbl_style)
        self.txt_motivo = QTextEdit()
        self.txt_motivo.setPlaceholderText("Escriba aquí los detalles de la consulta...")
        self.txt_motivo.setStyleSheet("border-radius: 15px; padding: 15px;")
        
        self.white_layout.addWidget(lbl_motivo)
        self.white_layout.addWidget(self.txt_motivo, stretch=1)

        self.white_layout.addSpacing(20)

        # --- BOTÓN GUARDAR ---
        btn_save = QPushButton("Guardar Consulta")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedSize(300, 60)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #b67cfc;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 30px;
            }
            QPushButton:hover { background-color: #a060e8; }
            QPushButton:pressed { background-color: #8a4cd0; }
        """)
        btn_save.clicked.connect(self.guardar_datos)

        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_save)
        btn_container.addStretch()
        
        self.white_layout.addLayout(btn_container)
        self.main_layout.addWidget(self.white_panel)

    # ============================================================
    #  LÓGICA
    # ============================================================
    def volver_al_menu(self):
        try:
            from UI_Veterinario import VeterinarioMenu 
            self.menu = VeterinarioMenu(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            print("UI_Veterinario_Menu no encontrado, cerrando ventana.")
            self.close()

    def guardar_datos(self):
        # 1. Obtener Datos
        consultorio = self.inp_cons.currentText()
        motivo = self.txt_motivo.toPlainText().strip()
        metodo_pago = self.inp_pago.currentText()
        id_vet_str = self.inp_vet.text().strip()
        id_mascota_str = self.inp_mascota.text().strip()
        id_cita_str = self.inp_cita.text().strip()

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")

        # 2. Validar
        if not motivo or not id_vet_str or not id_mascota_str:
            QMessageBox.warning(self, "Campos Vacíos", "ID Veterinario, ID Mascota y Motivo son obligatorios.")
            return

        try:
            fk_veterinario = int(id_vet_str)
            fk_mascota = int(id_mascota_str)
            fk_cita = int(id_cita_str) if id_cita_str else None
        except ValueError:
            QMessageBox.warning(self, "Error", "Los IDs deben ser numéricos.")
            return

        # 3. Insertar
        campos = ['consultorio', 'motivo', 'metodo_pago', 'fk_veterinario', 'fk_mascota', 'fecha', 'hora']
        datos = [consultorio, motivo, metodo_pago, fk_veterinario, fk_mascota, fecha_actual, hora_actual]

        if fk_cita is not None:
            campos.append('fk_cita')
            datos.append(fk_cita)

        try:
            self.conexion.insertar_datos('consulta', tuple(datos), tuple(campos))
            QMessageBox.information(self, "Éxito", "Consulta registrada correctamente.")
            self.txt_motivo.clear()
            self.inp_cita.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = VentanaConsulta("Mick")
    window.show()
    sys.exit(app.exec())