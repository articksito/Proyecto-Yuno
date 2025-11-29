import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout, QScrollArea) # Agregamos QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIntValidator

# --- 1. CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- 2. IMPORTACIONES ---
try:
    from db_connection import Conexion
    from UI_REP_main import MainWindow as MenuPrincipal 
except ImportError:
    class Conexion:
        def consultar_registro(self, *args, **kwargs): return None
    class MenuPrincipal(QMainWindow):
        def __init__(self, u): super().__init__(); self.show()

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.ventana = None 

        self.setWindowTitle(f"Sistema Veterinario Yuno - Revisar Cita ({self.nombre_usuario})")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600) # Evita que se haga muy pequeña

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS ---
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            
            /* Botones del Menú Lateral (Estilo Unificado) */
            QPushButton.menu-btn { 
                text-align: left; padding-left: 20px; 
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; 
                color: white; font-weight: bold; font-size: 18px; 
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px; 
            }
            QPushButton.menu-btn:hover { background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; }
            
            /* Sub-botones (Estilo Unificado) */
            QPushButton.sub-btn { 
                text-align: left; padding-left: 40px; 
                border-radius: 10px; color: #F0F0F0; font-size: 16px;
                background-color: rgba(0, 0, 0, 0.05); height: 35px; margin: 2px 10px; 
            }
            QPushButton.sub-btn:hover { color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; }
            
            /* ScrollArea Transparente */
            QScrollArea { background: transparent; border: none; }
            QScrollArea > QWidget > QWidget { background: transparent; }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # --- NAVEGACIÓN ---
    def return_to_menu(self):
        try:
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except Exception:
            self.close()

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        # Margen inferior 50 para subir el botón volver
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
                border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 20px;
                font-size: 14px; color: white; font-weight: bold; background-color: transparent;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.2); }
        """)
        self.sidebar_layout.addStretch()
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
        btn_main.clicked.connect(lambda: frame.setVisible(not frame.isVisible()))

    def abrir_ventana(self, categoria, opcion):
        if categoria == "Citas" and opcion == "Visualizar": return

        mapa = {
            "Citas": {"Agendar": "UI_REP_Crear_cita", "Visualizar": "UI_REP_Revisar_Cita", "Modificar": "UI_REP_Modificar_cita"},
            "Mascotas": {"Registrar": "UI_REP_Registrar_mascota", "Visualizar": "UI_Revisar_Mascota", "Modificar": "UI_REP_Modificar_Mascota"},
            "Clientes": {"Registrar": "UI_REP_Registra_cliente", "Visualizar": "UI_Revisar_cliente", "Modificar": "UI_REP_Modificar_cliente"}
        }
        
        archivo = mapa.get(categoria, {}).get(opcion)
        if archivo:
            try:
                module = __import__(archivo, fromlist=['MainWindow'])
                self.ventana = module.MainWindow(self.nombre_usuario)
                self.ventana.show()
                self.close()
            except ImportError as e:
                QMessageBox.warning(self, "Error", f"Falta archivo: {archivo}.py\n{e}")
        else:
            print(f"Ruta no mapeada: {categoria} -> {opcion}")

    # --- PANEL DE CONTENIDO ---
    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        
        # Layout principal del panel blanco
        main_white_layout = QVBoxLayout(self.white_panel)
        main_white_layout.setContentsMargins(50, 30, 50, 40)

        # 1. HEADER
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Visualizar Cita")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        # Botón cerrar vista (X) - Opcional, ya que tenemos volver en sidebar
    

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        
        main_white_layout.addLayout(header_layout)
        main_white_layout.addSpacing(20)

        # 2. SCROLL AREA (SOLUCIÓN PARA PANTALLAS PEQUEÑAS)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 10, 0) # Margen derecho para el scrollbar

        # --- CONTENIDO SCROLLABLE ---
        
        # Barra de Búsqueda
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0,0,0,0)
        
        lbl_s = QLabel("ID Cita:"); lbl_s.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        self.inp_search = QLineEdit(); self.inp_search.setPlaceholderText("ID..."); self.inp_search.setFixedWidth(200)
        # ESTILO CAMBIADO A TEXTO NEGRO SOBRE BLANCO PARA LEGIBILIDAD
        self.inp_search.setStyleSheet("color: #333; background-color: #F0F0F0 ; border: 2px solid #ddd; border-radius: 10px; padding: 5px 15px; font-size: 16px;")
        self.inp_search.setValidator(QIntValidator())

        btn_s = QPushButton("Buscar"); btn_s.setFixedSize(100, 40); btn_s.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_s.setStyleSheet("background-color: #7CEBFC; font-weight: bold; border-radius: 10px; border: 1px solid #5CD0E3;")
        btn_s.clicked.connect(self.buscar_cita)

        search_layout.addWidget(lbl_s); search_layout.addWidget(self.inp_search); search_layout.addWidget(btn_s); search_layout.addStretch()
        scroll_layout.addWidget(search_container)
        scroll_layout.addSpacing(30)

        # Contenedor Horizontal (Formulario + Info)
        data_container = QWidget()
        data_layout = QHBoxLayout(data_container)
        data_layout.setContentsMargins(0,0,0,0); data_layout.setSpacing(40)
        data_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setup_details_form(data_layout)
        self.setup_info_board(data_layout)

        scroll_layout.addWidget(data_container)
        scroll_layout.addStretch() # Empuja todo hacia arriba

        # --- FIN CONTENIDO SCROLLABLE ---

        scroll.setWidget(scroll_content)
        main_white_layout.addWidget(scroll)

    def setup_details_form(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20); grid.setHorizontalSpacing(20)
        
        style_ro = "background-color: #F0F0F0; border: 1px solid #DDD; border-radius: 10px; padding: 5px 15px; font-size: 18px; color: #555; height: 40px;"
        style_lbl = "font-size: 18px; font-weight: bold; color: #333;"

        # Campos
        self.inp_fecha = QLineEdit(); self.inp_fecha.setReadOnly(True); self.inp_fecha.setStyleSheet(style_ro)
        self.inp_hora = QLineEdit(); self.inp_hora.setReadOnly(True); self.inp_hora.setStyleSheet(style_ro)
        self.inp_estado = QLineEdit(); self.inp_estado.setReadOnly(True); self.inp_estado.setStyleSheet(style_ro)
        self.inp_mascota = QLineEdit(); self.inp_mascota.setReadOnly(True); self.inp_mascota.setStyleSheet(style_ro)
        self.inp_cliente = QLineEdit(); self.inp_cliente.setReadOnly(True); self.inp_cliente.setStyleSheet(style_ro)
        self.inp_vet = QLineEdit(); self.inp_vet.setReadOnly(True); self.inp_vet.setStyleSheet(style_ro)

        def add_row(r, label, widget):
            l = QLabel(label); l.setStyleSheet(style_lbl)
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
        board.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 15px;")
        vl = QVBoxLayout(board); vl.setContentsMargins(0,0,0,0); vl.setSpacing(0)

        # Header Degradado
        h = QFrame(); h.setFixedHeight(60)
        h.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8)); border-top-left-radius: 15px; border-top-right-radius: 15px; border-bottom: none;")
        hl = QVBoxLayout(h); lbl = QLabel("Motivo / Detalles"); lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); lbl.setStyleSheet("color: white; font-size: 18px; font-weight: bold; background: transparent; border: none;")
        hl.addWidget(lbl)

        # Content Board
        c = QFrame(); c.setStyleSheet("background: white; border-radius: 15px; border: none;")
        cl = QVBoxLayout(c); cl.setContentsMargins(20,20,20,20); cl.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.lbl_motivo = QLabel("Ingrese un ID para buscar..."); self.lbl_motivo.setWordWrap(True)
        self.lbl_motivo.setStyleSheet("font-size: 16px; color: #555;")
        
        cl.addWidget(self.lbl_motivo); cl.addStretch()
        vl.addWidget(h); vl.addWidget(c)
        parent_layout.addWidget(board, stretch=1)

    # --- LÓGICA DE BÚSQUEDA ---
    def buscar_cita(self):
        id_cita = self.inp_search.text().strip()
        if not id_cita: return QMessageBox.warning(self, "Aviso", "Ingresa un ID de cita.")

        self.limpiar_datos()
        
        try:
            cols = ["cita.fecha", "cita.hora", "cita.motivo", "cita.estado", 
                    "mascota.nombre", "cliente.nombre", "cliente.apellido", "usuario.nombre", "usuario.apellido"]
            
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
                self.inp_vet.setText(f"Dr. {registro[7]} {registro[8]}")
                QMessageBox.information(self, "Éxito", "Cita encontrada.")
            else:
                QMessageBox.warning(self, "Error", f"No se encontró la cita ID {id_cita}")

        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"Error en la consulta: {e}")

    def limpiar_datos(self):
        for w in [self.inp_fecha, self.inp_hora, self.inp_estado, self.inp_mascota, self.inp_cliente, self.inp_vet]:
            w.clear()
        self.lbl_motivo.setText("...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("Test User")
    window.show()
    sys.exit(app.exec())