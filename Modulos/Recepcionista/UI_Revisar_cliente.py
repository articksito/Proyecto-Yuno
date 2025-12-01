import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QMessageBox, 
                             QLineEdit, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- IMPORTACIONES BASE DE DATOS ---
try:
    from db_connection import Conexion
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    class Conexion:
        def consultar_registro(self, *args, **kwargs): return None

# --- IMPORTACIONES MENU ---
try:
    from UI_REP_main import MainWindow as MenuPrincipal
except ImportError:
    class MenuPrincipal(QMainWindow):
        def __init__(self, u): super().__init__(); self.show()

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.ventana = None 

        # Inicializar Conexión
        if DB_AVAILABLE:
            self.conexion = Conexion()

        self.setWindowTitle("Sistema Veterinario Yuno - Revisar Cliente")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS VISUALES (Copiados del diseño solicitado) ---
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
            QLineEdit {
                background-color: rgba(241, 131, 227, 0.15); 
                border: 1px solid rgba(241, 131, 227, 0.5);
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 16px;
                color: #333;
                height: 40px;
            }
            QLineEdit:focus {
                background-color: rgba(241, 131, 227, 0.25);
                border: 2px solid #FC7CE2;
            }
            /* Estilo específico para inputs de solo lectura */
            QLineEdit[readOnly="true"] {
                background-color: #F8F8F8;
                border: 1px solid #DDD;
                color: #555;
            }

            /* --- BOTONES DEL SIDEBAR --- */
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
            
            /* Botón Volver (Sidebar) */
            QPushButton.back-btn {
                text-align: center; border: 2px solid white; 
                border-radius: 15px; padding: 10px; margin-top: 20px;
                font-size: 14px; color: white; font-weight: bold;
                background-color: transparent;
            }
            QPushButton.back-btn:hover { background-color: rgba(255, 255, 255, 0.2); }

            /* Botón Buscar */
            QPushButton#BtnBuscar {
                background-color: #7CEBFC; color: #333; border-radius: 10px; 
                font-weight: bold; border: 1px solid #5CD0E3; font-size: 14px;
            }
            QPushButton#BtnBuscar:hover { background-color: #5CD0E3; }
        """)

        # 1. Barra Lateral
        self.setup_sidebar()

        # 2. Panel de Contenido
        self.setup_content_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

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

        # Logo
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "FILES", "logo_yuno.png")
        
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                lbl_logo.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        else:
            lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        
        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # Menús
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])

        self.sidebar_layout.addStretch()

        # Botón Volver
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setProperty("class", "back-btn")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.return_to_menu)
        self.sidebar_layout.addWidget(btn_back)

    def setup_accordion_group(self, title, options):
        btn_main = QPushButton(title)
        btn_main.setProperty("class", "menu-btn")
        btn_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebar_layout.addWidget(btn_main)

        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(2)
        
        for opt in options:
            btn = QPushButton(opt)
            btn.setProperty("class", "sub-btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, c=title, o=opt: self.abrir_ventana(c, o))
            layout.addWidget(btn)

        frame.hide()
        self.sidebar_layout.addWidget(frame)
        btn_main.clicked.connect(lambda: frame.setVisible(not frame.isVisible()))

    # ============================================================
    #  CONTENIDO (DISEÑO SOLICITADO)
    # ============================================================
    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # 1. Header (Título + Botón Cerrar)
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Revisar Cliente")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(40, 40)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; border-radius: 20px; font-size: 20px; color: #666; border: none; }
            QPushButton:hover { background-color: #ffcccc; color: #cc0000; }
        """)
        btn_close.clicked.connect(self.return_to_menu)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # 2. Barra de Búsqueda (Integrada en el diseño)
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("ID del Cliente:", styleSheet="font-size: 16px; font-weight: 500; color: #444;"))
        
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Ingrese ID para buscar...")
        self.inp_search.setFixedWidth(250)
        
        btn_search = QPushButton("Buscar")
        btn_search.setObjectName("BtnBuscar")
        btn_search.setFixedSize(120, 40)
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.clicked.connect(self.buscar_cliente)

        search_layout.addWidget(self.inp_search)
        search_layout.addWidget(btn_search)
        search_layout.addStretch() # Empujar a la izquierda
        
        self.white_layout.addLayout(search_layout)
        self.white_layout.addSpacing(30)

        # 3. Contenedor Dividido (Datos Izquierda | Info Derecha)
        content_split = QHBoxLayout()
        content_split.setSpacing(40)

        # --- A. IZQUIERDA: FORMULARIO (READ ONLY) ---
        self.setup_form_left(content_split)

        # --- B. DERECHA: TARJETA INFO ---
        self.setup_info_right(content_split)

        self.white_layout.addLayout(content_split)
        self.white_layout.addStretch()

    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        label_style = "font-size: 16px; font-weight: 500; color: #444;"

        # Definir campos como atributos para llenarlos luego
        self.inp_id = QLineEdit(); self.inp_id.setReadOnly(True)
        self.inp_nombre = QLineEdit(); self.inp_nombre.setReadOnly(True)
        self.inp_apellido = QLineEdit(); self.inp_apellido.setReadOnly(True)
        self.inp_direccion = QLineEdit(); self.inp_direccion.setReadOnly(True)
        self.inp_correo = QLineEdit(); self.inp_correo.setReadOnly(True)
        self.inp_telefono = QLineEdit(); self.inp_telefono.setReadOnly(True)

        # Placeholders
        self.inp_id.setPlaceholderText("-")
        self.inp_nombre.setPlaceholderText("-")
        
        # Agregar al Grid
        # (Label, Widget)
        campos = [
            ("ID Sistema:", self.inp_id),
            ("Nombre:", self.inp_nombre),
            ("Apellido:", self.inp_apellido),
            ("Dirección:", self.inp_direccion),
            ("Correo:", self.inp_correo),
            ("Teléfono:", self.inp_telefono)
        ]

        row = 0
        for label_text, widget in campos:
            grid.addWidget(QLabel(label_text, styleSheet=label_style), row, 0)
            grid.addWidget(widget, row, 1)
            row += 1

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
        lbl_tit = QLabel("Información del Cliente")
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
        lbl_pic.setStyleSheet("font-size: 60px; background: #f0f0f0; border-radius: 50px; min-height: 100px; min-width: 100px;")
        content_lay.addWidget(lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Datos Preview
        self.prev_nombre = QLabel("Nombre Cliente")
        self.prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_nombre.setWordWrap(True)
        self.prev_nombre.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")
        
        # Se ha eliminado el label "Activo" (prev_status) como se solicitó

        content_lay.addWidget(self.prev_nombre)
        content_lay.addStretch()

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    # ============================================================
    #  LÓGICA
    # ============================================================
    def buscar_cliente(self):
        id_cli = self.inp_search.text().strip()
        if not id_cli:
            QMessageBox.warning(self, "Aviso", "Por favor ingrese un ID de cliente.")
            return

        if not DB_AVAILABLE:
            QMessageBox.critical(self, "Error", "No hay conexión a la base de datos.")
            return

        try:
            # Consultamos la tabla 'cliente' por 'id_cliente'
            datos = self.conexion.consultar_registro('cliente', 'id_cliente', id_cli)
            
            if datos:
                # Llenar campos (Inputs ReadOnly)
                self.inp_id.setText(str(datos[0]))
                self.inp_nombre.setText(str(datos[1]))
                self.inp_apellido.setText(str(datos[2]))
                self.inp_direccion.setText(str(datos[3]))
                self.inp_correo.setText(str(datos[4]))
                self.inp_telefono.setText(str(datos[5]))
                
                # Actualizar tarjeta derecha
                self.prev_nombre.setText(f"{datos[1]} {datos[2]}")
                # Ya no actualizamos prev_status
            else:
                QMessageBox.warning(self, "No encontrado", "No se encontró un cliente con ese ID.")
                self.limpiar_datos()

        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"Error al buscar cliente: {e}")

    def limpiar_datos(self):
        for w in [self.inp_id, self.inp_nombre, self.inp_apellido, self.inp_direccion, self.inp_correo, self.inp_telefono]:
            w.clear()
        self.prev_nombre.setText("Nombre Cliente")
        # Ya no reseteamos prev_status

    def return_to_menu(self):
        try:
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except Exception as e:
            print(f"Error al volver al menú: {e}")
            self.close()

    def abrir_ventana(self, categoria, opcion):
        if categoria == "Clientes" and opcion == "Visualizar": return 
        ventana_map = {
            "Citas": {"Agendar": "UI_REP_Crear_cita", "Visualizar": "UI_REP_Revisar_Cita", "Modificar": "UI_REP_Modificar_cita"},
            "Mascotas": {"Registrar": "UI_REP_Registrar_mascota", "Visualizar": "UI_Revisar_Mascota", "Modificar": "UI_REP_Modificar_Mascota"},
            "Clientes": {"Registrar": "UI_REP_Registra_cliente", "Visualizar": "UI_Revisar_cliente", "Modificar": "UI_REP_Modificar_cliente"}
        }
        nombre_modulo = ventana_map.get(categoria, {}).get(opcion)
        if nombre_modulo:
            try:
                module = __import__(nombre_modulo, fromlist=['MainWindow'])
                self.ventana = module.MainWindow(self.nombre_usuario)
                self.ventana.show(); self.close()
            except ImportError as e: QMessageBox.warning(self, "Error", f"Falta archivo: {nombre_modulo}.py\n{e}")
            except Exception as e: QMessageBox.critical(self, "Error", f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())