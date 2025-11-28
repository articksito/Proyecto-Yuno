import sys
import os
import re
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QIntValidator

# Configuración del path para imports relativos
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Importar conexión a la base de datos y el Menú Principal
try:
    from db_connection import Conexion
    # 🛑 Importar el Menú Principal para el retorno
    from UI_Menu_Principal import MainWindow as MenuPrincipal 
except ImportError as e:
    # Mocks para evitar fallos si no se encuentran los archivos
    print(f"Error de importación (Mock activo): {e.name}")
    class Conexion:
        def insertar_datos(self, table, data, columns):
            print(f"INSERTAR SIMULADO EN {table}: {data}")
            return 999 
    class MenuPrincipal(QMainWindow):
        def __init__(self, nombre_usuario=""):
            super().__init__()
            self.setWindowTitle("MENU PRINCIPAL (MOCK)")
            self.resize(500, 300)
            self.setCentralWidget(QLabel("Ventana de Menú Principal (MOCK)"))


class MainWindow(QMainWindow):
    # Instancia de la conexión a la DB
    conexion1 = Conexion()

    def __init__(self, nombre_usuario="Recepcionista"): 
        super().__init__()
        
        self.nombre_usuario = nombre_usuario
        self.ventana = None

        self.setWindowTitle(f"Sistema Veterinario Yuno - Registrar Cliente ({self.nombre_usuario})")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal (Horizontal)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS (Mismo código CSS del original) ---
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

        # --- HEADER ---
        header_layout = QHBoxLayout()
        
        # Título
        lbl_header = QLabel("Registrar Cliente")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        # 🟢 NUEVO BOTÓN GUARDAR (PARTE SUPERIOR)
        btn_save_top = QPushButton("Guardar")
        btn_save_top.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save_top.setFixedSize(120, 40)
        btn_save_top.setStyleSheet("""
            QPushButton {
                background-color: #b67cfc; color: white; 
                font-weight: bold; border-radius: 10px; font-size: 16px;
            }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_save_top.clicked.connect(self.guardar_datos)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_save_top) # Añadido a la derecha del header

        self.white_layout.addLayout(header_layout)
        
        # Espaciador
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
        
        # Botón Guardar (Inferior - Original)
        self.setup_save_button()

        # Espaciador inferior
        self.white_layout.addStretch(2)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)


    # --- MÉTODO PARA VOLVER AL MENÚ PRINCIPAL ---
    def return_to_menu(self):
        try:
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el Menú Principal: {e}")
            self.close()

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
        
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])

        self.sidebar_layout.addStretch()

        # 🛑 BOTÓN RESTAURADO: EL MISMO DEL PRIMER CÓDIGO EN EL SIDEBAR
        btn_logout = QPushButton("↶ Volver al Menú")
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
        btn_logout.clicked.connect(self.return_to_menu)
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
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.abrir_ventana(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def abrir_ventana(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        if categoria == "Clientes" and opcion == "Registrar": return 
        target_window = None
        try:
            if categoria == "Citas":
                if opcion == "Agendar":
                    from UI_REP_Crear_cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_REP_Revisar_Cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    from UI_REP_Registrar_mascota import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_REP_Revisar_Mascota import MainWindow as Win 
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_mascota import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
            elif categoria == "Clientes":
                if opcion == "Visualizar":
                    from UI_REP_Revisar_cliente import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cliente import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                    
            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close()
        except ImportError as e:
            QMessageBox.warning(self, "Error de Navegación", f"Falta el archivo: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir ventana: {e}")

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def setup_register_form(self, parent_layout):
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Estilo Inputs (Original)
        input_style = """
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none; border-radius: 10px; padding: 5px 15px;
                font-size: 18px; color: #333; height: 45px;
            }
        """
        label_style = "font-size: 24px; color: black; font-weight: 400;"

        # --- Campos de Cliente ---
        lbl_nombre = QLabel("Nombre:"); lbl_nombre.setStyleSheet(label_style)
        self.inp_nombre = QLineEdit(); self.inp_nombre.setPlaceholderText("Nombre"); self.inp_nombre.setStyleSheet(input_style)

        lbl_apellido = QLabel("Apellido:"); lbl_apellido.setStyleSheet(label_style)
        self.inp_apellido = QLineEdit(); self.inp_apellido.setPlaceholderText("Apellido"); self.inp_apellido.setStyleSheet(input_style)

        lbl_tel = QLabel("Teléfono:"); lbl_tel.setStyleSheet(label_style)
        self.inp_telefono = QLineEdit(); self.inp_telefono.setPlaceholderText("10 dígitos"); self.inp_telefono.setStyleSheet(input_style)
        self.inp_telefono.setValidator(QIntValidator())

        lbl_correo = QLabel("Correo:"); lbl_correo.setStyleSheet(label_style)
        self.inp_correo = QLineEdit(); self.inp_correo.setPlaceholderText("email@ejemplo.com"); self.inp_correo.setStyleSheet(input_style)

        lbl_calle = QLabel("Calle:"); lbl_calle.setStyleSheet(label_style)
        self.inp_calle = QLineEdit(); self.inp_calle.setStyleSheet(input_style)

        # Números
        lbl_nums = QLabel("Num Ext / Int:"); lbl_nums.setStyleSheet(label_style)
        w_nums = QWidget(); l_nums = QHBoxLayout(w_nums); l_nums.setContentsMargins(0,0,0,0); l_nums.setSpacing(10)
        self.inp_ext = QLineEdit(); self.inp_ext.setPlaceholderText("Ext."); self.inp_ext.setStyleSheet(input_style)
        self.inp_int = QLineEdit(); self.inp_int.setPlaceholderText("Int."); self.inp_int.setStyleSheet(input_style)
        l_nums.addWidget(self.inp_ext); l_nums.addWidget(self.inp_int)

        # Col/CP
        lbl_col = QLabel("Colonia / CP:"); lbl_col.setStyleSheet(label_style)
        w_col = QWidget(); l_col = QHBoxLayout(w_col); l_col.setContentsMargins(0,0,0,0); l_col.setSpacing(10)
        self.inp_colonia = QLineEdit(); self.inp_colonia.setPlaceholderText("Colonia"); self.inp_colonia.setStyleSheet(input_style)
        self.inp_cp = QLineEdit(); self.inp_cp.setPlaceholderText("C.P."); self.inp_cp.setFixedWidth(100); self.inp_cp.setStyleSheet(input_style)
        self.inp_cp.setValidator(QIntValidator())
        l_col.addWidget(self.inp_colonia); l_col.addWidget(self.inp_cp)
        
        lbl_ciudad = QLabel("Ciudad:"); lbl_ciudad.setStyleSheet(label_style)
        self.inp_ciudad = QLineEdit(); self.inp_ciudad.setText("Tijuana"); self.inp_ciudad.setStyleSheet(input_style)

        # Preview triggers
        for w in [self.inp_nombre, self.inp_apellido, self.inp_telefono, self.inp_calle, self.inp_colonia]:
            w.textChanged.connect(self.update_preview)

        # Add to Grid
        grid_layout.addWidget(lbl_nombre, 0, 0); grid_layout.addWidget(self.inp_nombre, 0, 1)
        grid_layout.addWidget(lbl_apellido, 1, 0); grid_layout.addWidget(self.inp_apellido, 1, 1)
        grid_layout.addWidget(lbl_tel, 2, 0); grid_layout.addWidget(self.inp_telefono, 2, 1)
        grid_layout.addWidget(lbl_correo, 3, 0); grid_layout.addWidget(self.inp_correo, 3, 1)
        grid_layout.addWidget(lbl_calle, 4, 0); grid_layout.addWidget(self.inp_calle, 4, 1)
        grid_layout.addWidget(lbl_nums, 5, 0); grid_layout.addWidget(w_nums, 5, 1)
        grid_layout.addWidget(lbl_col, 6, 0); grid_layout.addWidget(w_col, 6, 1)
        grid_layout.addWidget(lbl_ciudad, 7, 0); grid_layout.addWidget(self.inp_ciudad, 7, 1)
        grid_layout.setRowStretch(8, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_board(self, parent_layout):
        board_container = QFrame()
        board_container.setFixedWidth(350)
        board_container.setStyleSheet("QFrame { background-color: white; border: 1px solid #DDD; border-radius: 10px; }")
        
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0); board_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8)); border-top-left-radius: 10px; border-top-right-radius: 10px;")
        header_layout = QVBoxLayout(header_frame)
        lbl_info_title = QLabel("Información")
        lbl_info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(lbl_info_title)

        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        lbl_preview = QLabel("Nuevo Cliente")
        lbl_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_preview.setStyleSheet("color: #888; font-size: 14px; font-weight: bold; margin-bottom: 10px;")

        self.lbl_prev_nombre = QLabel("Nombre Cliente")
        self.lbl_prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_nombre.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 15px;")
        self.lbl_prev_nombre.setWordWrap(True)

        self.lbl_prev_telefono = QLabel("Tel: --")
        self.lbl_prev_telefono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_telefono.setStyleSheet("font-size: 18px; color: #2c3e50; font-weight: bold; background-color: #ecf0f1; padding: 10px; border-radius: 5px;")

        self.lbl_prev_direccion = QLabel("Dirección: --")
        self.lbl_prev_direccion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_direccion.setWordWrap(True)
        self.lbl_prev_direccion.setStyleSheet("font-size: 14px; color: #555; margin-top: 15px;")

        content_layout.addWidget(lbl_preview)
        content_layout.addWidget(self.lbl_prev_nombre)
        content_layout.addWidget(self.lbl_prev_telefono)
        content_layout.addWidget(self.lbl_prev_direccion)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)
        parent_layout.addWidget(board_container, stretch=1)

    def setup_save_button(self):
        btn_save = QPushButton("Guardar Registro")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedSize(250, 60)
        btn_save.setStyleSheet("""
            QPushButton { background-color: #b67cfc; color: white; font-size: 24px; font-weight: bold; border-radius: 30px; }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_save.clicked.connect(self.guardar_datos)
        btn_container = QHBoxLayout()
        btn_container.addStretch(); btn_container.addWidget(btn_save); btn_container.addStretch()
        self.white_layout.addLayout(btn_container)

    def update_preview(self):
        nombre = f"{self.inp_nombre.text()} {self.inp_apellido.text()}".strip()
        self.lbl_prev_nombre.setText(nombre if nombre else "Nombre Cliente")
        self.lbl_prev_telefono.setText(f"Tel: {self.inp_telefono.text()}" if self.inp_telefono.text() else "Tel: --")
        dir_short = f"{self.inp_calle.text()} #{self.inp_ext.text()}" if self.inp_calle.text() else "Dirección: --"
        self.lbl_prev_direccion.setText(dir_short)

    def guardar_datos(self):
        nombre = self.inp_nombre.text().strip()
        apellido = self.inp_apellido.text().strip()
        tel = self.inp_telefono.text().strip()
        correo = self.inp_correo.text().strip()
        
        # Validar
        if not nombre or not apellido or not tel:
             QMessageBox.warning(self, "Aviso", "Nombre, Apellido y Teléfono son obligatorios.")
             return
        
        # Dirección
        dir_full = f"{self.inp_calle.text().strip()} #{self.inp_ext.text().strip()} Int {self.inp_int.text().strip()}, Col. {self.inp_colonia.text().strip()}, CP {self.inp_cp.text().strip()}, {self.inp_ciudad.text().strip()}"
        
        datos = (nombre, apellido, dir_full, correo, tel)
        try:
            nid = self.conexion1.insertar_datos('cliente', datos, ('nombre', 'apellido', 'direccion', 'correo', 'telefono'))
            if nid:
                QMessageBox.information(self, "Éxito", f"Cliente registrado.\nID: {nid}")
                self.limpiar()
            else:
                QMessageBox.warning(self, "Error", "Fallo al insertar en BD.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def limpiar(self):
        self.inp_nombre.clear(); self.inp_apellido.clear(); self.inp_telefono.clear(); self.inp_correo.clear()
        self.inp_calle.clear(); self.inp_ext.clear(); self.inp_int.clear(); self.inp_colonia.clear(); self.inp_cp.clear()
        self.update_preview()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow("Recepcionista Prueba") 
    window.show()
    sys.exit(app.exec())