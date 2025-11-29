import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QComboBox, QMessageBox)
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
        def insertar_datos(self, *args): return 999
    class MenuPrincipal(QMainWindow):
        def __init__(self, u): super().__init__(); self.show()

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.setWindowTitle(f"Sistema Veterinario Yuno - Registrar Mascota ({self.nombre_usuario})")
        
        # 1. TAMAÑO MÍNIMO (Estándar)
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
            QLabel { font-family: 'Segoe UI'; color: #333; }
            
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
            QLineEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none; border-radius: 10px; padding: 5px 15px; 
                font-size: 18px; color: #333; height: 45px;
            }
            QComboBox {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none; border-radius: 10px; padding: 5px 15px; 
                font-size: 18px; color: #333; height: 45px;
            }
            QComboBox::drop-down { border: 0px; }
        """)

        # 1. Barra Lateral
        self.setup_sidebar()
        
        # 2. Panel Principal
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        # Márgenes
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Registrar Mascota")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold;")
        
        # Botón Guardar Superior
       
        
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # Contenedor Formulario + Info
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)
        # Alineación Superior (Importante)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setup_form(content_layout)
        self.setup_info(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addStretch(1)

        # Botón Guardar Inferior
        self.setup_save_btn()
        self.white_layout.addSpacing(20)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # --- NAVEGACIÓN ---
    def return_to_menu(self):
        try:
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al volver: {e}")

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        # Margen inferior ajustado
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
        
        # Resorte para empujar botón al fondo
        self.sidebar_layout.addStretch()
        
        # Botón Volver
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setStyleSheet("""
            QPushButton {
                border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 10px;
                color: white; font-weight: bold; background-color: transparent; font-size: 14px;
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
        if categoria == "Mascotas" and opcion == "Registrar": return # Evitar recarga

        # Diccionario corregido
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
                QMessageBox.warning(self, "Error", f"Falta archivo: {nombre_modulo}.py\n{e}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al abrir: {e}")
        else:
            print(f"Ruta no mapeada: {categoria} -> {opcion}")

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def setup_form(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(30)
        grid.setContentsMargins(0, 0, 0, 0)
        
        lbl_style = "font-size: 24px; color: black; font-weight: 400;"
        
        self.inp_nom = QLineEdit()
        self.inp_eda = QLineEdit(); self.inp_eda.setValidator(QIntValidator())
        self.inp_pes = QLineEdit(); self.inp_pes.setValidator(QDoubleValidator())
        self.inp_esp = QComboBox(); self.inp_esp.addItems(["Perro", "Gato", "Ave", "Roedor", "Otro"])
        self.inp_raz = QLineEdit()
        self.inp_cli = QLineEdit(); self.inp_cli.setPlaceholderText("ID Dueño"); self.inp_cli.setValidator(QIntValidator())

        for x in [self.inp_nom, self.inp_eda, self.inp_pes, self.inp_raz, self.inp_cli]: x.textChanged.connect(self.upd_prev)
        self.inp_esp.currentTextChanged.connect(self.upd_prev)

        def add_row(r, label, widget): 
            lb = QLabel(label); lb.setStyleSheet(lbl_style)
            grid.addWidget(lb, r, 0); grid.addWidget(widget, r, 1)

        add_row(0, "Nombre:", self.inp_nom)
        add_row(1, "Edad (Años):", self.inp_eda)
        add_row(2, "Peso (Kg):", self.inp_pes)
        add_row(3, "Especie:", self.inp_esp)
        add_row(4, "Raza:", self.inp_raz)
        add_row(5, "Id Dueño:", self.inp_cli)
        
        grid.setRowStretch(6, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info(self, parent_layout):
        board = QFrame()
        board.setFixedWidth(350)
        board.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 10px;")
        vl = QVBoxLayout(board); vl.setContentsMargins(0,0,0,0)
        
        h = QFrame(); h.setFixedHeight(60)
        h.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 #FC7CE2); border-top-left-radius: 10px; border-top-right-radius: 10px;")
        vl.addWidget(h); h.setLayout(QVBoxLayout()); h.layout().addWidget(QLabel("Vista Previa", alignment=Qt.AlignmentFlag.AlignCenter, styleSheet="color: white; font-weight: bold; font-size: 18px; background: transparent;"))
        
        c = QFrame(); c.setStyleSheet("background: white; border-radius: 10px; border: none;")
        cl = QVBoxLayout(c); cl.setAlignment(Qt.AlignmentFlag.AlignTop); cl.setContentsMargins(20, 20, 20, 20)
        
        self.l_n = QLabel("Nombre"); self.l_n.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px 0; color: #333;")
        self.l_d = QLabel("Dueño: --"); self.l_d.setStyleSheet("font-size: 16px; background: #ecf0f1; padding: 5px; border-radius: 5px; color: #555;")
        self.l_i = QLabel("Info: --"); self.l_i.setStyleSheet("color: #666; margin-top: 10px; font-size: 16px;")
        
        cl.addWidget(self.l_n); cl.addWidget(self.l_d); cl.addWidget(self.l_i); cl.addStretch()
        vl.addWidget(c)
        parent_layout.addWidget(board, stretch=1)

    def setup_save_btn(self):
        b = QPushButton("Registrar Mascota")
        b.setFixedSize(250, 60)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setStyleSheet("background-color: #b67cfc; color: white; font-size: 24px; font-weight: bold; border-radius: 30px;")
        b.clicked.connect(self.guardar_datos)
        
        l = QHBoxLayout(); l.addStretch(); l.addWidget(b); l.addStretch()
        self.white_layout.addLayout(l)

    def upd_prev(self):
        self.l_n.setText(self.inp_nom.text() or "Nombre")
        self.l_d.setText(f"Dueño ID: {self.inp_cli.text()}" if self.inp_cli.text() else "Dueño: --")
        self.l_i.setText(f"{self.inp_esp.currentText()} - {self.inp_raz.text()} | {self.inp_eda.text()} años")

    def guardar_datos(self):
        if not self.inp_nom.text() or not self.inp_cli.text(): 
            return QMessageBox.warning(self, "Aviso", "Nombre y Dueño obligatorios.")
        
        try:
            d = (self.inp_nom.text(), int(self.inp_eda.text() or 0), float(self.inp_pes.text() or 0), self.inp_esp.currentText(), self.inp_raz.text(), int(self.inp_cli.text()))
            nid = self.conexion1.insertar_datos('mascota', d, ('nombre', 'edad', 'peso', 'especie', 'raza', 'fk_cliente'))
            if nid: 
                QMessageBox.information(self, "Éxito", f"Mascota ID {nid} registrada.")
                self.limpiar()
            else: 
                QMessageBox.warning(self, "Error", "Error BD.")
        except Exception as e: 
            QMessageBox.critical(self, "Error", str(e))

    def limpiar(self):
        self.inp_nom.clear(); self.inp_eda.clear(); self.inp_pes.clear(); self.inp_raz.clear(); self.inp_cli.clear(); self.inp_esp.setCurrentIndex(0)
        self.upd_prev()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())