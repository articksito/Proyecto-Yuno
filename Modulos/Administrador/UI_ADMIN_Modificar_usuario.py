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
                             QGridLayout, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QDoubleValidator

from db_connection import Conexion

class VentanaModificarUsuario(QMainWindow):
    def __init__(self, nombre_usuario="Admin"):
        super().__init__()
        
        # Conexión BD
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Sistema Veterinario Yuno - Modificar Usuario (Admin)")
        self.resize(1280, 720)
        
        # Variable para controlar edición
        self.current_user_id = None

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES (Mismo tema Glass/Pink) ---
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
            
            /* --- MENÚ LATERAL --- */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px; color: white;
                font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF;
            }
            QPushButton.sub-btn {
                text-align: left; font-family: 'Segoe UI', sans-serif;
                font-size: 16px; font-weight: normal; padding-left: 40px;
                border-radius: 10px; color: #F0F0F0;
                background-color: rgba(0, 0, 0, 0.05); height: 35px;
                margin-bottom: 2px; margin-left: 10px; margin-right: 10px;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
            
            /* Botón Logout */
            QPushButton.logout-btn {
                text-align: center; border: 2px solid white; border-radius: 15px;
                padding: 10px; margin-top: 20px; font-size: 14px; color: white;
                font-weight: bold; background-color: transparent;
            }
            QPushButton.logout-btn:hover { background-color: rgba(255, 255, 255, 0.2); }

            /* --- INPUTS Y FORMULARIO --- */
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
                background-color: white;
                border: 2px solid #FC7CE2;
            }
            QComboBox::drop-down { border: 0px; }
        """)

        self.setup_sidebar()
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- SETUP SIDEBAR ---
    # ==========================================

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # Logo
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)

        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled)
            else:
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        
        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # Menús Admin
        self.setup_accordion_group("Cita", ["Visualizar"])
        self.setup_accordion_group("Consulta", ["Visualizar"])
        self.setup_accordion_group("Mascota", ["Visualizar"])
        self.setup_accordion_group("Cliente", ["Visualizar"])
        self.setup_accordion_group("Hospitalizacion", ["Visualizar"])
        self.setup_accordion_group("Medicamentos", ["Visualizar", "Agregar"])
        self.setup_accordion_group("Usuarios", ["Agregar", "Modificar", "Visualizar"])
        self.setup_accordion_group("Especialidad", ["Agregar", "Modificar"])

        self.sidebar_layout.addStretch()

        # Cerrar Sesión
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
        layout_options.setSpacing(5)
        
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

    def navegar(self, categoria, opcion):
        print(f"Admin navegando a: {categoria} -> {opcion}")
        
        if categoria == "Usuarios" and opcion == "Modificar":
             QMessageBox.information(self, "Sistema", "Ya te encuentras en Modificar Usuario.")
             return

        try:
            # Ejemplo de navegación básica
            if categoria == "Usuarios" and opcion == "Agregar":
                from UI_ADMIN_Agregar_usuario import VentanaAgregarUsuario
                self.ventana = VentanaAgregarUsuario()
                self.ventana.show()
                self.close()
            elif categoria == "Usuarios" and opcion == "Visualizar":
                from UI_ADMIN_Revisar_usuario import VentanaRevisarUsuario
                self.ventana = VentanaRevisarUsuario()
                self.ventana.show()
                self.close()
            # Agregar los demás imports aquí...
            else:
                 QMessageBox.information(self, "Navegación", f"Ir a: {categoria} - {opcion}")

        except ImportError as e:
            QMessageBox.warning(self, "Error", f"Falta archivo: {e.name}")

    # ==========================================
    # --- PANEL DERECHO (Modificar Usuario) ---
    # ==========================================

    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(40, 40, 20, 40)

        # 1. Header
        header = QHBoxLayout()
        lbl_header = QLabel("Modificar Usuario")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-size: 16px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #E0E0E0; color: #333; }
        """)
        btn_back.clicked.connect(self.close)

        header.addWidget(lbl_header)
        header.addStretch()
        header.addWidget(btn_back)
        self.white_layout.addLayout(header)
        self.white_layout.addSpacing(10)

        # 2. Barra de Búsqueda (ID Usuario)
        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        # 3. Contenedor Dividido
        content_split = QHBoxLayout()
        content_split.setSpacing(40)

        # A. Izquierda: Formulario Editable
        self.setup_form_left(content_split)

        # B. Derecha: Preview Info
        self.setup_info_right(content_split)

        self.white_layout.addLayout(content_split)
        
        # 4. Botón Guardar
        self.setup_save_button()
        self.white_layout.addStretch()

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_search = QLabel("ID Usuario:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        
        self.inp_search_id = QLineEdit()
        self.inp_search_id.setPlaceholderText("Ej: 1")
        self.inp_search_id.setFixedWidth(200)
        self.inp_search_id.setStyleSheet("background-color: white;")
        
        btn_search = QPushButton("Buscar")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setFixedSize(120, 40)
        btn_search.setStyleSheet("""
            QPushButton { background-color: #7CEBFC; color: #333; font-weight: bold; font-size: 16px; border-radius: 10px; border: 1px solid #5CD0E3; }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_search.clicked.connect(self.buscar_usuario)
        
        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.inp_search_id)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_container)

    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        label_style = "font-size: 16px; font-weight: 500; color: #444;"

        # Campos
        self.inp_nombre = QLineEdit()
        self.inp_apellido = QLineEdit()
        self.inp_correo = QLineEdit()
        
        self.inp_telefono = QLineEdit()
        self.inp_telefono.setValidator(QDoubleValidator()) # Solo números
        
        self.inp_pass = QLineEdit()
        # self.inp_pass.setEchoMode(QLineEdit.EchoMode.Password) # Opcional: si quieres verlo al editar o no
        self.inp_pass.setPlaceholderText("Nueva contraseña (Opcional)")

        self.inp_rol = QComboBox()
        self.inp_rol.addItems(["ADMIN", "VET", "REP", "ENF"])
        
        self.inp_status = QComboBox()
        self.inp_status.addItems(["Activo", "Inactivo"])

        # Conectar Preview
        self.inp_nombre.textChanged.connect(self.update_preview)
        self.inp_apellido.textChanged.connect(self.update_preview)
        self.inp_rol.currentTextChanged.connect(self.update_preview)
        self.inp_status.currentTextChanged.connect(self.update_preview)

        # Grid
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

        # Deshabilitar hasta buscar
        form_widget.setEnabled(False)
        self.form_widget = form_widget 

        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_right(self, parent_layout):
        board = QFrame()
        board.setObjectName("InfoBoard")
        board.setMaximumWidth(400)
        
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)
        
        # Estilo borde
        board.setStyleSheet("""
            QFrame#InfoBoard {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 12px;
            }
        """)

        # Header
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

        # Content
        content = QWidget()
        content.setStyleSheet("background: white; border: none; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;")
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(20, 30, 20, 30)
        content_lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        lbl_pic = QLabel("👤")
        lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_pic.setStyleSheet("font-size: 50px; background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        content_lay.addWidget(lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        self.prev_nombre = QLabel("Nombre Usuario")
        self.prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_nombre.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.prev_rol = QLabel("ROL: --")
        self.prev_rol.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_rol.setStyleSheet("font-size: 16px; color: #555; font-weight: 600;")

        self.prev_status = QLabel("---")
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
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_guardar.setFixedSize(250, 55)
        self.btn_guardar.setEnabled(False)
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #b67cfc; color: white; font-size: 20px; font-weight: bold; border-radius: 27px;
            }
            QPushButton:hover { background-color: #a060e8; }
            QPushButton:disabled { background-color: #cccccc; color: #666; }
        """)
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        
        container.addStretch()
        container.addWidget(self.btn_guardar)
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

        if nom or ape:
            self.prev_nombre.setText(f"{nom} {ape}")
        else:
            self.prev_nombre.setText("Nombre Usuario")
        
        self.prev_rol.setText(f"ROL: {rol}")
        self.prev_status.setText(status)
        
        if status == "Activo":
            self.prev_status.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background: #4CAF50; padding: 5px 10px; border-radius: 15px; margin-top: 10px;")
        else:
            self.prev_status.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background: #F44336; padding: 5px 10px; border-radius: 15px; margin-top: 10px;")

    def buscar_usuario(self):
        id_busqueda = self.inp_search_id.text().strip()
        if not id_busqueda.isdigit():
            QMessageBox.warning(self, "Error", "Ingresa un ID válido.")
            return

        print(f"Buscando usuario {id_busqueda}...")
        
        # Columnas a recuperar
        cols = ['nombre', 'apellido', 'correo', 'telefono', 'contraseña', 'status', 'rol']
        
        datos = self.conexion.consultar_registro(
            tabla='usuario',
            id_columna='id_usuario',
            id_valor=id_busqueda,
            columnas=cols
        )
        
        if datos:
            # datos = (nombre, apellido, correo, telefono, contraseña, status, rol)
            self.current_user_id = id_busqueda
            
            self.inp_nombre.setText(str(datos[0]))
            self.inp_apellido.setText(str(datos[1]))
            self.inp_correo.setText(str(datos[2]))
            self.inp_telefono.setText(str(datos[3]))
            self.inp_pass.setText(str(datos[4]))
            
            status_bool = datos[5]
            self.inp_status.setCurrentText("Activo" if status_bool else "Inactivo")
            
            rol_db = str(datos[6])
            idx = self.inp_rol.findText(rol_db, Qt.MatchFlag.MatchFixedString)
            if idx >= 0: self.inp_rol.setCurrentIndex(idx)

            # Habilitar
            self.form_widget.setEnabled(True)
            self.btn_guardar.setEnabled(True)
            self.update_preview()
            
            QMessageBox.information(self, "Éxito", "Usuario encontrado.")
        else:
            QMessageBox.warning(self, "No encontrado", "No existe usuario con ese ID.")
            self.form_widget.setEnabled(False)
            self.btn_guardar.setEnabled(False)
            self.current_user_id = None
            self.limpiar_form()

    def guardar_cambios(self):
        if not self.current_user_id: return

        # Recolectar
        nombre = self.inp_nombre.text().strip()
        apellido = self.inp_apellido.text().strip()
        correo = self.inp_correo.text().strip()
        telefono = self.inp_telefono.text().strip()
        contra = self.inp_pass.text().strip()
        rol = self.inp_rol.currentText()
        status_txt = self.inp_status.currentText()
        
        status_bool = True if status_txt == "Activo" else False

        # Validar
        if not nombre or not apellido or not contra:
            QMessageBox.warning(self, "Error", "Nombre, Apellido y Contraseña son obligatorios.")
            return

        # Diccionario para update
        datos_nuevos = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "telefono": int(telefono) if telefono else None,
            "contraseña": contra,
            "rol": rol,
            "status": status_bool
        }

        # Actualizar
        try:
            exito = self.conexion.editar_registro(
                id=int(self.current_user_id),
                datos=datos_nuevos,
                tabla='usuario',
                id_columna='id_usuario'
            )
            
            if exito:
                QMessageBox.information(self, "Guardado", "Usuario modificado correctamente.")
                self.form_widget.setEnabled(False)
                self.btn_guardar.setEnabled(False)
                self.inp_search_id.clear()
                self.limpiar_form()
            else:
                QMessageBox.critical(self, "Error", "No se pudo guardar en la base de datos.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"{e}")

    def limpiar_form(self):
        self.inp_nombre.clear()
        self.inp_apellido.clear()
        self.inp_correo.clear()
        self.inp_telefono.clear()
        self.inp_pass.clear()
        self.prev_nombre.setText("Nombre Usuario")
        self.prev_rol.setText("ROL: --")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = VentanaModificarUsuario()
    window.show()
    sys.exit(app.exec())