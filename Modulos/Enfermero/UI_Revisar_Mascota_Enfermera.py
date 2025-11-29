import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, 
                             QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# --- AJUSTE DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) # Subir un nivel a 'Modulos'
if current_dir not in sys.path: sys.path.append(current_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)

# Intentar importar conexión
try:
    from db_connection import Conexion
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

class MainWindow(QMainWindow):
    # 1. RECIBIMOS EL NOMBRE
    def __init__(self, nombre_usuario="Enfermero"):
        super().__init__()
        
        # 2. GUARDAMOS EL NOMBRE
        self.nombre_usuario = nombre_usuario
        
        self.setWindowTitle(f"Sistema Veterinario Yuno - Revisar Mascota ({self.nombre_usuario})")
        self.resize(1280, 720)
        
        if DB_AVAILABLE:
            self.conexion1 = Conexion()

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES ---
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            QPushButton.menu-btn { text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; color: white; font-family: 'Segoe UI', sans-serif; font-weight: bold; font-size: 18px; background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px; }
            QPushButton.menu-btn:hover { background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; }
            QPushButton.sub-btn { text-align: left; font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: normal; padding-left: 40px; border-radius: 10px; color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05); height: 35px; margin-bottom: 2px; margin-left: 10px; margin-right: 10px; }
            QPushButton.sub-btn:hover { color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; }
        """)

        # --- Sidebar ---
        self.setup_sidebar()

        # --- PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Revisar Mascota")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()

        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # BARRA DE BÚSQUEDA
        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        # Contenedor Principal de Datos
        content_layout = QHBoxLayout()
        content_layout.setSpacing(50)

        self.setup_pet_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addLayout(content_layout)
        self.white_layout.addStretch()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        # --- LOGO ROBUSTO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ruta_logo = os.path.join(parent_dir, "FILES", "logo_yuno.png")
        
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                lbl_logo.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        
        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # Menús
        self.setup_accordion_group("Citas", ["Visualizar"])
        self.setup_accordion_group("Mascotas", ["Visualizar"])
        self.setup_accordion_group("Inventario", ["Farmacia", "Hospitalización"])
        self.setup_accordion_group("Expediente", ["Diagnóstico"])

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

        frame_options = QFrame()
        layout_options = QVBoxLayout(frame_options)
        layout_options.setContentsMargins(0, 0, 0, 10)
        layout_options.setSpacing(2)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # --- CONEXIÓN DE NAVEGACIÓN DIRECTA ---
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.abrir_ventana(t, o))
            
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_search = QLabel("ID Mascota:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Ej: 101")
        self.inp_search.setFixedWidth(300)
        self.inp_search.setStyleSheet("QLineEdit { border: 2px solid #ddd; border-radius: 10px; padding: 8px 15px; font-size: 16px; color: #333; background-color: #F9F9F9; }")
        
        btn_search = QPushButton("Buscar")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setFixedSize(120, 40)
        btn_search.setStyleSheet("QPushButton { background-color: #7CEBFC; color: #333; font-weight: bold; font-size: 16px; border-radius: 10px; border: 1px solid #5CD0E3; } QPushButton:hover { background-color: #5CD0E3; }")
        btn_search.clicked.connect(self.buscar_mascota)
        
        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.inp_search)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_container)

    def setup_pet_form(self, parent_layout):
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        readonly_style = "QLineEdit { background-color: #F0F0F0; border: 1px solid #DDD; border-radius: 10px; padding: 5px 15px; font-size: 18px; color: #555; height: 40px; }"
        label_style = "font-size: 20px; color: #666; font-weight: 400;"

        def add_row(row, label_text, attr_name):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            inp = QLineEdit()
            inp.setReadOnly(True)
            inp.setText("---")
            inp.setStyleSheet(readonly_style)
            setattr(self, attr_name, inp)
            grid_layout.addWidget(lbl, row, 0)
            grid_layout.addWidget(inp, row, 1)

        add_row(0, "Nombre:", "inp_nombre")
        add_row(1, "Especie:", "inp_especie")
        add_row(2, "Raza:", "inp_raza")
        add_row(3, "Sexo:", "inp_sexo")
        add_row(4, "Edad:", "inp_edad")
        add_row(5, "Peso:", "inp_peso")
        add_row(6, "Dueño:", "inp_dueno")

        grid_layout.setRowStretch(7, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_board(self, parent_layout):
        board_container = QFrame()
        board_container.setFixedWidth(400)
        board_container.setStyleSheet("QFrame { background-color: white; border: 1px solid #CCC; border-radius: 10px; }")
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8)); border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom: none;")
        header_layout = QVBoxLayout(header_frame)
        lbl_info_title = QLabel("Notas Veterinarias")
        lbl_info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info_title.setStyleSheet("color: white; font-size: 22px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(lbl_info_title)

        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(30, 30, 30, 30)
        
        self.txt_notas = QLabel("Busca una mascota para ver información...")
        self.txt_notas.setWordWrap(True)
        self.txt_notas.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.txt_notas.setStyleSheet("color: #555; font-size: 16px; border: none; line-height: 1.4;")
        
        content_layout.addWidget(self.txt_notas)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)

        parent_layout.addWidget(board_container, stretch=2)

    def buscar_mascota(self):
        id_mascota = self.inp_search.text().strip()
        if not id_mascota:
            QMessageBox.warning(self, "Aviso", "Ingresa un ID de mascota.")
            return

        if not DB_AVAILABLE:
            QMessageBox.critical(self, "Error", "No hay conexión a la base de datos.")
            return

        try:
            columnas = [
                "mascota.nombre", "mascota.especie", "mascota.raza", 
                "mascota.sexo", "mascota.edad", "mascota.peso",
                "cliente.nombre", "cliente.apellido"
            ]
            joins = "JOIN cliente ON mascota.fk_cliente = cliente.id_cliente"
            
            registro = self.conexion1.consultar_registro(
                tabla='mascota', 
                id_columna='id_mascota', 
                id_valor=id_mascota,
                columnas=columnas,
                joins=joins
            )

            if registro:
                self.inp_nombre.setText(str(registro[0]))
                self.inp_especie.setText(str(registro[1]))
                self.inp_raza.setText(str(registro[2]))
                self.inp_sexo.setText(str(registro[3]))
                self.inp_edad.setText(str(registro[4]))
                self.inp_peso.setText(str(registro[5]) + " kg")
                self.inp_dueno.setText(f"{registro[6]} {registro[7]}")
                self.txt_notas.setText("Información cargada exitosamente.")
            else:
                self.limpiar_datos()
                QMessageBox.warning(self, "No encontrado", "No existe mascota con ese ID.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al buscar: {e}")

    def limpiar_datos(self):
        self.inp_nombre.setText("---")
        self.inp_especie.setText("---")
        self.inp_raza.setText("---")
        self.inp_sexo.setText("---")
        self.inp_edad.setText("---")
        self.inp_peso.setText("---")
        self.inp_dueno.setText("---")
        self.txt_notas.setText("...")

    # --- NAVEGACIÓN ---
    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import EnfermeroMain
            self.menu = EnfermeroMain(self.nombre_usuario) # DEVOLVEMOS EL NOMBRE
            self.menu.show()
            self.close()
        except ImportError:
            QMessageBox.warning(self, "Error", "No se encuentra el menú de enfermera.")

    # --- FUNCION DE NAVEGACIÓN DIRECTA (ROUTER) ---
    def abrir_ventana(self, categoria, opcion):
        try:
            target_window = None

            if categoria == "Citas" and opcion == "Visualizar":
                from UI_Cita_Enfermera import MainWindow as Win
                target_window = Win(self.nombre_usuario) # PASAR NOMBRE
            
            elif categoria == "Mascotas" and opcion == "Visualizar":
                pass # Ya estamos aquí
            
            elif categoria == "Inventario":
                if opcion == "Farmacia":
                    from UI_Farmacia import MainWindow as Win
                    target_window = Win(self.nombre_usuario) # PASAR NOMBRE
                elif opcion == "Hospitalización":
                    from UI_Hospitalizacion import MainWindow as Win
                    target_window = Win(self.nombre_usuario) # PASAR NOMBRE
            
            elif categoria == "Expediente" and opcion == "Diagnóstico":
                from UI_Diagnostico import MainWindow as Win
                target_window = Win(self.nombre_usuario) # PASAR NOMBRE

            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close() 
            
        except ImportError as e:
            QMessageBox.warning(self, "Error", f"No se encuentra el archivo de destino.\n{e}")
        except Exception as e:
            print(f"Error navegando: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("TEST USER")
    window.show()
    sys.exit(app.exec())