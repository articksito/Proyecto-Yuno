import sys
import os

# --- CONFIGURACIÓN DE RUTAS ---
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
from PyQt6.QtGui import QFont, QPixmap, QDoubleValidator

from db_conexionNew import Conexion

class VentanaAgregarUsuario(QMainWindow):
    def __init__(self, nombre_usuario="Admin"):
        super().__init__()
        
        # Conexión
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Sistema Veterinario Yuno - Agregar Usuario (Admin)")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
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
            
            /* --- INPUTS DEL FORMULARIO --- */
            QLineEdit, QComboBox {
                background-color: rgba(241, 131, 227, 0.15); 
                border: 1px solid rgba(241, 131, 227, 0.5);
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 16px;
                color: #333;
                height: 40px;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: rgba(241, 131, 227, 0.25);
                border: 2px solid #FC7CE2;
            }
            QComboBox::drop-down { border: 0px; }

            /* --- BOTONES DEL SIDEBAR (ADMIN) --- */
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
            QPushButton.logout-btn:hover { background-color: rgba(255, 255, 255, 0.2); }
            
            /* Labels de datos (Panel Derecho) */
            QLabel.label-key { font-size: 18px; color: #666; font-weight: normal; }
            QLabel.label-value { font-size: 22px; color: #000; font-weight: bold; padding-bottom: 5px; border-bottom: 1px solid #EEE; }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ============================================================
    #  SIDEBAR (ACTUALIZADO SEGÚN UI_ADMIN_main.py)
    # ============================================================
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
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")

        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # --- MENÚS DESPLEGABLES (IGUAL A MAIN) ---
        
        # Cita
        self.setup_accordion_group("Cita", ["Visualizar"])
        
        # Consulta
        self.setup_accordion_group("Consulta", ["Visualizar"])
        
        # Mascota (AHORA CON MODIFICAR)
        self.setup_accordion_group("Mascota", ["Visualizar", "Modificar"])
        
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
        btn_logout.setProperty("class", "logout-btn")
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
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.navegar(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    # ============================================================
    #  NAVEGACIÓN (LÓGICA ACTUALIZADA)
    # ============================================================
    def navegar(self, categoria, opcion):
        print(f"Admin navegando a: {categoria} -> {opcion}")
        
        # Evitar recargar la misma ventana
        if categoria == "Usuarios" and opcion == "Agregar":
             return

        try:
            # --- CITA ---
            if categoria == "Cita":
                if opcion == "Visualizar":
                    from UI_ADMIN_Revisar_cita import MainWindow as UI_Revisar_Cita
                    self.ventana = UI_Revisar_Cita(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

            # --- CONSULTA ---
            elif categoria == "Consulta":
                if opcion == "Visualizar":
                    from UI_ADMIN_Revisar_consulta import VentanaRevisarConsulta
                    self.ventana = VentanaRevisarConsulta(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

            # --- MASCOTA ---
            elif categoria == "Mascota":
                if opcion == "Visualizar":
                   from UI_ADMIN_Revisar_Paciente import MainWindow as revisar_mascota
                   self.ventana = revisar_mascota(self.nombre_usuario)
                   self.ventana.show()
                   self.close()
                elif opcion == "Modificar":
                   from UI_Admin_Modificar_Mascota import MainWindow as UI_Modificar_Mascota
                   self.ventana = UI_Modificar_Mascota(self.nombre_usuario)
                   self.ventana.show()
                   self.close()

            # --- CLIENTE ---
            elif categoria == "Cliente":
                if opcion == "Visualizar":
                    from UI_ADMIN_Visualizar_cliente import MainWindow as UI_Modificar_cliente
                    self.ventana = UI_Modificar_cliente(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

            # --- HOSPITALIZACION ---
            elif categoria == "Hospitalizacion":
                if opcion == "Visualizar":
                    from UI_ADMIN_RevisarHospitalizacion import VentanaRevisarHospitalizacion
                    self.ventana = VentanaRevisarHospitalizacion(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

            # --- MEDICAMENTOS ---
            elif categoria == "Medicamentos":
                if opcion == "Visualizar":
                    from UI_ADMIN_Revisar_medicina import VentanaRevisarMedicina
                    self.ventana = VentanaRevisarMedicina(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Agregar":
                    from UI_ADMIN_Agregar_medicina import MainWindow as AddMed
                    self.ventana = AddMed(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

            # --- USUARIOS ---
            elif categoria == "Usuarios":
                if opcion == "Agregar":
                    # Ya estamos aquí
                    pass
                elif opcion == "Modificar":
                    from UI_ADMIN_Modificar_usuario import VentanaModificarUsuario
                    self.ventana = VentanaModificarUsuario(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Visualizar":
                    from UI_ADMIN_Revisar_usuario import VentanaRevisarUsuario
                    self.ventana = VentanaRevisarUsuario(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

            # --- ESPECIALIDAD ---
            elif categoria == "Especialidad":
                if opcion == "Agregar":
                    from UI_ADMIN_Agregar_Especialidad import VentanaAgregarEspecialidad
                    self.ventana = VentanaAgregarEspecialidad(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_ADMIN_Modificar_especialidad import VentanaModificarEspecialidad
                    self.ventana = VentanaModificarEspecialidad(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

        except ImportError as e:
            QMessageBox.warning(self, "Error", f"No se encontró la ventana o archivo: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error general al navegar: {e}")

    # ============================================================
    #  PANEL CENTRAL (AGREGAR USUARIO)
    # ============================================================
    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Agregar Nuevo Usuario")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("✕")
        btn_back.setFixedSize(40, 40)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
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

        # Contenedor Dividido (Formulario | Preview)
        content_split = QHBoxLayout()
        content_split.setSpacing(40)

        # --- A. IZQUIERDA: FORMULARIO ---
        self.setup_form_left(content_split)

        # --- B. DERECHA: PREVIEW ---
        self.setup_info_right(content_split)

        self.white_layout.addLayout(content_split)
        self.white_layout.addSpacing(20)

        # Botón Guardar
        self.setup_save_button()
        self.white_layout.addStretch()

    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        label_style = "font-size: 16px; font-weight: 500; color: #444;"

        # Campos
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setPlaceholderText("Ej: Juan")
        
        self.inp_apellido = QLineEdit()
        self.inp_apellido.setPlaceholderText("Ej: Pérez")
        
        self.inp_correo = QLineEdit()
        self.inp_correo.setPlaceholderText("usuario@yuno.com")
        
        self.inp_telefono = QLineEdit()
        self.inp_telefono.setPlaceholderText("Solo números")
        # Validador para BigInt (solo números)
        self.inp_telefono.setValidator(QDoubleValidator()) 

        self.inp_pass = QLineEdit()
        self.inp_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.inp_pass.setPlaceholderText("********")

        # Combobox Roles
        self.inp_rol = QComboBox()
        self.inp_rol.addItems(["ADMIN", "VET", "REP", "ENF"])
        
        # Combobox Status
        self.inp_status = QComboBox()
        self.inp_status.addItems(["Activo", "Inactivo"])

        # Conectar señales para Live Preview
        self.inp_nombre.textChanged.connect(self.update_preview)
        self.inp_apellido.textChanged.connect(self.update_preview)
        self.inp_rol.currentTextChanged.connect(self.update_preview)
        self.inp_status.currentTextChanged.connect(self.update_preview)

        # Agregar al Grid
        # (Label, Row, Col)
        grid.addWidget(QLabel("Nombre:", styleSheet=label_style), 0, 0)
        grid.addWidget(self.inp_nombre, 0, 1)

        grid.addWidget(QLabel("Apellido:", styleSheet=label_style), 1, 0)
        grid.addWidget(self.inp_apellido, 1, 1)

        grid.addWidget(QLabel("Correo:", styleSheet=label_style), 2, 0)
        grid.addWidget(self.inp_correo, 2, 1)

        grid.addWidget(QLabel("Teléfono:", styleSheet=label_style), 3, 0)
        grid.addWidget(self.inp_telefono, 3, 1)

        grid.addWidget(QLabel("Contraseña:", styleSheet=label_style), 4, 0)
        grid.addWidget(self.inp_pass, 4, 1)

        grid.addWidget(QLabel("Rol:", styleSheet=label_style), 5, 0)
        grid.addWidget(self.inp_rol, 5, 1)

        grid.addWidget(QLabel("Estatus:", styleSheet=label_style), 6, 0)
        grid.addWidget(self.inp_status, 6, 1)

        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_right(self, parent_layout):
        board = QFrame()
        board.setFixedWidth(350)
        board.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 12px;
            }
        """)
        
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)

        # Header Board
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 rgba(252, 124, 226, 0.9));
            border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: none;
        """)
        head_lay = QHBoxLayout(header)
        lbl_tit = QLabel("Vista Previa")
        lbl_tit.setStyleSheet("color: white; font-weight: bold; font-size: 16px; border: none; background: transparent;")
        head_lay.addWidget(lbl_tit, alignment=Qt.AlignmentFlag.AlignCenter)
        board_lay.addWidget(header)

        # Contenido
        content = QWidget()
        content.setStyleSheet("background: white; border: none; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;")
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(20, 30, 20, 30)
        content_lay.setSpacing(10)
        content_lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Icono Usuario
        lbl_pic = QLabel("👤")
        lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_pic.setStyleSheet("font-size: 50px; background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        content_lay.addWidget(lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Datos Preview
        self.prev_nombre = QLabel("Nombre Usuario")
        self.prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_nombre.setWordWrap(True)
        self.prev_nombre.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.prev_rol = QLabel("ROL: --")
        self.prev_rol.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_rol.setStyleSheet("font-size: 16px; color: #555; font-weight: 600;")

        self.prev_status = QLabel("Inactivo")
        self.prev_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_status.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background: #999; padding: 5px 10px; border-radius: 15px; margin-top: 10px;")

        content_lay.addWidget(self.prev_nombre)
        content_lay.addWidget(self.prev_rol)
        content_lay.addWidget(self.prev_status)
        content_lay.addStretch()

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    def setup_save_button(self):
        container = QHBoxLayout()
        btn_save = QPushButton("Registrar Usuario")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedSize(250, 55)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #b67cfc; color: white; font-size: 20px; font-weight: bold; border-radius: 27px;
            }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_save.clicked.connect(self.guardar_datos)
        
        container.addStretch()
        container.addWidget(btn_save)
        container.addStretch()
        self.white_layout.addLayout(container)

    # ==========================================
    # --- LÓGICA ---
    # ==========================================

    def update_preview(self):
        nom = self.inp_nombre.text()
        ape = self.inp_apellido.text()
        rol = self.inp_rol.currentText()
        status = self.inp_status.currentText()

        # Nombre
        if nom or ape:
            self.prev_nombre.setText(f"{nom} {ape}")
        else:
            self.prev_nombre.setText("Nombre Usuario")
        
        # Rol
        self.prev_rol.setText(f"ROL: {rol}")

        # Status (Color)
        self.prev_status.setText(status)
        if status == "Activo":
            self.prev_status.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background: #4CAF50; padding: 5px 10px; border-radius: 15px; margin-top: 10px;")
        else:
            self.prev_status.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background: #F44336; padding: 5px 10px; border-radius: 15px; margin-top: 10px;")

    def volver_al_menu(self):
        try:
            from UI_ADMIN_main import MainWindow as AdminMenu 
            self.menu = AdminMenu(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            self.close()

    def guardar_datos(self):
        # 1. Recolectar
        nombre = self.inp_nombre.text().strip()
        apellido = self.inp_apellido.text().strip()
        correo = self.inp_correo.text().strip()
        tel_str = self.inp_telefono.text().strip()
        contra = self.inp_pass.text().strip()
        rol = self.inp_rol.currentText()
        status_txt = self.inp_status.currentText()
        # 2. Validar Campos Obligatorios
        if not nombre or not apellido or not contra or not rol:
            QMessageBox.warning(self, "Campos Vacíos", "Nombre, Apellido, Contraseña y Rol son obligatorios.")
            return
        # 3. Conversiones
        telefono = int(tel_str) if tel_str else None
        status_bool = True if status_txt == "Activo" else False
        # 4. Insertar
        campos = ('nombre', 'apellido', 'correo', 'telefono', 'contraseña', 'status', 'rol')
        datos = (nombre, apellido, correo, telefono, contra, status_bool, rol)
        tabla = 'usuario'

        try:
            nuevo_id = self.conexion.insertar_datos(tabla, datos, campos)
            
            if nuevo_id:
                QMessageBox.information(self, "Éxito", f"Usuario registrado correctamente.\nID Generado: {nuevo_id}")
                # Limpiar
                self.inp_nombre.clear()
                self.inp_apellido.clear()
                self.inp_correo.clear()
                self.inp_telefono.clear()
                self.inp_pass.clear()
                self.inp_rol.setCurrentIndex(0)
                self.inp_status.setCurrentIndex(0)
            else:
                 QMessageBox.warning(self, "Error", "No se pudo obtener el ID del nuevo usuario.")

        except Exception as e:
            QMessageBox.critical(self, "Error Base de Datos", f"Error al guardar:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = VentanaAgregarUsuario()
    window.show()
    sys.exit(app.exec())
