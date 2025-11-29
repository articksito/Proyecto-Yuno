import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QIntValidator

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- IMPORTACIONES ---
try:
    from db_connection import Conexion
    # Importamos el menú principal correcto según tu lista de archivos
    from UI_REP_main import MainWindow as MenuPrincipal
except ImportError as e:
    print(f"Error de importación (Mock activo): {e.name}")
    # Clases Mock para pruebas sin dependencias
    class Conexion:
        def consultar_registro(self, tabla, col_clave, val_clave, columnas): 
            print(f"MOCK SELECT FROM {tabla} WHERE {col_clave}={val_clave}")
            return None
        def editar_registro(self, val_clave, datos, tabla, col_clave): 
            print(f"MOCK UPDATE {tabla} SET {datos} WHERE {col_clave}={val_clave}")
            return True
    class MenuPrincipal(QMainWindow):
        def __init__(self, nombre_usuario=""):
            super().__init__()
            self.setWindowTitle("MENU PRINCIPAL (MOCK)")
            self.setCentralWidget(QLabel("Menu Principal Mock"))

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.ventana = None # Referencia para navegación
        
        self.setWindowTitle(f"Sistema Veterinario Yuno - Modificar Cliente ({self.nombre_usuario})")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS CSS ---
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC);
            }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel {
                background-color: white;
                border-top-left-radius: 30px; border-bottom-left-radius: 30px;
                margin: 20px 20px 20px 0px; 
            }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            /* Botones Menú */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px;
                color: white; font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF;
            }
            /* Sub-botones */
            QPushButton.sub-btn {
                text-align: left; padding-left: 40px; font-size: 16px;
                border-radius: 10px; color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05);
                height: 35px; margin: 2px 10px;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
        """)

        self.setup_sidebar()

        # Panel Blanco
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Modificar Cliente")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        # Botón Guardar Superior

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()

        self.white_layout.addLayout(header_layout)
        self.white_layout.addStretch(1)

        # Contenido
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        self.setup_edit_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addSpacing(30)
        
        self.setup_save_button() # Botón inferior grande
        self.white_layout.addStretch(2)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # --- NAVEGACIÓN ---
    def return_to_menu(self):
        try:
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al volver al menú: {e}")
            self.close()

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
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.sidebar_layout.addWidget(lbl_logo)

        # Menús
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])
        
        self.sidebar_layout.addStretch()

        # 🟢 BOTÓN VOLVER AL MENÚ
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setStyleSheet("""
            QPushButton {
                border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 20px;
                font-size: 14px; color: white; font-weight: bold; background-color: transparent;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.2); }
        """)
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
        layout.setContentsMargins(0,0,0,10)
        
        for opt in options:
            btn = QPushButton(opt)
            btn.setProperty("class", "sub-btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, c=title, o=opt: self.abrir_ventana(c, o))
            layout.addWidget(btn)
        
        frame.hide()
        self.sidebar_layout.addWidget(frame)
        btn_main.clicked.connect(lambda: frame.setVisible(not frame.isVisible()))

    def abrir_ventana(self, categoria, opcion):
        # Evitar recargar la misma ventana
        if categoria == "Clientes" and opcion == "Modificar": return

        ventana_map = {
            "Citas": {
                "Agendar": "UI_REP_Crear_cita",
                "Visualizar": "UI_REP_Revisar_Cita",
                "Modificar": "UI_REP_Modificar_cita"
            },
            "Mascotas": {
                "Registrar": "UI_REP_Registrar_mascota",
                "Visualizar": "UI_REP_Revisar_Mascota", # Ojo con el nombre exacto en tu carpeta
                "Modificar": "UI_REP_Modificar_Mascota"
            },
            "Clientes": {
                "Registrar": "UI_REP_Registra_cliente",
                "Visualizar": "UI_Revisar_cliente", # Ojo con el nombre exacto en tu carpeta
                "Modificar": "UI_REP_Modificar_cliente"
            }
        }

        nombre_modulo = ventana_map.get(categoria, {}).get(opcion)

        if nombre_modulo:
            try:
                # Import dinámico para no llenar el encabezado
                module = __import__(nombre_modulo, fromlist=['MainWindow'])
                self.ventana = module.MainWindow(self.nombre_usuario)
                self.ventana.show()
                self.close()
            except ImportError as e:
                QMessageBox.warning(self, "Error", f"Falta archivo: {nombre_modulo}.py\n{e}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al abrir: {e}")
        else:
            print(f"Ruta no mapeada: {categoria} -> {opcion}")

    def setup_edit_form(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(30)

        style_input = "background-color: rgba(241, 131, 227, 0.35); border: none; border-radius: 10px; padding: 5px 15px; font-size: 18px; color: #333; height: 45px;"
        style_lbl = "font-size: 24px; color: black;"

        # 1. Búsqueda
        lbl_id = QLabel("Id Cliente:"); lbl_id.setStyleSheet(style_lbl)
        self.inp_id = QLineEdit(); self.inp_id.setPlaceholderText("ID..."); self.inp_id.setStyleSheet(style_input)
        self.inp_id.setValidator(QIntValidator()) # Solo números en ID
        
        btn_search = QPushButton("Buscar")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("background-color: #7CEBFC; border-radius: 10px; font-weight: bold; border: 1px solid #5CD0E3;")
        btn_search.setFixedSize(100, 45)
        btn_search.clicked.connect(self.buscar_cliente)

        # 2. Campos
        self.inp_nombre = QLineEdit(); self.inp_nombre.setStyleSheet(style_input)
        self.inp_apellido = QLineEdit(); self.inp_apellido.setStyleSheet(style_input)
        self.inp_correo = QLineEdit(); self.inp_correo.setStyleSheet(style_input)
        self.inp_direccion = QLineEdit(); self.inp_direccion.setStyleSheet(style_input)
        self.inp_telefono = QLineEdit(); self.inp_telefono.setStyleSheet(style_input)
        self.inp_telefono.setValidator(QIntValidator())

        # Grid
        grid.addWidget(lbl_id, 0, 0)
        grid.addWidget(self.inp_id, 0, 1)
        grid.addWidget(btn_search, 0, 2)

        self.add_row(grid, 1, "Nombre:", self.inp_nombre, style_lbl)
        self.add_row(grid, 2, "Apellido:", self.inp_apellido, style_lbl)
        self.add_row(grid, 3, "Correo:", self.inp_correo, style_lbl)
        self.add_row(grid, 4, "Dirección:", self.inp_direccion, style_lbl)
        self.add_row(grid, 5, "Teléfono:", self.inp_telefono, style_lbl)

        grid.setRowStretch(6, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def add_row(self, grid, row, label, widget, style):
        l = QLabel(label); l.setStyleSheet(style)
        grid.addWidget(l, row, 0)
        grid.addWidget(widget, row, 1, 1, 2)

    def setup_info_board(self, parent_layout):
        board = QFrame()
        board.setFixedWidth(350)
        board.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 10px;")
        layout = QVBoxLayout(board); layout.setContentsMargins(0,0,0,0)

        # Header Board
        h_frame = QFrame(); h_frame.setFixedHeight(60)
        h_frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8)); border-top-left-radius: 10px; border-top-right-radius: 10px;")
        hl = QVBoxLayout(h_frame)
        lbl = QLabel("Información"); lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); lbl.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background: transparent;")
        hl.addWidget(lbl)

        # Content
        c_frame = QFrame(); c_frame.setStyleSheet("background: white; border-radius: 10px;")
        cl = QVBoxLayout(c_frame); cl.setContentsMargins(20,20,20,20); cl.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        lbl_nota = QLabel("Observaciones:"); lbl_nota.setStyleSheet("font-weight: bold; color: #333;")
        self.txt_notas = QTextEdit(); self.txt_notas.setPlaceholderText("Notas locales (no guardadas en BD)...")
        self.txt_notas.setStyleSheet("border: 1px solid #DDD; background: #FAFAFA; border-radius: 5px; padding: 5px;")
        
        cl.addWidget(lbl_nota)
        cl.addWidget(self.txt_notas)

        layout.addWidget(h_frame)
        layout.addWidget(c_frame)
        parent_layout.addWidget(board, stretch=1)

    def setup_save_button(self):
        btn = QPushButton("Guardar Cambios")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(250, 60)
        btn.setStyleSheet("QPushButton { background-color: #b67cfc; color: white; font-size: 24px; font-weight: bold; border-radius: 30px; } QPushButton:hover { background-color: #a060e8; }")
        btn.clicked.connect(self.guardar_cambios)
        
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(btn)
        layout.addStretch()
        self.white_layout.addLayout(layout)

    # --- LÓGICA ---
    def buscar_cliente(self):
        cid = self.inp_id.text().strip()
        if not cid: return QMessageBox.warning(self, "Aviso", "Ingresa un ID.")

        cols = ['nombre', 'apellido', 'correo', 'direccion', 'telefono']
        try:
            res = self.conexion1.consultar_registro('cliente', 'id_cliente', cid, cols)
            if res:
                self.inp_nombre.setText(str(res[0]))
                self.inp_apellido.setText(str(res[1]))
                self.inp_correo.setText(str(res[2]))
                self.inp_direccion.setText(str(res[3]))
                self.inp_telefono.setText(str(res[4]))
                self.txt_notas.clear()
                QMessageBox.information(self, "Éxito", "Cliente encontrado.")
            else:
                QMessageBox.warning(self, "Error", "Cliente no encontrado.")
                self.limpiar_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def guardar_cambios(self):
        cid = self.inp_id.text().strip()
        if not cid: return QMessageBox.warning(self, "Aviso", "Busca un cliente primero.")
        
        nom = self.inp_nombre.text().strip()
        ape = self.inp_apellido.text().strip()
        tel_str = self.inp_telefono.text().strip()

        if not nom or not ape or not tel_str:
            return QMessageBox.warning(self, "Aviso", "Nombre, Apellido y Teléfono obligatorios.")

        datos = {
            "nombre": nom,
            "apellido": ape,
            "correo": self.inp_correo.text().strip(),
            "direccion": self.inp_direccion.text().strip(),
            "telefono": int(tel_str)
        }

        try:
            if self.conexion1.editar_registro(cid, datos, 'cliente', 'id_cliente'):
                QMessageBox.information(self, "Éxito", "Cliente modificado.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo modificar.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def limpiar_form(self):
        self.inp_nombre.clear(); self.inp_apellido.clear(); self.inp_correo.clear()
        self.inp_direccion.clear(); self.inp_telefono.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())