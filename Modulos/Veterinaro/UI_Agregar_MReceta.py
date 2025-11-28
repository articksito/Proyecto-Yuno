import sys
import os

# --- 1. CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Ajuste para subir niveles correctamente
if 'Veterinaro' in current_dir:
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
else:
    project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)
    
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from db_connection import Conexion

class VentanaAgregarMedicamento(QMainWindow):
    def __init__(self, nombre_usuario):
        super().__init__()
        self.nombre_usuario=nombre_usuario
        
        # Conexión solo para verificar (la inserción usa FuncinesVete)
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")
        self.setWindowTitle("Sistema Veterinario Yuno - Agregar Medicamento")
        self.resize(1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS VISUALES (Uniforme con el resto del sistema) ---
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
            
            /* Inputs del Formulario */
            QLineEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 16px;
                color: #333;
            }
            QLineEdit:focus {
                background-color: rgba(241, 131, 227, 0.5);
            }

            /* BOTONES MENU PRINCIPAL */
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

            /* SUB-BOTONES */
            QPushButton.sub-btn {
                text-align: left;
                padding-left: 40px;
                border-radius: 10px;
                color: #F0F0F0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: normal;
                background-color: rgba(0, 0, 0, 0.05);
                height: 35px;
                margin-bottom: 2px;
                margin-left: 10px;
                margin-right: 10px;
                border: none;
            }
            QPushButton.sub-btn:hover {
                color: white;
                background-color: rgba(255, 255, 255, 0.3);
                font-weight: bold;
            }
            
            /* Botón Logout */
            QPushButton.logout-btn {
                text-align: center; border: 2px solid white; 
                border-radius: 15px; padding: 10px; margin-top: 20px;
                font-size: 14px; color: white; font-weight: bold;
                background-color: transparent;
            }
            QPushButton.logout-btn:hover { background-color: rgba(255,255,255,0.2); }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

    # ============================================================
    #  SIDEBAR
    # ============================================================
    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # --- LOGO ROBUSTO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)

        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")

        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)
        
        # --- MENÚS DESPLEGABLES ---
        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro", "Agregar medicina a receta"])
        self.setup_accordion_group("Extra", ["Visualizar mascotas", "Visualizar medicamento", "Agregar notas para internar"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setProperty("class", "logout-btn")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)

        self.main_layout.addWidget(self.sidebar)

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
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.router_ventanas(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def router_ventanas(self, categoria, opcion):
        print(f"Navegando: {categoria} -> {opcion}")
        try:
            # --- CONSULTAS ---
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

            # --- RECETAS ---
            elif categoria == "Recetas":
                if opcion == "Crear Receta":
                    from UI_Registrar_receta import VentanaReceta
                    self.v = VentanaReceta(self.nombre_usuario)
                    self.v.show()
                    self.close()
                elif opcion == "Ver Registro":
                    from UI_Revisar_recetas import VentanaRevisarReceta
                    self.v = VentanaRevisarReceta(self.nombre_usuario)
                    self.v.show()
                    self.close()
                elif opcion == "Agregar medicina a receta":
                    QMessageBox.information(self, "Sistema", "Ya estás en Agregar Medicina.")

            # --- EXTRA ---
            elif categoria == "Extra":
                if opcion == "Visualizar mascotas":
                    from UI_RevisarMascota_Vete import VentanaRevisarMascota
                    self.v = VentanaRevisarMascota(self.nombre_usuario)
                    self.v.show()
                    self.close()
                elif opcion == "Visualizar medicamento":
                    from UI_RevisarMedicamento import VentanaRevisarMedicamento
                    self.ventana = VentanaRevisarMedicamento(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                
                elif opcion == "Agregar notas para internar":
                    QMessageBox.information(self, "Construcción", "Aquí iría Notas Internación.")

        except ImportError as e:
            QMessageBox.warning(self, "Error", f"Falta archivo: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")

    # ============================================================
    #  PANEL CENTRAL (FORMULARIO AGREGAR MEDICAMENTO)
    # ============================================================
    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Agregar Medicamento a Receta")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("✕")
        btn_back.setFixedSize(40, 40)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; border-radius: 20px; font-size: 20px; color: #666; border: none; }
            QPushButton:hover { background-color: #ffcccc; color: #cc0000; }
        """)
        btn_back.clicked.connect(self.volver_al_menu)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_back)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(30)

        # --- FORMULARIO ---
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(25)
        grid.setHorizontalSpacing(30)

        lbl_style = "font-size: 20px; color: black; font-weight: 400;"
        input_height = "height: 45px;"

        # 1. ID Receta
        lbl_receta = QLabel("ID Receta:")
        lbl_receta.setStyleSheet(lbl_style)
        self.inp_receta = QLineEdit()
        self.inp_receta.setPlaceholderText("ID de la Receta")
        self.inp_receta.setStyleSheet(input_height)

        # 2. ID Medicamento
        lbl_medicamento = QLabel("ID Medicamento:")
        lbl_medicamento.setStyleSheet(lbl_style)
        self.inp_medicamento = QLineEdit()
        self.inp_medicamento.setPlaceholderText("ID del Medicamento")
        self.inp_medicamento.setStyleSheet(input_height)

        # 3. Cantidad
        lbl_cantidad = QLabel("Cantidad:")
        lbl_cantidad.setStyleSheet(lbl_style)
        self.inp_cantidad = QLineEdit()
        self.inp_cantidad.setPlaceholderText("Ej: 2")
        self.inp_cantidad.setStyleSheet(input_height)

        # Layout
        grid.addWidget(lbl_receta, 0, 0)
        grid.addWidget(self.inp_receta, 0, 1)

        grid.addWidget(lbl_medicamento, 1, 0)
        grid.addWidget(self.inp_medicamento, 1, 1)

        grid.addWidget(lbl_cantidad, 2, 0)
        grid.addWidget(self.inp_cantidad, 2, 1)

        grid.setRowStretch(3, 1)

        self.white_layout.addWidget(form_widget)
        self.white_layout.addSpacing(20)

        # Botón Guardar
        btn_save = QPushButton("Agregar Medicamento")
        btn_save.setFixedSize(300, 60)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #b67cfc; color: white;
                font-size: 22px; font-weight: bold; border-radius: 30px;
            }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_save.clicked.connect(self.guardar_datos)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_save)
        btn_layout.addStretch()

        self.white_layout.addLayout(btn_layout)
        self.white_layout.addStretch()

        self.main_layout.addWidget(self.sidebar)
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
        id_receta_str = self.inp_receta.text().strip()
        id_med_str = self.inp_medicamento.text().strip()
        cantidad_str = self.inp_cantidad.text().strip()

        if not id_receta_str or not id_med_str or not cantidad_str:
            QMessageBox.warning(self, "Campos Vacíos", "Todos los campos son obligatorios.")
            return

        try:
            fk_receta = int(id_receta_str)
            fk_medicamento = int(id_med_str)
            cantidad = int(cantidad_str)
        except ValueError:
            QMessageBox.warning(self, "Error de Formato", "Los IDs y la Cantidad deben ser números enteros.")
            return

        # Insertar en tabla intermedia 'receta_medicamento'
        tabla = 'receta_medicamento' 
        # IMPORTANTE: Asegúrate que el orden coincida con el orden de las columnas en BD o especifica tupla
        # Según tu petición: fk_receta, fk_medicamento, cantidad
        campos = ('fk_receta', 'fk_medicamento', 'cantidad')
        datos = (fk_receta, fk_medicamento, cantidad)

        try:
            # Usando funciones_vete como pediste
            from funciones_vete import FuncinesVete
            
            # Instanciamos la clase (corrige el error de tu ejemplo donde faltaban parentesis)
            self.funcion = FuncinesVete()
            
            # Llamamos al método
            self.funcion.insertar_sindevolverId(tabla, datos, campos)
            
            QMessageBox.information(self, "Éxito", "Medicamento agregado a la receta correctamente.")
            
            # Limpiar campos para seguir agregando
            self.inp_medicamento.clear()
            self.inp_cantidad.clear()
            # self.inp_receta.clear() # Dejamos el ID receta para agilizar

        except Exception as e:
            msg = str(e)
            if "violates foreign key constraint" in msg:
                QMessageBox.warning(self, "Error de ID", "El ID de Receta o Medicamento no existe.")
            else:
                QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{msg}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = VentanaAgregarMedicamento()
    window.show()
    sys.exit(app.exec())