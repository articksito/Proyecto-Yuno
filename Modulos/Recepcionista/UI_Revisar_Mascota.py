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

        self.setWindowTitle("Sistema Veterinario Yuno - Revisar Mascota")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS VISUALES (Mismo diseño que Clientes) ---
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
            
            /* --- INPUTS --- */
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
            /* Solo lectura */
            QLineEdit[readOnly="true"] {
                background-color: #F8F8F8;
                border: 1px solid #DDD;
                color: #555;
            }

            /* --- BOTONES SIDEBAR --- */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px;
                color: white; font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF;
            }
            QPushButton.sub-btn {
                text-align: left; padding-left: 40px; border-radius: 10px;
                color: #F0F0F0; font-family: 'Segoe UI', sans-serif; font-size: 16px;
                background-color: rgba(0, 0, 0, 0.05); height: 35px; margin: 2px 10px; border: none;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
            
            /* Botón Volver */
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

        self.setup_sidebar()
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
    #  CONTENIDO (DISEÑO REVISIÓN MASCOTA)
    # ============================================================
    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # 1. Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Revisar Mascota")
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

        # 2. Barra de Búsqueda
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("ID Mascota:", styleSheet="font-size: 16px; font-weight: 500; color: #444;"))
        
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Ingrese ID (ej. 10)...")
        self.inp_search.setFixedWidth(250)
        
        btn_search = QPushButton("Buscar")
        btn_search.setObjectName("BtnBuscar")
        btn_search.setFixedSize(120, 40)
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.clicked.connect(self.buscar_mascota)

        search_layout.addWidget(self.inp_search)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addLayout(search_layout)
        self.white_layout.addSpacing(30)

        # 3. Contenedor Dividido
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

        # Campos
        self.inp_id = QLineEdit(); self.inp_id.setReadOnly(True)
        self.inp_nombre = QLineEdit(); self.inp_nombre.setReadOnly(True)
        # self.inp_especie = QLineEdit(); self.inp_especie.setReadOnly(True) # Especie removida
        self.inp_raza = QLineEdit(); self.inp_raza.setReadOnly(True)
        self.inp_edad = QLineEdit(); self.inp_edad.setReadOnly(True)
        self.inp_peso = QLineEdit(); self.inp_peso.setReadOnly(True)
        self.inp_dueno = QLineEdit(); self.inp_dueno.setReadOnly(True) # Para ID o Nombre del dueño

        self.inp_id.setPlaceholderText("-")
        self.inp_nombre.setPlaceholderText("-")
        
        # Grid
        campos = [
            ("ID Sistema:", self.inp_id),
            ("Nombre:", self.inp_nombre),
            # ("Especie:", self.inp_especie), # Especie removida
            ("Raza:", self.inp_raza),
            ("Edad:", self.inp_edad),
            ("Peso (kg):", self.inp_peso),
            ("Dueño (ID):", self.inp_dueno)
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
        lbl_tit = QLabel("Información Mascota")
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

        # Icono Mascota
        lbl_pic = QLabel("🐶")
        lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_pic.setStyleSheet("font-size: 60px; background: #f0f0f0; border-radius: 50px; min-height: 100px; min-width: 100px;")
        content_lay.addWidget(lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Nombre y Estado
        self.prev_nombre = QLabel("Nombre Mascota")
        self.prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_nombre.setWordWrap(True)
        self.prev_nombre.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")
        
        content_lay.addWidget(self.prev_nombre)
        content_lay.addStretch()

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    # ============================================================
    #  LÓGICA DE BÚSQUEDA
    # ============================================================
    def buscar_mascota(self):
        id_masc = self.inp_search.text().strip()
        if not id_masc:
            QMessageBox.warning(self, "Aviso", "Por favor ingrese un ID de mascota.")
            return

        if not DB_AVAILABLE:
            QMessageBox.critical(self, "Error", "No hay conexión a la base de datos.")
            return

        try:
            # Consultamos tabla 'mascota' por 'id_mascota'
            # Asumiendo estructura típica: id, nombre, edad, peso, especie, raza, fk_cliente
            # Ajustar índices según tu base de datos real
            datos = self.conexion.consultar_registro('mascota', 'id_mascota', id_masc)
            
            if datos:
                # Mapeo tentativo (ajusta según tus columnas reales en DB)
                # 0: id, 1: nombre, 2: edad, 3: peso, 4: especie, 5: raza, 6: fk_cliente
                self.inp_id.setText(str(datos[0]))
                self.inp_nombre.setText(str(datos[1]))
                self.inp_edad.setText(str(datos[2]))
                self.inp_peso.setText(str(datos[3]))
                # self.inp_especie.setText(str(datos[4])) # Especie removida
                self.inp_raza.setText(str(datos[5]))
                self.inp_dueno.setText(str(datos[6])) # ID Cliente
                
                # Actualizar tarjeta derecha
                self.prev_nombre.setText(str(datos[1]))
            else:
                QMessageBox.warning(self, "No encontrado", "No se encontró una mascota con ese ID.")
                self.limpiar_datos()

        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"Error al buscar mascota: {e}")

    def limpiar_datos(self):
        # for w in [self.inp_id, self.inp_nombre, self.inp_especie, self.inp_raza, self.inp_edad, self.inp_peso, self.inp_dueno]:
        for w in [self.inp_id, self.inp_nombre, self.inp_raza, self.inp_edad, self.inp_peso, self.inp_dueno]:
            w.clear()
        self.prev_nombre.setText("Nombre Mascota")

    def return_to_menu(self):
        try:
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except Exception as e:
            print(f"Error al volver al menú: {e}")
            self.close()

    def abrir_ventana(self, categoria, opcion):
        if categoria == "Mascotas" and opcion == "Visualizar": return 
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