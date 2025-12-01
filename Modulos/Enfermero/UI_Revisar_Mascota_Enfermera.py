import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# --- AJUSTE DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) 
if current_dir not in sys.path: sys.path.append(current_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)

# Intentar importar conexión
try:
    from db_connection import Conexion
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    class Conexion:
        def consultar_registro(self, *args, **kwargs): return None

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Enfermero"):
        super().__init__()
        
        self.nombre_usuario = nombre_usuario
        self.setWindowTitle(f"Sistema Veterinario Yuno - Revisar Mascota ({self.nombre_usuario})")
        self.resize(1280, 720)
        # 1. TAMAÑO MÍNIMO
        self.setMinimumSize(1024, 600)
        
        if DB_AVAILABLE:
            self.conexion1 = Conexion()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS ---
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QWidget#Sidebar { background-color: transparent; }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            
            /* Botones Menú Lateral (Estilo Unificado) */
            QPushButton.menu-btn { 
                text-align: left; padding-left: 20px; 
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; 
                color: white; font-family: 'Segoe UI', sans-serif; 
                font-weight: bold; font-size: 18px; 
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px; 
            }
            QPushButton.menu-btn:hover { 
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; 
            }
            QPushButton.sub-btn { 
                text-align: left; font-family: 'Segoe UI', sans-serif; font-size: 16px; 
                font-weight: normal; padding-left: 40px; border-radius: 10px; 
                color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05); 
                height: 35px; margin-bottom: 2px; margin-left: 10px; margin-right: 10px; 
            }
            QPushButton.sub-btn:hover { 
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; 
            }
            
            /* Inputs Solo Lectura */
            QLineEdit { 
                background-color: #F0F0F0; 
                border: 1px solid #DDD; border-radius: 10px; 
                padding: 5px 15px; font-size: 16px; color: #555; height: 40px; 
            }
        """)

        self.setup_sidebar()

        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Revisar Mascota")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # Barra de Búsqueda
        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        # Contenido
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setup_pet_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addStretch(2)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        # 2. MÁRGENES OPTIMIZADOS
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        # Logo
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_logo = os.path.join(parent_dir, "FILES", "logo_yuno.png")
        
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                lbl_logo.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        else:
            lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        
        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        self.setup_accordion_group("Citas", ["Visualizar"])
        self.setup_accordion_group("Mascotas", ["Visualizar"])
        self.setup_accordion_group("Inventario", ["Farmacia", "Hospitalización"])
        self.setup_accordion_group("Expediente", ["Diagnóstico"])

        # 3. EL RESORTE MÁGICO
        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Volver al Menú")
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
        btn_logout.clicked.connect(self.regresar_menu)
        self.sidebar_layout.addWidget(btn_logout)

    def setup_accordion_group(self, title, options):
        btn_main = QPushButton(title)
        btn_main.setProperty("class", "menu-btn")
        btn_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebar_layout.addWidget(btn_main)

        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(2)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.abrir_ventana(t, o))
            layout.addWidget(btn_sub)

        frame.hide()
        self.sidebar_layout.addWidget(frame)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def setup_search_bar(self):
        search_frame = QFrame()
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(0, 0, 0, 10)

        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Buscar ID Mascota...")
        # Estilo específico para el input de búsqueda (Rosa suave)
        self.inp_search.setStyleSheet("background-color: rgba(241, 131, 227, 0.15); border: 1px solid #DDD; border-radius: 10px; padding: 5px 15px; font-size: 16px; color: #333;")
        self.inp_search.setFixedWidth(250)

        btn_search = QPushButton("Buscar")
        btn_search.setFixedSize(100, 40)
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("QPushButton { background-color: #7CEBFC; color: #333; border-radius: 10px; font-weight: bold; border: 1px solid #5CD0E3; } QPushButton:hover { background-color: #5CD0E3; }")
        btn_search.clicked.connect(self.buscar_mascota)

        search_layout.addWidget(QLabel("ID Mascota:", styleSheet="font-weight: bold; font-size: 16px; color: #555;"))
        search_layout.addWidget(self.inp_search)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_frame)

    def setup_pet_form(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(30)
        grid.setContentsMargins(0, 0, 0, 0)

        label_style = "font-size: 18px; color: #333; font-weight: 500;"

        def add_row(row, label_text, attr_name):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            inp = QLineEdit()
            inp.setReadOnly(True)
            inp.setText("---")
            setattr(self, attr_name, inp)
            grid.addWidget(lbl, row, 0)
            grid.addWidget(inp, row, 1)

        add_row(0, "Nombre:", "inp_nombre")
        add_row(1, "Especie:", "inp_especie")
        add_row(2, "Raza:", "inp_raza")
        add_row(3, "Edad:", "inp_edad")
        add_row(4, "Peso:", "inp_peso")
        add_row(5, "Dueño:", "inp_dueno")

        grid.setRowStretch(7, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_board(self, parent_layout):
        board = QFrame(); board.setFixedWidth(350)
        board.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 10px;")
        vl = QVBoxLayout(board); vl.setContentsMargins(0,0,0,0); vl.setSpacing(0)

        h = QFrame(); h.setFixedHeight(60)
        h.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8)); border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom: none;")
        hl = QVBoxLayout(h); l = QLabel("Estado"); l.setAlignment(Qt.AlignmentFlag.AlignCenter); l.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background: transparent;")
        hl.addWidget(l)

        c = QFrame(); c.setStyleSheet("background: white; border-radius: 10px; border: none;")
        cl = QVBoxLayout(c); cl.setContentsMargins(20,20,20,20); cl.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.txt_notas = QLabel("Busca una mascota para ver información...")
        self.txt_notas.setWordWrap(True)
        self.txt_notas.setStyleSheet("color: #555; font-size: 16px;")
        
        cl.addWidget(self.txt_notas); cl.addStretch()
        vl.addWidget(h); vl.addWidget(c)
        parent_layout.addWidget(board, stretch=2)

    def buscar_mascota(self):
        id_mascota = self.inp_search.text().strip()
        if not id_mascota: return QMessageBox.warning(self, "Aviso", "Ingresa un ID.")
        
        self.limpiar_datos()

        if not DB_AVAILABLE: return

        try:
            cols = ["mascota.nombre", "mascota.especie", "mascota.raza", "mascota.edad", "mascota.peso",
                    "cliente.nombre", "cliente.apellido"]
            joins = "JOIN cliente ON mascota.fk_cliente = cliente.id_cliente"
            
            reg = self.conexion1.consultar_registro('mascota', 'id_mascota', id_mascota, cols, joins=joins)

            if reg:
                self.inp_nombre.setText(str(reg[0]))
                self.inp_especie.setText(str(reg[1]))
                self.inp_raza.setText(str(reg[2]))
                self.inp_edad.setText(str(reg[3]))
                self.inp_peso.setText(str(reg[4]) + " kg")
                self.inp_dueno.setText(f"{reg[5]} {reg[6]}")
                self.txt_notas.setText("Mascota encontrada. Verifique los datos.")
                QMessageBox.information(self, "Éxito", "Mascota cargada.")
            else:
                QMessageBox.warning(self, "Error", "Mascota no encontrada.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def limpiar_datos(self):
        for attr in ["inp_nombre", "inp_especie", "inp_raza", "inp_edad", "inp_peso", "inp_dueno"]:
            getattr(self, attr).setText("---")
        self.txt_notas.setText("...")

    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import EnfermeroMain
            self.menu = EnfermeroMain(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError: QMessageBox.warning(self, "Error", "No se encuentra el menú.")

    def abrir_ventana(self, categoria, opcion):
        try:
            target_window = None
            if categoria == "Citas" and opcion == "Visualizar": from UI_Cita_Enfermera import MainWindow as Win; target_window = Win(self.nombre_usuario)
            elif categoria == "Mascotas" and opcion == "Visualizar": pass # Ya estamos aquí
            elif categoria == "Inventario":
                if opcion == "Farmacia": from UI_Farmacia import MainWindow as Win; target_window = Win(self.nombre_usuario)
                elif opcion == "Hospitalización": from UI_Hospitalizacion import MainWindow as Win; target_window = Win(self.nombre_usuario)
            elif categoria == "Expediente": from UI_Diagnostico import MainWindow as Win; target_window = Win(self.nombre_usuario)

            if target_window: self.ventana = target_window; self.ventana.show(); self.close()
        except Exception as e: QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("TEST USER")
    window.show()
    sys.exit(app.exec())