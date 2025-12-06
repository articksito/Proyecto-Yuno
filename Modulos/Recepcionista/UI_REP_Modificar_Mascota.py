import sys
import os

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPixmap, QIntValidator, QDoubleValidator, QPainter, QColor

# Intentamos importar la conexión nueva, si falla usamos la genérica o mock
try:
    from db_conexionNew import Conexion
except ImportError:  
    class Conexion:
        def consultar_registro(self, *args, **kwargs): return None
        def editar_registro(self, *args, **kwargs): return False

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle(f"Sistema Veterinario Yuno - Modificar Mascota ({self.nombre_usuario})")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)
        
        # Conexión Base de Datos
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")
        
        # Variable para saber qué ID estamos editando
        self.current_mascota_id = None

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

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
                font-family: 'Segoe UI', sans-serif; color: #333;
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
            
            /* Botón Logout / Volver */
            QPushButton.action-btn {
                border: 2px solid white; border-radius: 15px; padding: 10px; 
                margin-top: 10px; font-size: 14px; color: white; font-weight: bold; 
                background-color: transparent;
            }
            QPushButton.action-btn:hover { background-color: rgba(255, 255, 255, 0.2); }

            /* --- INPUTS Y FORMULARIO (COLOR ROSA) --- */
            QLineEdit, QComboBox {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 16px;
                color: #333;
                height: 40px;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: rgba(241, 131, 227, 0.5); 
            }
            QLineEdit:disabled, QComboBox:disabled {
                background-color: #F0F0F0; color: #999;
            }
            QComboBox::drop-down { border: 0px; }
            
            /* --- PANEL DERECHO (INFO) --- */
            QFrame#InfoBoard {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 12px;
            }
        """)

        # --- 1. BARRA LATERAL ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO ---
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- SETUP SIDEBAR (RECEPCIONISTA) ---
    # ==========================================

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # --- LOGO ---
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

        # --- MENÚS ---
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])
        
        self.sidebar_layout.addStretch()

        # Botón Volver
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setProperty("class", "action-btn")
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
        
        for opt in options:
            btn = QPushButton(opt)
            btn.setProperty("class", "sub-btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, c=title, o=opt: self.navegar(c, o))
            layout.addWidget(btn)
        
        frame.hide()
        self.sidebar_layout.addWidget(frame)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def return_to_menu(self):
        try:
            from UI_REP_main import MainWindow as MenuPrincipal
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except ImportError:
            self.close()

    def navegar(self, categoria, opcion):
        if categoria == "Mascotas" and opcion == "Modificar": return

        ventana_map = {
            "Citas": {
                "Agendar": "UI_REP_Crear_cita",
                "Visualizar": "UI_REP_Revisar_Cita",
                "Modificar": "UI_REP_Modificar_cita"
            },
            "Mascotas": {
                "Registrar": "UI_REP_Registrar_mascota",
                "Visualizar": "UI_Revisar_Mascota",
                "Modificar": "UI_REP_Modificar_Mascota"
            },
            "Clientes": {
                "Registrar": "UI_REP_Registra_cliente",
                "Visualizar": "UI_Revisar_cliente", 
                "Modificar": "UI_REP_Modificar_cliente"
            }
        }

        nombre_modulo = ventana_map.get(categoria, {}).get(opcion)

        if nombre_modulo:
            try:
                module = __import__(nombre_modulo, fromlist=['MainWindow'])
                self.ventana = module.MainWindow(self.nombre_usuario)
                self.ventana.show()
                self.close()
            except ImportError as e:
                QMessageBox.warning(self, "Error de Navegación", f"Falta el archivo: {nombre_modulo}.py\n{e}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al abrir ventana: {e}")

    # ==========================================
    # --- PANEL CENTRAL ---
    # ==========================================

    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(40, 40, 20, 40)

        # 1. Header
        header = QHBoxLayout()
        lbl_header = QLabel("Modificar Mascota")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        header.addWidget(lbl_header)
        header.addStretch()
        self.white_layout.addLayout(header)
        self.white_layout.addSpacing(10)

        # 2. Barra de Búsqueda
        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        # 3. Contenedor Dividido
        content_split = QHBoxLayout()
        content_split.setSpacing(40)

        self.setup_form_left(content_split)
        self.setup_info_right(content_split)

        self.white_layout.addLayout(content_split)
        self.white_layout.addStretch()

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_search = QLabel("ID Mascota:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        
        self.inp_search_id = QLineEdit()
        self.inp_search_id.setPlaceholderText("Ej: 105")
        self.inp_search_id.setFixedWidth(200)
        self.inp_search_id.setValidator(QIntValidator())
        self.inp_search_id.setStyleSheet("""
            QLineEdit { border: 2px solid #ddd; border-radius: 10px; padding: 8px 15px; font-size: 16px; color: #333; background-color: #F9F9F9; }
        """)
        
        btn_search = QPushButton("Buscar")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setFixedSize(120, 40)
        btn_search.setStyleSheet("""
            QPushButton { background-color: #7CEBFC; color: #333; font-weight: bold; font-size: 16px; border-radius: 10px; border: 1px solid #5CD0E3; }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_search.clicked.connect(self.buscar_mascota)
        
        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.inp_search_id)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_container)

    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        label_style = "font-size: 18px; font-weight: 500; color: #444;"

        # Campos
        self.inp_nombre = QLineEdit()
        self.inp_edad = QLineEdit()
        self.inp_edad.setValidator(QIntValidator())
        self.inp_edad.setPlaceholderText("Años")
        
        self.inp_peso = QLineEdit()
        self.inp_peso.setValidator(QDoubleValidator())
        self.inp_peso.setPlaceholderText("Kg")
        
        self.inp_especie = QComboBox()
        self.inp_especie.addItems(["Canino", "Felino", "Ave", "Roedor", "Otro"])
        
        self.inp_raza = QLineEdit()
        
        self.inp_dueno = QLineEdit() 
        self.inp_dueno.setValidator(QIntValidator())
        self.inp_dueno.setPlaceholderText("ID Cliente")

        # Conectar señales
        self.inp_nombre.textChanged.connect(self.update_preview)
        self.inp_edad.textChanged.connect(self.update_preview)
        self.inp_peso.textChanged.connect(self.update_preview)
        self.inp_especie.currentTextChanged.connect(self.update_preview)
        self.inp_raza.textChanged.connect(self.update_preview)
        self.inp_dueno.textChanged.connect(self.update_preview)

        # Agregar al Grid
        self.add_form_row(grid, 0, "Nombre:", self.inp_nombre, label_style)
        self.add_form_row(grid, 1, "Edad:", self.inp_edad, label_style)
        self.add_form_row(grid, 2, "Peso:", self.inp_peso, label_style)
        self.add_form_row(grid, 3, "Especie:", self.inp_especie, label_style)
        self.add_form_row(grid, 4, "Raza:", self.inp_raza, label_style)
        self.add_form_row(grid, 5, "ID Dueño:", self.inp_dueno, label_style)

        form_widget.setEnabled(False)
        self.form_widget = form_widget

        parent_layout.addWidget(form_widget, stretch=3)

    def add_form_row(self, grid, row, label_text, widget, style):
        lbl = QLabel(label_text)
        lbl.setStyleSheet(style)
        grid.addWidget(lbl, row, 0)
        grid.addWidget(widget, row, 1)

    def setup_info_right(self, parent_layout):
        board = QFrame()
        board.setObjectName("InfoBoard")
        board.setMaximumWidth(400)
        
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)

        # Header Board
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("""
            background-color: #7CEBFC; 
            border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: none;
        """)
        head_lay = QHBoxLayout(header)
        lbl_tit = QLabel("Vista Previa")
        lbl_tit.setStyleSheet("color: #444; font-weight: bold; font-size: 16px; border: none; background: transparent;")
        head_lay.addWidget(lbl_tit, alignment=Qt.AlignmentFlag.AlignCenter)
        board_lay.addWidget(header)

        # Contenido
        content = QWidget()
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(20, 30, 20, 30)
        content_lay.setSpacing(10)
        content_lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- IMAGEN MASCOTA ---
        self.lbl_pic = QLabel("🐾") # Fallback emoji
        self.lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_pic.setStyleSheet("background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        
        # Cargar icono 'pets.png'
        ruta_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "pets.png")
        
        if os.path.exists(ruta_icon):
            pixmap = QPixmap(ruta_icon)
            if not pixmap.isNull():
                self.lbl_pic.setPixmap(pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                self.lbl_pic.setText("")
            else:
                self.lbl_pic.setStyleSheet(self.lbl_pic.styleSheet() + "font-size: 40px;")
        else:
            self.lbl_pic.setStyleSheet(self.lbl_pic.styleSheet() + "font-size: 40px;")
        
        content_lay.addWidget(self.lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Datos Preview
        self.prev_nombre = QLabel("Nombre Mascota")
        self.prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_nombre.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.prev_detalle = QLabel("Especie | Raza")
        self.prev_detalle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_detalle.setStyleSheet("font-size: 16px; color: #666;")

        self.prev_dueno = QLabel("Dueño ID: --")
        self.prev_dueno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_dueno.setStyleSheet("font-size: 14px; font-weight: bold; color: #FC7CE2; background: #FFF0F5; padding: 5px; border-radius: 5px; margin-top: 5px;")

        self.prev_stats = QLabel("Edad: -- | Peso: --")
        self.prev_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_stats.setStyleSheet("font-size: 14px; color: #888; margin-top: 10px;")

        content_lay.addWidget(self.prev_nombre)
        content_lay.addWidget(self.prev_detalle)
        content_lay.addWidget(self.prev_dueno)
        content_lay.addWidget(self.prev_stats)
        
        content_lay.addStretch() 
        
        # Botón Guardar
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_guardar.setFixedSize(250, 50)
        self.btn_guardar.setEnabled(False) 
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #7CEBFC; 
                color: #444; 
                font-size: 18px; 
                font-weight: bold; 
                border-radius: 25px;
                border: 1px solid #5CD0E3;
            }
            QPushButton:hover { background-color: #5CD0E3; }
            QPushButton:disabled { background-color: #f0f0f0; color: #aaa; border: 1px solid #ddd; }
        """)
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(self.btn_guardar)
        btn_container.addStretch()
        
        content_lay.addLayout(btn_container)
        content_lay.addSpacing(10)

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    # ==========================================
    # --- LÓGICA ---
    # ==========================================

    def update_preview(self):
        nom = self.inp_nombre.text()
        esp = self.inp_especie.currentText()
        raz = self.inp_raza.text()
        due = self.inp_dueno.text()
        eda = self.inp_edad.text()
        pes = self.inp_peso.text()

        self.prev_nombre.setText(nom if nom else "Nombre Mascota")
        self.prev_detalle.setText(f"{esp} | {raz if raz else 'Raza'}")
        self.prev_dueno.setText(f"Dueño ID: {due}" if due else "Dueño ID: --")
        self.prev_stats.setText(f"Edad: {eda if eda else '-'} | Peso: {pes if pes else '-'} kg")

    def buscar_mascota(self):
        mid = self.inp_search_id.text().strip()
        if not mid:
            return QMessageBox.warning(self, "Aviso", "Ingresa un ID de Mascota.")

        try:
            columnas = ['nombre', 'edad', 'peso', 'especie', 'raza', 'fk_cliente']
            res = self.conexion.consultar_registro('mascota', 'id_mascota', mid, columnas)
            
            if res:
                self.current_mascota_id = mid
                
                self.inp_nombre.setText(str(res[0]))
                self.inp_edad.setText(str(res[1]))
                self.inp_peso.setText(str(res[2]))
                
                # Manejar el ComboBox
                idx = self.inp_especie.findText(str(res[3]), Qt.MatchFlag.MatchFixedString)
                if idx >= 0: self.inp_especie.setCurrentIndex(idx)
                
                self.inp_raza.setText(str(res[4]))
                self.inp_dueno.setText(str(res[5]))
                
                self.form_widget.setEnabled(True)
                self.btn_guardar.setEnabled(True)
                self.update_preview()
                
                QMessageBox.information(self, "Éxito", "Mascota encontrada.")
            else:
                QMessageBox.warning(self, "Error", "Mascota no encontrada.")
                self.limpiar_form()
                self.form_widget.setEnabled(False)
                self.btn_guardar.setEnabled(False)
                self.current_mascota_id = None

        except Exception as e:
            QMessageBox.critical(self, "Error BD", str(e))

    def guardar_cambios(self):
        if not self.current_mascota_id: 
            return QMessageBox.warning(self, "Aviso", "Busca una mascota primero.")
        
        nom = self.inp_nombre.text().strip()
        due = self.inp_dueno.text().strip()

        if not nom or not due:
            return QMessageBox.warning(self, "Aviso", "El nombre y el dueño son obligatorios.")

        datos = {
            "nombre": nom,
            "edad": self.inp_edad.text(),
            "peso": self.inp_peso.text(),
            "especie": self.inp_especie.currentText(),
            "raza": self.inp_raza.text(),
            "fk_cliente": due
        }

        try:
            if self.conexion.editar_registro(self.current_mascota_id, datos, 'mascota', 'id_mascota'):
                QMessageBox.information(self, "Éxito", "Mascota modificada correctamente.")
                self.inp_search_id.clear()
                self.limpiar_form()
                self.form_widget.setEnabled(False)
                self.btn_guardar.setEnabled(False)
                self.current_mascota_id = None
                self.update_preview()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la mascota.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def limpiar_form(self):
        self.inp_nombre.clear()
        self.inp_edad.clear()
        self.inp_peso.clear()
        self.inp_raza.clear()
        self.inp_dueno.clear()
        self.inp_especie.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())