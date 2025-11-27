import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
sys.path.append(current_dir)

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout, QTextEdit, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from db_connection import Conexion

class VentanaReceta(QMainWindow):
    def __init__(self, nombre_usuario="Mick"):
        super().__init__()
        
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Sistema Veterinario Yuno - Nueva Receta")
        self.resize(1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS ---
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            QLineEdit, QTextEdit { background-color: rgba(241, 131, 227, 0.35); border: none; border-radius: 10px; padding: 5px 15px; font-size: 16px; color: #333; }
            QLineEdit:focus, QTextEdit:focus { background-color: rgba(241, 131, 227, 0.5); }
            QPushButton.menu-btn { text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; color: white; font-family: 'Segoe UI', sans-serif; font-weight: bold; font-size: 18px; background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px; }
            QPushButton.menu-btn:hover { background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; }
            QPushButton.sub-btn { text-align: left; padding-left: 40px; border-radius: 10px; color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05); height: 35px; margin-bottom: 2px; margin-left: 10px; margin-right: 10px; }
            QPushButton.sub-btn:hover { color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        lbl_logo = QLabel("YUNO VET\nMÉDICO")
        lbl_logo.setStyleSheet("color: white; font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(lbl_logo)
        
        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro"])

        self.sidebar_layout.addStretch()
        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("QPushButton { text-align: center; border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 20px; font-size: 14px; color: white; font-weight: bold; background-color: transparent; } QPushButton:hover { background-color: rgba(255,255,255,0.2); }")
        btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)
        self.main_layout.addWidget(self.sidebar)

    def setup_accordion_group(self, title, options):
        btn_main = QPushButton(title)
        btn_main.setProperty("class", "menu-btn")
        self.sidebar_layout.addWidget(btn_main)
        frame_options = QFrame()
        layout_options = QVBoxLayout(frame_options)
        layout_options.setContentsMargins(0, 0, 0, 10)
        layout_options.setSpacing(5)
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.router_ventanas(cat, opt))
            layout_options.addWidget(btn_sub)
        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def router_ventanas(self, categoria, opcion):
        print(f"Navegando: {categoria} -> {opcion}")
        try:
            if categoria == "Consultas":
                if opcion == "Crear Consulta":
                    from UI_Realizar_consulta import VentanaConsulta
                    self.v = VentanaConsulta(self.nombre_usuario)
                    self.v.show()
                    self.close()
                elif opcion == "Ver Registro":
                    from UI_Revisar_consulta import VentanaRevisarConsulta
                    self.v = VentanaRevisarConsulta(self.nombre_usuario)
                    self.v.show()
                    self.close()
            elif categoria == "Recetas":
                if opcion == "Crear Receta":
                    QMessageBox.information(self, "Sistema", "Ya estás creando una Receta.")
                elif opcion == "Ver Registro":
                    from UI_Revisar_recetas import VentanaRevisarReceta
                    self.v = VentanaRevisarReceta(self.nombre_usuario)
                    self.v.show()
                    self.close()
        except ImportError as e:
            QMessageBox.warning(self, "Error", f"No se encontró el archivo: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        header_layout = QHBoxLayout()
        lbl_header = QLabel("Generar Receta Médica")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(40, 40)
        btn_close.setStyleSheet("background-color: #f0f0f0; border-radius: 20px; font-size: 20px; color: #666; border: none;")
        btn_close.clicked.connect(self.volver_al_menu)
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close)
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(30)

        lbl_style = "font-size: 20px; color: black; font-weight: 400;"
        input_height = "height: 45px;"

        # --- AQUI ESTA LA CORRECCION ---
        # 1. ID Consulta (Ahora es obligatorio, es el único enlace)
        lbl_consulta = QLabel("ID Consulta:")
        lbl_consulta.setStyleSheet(lbl_style)
        self.inp_consulta = QLineEdit()
        self.inp_consulta.setPlaceholderText("ID de la Consulta Previa")
        self.inp_consulta.setStyleSheet(input_height)

        # 2. Fecha
        lbl_fecha = QLabel("Fecha Emisión:")
        lbl_fecha.setStyleSheet(lbl_style)
        self.inp_fecha = QLineEdit()
        self.inp_fecha.setText(datetime.now().strftime("%Y-%m-%d"))
        self.inp_fecha.setReadOnly(True)
        self.inp_fecha.setStyleSheet(input_height + "background-color: rgba(200, 200, 200, 0.3);")

        grid.addWidget(lbl_consulta, 0, 0)
        grid.addWidget(self.inp_consulta, 0, 1)
        grid.addWidget(lbl_fecha, 0, 2)
        grid.addWidget(self.inp_fecha, 0, 3)

        self.white_layout.addWidget(form_widget)
        self.white_layout.addSpacing(20)

        lbl_indicaciones = QLabel("Medicamentos e Indicaciones:")
        lbl_indicaciones.setStyleSheet(lbl_style)
        self.txt_indicaciones = QTextEdit()
        self.txt_indicaciones.setPlaceholderText("1. Medicamento X - Dosis - Frecuencia...")
        self.txt_indicaciones.setStyleSheet("border-radius: 15px; padding: 15px;")
        
        self.white_layout.addWidget(lbl_indicaciones)
        self.white_layout.addWidget(self.txt_indicaciones, stretch=1)
        self.white_layout.addSpacing(20)

        btn_save = QPushButton("Generar Receta")
        btn_save.setFixedSize(300, 60)
        btn_save.setStyleSheet("QPushButton { background-color: #b67cfc; color: white; font-size: 24px; font-weight: bold; border-radius: 30px; } QPushButton:hover { background-color: #a060e8; }")
        btn_save.clicked.connect(self.guardar_datos)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_save)
        btn_container.addStretch()
        self.white_layout.addLayout(btn_container)
        self.main_layout.addWidget(self.white_panel)

    def volver_al_menu(self):
        try:
            from UI_Veterinario import VeterinarioMenu 
            self.menu = VeterinarioMenu(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            self.close()

    def guardar_datos(self):
        indicaciones = self.txt_indicaciones.toPlainText().strip()
        id_consulta_str = self.inp_consulta.text().strip()
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        if not indicaciones or not id_consulta_str:
            QMessageBox.warning(self, "Campos Vacíos", "ID Consulta e Indicaciones son obligatorios.")
            return

        try:
            fk_consulta = int(id_consulta_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "El ID Consulta debe ser numérico.")
            return

        # INSERTAR EN RECETA (Solo fk_consulta, indicaciones, fecha)
        campos = ['indicaciones', 'fk_consulta', 'fecha']
        datos = [indicaciones, fk_consulta, fecha_actual]

        try:
            self.conexion.insertar_datos('receta', tuple(datos), tuple(campos))
            QMessageBox.information(self, "Éxito", "Receta generada correctamente.")
            self.txt_indicaciones.clear()
            self.inp_consulta.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaReceta()
    window.show()
    sys.exit(app.exec())