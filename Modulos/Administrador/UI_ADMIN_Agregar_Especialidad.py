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
                             QGridLayout, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from db_connection import Conexion

class VentanaAgregarEspecialidad(QMainWindow):
    def __init__(self, nombre_usuario="Admin"):
        super().__init__()
        
        # Conexión
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Sistema Veterinario Yuno - Agregar Especialidad (Admin)")
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
            QLineEdit, QTextEdit {
                background-color: rgba(241, 131, 227, 0.15); 
                border: 1px solid rgba(241, 131, 227, 0.5);
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 16px;
                color: #333;
            }
            QLineEdit:focus, QTextEdit:focus {
                background-color: rgba(241, 131, 227, 0.25);
                border: 2px solid #FC7CE2;
            }
            
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
    #  SIDEBAR (ADMIN COMPLETO)
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

        # --- MENÚS DESPLEGABLES (ADMIN) ---
        self.setup_accordion_group("Cita", ["Visualizar"])
        self.setup_accordion_group("Consulta", ["Visualizar"])
        self.setup_accordion_group("Mascota", ["Visualizar"])
        self.setup_accordion_group("Cliente", ["Visualizar"])
        self.setup_accordion_group("Hospitalizacion", ["Visualizar"])
        self.setup_accordion_group("Medicamentos", ["Visualizar", "Agregar"])
        self.setup_accordion_group("Usuarios", ["Agregar", "Modificar", "Visualizar"])
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
            # Conexión al navegador
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
        
        if categoria == "Especialidad" and opcion == "Agregar":
             QMessageBox.information(self, "Sistema", "Ya te encuentras en Agregar Especialidad.")
             return

        try:
            # Ejemplo de navegación básica
            if categoria == "Usuarios" and opcion == "Agregar":
                from UI_ADMIN_Agregar_usuario import VentanaAgregarUsuario
                self.ventana = VentanaAgregarUsuario()
                self.ventana.show()
                self.close()
            elif categoria == "Usuarios" and opcion == "Modificar":
                from UI_ADMIN_Modificar_usuario import VentanaModificarUsuario
                self.ventana = VentanaModificarUsuario()
                self.ventana.show()
                self.close()
            # Agregar los demás imports aquí...
            else:
                 QMessageBox.information(self, "Navegación", f"Ir a: {categoria} - {opcion}")

        except ImportError as e:
            QMessageBox.warning(self, "Error", f"Falta archivo: {e.name}")

    # ==========================================
    # --- PANEL DERECHO (Agregar Especialidad) ---
    # ==========================================

    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # 1. Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Agregar Especialidad")
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
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        label_style = "font-size: 16px; font-weight: 500; color: #444;"

        # Campos
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setPlaceholderText("Ej: Cardiología")
        self.inp_nombre.setMaxLength(24)
        
        self.inp_descripcion = QTextEdit()
        self.inp_descripcion.setPlaceholderText("Descripción de la especialidad...")
        self.inp_descripcion.setFixedHeight(100) # Altura fija para el área de texto

        # Conectar señales para Live Preview
        self.inp_nombre.textChanged.connect(self.update_preview)
        self.inp_descripcion.textChanged.connect(self.update_preview)

        # Agregar al Grid
        # (Label, Row, Col)
        grid.addWidget(QLabel("Nombre:", styleSheet=label_style), 0, 0)
        grid.addWidget(self.inp_nombre, 0, 1)

        grid.addWidget(QLabel("Descripción:", styleSheet=label_style), 1, 0, Qt.AlignmentFlag.AlignTop) # Alinear label arriba
        grid.addWidget(self.inp_descripcion, 1, 1)

        # Empujar hacia arriba
        grid.setRowStretch(2, 1)

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

        # Icono Especialidad
        lbl_pic = QLabel("🩺")
        lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_pic.setStyleSheet("font-size: 50px; background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        content_lay.addWidget(lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Datos Preview
        self.prev_nombre = QLabel("Nombre Especialidad")
        self.prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_nombre.setWordWrap(True)
        self.prev_nombre.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.prev_desc = QLabel("Descripción: --")
        self.prev_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_desc.setWordWrap(True)
        self.prev_desc.setStyleSheet("font-size: 16px; color: #555; margin-top: 10px;")

        content_lay.addWidget(self.prev_nombre)
        content_lay.addWidget(self.prev_desc)
        content_lay.addStretch()

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    def setup_save_button(self):
        container = QHBoxLayout()
        btn_save = QPushButton("Registrar Especialidad")
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
        desc = self.inp_descripcion.toPlainText()

        if nom:
            self.prev_nombre.setText(nom)
        else:
            self.prev_nombre.setText("Nombre Especialidad")
        
        if desc:
            # Truncar descripción si es muy larga para la preview
            if len(desc) > 50:
                self.prev_desc.setText(f"Descripción: {desc[:50]}...")
            else:
                self.prev_desc.setText(f"Descripción: {desc}")
        else:
            self.prev_desc.setText("Descripción: --")

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
        descripcion = self.inp_descripcion.toPlainText().strip()

        # 2. Validar Campos Obligatorios
        if not nombre:
            QMessageBox.warning(self, "Campos Vacíos", "El nombre de la especialidad es obligatorio.")
            return

        # 3. Insertar
        # Columnas: nombre, descripcion
        campos = ('nombre', 'descripcion')
        datos = (nombre, descripcion)
        tabla = 'especialidad'

        try:
            nuevo_id = self.conexion.insertar_datos(tabla, datos, campos)
            
            if nuevo_id:
                QMessageBox.information(self, "Éxito", f"Especialidad registrada correctamente.\nID Generado: {nuevo_id}")
                # Limpiar
                self.inp_nombre.clear()
                self.inp_descripcion.clear()
            else:
                 QMessageBox.warning(self, "Error", "No se pudo obtener el ID de la nueva especialidad.")

        except Exception as e:
            QMessageBox.critical(self, "Error Base de Datos", f"Error al guardar:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = VentanaAgregarEspecialidad()
    window.show()
    sys.exit(app.exec())