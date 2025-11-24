import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QIntValidator

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
            QLabel#Logo {
                color: white; 
                font-size: 36px; 
                font-weight: bold; 
                margin-bottom: 30px;
            }
            QPushButton.menu-btn {
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
            QPushButton.menu-btn:hover {
                color: #E0E0E0;
                background-color: rgba(255, 255, 255, 0.1);
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
            QPushButton.sub-btn {
                text-align: left;
                border: none;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: normal;
                padding-left: 50px;
                color: #F0F0F0;
                background-color: transparent;
                height: 30px;
            }
            QPushButton.sub-btn:hover {
                color: #333;
                background-color: rgba(255, 255, 255, 0.2);
                font-weight: bold;
            }
        """)

        self.setup_sidebar()

        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
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
        self.white_layout.addSpacing(20)

        # Contenedor Formulario
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        self.setup_register_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        
        self.setup_save_button()
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        # --- LOGO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ruta_logo = "logo.png" 
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
        layout_options.setSpacing(2)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # CONEXIÓN DE BOTONES
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
                    from UI_Revisar_cliente import MainWindow as Modficiar_dueno
                    self.ventana = Modficiar_dueno()
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
        
        # Estilo centrado para los campos pequeños de teléfono
        small_input_style = """
            QLineEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none;
                border-radius: 10px;
                padding: 5px;
                font-size: 18px;
                color: #333;
                height: 45px;
            }
        """
        label_style = "font-size: 24px; color: black; font-weight: 400;"

        # --- Campos ---
        
        lbl_nombre = QLabel("Nombre:")
        lbl_nombre.setStyleSheet(label_style)
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setPlaceholderText("Ej: Juan")
        self.inp_nombre.setStyleSheet(input_style)

        lbl_apellido = QLabel("Apellido:")
        lbl_apellido.setStyleSheet(label_style)
        self.inp_apellido = QLineEdit()
        self.inp_apellido.setPlaceholderText("Ej: Pérez")
        self.inp_apellido.setStyleSheet(input_style)

        lbl_correo = QLabel("Correo:")
        lbl_correo.setStyleSheet(label_style)
        self.inp_correo = QLineEdit()
        self.inp_correo.setPlaceholderText("Ej: juan.perez@email.com")
        self.inp_correo.setStyleSheet(input_style)

        lbl_direccion = QLabel("Dirección:")
        lbl_direccion.setStyleSheet(label_style)
        self.inp_direccion = QLineEdit()
        self.inp_direccion.setPlaceholderText("Ej: Av. Principal #123")
        self.inp_direccion.setStyleSheet(input_style)

        # --- SECCIÓN TELÉFONO DIVIDIDA (000-000-00-00) ---
        lbl_telefono = QLabel("Teléfono:")
        lbl_telefono.setStyleSheet(label_style)
        
        # Contenedor para los inputs
        phone_widget = QWidget()
        phone_layout = QHBoxLayout(phone_widget)
        phone_layout.setContentsMargins(0, 0, 0, 0)
        phone_layout.setSpacing(5)

        # Validador para solo permitir números
        int_validator = QIntValidator()

        # Input 1: 3 dígitos
        self.inp_tel1 = QLineEdit()
        self.inp_tel1.setPlaceholderText("000")
        self.inp_tel1.setMaxLength(3)
        self.inp_tel1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inp_tel1.setValidator(int_validator)
        self.inp_tel1.setStyleSheet(small_input_style)

        # Input 2: 3 dígitos
        self.inp_tel2 = QLineEdit()
        self.inp_tel2.setPlaceholderText("000")
        self.inp_tel2.setMaxLength(3)
        self.inp_tel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inp_tel2.setValidator(int_validator)
        self.inp_tel2.setStyleSheet(small_input_style)

        # Input 3: 2 dígitos
        self.inp_tel3 = QLineEdit()
        self.inp_tel3.setPlaceholderText("00")
        self.inp_tel3.setMaxLength(2)
        self.inp_tel3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inp_tel3.setValidator(int_validator)
        self.inp_tel3.setStyleSheet(small_input_style)

        # Input 4: 2 dígitos
        self.inp_tel4 = QLineEdit()
        self.inp_tel4.setPlaceholderText("00")
        self.inp_tel4.setMaxLength(2)
        self.inp_tel4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inp_tel4.setValidator(int_validator)
        self.inp_tel4.setStyleSheet(small_input_style)

        # Guiones
        dash_style = "font-size: 24px; font-weight: bold; color: #555;"
        dash1 = QLabel("-")
        dash1.setStyleSheet(dash_style)
        dash2 = QLabel("-")
        dash2.setStyleSheet(dash_style)
        dash3 = QLabel("-")
        dash3.setStyleSheet(dash_style)

        # Agregar al layout horizontal
        phone_layout.addWidget(self.inp_tel1)
        phone_layout.addWidget(dash1)
        phone_layout.addWidget(self.inp_tel2)
        phone_layout.addWidget(dash2)
        phone_layout.addWidget(self.inp_tel3)
        phone_layout.addWidget(dash3)
        phone_layout.addWidget(self.inp_tel4)

        # --- CONEXIÓN DE SEÑALES PARA PREVIEW ---
        self.inp_nombre.textChanged.connect(self.update_preview)
        self.inp_apellido.textChanged.connect(self.update_preview)
        self.inp_correo.textChanged.connect(self.update_preview)
        self.inp_direccion.textChanged.connect(self.update_preview)
        
        # Conectamos las 4 partes del teléfono
        self.inp_tel1.textChanged.connect(self.update_preview)
        self.inp_tel2.textChanged.connect(self.update_preview)
        self.inp_tel3.textChanged.connect(self.update_preview)
        self.inp_tel4.textChanged.connect(self.update_preview)

        # Añadir al Grid
        grid_layout.addWidget(lbl_nombre, 0, 0)
        grid_layout.addWidget(self.inp_nombre, 0, 1)

        grid_layout.addWidget(lbl_apellido, 1, 0)
        grid_layout.addWidget(self.inp_apellido, 1, 1)

        grid_layout.addWidget(lbl_correo, 2, 0)
        grid_layout.addWidget(self.inp_correo, 2, 1)

        grid_layout.addWidget(lbl_direccion, 3, 0)
        grid_layout.addWidget(self.inp_direccion, 3, 1)

        grid_layout.addWidget(lbl_telefono, 4, 0)
        grid_layout.addWidget(phone_widget, 4, 1) # Agregamos el contenedor

        grid_layout.setRowStretch(5, 1)
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

    # --- FUNCIÓN DE ACTUALIZACIÓN EN TIEMPO REAL ---
    def update_preview(self):
        nombre = self.inp_nombre.text().strip()
        apellido = self.inp_apellido.text().strip()
        correo = self.inp_correo.text().strip()
        direccion = self.inp_direccion.text().strip()
        
        # Construir teléfono
        t1 = self.inp_tel1.text()
        t2 = self.inp_tel2.text()
        t3 = self.inp_tel3.text()
        t4 = self.inp_tel4.text()
        
        telefono = ""
        if t1 or t2 or t3 or t4:
            telefono = f"{t1}-{t2}-{t3}-{t4}"

        # Actualizar Nombre Completo
        if nombre or apellido:
            self.lbl_prev_nombre.setText(f"{nombre} {apellido}")
        else:
            self.lbl_prev_nombre.setText("Nombre del Cliente")

        # Actualizar Teléfono
        if telefono:
            self.lbl_prev_contacto.setText(f"📞 {telefono}")
        else:
            self.lbl_prev_contacto.setText("📞 ---")

        # Actualizar Correo
        if correo:
            self.lbl_prev_email.setText(f"✉️ {correo}")
        else:
            self.lbl_prev_email.setText("✉️ ---")

        # Actualizar Dirección
        if direccion:
            self.lbl_prev_direccion.setText(f"🏠 {direccion}")
        else:
            self.lbl_prev_direccion.setText("🏠 ---")

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
        apellido = self.inp_apellido.text().strip()
        correo = self.inp_correo.text().strip()
        direccion = self.inp_direccion.text().strip()
        
        t1 = self.inp_tel1.text().strip()
        t2 = self.inp_tel2.text().strip()
        t3 = self.inp_tel3.text().strip()
        t4 = self.inp_tel4.text().strip()
        
        telefono = f"{t1}-{t2}-{t3}-{t4}"

        # 2. Validaciones (Básica: que haya algo escrito en tel)
        if not nombre or not apellido or len(telefono) < 10: 
            QMessageBox.warning(self, "Datos incompletos", "Por favor complete Nombre, Apellido y un Teléfono válido.")
            return

        # 3. Insertar en BD
        datos = (nombre, apellido, correo, direccion, telefono)
        columnas = ('nombre', 'apellido', 'correo', 'direccion', 'telefono')
        table = 'cliente'

        try:
            nuevo_id = self.conexion1.insertar_datos(table, datos, columnas)
            QMessageBox.information(self, "Éxito", f"Cliente registrado correctamente.\nID Generado: {nuevo_id}")
            
            # Limpiar campos
            self.inp_nombre.clear()
            self.inp_apellido.clear()
            self.inp_correo.clear()
            self.inp_direccion.clear()
            self.inp_tel1.clear()
            self.inp_tel2.clear()
            self.inp_tel3.clear()
            self.inp_tel4.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el cliente.\nError: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())