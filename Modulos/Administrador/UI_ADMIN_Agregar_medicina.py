import sys
import os

# --- CONFIGURACIÓN DE RUTAS PARA IMPORTACIONES ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap

# Importar conexión
from db_connection import Conexion

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Agregar Medicamento")
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

        # --- 1. BARRA LATERAL ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Agregar Tipo de Medicina")
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
        btn_close_view.clicked.connect(self.close)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close_view)

        self.white_layout.addLayout(header_layout)
        
        # --- ESPACIADOR SUPERIOR (Centrado) ---
        self.white_layout.addStretch(1)

        # Contenedor Formulario
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        self.setup_register_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        
        # Espacio
        self.white_layout.addSpacing(30)
        
        # Botón Guardar
        self.setup_save_button()

        # --- ESPACIADOR INFERIOR (Centrado) ---
        self.white_layout.addStretch(2)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

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
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")

        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # --- MENÚ LATERAL EXTENDIDO ---
        
        # Cita
        self.setup_accordion_group("Cita", ["Visualizar"])
        
        # Consulta
        self.setup_accordion_group("Consulta", ["Visualizar"])
        
        # Mascota
        self.setup_accordion_group("Mascota", ["Visualizar"])
        
        # Cliente
        self.setup_accordion_group("Cliente", ["Visualizar"])
        
        # Hospitalizacion
        self.setup_accordion_group("Hospitalizacion", ["Visualizar"])
        
        # Medicamentos
        self.setup_accordion_group("Medicamentos", ["Visualizar", "Agregar"])
        
        # Usuarios
        self.setup_accordion_group("Usuarios", ["Agregar", "Modificar", "Visualizar"])
        
        # Especialidad
        self.setup_accordion_group("Especialidad", ["Agregar", "Modificar"])


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
        layout_options.setSpacing(5)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            # Conexión al router
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

    # --- GESTOR DE VENTANAS ---
    def router_ventanas(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        try:
            # --- CITA ---
            if categoria == "Cita":
                if opcion == "Visualizar":
                    from UI_Revisar_Cita import MainWindow as CitasWindow
                    self.ventana = CitasWindow()
                    self.ventana.show()
                    self.close()

            # --- CONSULTA ---
            elif categoria == "Consulta":
                if opcion == "Visualizar":
                    # self.abrir_visualizar_consulta()
                    pass

            # --- MASCOTA ---
            elif categoria == "Mascota":
                if opcion == "Visualizar":
                   from UI_ADMIN_Paciente import MainWindow as UI_ADMIN_Paciente
                   self.apaciente = UI_ADMIN_Paciente()
                   self.apaciente.show()
                   self.close()

            # --- CLIENTE ---
            elif categoria == "Cliente":
                if opcion == "Visualizar":
                    from UI_Modificar_cliente import MainWindow as ClientesWindow
                    self.ventana = ClientesWindow()
                    self.ventana.show()
                    self.close()

            # --- HOSPITALIZACION ---
            elif categoria == "Hospitalizacion":
                if opcion == "Visualizar":
                    # self.abrir_hospitalizacion()
                    pass

            # --- MEDICAMENTOS ---
            elif categoria == "Medicamentos":
                if opcion == "Visualizar":
                    pass # Seria lista de medicamentos
                elif opcion == "Agregar":
                    pass # Ya estamos aquí

            # --- USUARIOS ---
            elif categoria == "Usuarios":
                if opcion == "Agregar":
                    # self.abrir_crear_usuario()
                    pass
                elif opcion == "Modificar":
                    # self.abrir_modificar_usuario()
                    pass
                elif opcion == "Visualizar":
                    # self.abrir_consultar_usuario()
                    pass

            # --- ESPECIALIDAD ---
            elif categoria == "Especialidad":
                if opcion == "Agregar":
                    # self.abrir_agregar_especialidad()
                    pass
                elif opcion == "Modificar":
                    # self.abrir_modificar_especialidad()
                    pass

        except ImportError as e:
            QMessageBox.warning(self, "Error de Navegación", f"No se pudo abrir la ventana solicitada.\nFalta el archivo: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al intentar abrir la ventana: {e}")

    def setup_register_form(self, parent_layout):
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Estilo de Inputs
        input_style = """
            QLineEdit, QComboBox {
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
        label_style = "font-size: 24px; color: black; font-weight: 400;"

        # --- Campos ---
        
        # 1. Nombre
        lbl_nombre = QLabel("Nombre:")
        lbl_nombre.setStyleSheet(label_style)
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setPlaceholderText("Ej: Amoxicilina")
        self.inp_nombre.setStyleSheet(input_style)

        # 2. Tipo
        lbl_tipo = QLabel("Tipo:")
        lbl_tipo.setStyleSheet(label_style)
        self.inp_tipo = QComboBox()
        self.inp_tipo.addItems(["Antibiótico", "Analgésico", "Antiinflamatorio", "Vacuna", "Desparasitante", "Otro"])
        self.inp_tipo.setStyleSheet(input_style)

        # 3. Composición
        lbl_comp = QLabel("Composición:")
        lbl_comp.setStyleSheet(label_style)
        self.inp_comp = QLineEdit()
        self.inp_comp.setPlaceholderText("Ej: 500mg")
        self.inp_comp.setStyleSheet(input_style)

        # 4. Dosis Recomendada
        lbl_dosis = QLabel("Dosis R.:")
        lbl_dosis.setStyleSheet(label_style)
        self.inp_dosis = QLineEdit()
        self.inp_dosis.setPlaceholderText("Ej: 10 mg/kg")
        self.inp_dosis.setStyleSheet(input_style)

        # 5. Vía de Administración
        lbl_via = QLabel("Vía de A.:")
        lbl_via.setStyleSheet(label_style)
        self.inp_via = QComboBox()
        self.inp_via.addItems(["Oral", "Intravenosa", "Intramuscular", "Subcutánea", "Tópica"])
        self.inp_via.setStyleSheet(input_style)

        # --- CONEXIÓN PARA VISTA PREVIA ---
        self.inp_nombre.textChanged.connect(self.update_preview)
        self.inp_tipo.currentTextChanged.connect(self.update_preview)
        self.inp_comp.textChanged.connect(self.update_preview)
        self.inp_dosis.textChanged.connect(self.update_preview)
        self.inp_via.currentTextChanged.connect(self.update_preview)

        # Añadir al Grid
        grid_layout.addWidget(lbl_nombre, 0, 0)
        grid_layout.addWidget(self.inp_nombre, 0, 1)

        grid_layout.addWidget(lbl_tipo, 1, 0)
        grid_layout.addWidget(self.inp_tipo, 1, 1)

        grid_layout.addWidget(lbl_comp, 2, 0)
        grid_layout.addWidget(self.inp_comp, 2, 1)

        grid_layout.addWidget(lbl_dosis, 3, 0)
        grid_layout.addWidget(self.inp_dosis, 3, 1)

        grid_layout.addWidget(lbl_via, 4, 0)
        grid_layout.addWidget(self.inp_via, 4, 1)

        grid_layout.setRowStretch(5, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_board(self, parent_layout):
        # Panel derecho
        board_container = QFrame()
        board_container.setFixedWidth(350)
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

        # Contenido (Vista Previa)
        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Título
        lbl_preview = QLabel("Ficha de Medicamento")
        lbl_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_preview.setStyleSheet("color: #888; font-size: 14px; font-weight: bold; margin-bottom: 10px;")

        # Nombre
        self.lbl_prev_nombre = QLabel("Nombre Medicina")
        self.lbl_prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_nombre.setWordWrap(True)
        self.lbl_prev_nombre.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")

        # Tipo y Comp
        self.lbl_prev_detalles = QLabel("Tipo | Composición")
        self.lbl_prev_detalles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_detalles.setStyleSheet("font-size: 16px; color: #555; margin-top: 5px;")

        # Dosis y Vía
        self.lbl_prev_uso = QLabel("Dosis -- | Vía --")
        self.lbl_prev_uso.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_uso.setStyleSheet("font-size: 14px; color: #888; margin-top: 5px;")

        content_layout.addWidget(lbl_preview)
        content_layout.addWidget(self.lbl_prev_nombre)
        content_layout.addWidget(self.lbl_prev_detalles)
        content_layout.addWidget(self.lbl_prev_uso)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)

        parent_layout.addWidget(board_container, stretch=1)

    # --- ACTUALIZACIÓN PREVIEW ---
    def update_preview(self):
        nombre = self.inp_nombre.text().strip()
        tipo = self.inp_tipo.currentText()
        comp = self.inp_comp.text().strip()
        dosis = self.inp_dosis.text().strip()
        via = self.inp_via.currentText()

        self.lbl_prev_nombre.setText(nombre if nombre else "Nombre Medicina")
        self.lbl_prev_detalles.setText(f"{tipo} | {comp if comp else '--'}")
        self.lbl_prev_uso.setText(f"{dosis if dosis else '--'} | {via}")

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
        
        btn_save.clicked.connect(self.guardar_datos)

        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_save)
        btn_container.addStretch()
        
        self.white_layout.addLayout(btn_container)

    # --- LÓGICA DE GUARDADO ---
    def guardar_datos(self):
        # 1. Obtener datos
        nombre = self.inp_nombre.text().strip()
        tipo = self.inp_tipo.currentText()
        composicion = self.inp_comp.text().strip()
        dosis_recomendada = self.inp_dosis.text().strip()
        via_administracion = self.inp_via.currentText()

        # 2. Validaciones
        if not nombre:
            QMessageBox.warning(self, "Campos vacíos", "El nombre del medicamento es obligatorio.")
            return

        # 3. Insertar en BD
        datos = (nombre, tipo, composicion, dosis_recomendada, via_administracion)
        # Asumiendo tabla 'medicamento' con estas columnas
        columnas = ('nombre', 'tipo', 'composicion', 'dosis_recomendada', 'via_administracion')
        table = 'medicamento'

        try:
            nuevo_id = self.conexion1.insertar_datos(table, datos, columnas)
            QMessageBox.information(self, "Éxito", f"Medicamento registrado correctamente.\nID Generado: {nuevo_id}")
            
            # Limpiar campos
            self.inp_nombre.clear()
            self.inp_comp.clear()
            self.inp_dosis.clear()
            self.inp_tipo.setCurrentIndex(0)
            self.inp_via.setCurrentIndex(0)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el medicamento.\nError: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())