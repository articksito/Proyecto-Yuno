import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QIntValidator, QDoubleValidator

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
    from UI_REP_main import MainWindow as MenuPrincipal 
except ImportError:
    class Conexion:
        def consultar_registro(self, *args): return None
        def editar_registro(self, *args): return True
    class MenuPrincipal(QMainWindow):
        def __init__(self, u): super().__init__(); self.show()

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.ventana = None
        self.mascota_id_cargada = None

        self.setWindowTitle(f"Sistema Veterinario Yuno - Modificar Mascota ({self.nombre_usuario})")
        
        # 1. TAMAÑO MÍNIMO
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES ---
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
            
            /* Inputs */
            QLineEdit:disabled, QComboBox:disabled {
                background-color: #F0F0F0; color: #999; border: 1px solid #DDD;
            }
        """)

        # 1. Barra Lateral
        self.setup_sidebar()

        # 2. Panel Blanco
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Modificar Mascota")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        # Botón Guardar Superior
        
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()

        self.white_layout.addLayout(header_layout)
        self.white_layout.addStretch(1)

        # Contenedor Formulario + Info
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)
        # Alineación Superior
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setup_edit_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addStretch(1)
        
        # Botón Guardar Inferior
        self.setup_save_button()
        self.white_layout.addSpacing(20)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

        # Estado inicial
        self.set_form_editable(False)

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
        # MARGEN INFERIOR OPTIMIZADO
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

        # Menús
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])
        
        self.sidebar_layout.addStretch()

        # Botón Volver
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setStyleSheet("""
            QPushButton {
                border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 10px;
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
        layout.setContentsMargins(0, 0, 0, 10)
        
        for opt in options:
            btn = QPushButton(opt)
            btn.setProperty("class", "sub-btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, c=title, o=opt: self.abrir_ventana(c, o))
            layout.addWidget(btn)

        frame.hide()
        self.sidebar_layout.addWidget(frame)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame))

    def abrir_ventana(self, categoria, opcion):
        if categoria == "Mascotas" and opcion == "Modificar": return

        # MAPEO CORREGIDO
        ventana_map = {
            "Citas": {
                "Agendar": "UI_REP_Crear_cita",
                "Visualizar": "UI_REP_Revisar_Cita",
                "Modificar": "UI_REP_Modificar_cita"
            },
            "Mascotas": {
                "Registrar": "UI_REP_Registrar_mascota",
                "Visualizar": "UI_Revisar_Mascota",   # Sin REP
                "Modificar": "UI_REP_Modificar_Mascota"
            },
            "Clientes": {
                "Registrar": "UI_REP_Registra_cliente",
                "Visualizar": "UI_Revisar_cliente",   # Sin REP
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

    def setup_edit_form(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(30)
        grid.setContentsMargins(0, 0, 0, 0)

        style_input = "background-color: rgba(241, 131, 227, 0.35); border: none; border-radius: 10px; padding: 5px 15px; font-size: 18px; color: #333; height: 45px;"
        style_lbl = "font-size: 24px; color: black; font-weight: 400;"

        # 1. Búsqueda
        lbl_id = QLabel("Id Mascota:"); lbl_id.setStyleSheet(style_lbl)
        self.inp_id = QLineEdit(); self.inp_id.setPlaceholderText("ID..."); self.inp_id.setStyleSheet(style_input)
        self.inp_id.setValidator(QIntValidator())
        
        btn_search = QPushButton("Buscar")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("background-color: #7CEBFC; border-radius: 10px; font-weight: bold; border: 1px solid #5CD0E3;")
        btn_search.setFixedSize(100, 45)
        btn_search.clicked.connect(self.buscar_mascota)

        # 2. Campos
        self.inp_nombre = QLineEdit(); self.inp_nombre.setStyleSheet(style_input)
        self.inp_edad = QLineEdit(); self.inp_edad.setPlaceholderText("Años"); self.inp_edad.setStyleSheet(style_input); self.inp_edad.setValidator(QIntValidator())
        self.inp_peso = QLineEdit(); self.inp_peso.setPlaceholderText("Kg"); self.inp_peso.setStyleSheet(style_input); self.inp_peso.setValidator(QDoubleValidator())
        
        self.inp_especie = QComboBox(); self.inp_especie.addItems(["Perro", "Gato", "Ave", "Roedor", "Otro"]); self.inp_especie.setStyleSheet(style_input.replace("QLineEdit", "QComboBox"))
        self.inp_raza = QLineEdit(); self.inp_raza.setStyleSheet(style_input)
        self.inp_cliente = QLineEdit(); self.inp_cliente.setPlaceholderText("ID Dueño"); self.inp_cliente.setStyleSheet(style_input); self.inp_cliente.setValidator(QIntValidator())

        # Conexiones
        for w in [self.inp_nombre, self.inp_edad, self.inp_peso, self.inp_raza, self.inp_cliente]:
            w.textChanged.connect(self.update_preview)
        self.inp_especie.currentTextChanged.connect(self.update_preview)

        # Grid
        grid.addWidget(lbl_id, 0, 0)
        grid.addWidget(self.inp_id, 0, 1); grid.addWidget(btn_search, 0, 2)

        self.add_row(grid, 1, "Nombre:", self.inp_nombre, style_lbl)
        self.add_row(grid, 2, "Edad:", self.inp_edad, style_lbl)
        self.add_row(grid, 3, "Peso:", self.inp_peso, style_lbl)
        self.add_row(grid, 4, "Especie:", self.inp_especie, style_lbl)
        self.add_row(grid, 5, "Raza:", self.inp_raza, style_lbl)
        self.add_row(grid, 6, "Id Dueño:", self.inp_cliente, style_lbl)

        grid.setRowStretch(7, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def add_row(self, grid, row, label, widget, style):
        l = QLabel(label); l.setStyleSheet(style)
        grid.addWidget(l, row, 0)
        grid.addWidget(widget, row, 1, 1, 2)

    def setup_info_board(self, parent_layout):
        board = QFrame(); board.setFixedWidth(350)
        board.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 10px;")
        vl = QVBoxLayout(board); vl.setContentsMargins(0,0,0,0); vl.setSpacing(0)

        h = QFrame(); h.setFixedHeight(60)
        h.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252,124,226,0.8)); border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom: none;")
        hl = QVBoxLayout(h); l = QLabel("Vista Previa"); l.setAlignment(Qt.AlignmentFlag.AlignCenter); l.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background: transparent;")
        hl.addWidget(l)

        c = QFrame(); c.setStyleSheet("background: white; border-radius: 10px; border: none;")
        cl = QVBoxLayout(c); cl.setContentsMargins(20,20,20,20); cl.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.lbl_prev_nombre = QLabel("Nombre Mascota"); self.lbl_prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter); self.lbl_prev_nombre.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin: 10px 0;")
        self.lbl_prev_dueno = QLabel("Dueño ID: --"); self.lbl_prev_dueno.setAlignment(Qt.AlignmentFlag.AlignCenter); self.lbl_prev_dueno.setStyleSheet("font-size: 16px; background: #ecf0f1; padding: 5px; border-radius: 5px;")
        self.lbl_prev_detalles = QLabel("Especie - Raza"); self.lbl_prev_detalles.setAlignment(Qt.AlignmentFlag.AlignCenter); self.lbl_prev_detalles.setStyleSheet("color: #555; margin-top: 10px;")
        self.lbl_prev_stats = QLabel("Edad: -- | Peso: --"); self.lbl_prev_stats.setAlignment(Qt.AlignmentFlag.AlignCenter); self.lbl_prev_stats.setStyleSheet("color: #888;")

        cl.addWidget(self.lbl_prev_nombre); cl.addWidget(self.lbl_prev_dueno); cl.addWidget(self.lbl_prev_detalles); cl.addWidget(self.lbl_prev_stats); cl.addStretch()

        vl.addWidget(h); vl.addWidget(c)
        parent_layout.addWidget(board, stretch=1)

    def setup_save_button(self):
        btn = QPushButton("Guardar Cambios")
        btn.setObjectName("btn_guardar")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(250, 60)
        btn.setStyleSheet("QPushButton { background-color: #b67cfc; color: white; font-size: 24px; font-weight: bold; border-radius: 30px; } QPushButton:hover { background-color: #a060e8; }")
        btn.clicked.connect(self.guardar_cambios)
        l = QHBoxLayout(); l.addStretch(); l.addWidget(btn); l.addStretch()
        self.white_layout.addLayout(l)

    def set_form_editable(self, enabled):
        for w in [self.inp_nombre, self.inp_edad, self.inp_peso, self.inp_especie, self.inp_raza, self.inp_cliente]:
            w.setEnabled(enabled)
        self.findChild(QPushButton, "btn_guardar").setEnabled(enabled)

    def update_preview(self):
        nom = self.inp_nombre.text()
        dueno = self.inp_cliente.text()
        esp = self.inp_especie.currentText()
        raza = self.inp_raza.text()
        e = self.inp_edad.text(); p = self.inp_peso.text()
        
        self.lbl_prev_nombre.setText(nom if nom else "Nombre Mascota")
        self.lbl_prev_dueno.setText(f"Dueño ID: {dueno}" if dueno else "Dueño ID: --")
        self.lbl_prev_detalles.setText(f"{esp} - {raza}" if raza else esp)
        self.lbl_prev_stats.setText(f"{e if e else '-'} años | {p if p else '-'} kg")

    def buscar_mascota(self):
        mid = self.inp_id.text().strip()
        self.mascota_id_cargada = None
        self.set_form_editable(False)

        if not mid: return QMessageBox.warning(self, "Aviso", "Ingresa un ID.")

        try:
            cols = ['nombre', 'edad', 'peso', 'especie', 'raza', 'fk_cliente']
            reg = self.conexion1.consultar_registro('mascota', 'id_mascota', int(mid), cols)
            
            if reg:
                self.inp_nombre.setText(str(reg[0]))
                self.inp_edad.setText(str(reg[1]))
                self.inp_peso.setText(f"{reg[2]:.1f}")
                self.inp_especie.setCurrentText(str(reg[3]))
                self.inp_raza.setText(str(reg[4]))
                self.inp_cliente.setText(str(reg[5]))
                
                self.mascota_id_cargada = int(mid)
                self.set_form_editable(True)
                QMessageBox.information(self, "Éxito", "Mascota cargada.")
            else:
                QMessageBox.warning(self, "Error", "Mascota no encontrada.")
                self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def guardar_cambios(self):
        if not self.mascota_id_cargada: return QMessageBox.warning(self, "Aviso", "Busca una mascota primero.")

        nom = self.inp_nombre.text().strip()
        cli = self.inp_cliente.text().strip()
        if not nom or not cli: return QMessageBox.warning(self, "Aviso", "Nombre y Dueño obligatorios.")

        try:
            datos = {
                "nombre": nom,
                "edad": int(self.inp_edad.text()) if self.inp_edad.text() else 0,
                "peso": float(self.inp_peso.text()) if self.inp_peso.text() else 0.0,
                "especie": self.inp_especie.currentText(),
                "raza": self.inp_raza.text().strip(),
                "fk_cliente": int(cli)
            }
            if self.conexion1.editar_registro(self.mascota_id_cargada, datos, 'mascota', 'id_mascota'):
                QMessageBox.information(self, "Éxito", "Mascota actualizada.")
                self.limpiar_campos(); self.inp_id.clear()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Edad y Peso deben ser numéricos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def limpiar_campos(self):
        self.inp_nombre.clear(); self.inp_edad.clear(); self.inp_peso.clear(); self.inp_raza.clear(); self.inp_cliente.clear()
        self.inp_especie.setCurrentIndex(0)
        self.update_preview()
        self.set_form_editable(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())