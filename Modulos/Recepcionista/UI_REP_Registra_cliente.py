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
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QIntValidator, QDoubleValidator

# Importar conexión
from db_connection import Conexion

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Registrar Cliente")
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

        # --- 1. BARRA LATERAL (Izquierda) ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO (Derecha - Registro Cliente) ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header con Título y Botón Cerrar
        header_layout = QHBoxLayout()
        
        lbl_header = QLabel("Registrar cliente")
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

        # Contenedor Horizontal para Formulario + Panel Info
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        # --- A. FORMULARIO DE REGISTRO (Izquierda) ---
        self.setup_register_form(content_layout)

        # --- B. PANEL DE INFORMACIÓN (Derecha) ---
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        
        # Espacio entre form y botón
        self.white_layout.addSpacing(30)
        
        # Botón Guardar
        self.setup_save_button()

        # --- ESPACIADOR INFERIOR (Centrado) ---
        self.white_layout.addStretch(2)

        # Agregar al layout principal
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_sidebar(self):
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
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                lbl_logo.setText("YUNO VET")
        else:
            lbl_logo.setText("YUNO VET")

        self.sidebar_layout.addWidget(lbl_logo)
        
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Modificar"])

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
            # Conexión de botones
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.abrir_ventana(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    # --- GESTOR DE VENTANAS ---
    def abrir_ventana(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        try:
            if categoria == "Citas":
                if opcion == "Agendar":
                    from UI_Crear_cita import MainWindow as Agendar_cita
                    self.ventana = Agendar_cita()
                    self.ventana.show()
                    self.close()
                elif opcion == "Visualizar":
                    from UI_Revisar_Cita import MainWindow as Visualizar_cita
                    self.ventana = Visualizar_cita()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_Modificar_cita import MainWindow as Modificar_cita
                    self.ventana = Modificar_cita()
                    self.ventana.show()
                    self.close()

            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    from UI_Registrar_mascota import MainWindow as Registrar_mascota
                    self.ventana = Registrar_mascota()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_Revisar_Mascota import MainWindow as Modificar_mascota
                    self.ventana = Modificar_mascota()
                    self.ventana.show()
                    self.close()

            elif categoria == "Clientes":
                if opcion == "Registrar":
                    pass # Ya estamos aquí
                elif opcion == "Modificar":
                    from UI_Modificar_cliente import MainWindow as Modificar_cliente
                    self.ventana = Modificar_cliente()
                    self.ventana.show()
                    self.close()
                    
        except ImportError as e:
            QMessageBox.warning(self, "Error de Navegación", f"No se pudo abrir la ventana solicitada.\nFalta el archivo: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al intentar abrir la ventana: {e}")

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def setup_register_form(self, parent_layout):
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        input_style = """
            QLineEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 18px;
                color: #333;
                height: 45px;
            }
        """
        label_style = "font-size: 24px; color: black; font-weight: 400;"

        # --- Campos ---
        
        # 1. Nombre
        lbl_nombre = QLabel("Nombre:")
        lbl_nombre.setStyleSheet(label_style)
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setPlaceholderText("Ej: Juan")
        self.inp_nombre.setStyleSheet(input_style)

        # 2. Apellido
        lbl_apellido = QLabel("Apellido:")
        lbl_apellido.setStyleSheet(label_style)
        self.inp_apellido = QLineEdit()
        self.inp_apellido.setPlaceholderText("Ej: Pérez")
        self.inp_apellido.setStyleSheet(input_style)

        # 3. Correo
        lbl_correo = QLabel("Correo:")
        lbl_correo.setStyleSheet(label_style)
        self.inp_correo = QLineEdit()
        self.inp_correo.setPlaceholderText("Ej: juan.perez@email.com")
        self.inp_correo.setStyleSheet(input_style)

        # --- SUBDIVISIÓN DE DIRECCIÓN ---
        # A. Calle
        lbl_calle = QLabel("Calle:")
        lbl_calle.setStyleSheet(label_style)
        self.inp_calle = QLineEdit()
        self.inp_calle.setPlaceholderText("Calle Principal")
        self.inp_calle.setStyleSheet(input_style)

        # B. Números (Exterior e Interior)
        lbl_numeros = QLabel("Num Ext / Int:")
        lbl_numeros.setStyleSheet(label_style)
        
        num_container = QWidget()
        num_layout = QHBoxLayout(num_container)
        num_layout.setContentsMargins(0,0,0,0)
        num_layout.setSpacing(10)
        
        self.inp_no_ext = QLineEdit()
        self.inp_no_ext.setPlaceholderText("Ext. #")
        self.inp_no_ext.setStyleSheet(input_style)
        
        self.inp_no_int = QLineEdit()
        self.inp_no_int.setPlaceholderText("Int. # (Opc)")
        self.inp_no_int.setStyleSheet(input_style)
        
        num_layout.addWidget(self.inp_no_ext)
        num_layout.addWidget(self.inp_no_int)

        # C. Colonia y CP
        lbl_colonia_cp = QLabel("Colonia / CP:")
        lbl_colonia_cp.setStyleSheet(label_style)
        
        col_cp_container = QWidget()
        col_cp_layout = QHBoxLayout(col_cp_container)
        col_cp_layout.setContentsMargins(0,0,0,0)
        col_cp_layout.setSpacing(10)
        
        self.inp_colonia = QLineEdit()
        self.inp_colonia.setPlaceholderText("Colonia")
        self.inp_colonia.setStyleSheet(input_style)
        
        self.inp_cp = QLineEdit()
        self.inp_cp.setPlaceholderText("C.P.")
        self.inp_cp.setFixedWidth(120) # CP más pequeño
        self.inp_cp.setStyleSheet(input_style)
        
        col_cp_layout.addWidget(self.inp_colonia)
        col_cp_layout.addWidget(self.inp_cp)

        # D. Ciudad
        lbl_ciudad = QLabel("Ciudad:")
        lbl_ciudad.setStyleSheet(label_style)
        self.inp_ciudad = QLineEdit()
        self.inp_ciudad.setText("Tijuana") # Valor por defecto
        self.inp_ciudad.setStyleSheet(input_style)

        # --- TELÉFONO ---
        lbl_telefono = QLabel("Teléfono:")
        lbl_telefono.setStyleSheet(label_style)
        self.inp_telefono = QLineEdit()
        self.inp_telefono.setPlaceholderText("Ej: 6641234567")
        self.inp_telefono.setStyleSheet(input_style)
        
        # Validador Double para permitir números grandes
        validator = QDoubleValidator() 
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setDecimals(0) # Sin decimales
        self.inp_telefono.setValidator(validator)

        # --- CONEXIÓN DE SEÑALES PARA PREVIEW ---
        self.inp_nombre.textChanged.connect(self.update_preview)
        self.inp_apellido.textChanged.connect(self.update_preview)
        self.inp_correo.textChanged.connect(self.update_preview)
        self.inp_telefono.textChanged.connect(self.update_preview)
        
        # Conectar campos de dirección
        self.inp_calle.textChanged.connect(self.update_preview)
        self.inp_no_ext.textChanged.connect(self.update_preview)
        self.inp_no_int.textChanged.connect(self.update_preview)
        self.inp_colonia.textChanged.connect(self.update_preview)
        self.inp_cp.textChanged.connect(self.update_preview)
        self.inp_ciudad.textChanged.connect(self.update_preview)

        # Añadir al Grid
        grid_layout.addWidget(lbl_nombre, 0, 0)
        grid_layout.addWidget(self.inp_nombre, 0, 1)

        grid_layout.addWidget(lbl_apellido, 1, 0)
        grid_layout.addWidget(self.inp_apellido, 1, 1)

        grid_layout.addWidget(lbl_correo, 2, 0)
        grid_layout.addWidget(self.inp_correo, 2, 1)

        grid_layout.addWidget(lbl_calle, 3, 0)
        grid_layout.addWidget(self.inp_calle, 3, 1)

        grid_layout.addWidget(lbl_numeros, 4, 0)
        grid_layout.addWidget(num_container, 4, 1)

        grid_layout.addWidget(lbl_colonia_cp, 5, 0)
        grid_layout.addWidget(col_cp_container, 5, 1)

        grid_layout.addWidget(lbl_ciudad, 6, 0)
        grid_layout.addWidget(self.inp_ciudad, 6, 1)

        grid_layout.addWidget(lbl_telefono, 7, 0)
        grid_layout.addWidget(self.inp_telefono, 7, 1)

        grid_layout.setRowStretch(8, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_board(self, parent_layout):
        # Panel derecho para información / vista previa
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

        # Contenido (Vista Previa en Tiempo Real)
        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Título de la sección
        lbl_preview = QLabel("Vista Previa")
        lbl_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_preview.setStyleSheet("color: #888; font-size: 14px; font-weight: bold; margin-bottom: 10px;")

        # Nombre Grande
        self.lbl_prev_nombre = QLabel("Nombre del Cliente")
        self.lbl_prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_nombre.setWordWrap(True)
        self.lbl_prev_nombre.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 15px;")

        # Detalles
        self.lbl_prev_contacto = QLabel("📞 ---")
        self.lbl_prev_contacto.setStyleSheet("font-size: 16px; color: #555; margin: 2px;")
        
        self.lbl_prev_email = QLabel("✉️ ---")
        self.lbl_prev_email.setStyleSheet("font-size: 16px; color: #555; margin: 2px;")
        
        self.lbl_prev_direccion = QLabel("🏠 ---")
        self.lbl_prev_direccion.setWordWrap(True)
        self.lbl_prev_direccion.setStyleSheet("font-size: 16px; color: #555; margin: 2px;")

        content_layout.addWidget(lbl_preview)
        content_layout.addWidget(self.lbl_prev_nombre)
        content_layout.addWidget(self.lbl_prev_contacto)
        content_layout.addWidget(self.lbl_prev_email)
        content_layout.addWidget(self.lbl_prev_direccion)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)

        parent_layout.addWidget(board_container, stretch=1)

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

    # --- FUNCIÓN DE ACTUALIZACIÓN EN TIEMPO REAL ---
    def update_preview(self):
        nombre = self.inp_nombre.text().strip()
        apellido = self.inp_apellido.text().strip()
        correo = self.inp_correo.text().strip()
        telefono = self.inp_telefono.text().strip()
        
        # Construir dirección completa
        calle = self.inp_calle.text().strip()
        ext = self.inp_no_ext.text().strip()
        inte = self.inp_no_int.text().strip()
        col = self.inp_colonia.text().strip()
        cp = self.inp_cp.text().strip()
        ciudad = self.inp_ciudad.text().strip()
        
        direccion_parts = []
        if calle: direccion_parts.append(calle)
        if ext: direccion_parts.append(f"#{ext}")
        if inte: direccion_parts.append(f"Int {inte}")
        if col: direccion_parts.append(f"Col. {col}")
        if cp: direccion_parts.append(f"CP {cp}")
        if ciudad: direccion_parts.append(ciudad)
        
        direccion_full = ", ".join(direccion_parts)

        # Actualizar Labels
        if nombre or apellido:
            self.lbl_prev_nombre.setText(f"{nombre} {apellido}")
        else:
            self.lbl_prev_nombre.setText("Nombre del Cliente")

        if telefono:
            self.lbl_prev_contacto.setText(f"📞 {telefono}")
        else:
            self.lbl_prev_contacto.setText("📞 ---")

        if correo:
            self.lbl_prev_email.setText(f"✉️ {correo}")
        else:
            self.lbl_prev_email.setText("✉️ ---")

        if direccion_full:
            self.lbl_prev_direccion.setText(f"🏠 {direccion_full}")
        else:
            self.lbl_prev_direccion.setText("🏠 ---")

    # --- LÓGICA DE GUARDADO ---
    def guardar_datos(self):
        # 1. Obtener datos
        nombre = self.inp_nombre.text().strip()
        apellido = self.inp_apellido.text().strip()
        correo = self.inp_correo.text().strip()
        telefono_str = self.inp_telefono.text().strip() # Se guarda como string temp
        
        # Construir dirección
        calle = self.inp_calle.text().strip()
        ext = self.inp_no_ext.text().strip()
        inte = self.inp_no_int.text().strip()
        col = self.inp_colonia.text().strip()
        cp = self.inp_cp.text().strip()
        ciudad = self.inp_ciudad.text().strip()
        
        # Unir dirección en una sola cadena para la BD (campo unico 'direccion')
        direccion_full = f"{calle} #{ext}"
        if inte: direccion_full += f" Int {inte}"
        direccion_full += f", Col. {col}, CP {cp}, {ciudad}"

        # 2. Validaciones
        if not nombre or not apellido or not telefono_str or not calle or not ext:
            QMessageBox.warning(self, "Campos vacíos", "Nombre, Apellido, Teléfono, Calle y Número Ext. son obligatorios.")
            return

        # 3. Conversión de Teléfono (BigInt)
        try:
            # Removemos posibles espacios o guiones si se colaron
            telefono_limpio = telefono_str.replace("-", "").replace(" ", "")
            telefono_num = int(telefono_limpio) # Convertir a INT para BigInt en BD
        except ValueError:
            QMessageBox.warning(self, "Error Teléfono", "El teléfono debe contener solo números.")
            return

        # 4. Insertar en BD
        datos = (nombre, apellido, direccion_full, correo, telefono_num)
        columnas = ('nombre', 'apellido', 'direccion', 'correo', 'telefono')
        table = 'cliente'

        try:
            nuevo_id = self.conexion1.insertar_datos(table, datos, columnas)
            QMessageBox.information(self, "Éxito", f"Cliente registrado correctamente.\nID Generado: {nuevo_id}")
            
            # Limpiar campos
            self.inp_nombre.clear()
            self.inp_apellido.clear()
            self.inp_correo.clear()
            self.inp_calle.clear()
            self.inp_no_ext.clear()
            self.inp_no_int.clear()
            self.inp_colonia.clear()
            self.inp_cp.clear()
            self.inp_telefono.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el cliente.\nError: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())