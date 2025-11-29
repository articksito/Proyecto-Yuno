import sys
import os
import re
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QMessageBox)
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
    # 🛑 IMPORTANTE: Importamos el menú principal correcto
    from UI_REP_main import MainWindow as MenuPrincipal 
except ImportError as e:
    print(f"Error de importación (Mock activo): {e.name}")
    class Conexion:
        def insertar_datos(self, table, data, columns):
            print(f"MOCK INSERT INTO {table}: {data}")
            return 999 
    class MenuPrincipal(QMainWindow):
        def __init__(self, nombre_usuario=""):
            super().__init__()
            self.setWindowTitle("MENU PRINCIPAL (MOCK)")
            self.setCentralWidget(QLabel("Mock Menu"))

class MainWindow(QMainWindow):
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
            /* Botones del Menú Lateral */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px;
                color: white; font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF;
            }
            /* Botones del Submenú */
            QPushButton.sub-btn {
                text-align: left; padding-left: 40px; font-size: 16px;
                border-radius: 10px; color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05);
                height: 35px; margin: 2px 10px;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
        """)

        # 1. Barra Lateral (Sidebar)
        self.setup_sidebar()

        # 2. Panel Blanco (Contenido)
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # --- HEADER (Título + Botón Guardar Superior) ---
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Registrar Cliente")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_save_top = QPushButton("Guardar")
        btn_save_top.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save_top.setFixedSize(120, 40)
        btn_save_top.setStyleSheet("""
            QPushButton { background-color: #b67cfc; color: white; font-weight: bold; border-radius: 10px; font-size: 16px; }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_save_top.clicked.connect(self.guardar_datos)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_save_top)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addStretch(1)

        # --- CONTENEDOR CENTRAL (Formulario + Info) ---
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        self.setup_register_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addSpacing(30)
        
        # --- BOTÓN GUARDAR INFERIOR ---
        self.setup_save_button()
        self.white_layout.addStretch(2)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # --- FUNCIÓN PARA VOLVER AL MENÚ ---
    def return_to_menu(self):
        try:
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el Menú Principal: {e}")
            self.close()

    # --- CONFIGURACIÓN DE LA BARRA LATERAL ---
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
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        self.sidebar_layout.addWidget(lbl_logo)
        

        # Menús
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])

        
        # Espaciador para empujar el botón al fondo
        self.sidebar_layout.addStretch()
