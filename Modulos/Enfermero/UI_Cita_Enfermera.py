import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout)
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
        def consultar_registro(self, *args): return None

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Enfermero"):
        super().__init__()
        
        self.nombre_usuario = nombre_usuario
        self.setWindowTitle(f"Sistema Veterinario Yuno - Revisar Cita ({self.nombre_usuario})")
        self.resize(1280, 720)
        # 1. TAMAÑO MÍNIMO (Para evitar miniatura)
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
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            
            /* Botones Menú */
            QPushButton.menu-btn { text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; color: white; font-weight: bold; font-size: 18px; background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px; }
            QPushButton.menu-btn:hover { background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; }
            QPushButton.sub-btn { text-align: left; padding-left: 40px; border-radius: 10px; color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05); height: 35px; margin: 2px 10px; }
            QPushButton.sub-btn:hover { color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; }
            
            /* Inputs Solo Lectura */
            QLineEdit { background-color: #F0F0F0; border: 1px solid #DDD; border-radius: 10px; padding: 5px 15px; font-size: 16px; color: #555; height: 40px; }
        """)

        self.setup_sidebar()

        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Revisar Cita")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        self.white_layout.addLayout(header_layout)
        self.white_layout.addStretch(1)

        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setup_details_form(content_layout)
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

        # 3. EL RESORTE MÁGICO (Para que el botón no desaparezca)
        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Volver al Menú")
        btn_logout.setStyleSheet("QPushButton { text-align: center; border: 2px solid white; border-radius: 15px; padding: 10px; font-size: 14px; color: white; font-weight: bold; background-color: transparent; } QPushButton:hover { background-color: rgba(255,255,255,0.2); }")
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
        self.inp_search.setPlaceholderText("ID Cita...")
        # Estilo específico para el buscador (Rosa suave)
        self.inp_search.setStyleSheet("background-color: rgba(241, 131, 227, 0.15); border: 1px solid #DDD; border-radius: 10px; padding: 5px 15px; font-size: 16px; color: #333;")
        self.inp_search.setFixedWidth(250)

        btn_search = QPushButton("Buscar")
        btn_search.setFixedSize(100, 40)
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("QPushButton { background-color: #7CEBFC; color: #333; border-radius: 10px; font-weight: bold; border: 1px solid #5CD0E3; } QPushButton:hover { background-color: #5CD0E3; }")
        btn_search.clicked.connect(self.buscar_cita)

        search_layout.addWidget(QLabel("ID Cita:", styleSheet="font-weight: bold; font-size: 16px; color: #555;"))
        search_layout.addWidget(self.inp_search)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_frame)

    def setup_details_form(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(20)

        self.inp_fecha = QLineEdit(); self.inp_fecha.setReadOnly(True)
        self.inp_hora = QLineEdit(); self.inp_hora.setReadOnly(True)
        self.inp_estado = QLineEdit(); self.inp_estado.setReadOnly(True)
        self.inp_mascota = QLineEdit(); self.inp_mascota.setReadOnly(True)
        self.inp_cliente = QLineEdit(); self.inp_cliente.setReadOnly(True)
        self.inp_vet = QLineEdit(); self.inp_vet.setReadOnly(True)

        def add_row(r, label, widget):
            l = QLabel(label); l.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
            grid.addWidget(l, r, 0); grid.addWidget(widget, r, 1)

        add_row(0, "Fecha:", self.inp_fecha)
        add_row(1, "Hora:", self.inp_hora)
        add_row(2, "Estado:", self.inp_estado)
        add_row(3, "Mascota:", self.inp_mascota)
        add_row(4, "Cliente:", self.inp_cliente)
        add_row(5, "Veterinario:", self.inp_vet)

        parent_layout.addWidget(form_widget, stretch=2)

    def setup_info_board(self, parent_layout):
        board = QFrame(); board.setFixedWidth(350)
        board.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 10px;")
        vl = QVBoxLayout(board); vl.setContentsMargins(0,0,0,0); vl.setSpacing(0)

        h = QFrame(); h.setFixedHeight(60)
        h.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252,124,226,0.8)); border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom: none;")
        hl = QVBoxLayout(h); l = QLabel("Motivo / Detalles"); l.setAlignment(Qt.AlignmentFlag.AlignCenter); l.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background: transparent;")
        hl.addWidget(l)

        c = QFrame(); c.setStyleSheet("background: white; border-radius: 10px; border: none;")
        cl = QVBoxLayout(c); cl.setContentsMargins(20,20,20,20); cl.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.lbl_motivo = QLabel("Ingrese un ID para ver detalles..."); self.lbl_motivo.setWordWrap(True)
        self.lbl_motivo.setStyleSheet("font-size: 16px; color: #555;")
        
        cl.addWidget(self.lbl_motivo); cl.addStretch()
        vl.addWidget(h); vl.addWidget(c)
        parent_layout.addWidget(board, stretch=1)

    def buscar_cita(self):
        id_cita = self.inp_search.text().strip()
        if not id_cita: return QMessageBox.warning(self, "Aviso", "Ingresa un ID.")
        
        self.limpiar_datos()

        if not DB_AVAILABLE: return

        try:
            cols = ["cita.fecha", "cita.hora", "cita.motivo", "cita.estado", 
                    "mascota.nombre", "cliente.nombre", "cliente.apellido", 
                    "usuario.nombre", "usuario.apellido"]
            
            joins = """
                JOIN mascota ON cita.fk_mascota = mascota.id_mascota
                JOIN cliente ON mascota.fk_cliente = cliente.id_cliente
                JOIN veterinario ON cita.fk_veterinario = veterinario.id_veterinario
                JOIN usuario ON veterinario.fk_usuario = usuario.id_usuario
            """

            registro = self.conexion1.consultar_registro('cita', 'cita.id_cita', id_cita, cols, joins=joins)

            if registro:
                self.inp_fecha.setText(str(registro[0]))
                self.inp_hora.setText(str(registro[1]))
                self.lbl_motivo.setText(str(registro[2]))
                self.inp_estado.setText(str(registro[3]))
                self.inp_mascota.setText(str(registro[4]))
                self.inp_cliente.setText(f"{registro[5]} {registro[6]}")
                
                nom_vet = str(registro[7])
                if len(registro) > 8: nom_vet += f" {registro[8]}"
                self.inp_vet.setText(f"Dr. {nom_vet}")
                
                QMessageBox.information(self, "Éxito", "Cita encontrada.")
            else:
                QMessageBox.warning(self, "Aviso", "No encontrada.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def limpiar_datos(self):
        for w in [self.inp_fecha, self.inp_hora, self.inp_estado, self.inp_mascota, self.inp_cliente, self.inp_vet]:
            w.clear()
        self.lbl_motivo.setText("...")

    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import EnfermeroMain
            self.menu = EnfermeroMain(self.nombre_usuario) 
            self.menu.show(); self.close()
        except ImportError: QMessageBox.warning(self, "Error", "No se encuentra el menú.")

    def abrir_ventana(self, categoria, opcion):
        if categoria == "Citas" and opcion == "Visualizar": return
        try:
            target = None
            if categoria == "Mascotas": from UI_Revisar_Mascota_Enfermera import MainWindow as Win; target = Win(self.nombre_usuario)
            elif categoria == "Inventario" and opcion == "Farmacia": from UI_Farmacia import MainWindow as Win; target = Win(self.nombre_usuario)
            elif categoria == "Inventario" and opcion == "Hospitalización": from UI_Hospitalizacion import MainWindow as Win; target = Win(self.nombre_usuario)
            elif categoria == "Expediente": from UI_Diagnostico import MainWindow as Win; target = Win(self.nombre_usuario)

            if target: self.ventana = target; self.ventana.show(); self.close()
        except Exception as e: QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("TEST USER")
    window.show()
    sys.exit(app.exec())