# 🛑 Botón Modificado: Ahora es "Volver al Menú"
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
        # 🛑 Conectar al retorno al menú
        btn_logout.clicked.connect(self.return_to_menu)
        self.sidebar_layout.addWidget(btn_logout)
        # 🟢 BOTÓN VOLVER AL MENÚ (Asegurado)
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setStyleSheet("""
            QPushButton {
                border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 20px;
                font-size: 14px; color: white; font-weight: bold; background-color: transparent;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.2); }
        """)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        # Conexión al método return_to_menu
        btn_back.clicked.connect(self.return_to_menu)
        
        self.sidebar_layout.addWidget(btn_back)

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
        # Si ya estamos en Registrar Cliente, no hacemos nada
        if categoria == "Clientes" and opcion == "Registrar": return 

        # Diccionario de navegación
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
        else:
            print(f"Ruta no mapeada: {categoria} -> {opcion}")

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def setup_register_form(self, parent_layout):
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Estilos
        style_input = "background-color: rgba(241, 131, 227, 0.35); border: none; border-radius: 10px; padding: 5px 15px; font-size: 18px; color: #333; height: 45px;"
        style_lbl = "font-size: 24px; color: black; font-weight: 400;"

        # Campos
        self.inp_nombre = QLineEdit(); self.inp_nombre.setPlaceholderText("Nombre"); self.inp_nombre.setStyleSheet(style_input)
        self.inp_apellido = QLineEdit(); self.inp_apellido.setPlaceholderText("Apellido"); self.inp_apellido.setStyleSheet(style_input)
        
        self.inp_telefono = QLineEdit(); self.inp_telefono.setPlaceholderText("10 dígitos"); self.inp_telefono.setStyleSheet(style_input)
        self.inp_telefono.setValidator(QIntValidator()) # Solo números
        
        self.inp_correo = QLineEdit(); self.inp_correo.setPlaceholderText("email@ejemplo.com"); self.inp_correo.setStyleSheet(style_input)
        self.inp_calle = QLineEdit(); self.inp_calle.setPlaceholderText("Calle Principal"); self.inp_calle.setStyleSheet(style_input)

        # Números
        self.inp_ext = QLineEdit(); self.inp_ext.setPlaceholderText("Ext."); self.inp_ext.setStyleSheet(style_input)
        self.inp_int = QLineEdit(); self.inp_int.setPlaceholderText("Int."); self.inp_int.setStyleSheet(style_input)
        w_nums = QWidget(); l_nums = QHBoxLayout(w_nums); l_nums.setContentsMargins(0,0,0,0); l_nums.addWidget(self.inp_ext); l_nums.addWidget(self.inp_int)

        # Col/CP
        self.inp_colonia = QLineEdit(); self.inp_colonia.setPlaceholderText("Colonia"); self.inp_colonia.setStyleSheet(style_input)
        self.inp_cp = QLineEdit(); self.inp_cp.setPlaceholderText("C.P."); self.inp_cp.setFixedWidth(100); self.inp_cp.setStyleSheet(style_input)
        self.inp_cp.setValidator(QIntValidator())
        w_col = QWidget(); l_col = QHBoxLayout(w_col); l_col.setContentsMargins(0,0,0,0); l_col.addWidget(self.inp_colonia); l_col.addWidget(self.inp_cp)
        
        self.inp_ciudad = QLineEdit(); self.inp_ciudad.setText("Tijuana"); self.inp_ciudad.setStyleSheet(style_input)

        # Grid
        self.add_row(grid_layout, 0, "Nombre:", self.inp_nombre, style_lbl)
        self.add_row(grid_layout, 1, "Apellido:", self.inp_apellido, style_lbl)
        self.add_row(grid_layout, 2, "Teléfono:", self.inp_telefono, style_lbl)
        self.add_row(grid_layout, 3, "Correo:", self.inp_correo, style_lbl)
        self.add_row(grid_layout, 4, "Calle:", self.inp_calle, style_lbl)
        
        l_n = QLabel("Num Ext/Int:"); l_n.setStyleSheet(style_lbl)
        grid_layout.addWidget(l_n, 5, 0); grid_layout.addWidget(w_nums, 5, 1)

        l_c = QLabel("Colonia/CP:"); l_c.setStyleSheet(style_lbl)
        grid_layout.addWidget(l_c, 6, 0); grid_layout.addWidget(w_col, 6, 1)

        self.add_row(grid_layout, 7, "Ciudad:", self.inp_ciudad, style_lbl)

        # Trigger Preview
        for w in [self.inp_nombre, self.inp_apellido, self.inp_telefono, self.inp_calle, self.inp_colonia]:
            w.textChanged.connect(self.update_preview)

        grid_layout.setRowStretch(8, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def add_row(self, grid, row, text, widget, style):
        l = QLabel(text); l.setStyleSheet(style)
        grid.addWidget(l, row, 0)
        grid.addWidget(widget, row, 1)

    def setup_info_board(self, parent_layout):
        board = QFrame()
        board.setFixedWidth(350)
        board.setStyleSheet("QFrame { background-color: white; border: 1px solid #DDD; border-radius: 10px; }")
        layout = QVBoxLayout(board); layout.setContentsMargins(0,0,0,0)

        h_frame = QFrame(); h_frame.setFixedHeight(60)
        h_frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8)); border-top-left-radius: 10px; border-top-right-radius: 10px;")
        hl = QVBoxLayout(h_frame)
        l = QLabel("Información"); l.setAlignment(Qt.AlignmentFlag.AlignCenter); l.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background: transparent;")
        hl.addWidget(l)

        c_frame = QFrame(); c_frame.setStyleSheet("background: white; border-radius: 10px;")
        cl = QVBoxLayout(c_frame); cl.setContentsMargins(20,20,20,20); cl.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        lbl_p = QLabel("Nuevo Cliente"); lbl_p.setAlignment(Qt.AlignmentFlag.AlignCenter); lbl_p.setStyleSheet("color: #888; font-weight: bold;")
        self.lbl_prev_nom = QLabel("Nombre Cliente"); self.lbl_prev_nom.setAlignment(Qt.AlignmentFlag.AlignCenter); self.lbl_prev_nom.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin: 10px 0;")
        self.lbl_prev_tel = QLabel("Tel: --"); self.lbl_prev_tel.setAlignment(Qt.AlignmentFlag.AlignCenter); self.lbl_prev_tel.setStyleSheet("font-size: 18px; font-weight: bold; background: #ecf0f1; padding: 5px; border-radius: 5px;")
        self.lbl_prev_dir = QLabel("Dirección: --"); self.lbl_prev_dir.setAlignment(Qt.AlignmentFlag.AlignCenter); self.lbl_prev_dir.setStyleSheet("color: #555; margin-top: 10px;"); self.lbl_prev_dir.setWordWrap(True)

        cl.addWidget(lbl_p); cl.addWidget(self.lbl_prev_nom); cl.addWidget(self.lbl_prev_tel); cl.addWidget(self.lbl_prev_dir); cl.addStretch()

        layout.addWidget(h_frame); layout.addWidget(c_frame)
        parent_layout.addWidget(board, stretch=1)

    def setup_save_button(self):
        btn = QPushButton("Guardar Registro")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(250, 60)
        btn.setStyleSheet("QPushButton { background-color: #b67cfc; color: white; font-size: 24px; font-weight: bold; border-radius: 30px; } QPushButton:hover { background-color: #a060e8; }")
        btn.clicked.connect(self.guardar_datos)
        l = QHBoxLayout(); l.addStretch(); l.addWidget(btn); l.addStretch()
        self.white_layout.addLayout(l)

    def update_preview(self):
        n = f"{self.inp_nombre.text()} {self.inp_apellido.text()}".strip()
        self.lbl_prev_nom.setText(n if n else "Nombre Cliente")
        self.lbl_prev_tel.setText(f"Tel: {self.inp_telefono.text()}" if self.inp_telefono.text() else "Tel: --")
        d = f"{self.inp_calle.text()} #{self.inp_ext.text()}" if self.inp_calle.text() else "Dirección: --"
        self.lbl_prev_dir.setText(d)
    

    def guardar_datos(self):
        nom = self.inp_nombre.text().strip()
        ape = self.inp_apellido.text().strip()
        tel = self.inp_telefono.text().strip()
        
        if not nom or not ape or not tel:
            return QMessageBox.warning(self, "Aviso", "Nombre, Apellido y Teléfono obligatorios.")
        
        # Construir Dirección
        calle = self.inp_calle.text().strip()
        ext = self.inp_ext.text().strip()
        inte = self.inp_int.text().strip()
        col = self.inp_colonia.text().strip()
        cp = self.inp_cp.text().strip()
        ciu = self.inp_ciudad.text().strip()
        
        dir_full = f"{calle} #{ext}"
        if inte: dir_full += f" Int {inte}"
        if col: dir_full += f", Col. {col}"
        if cp: dir_full += f", CP {cp}"
        dir_full += f", {ciu}"

        datos = (nom, ape, dir_full, self.inp_correo.text().strip(), tel)
        
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec())