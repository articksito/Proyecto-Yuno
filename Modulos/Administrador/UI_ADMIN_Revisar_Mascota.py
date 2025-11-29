import sys
import os

# --- CONFIGURACIÓN DE RUTAS PARA IMPORTACIONES ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)


from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# Si tienes un archivo db_connection.py, descomenta la siguiente línea:
# from db_connection import Conexion

class MainWindow(QMainWindow):
    # conexion1 = Conexion() # Descomentar cuando tengas la conexión real

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Revisar Mascota")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES (Mismo diseño que Cliente) ---
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
            
            /* --- MENU LATERAL --- */
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

            /* --- ESTILOS ESPECÍFICOS DE MASCOTA --- */
            /* Panel de Historial (Derecha) */
            QFrame#InfoBoard {
                background-color: white;
                border: 2px solid #E0E0E0; /* Borde sólido para compatibilidad */
                border-radius: 12px;
            }
            /* Tarjetas de información */
            QFrame.info-block {
                background-color: #FAFAFA;
                border-radius: 8px;
                border-left: 5px solid #FC7CE2;
            }
            QLabel.info-title { font-weight: bold; color: #FC7CE2; text-transform: uppercase; font-size: 13px; }
            QLabel.info-content { color: #444; font-size: 15px; margin-top: 2px; }
            
            /* Datos Izquierda */
            QLabel.label-key { font-size: 16px; color: #888; }
            QLabel.label-value { font-size: 20px; color: #333; font-weight: bold; border-bottom: 1px solid #EEE; padding-bottom: 5px;}
        """)

        # --- 1. BARRA LATERAL ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO ---
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- UI SETUP ---
    # ==========================================

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # --- LOGO ROBUSTO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)
         
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled)
            else:
                lbl_logo.setText("YUNO VET")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # Menús
        self.setup_accordion_group("Cita", ["Visualizar"])
        self.setup_accordion_group("Consulta", ["Visualizar"])
        self.setup_accordion_group("Mascota", ["Visualizar"])
        self.setup_accordion_group("Cliente", ["Visualizar"])
        self.setup_accordion_group("Hospitalizacion", ["Visualizar"])
        self.setup_accordion_group("Medicamentos", ["Visualizar", "Agregar"])
        self.setup_accordion_group("Usuarios", ["Agregar", "Modificar", "Visualizar"])
        self.setup_accordion_group("Especialidad", ["Agregar", "Modificar"])

        self.sidebar_layout.addStretch()

        # Botón Salir
        btn_logout = QPushButton("Cerrar Sesión")
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
        btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)

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
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.navegar(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # 1. Header
        header = QHBoxLayout()
        lbl_header = QLabel("Expediente de Mascota")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-size: 16px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #E0E0E0; color: #333; }
        """)
        btn_back.clicked.connect(self.close)

        header.addWidget(lbl_header)
        header.addStretch()
        header.addWidget(btn_back)
        self.white_layout.addLayout(header)
        self.white_layout.addSpacing(20)

        # 2. Barra de Búsqueda (Estilo Cliente)
        self.setup_search_bar()
        self.white_layout.addSpacing(30)

        # 3. Contenedor de Información (Dividido)
        content_split = QHBoxLayout()
        content_split.setSpacing(50)

        # --- A. Izquierda: Datos Mascota ---
        self.left_data_widget = QWidget()
        self.left_data_layout = QVBoxLayout(self.left_data_widget)
        self.left_data_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_split.addWidget(self.left_data_widget, stretch=2)

        # --- B. Derecha: Historial Clínico ---
        self.right_info_widget = QWidget()
        self.right_info_layout = QVBoxLayout(self.right_info_widget)
        self.right_info_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        content_split.addWidget(self.right_info_widget, stretch=3)

        self.white_layout.addLayout(content_split)
        self.white_layout.addStretch()

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_search = QLabel("ID Mascota:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        
        self.inp_id = QLineEdit()
        self.inp_id.setPlaceholderText("Ej: 1092")
        self.inp_id.setFixedWidth(250)
        self.inp_id.setStyleSheet("""
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
        search_layout.addWidget(self.inp_id)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_container)

    # ==========================================
    # --- LOGICA Y RENDERIZADO ---
    # ==========================================

    def buscar_mascota(self):
        id_mascota = self.inp_id.text().strip()
        
        if not id_mascota:
            QMessageBox.warning(self, "Aviso", "Ingresa un ID de mascota.")
            return

        print(f"Buscando mascota ID: {id_mascota}")
        
        # 1. Obtener Datos (Conexión BD)
        info_basica = self.db_get_info_basica(id_mascota)
        
        if info_basica:
            # 2. Renderizar Datos Básicos
            self.renderizar_datos_izquierda(info_basica)
            
            # 3. Obtener y Renderizar Historial
            historial = self.db_get_historial_clinico(id_mascota)
            if historial:
                self.renderizar_panel_derecho(historial)
            else:
                self.limpiar_panel_derecho() # Si existe pero no tiene historial
                
            QMessageBox.information(self, "Éxito", "Mascota encontrada.")
        else:
            QMessageBox.warning(self, "Error", "Mascota no encontrada en la base de datos.")
            self.limpiar_todo()

    def renderizar_datos_izquierda(self, data_dict):
        # Limpiar layout
        while self.left_data_layout.count():
            item = self.left_data_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        # Foto / Inicial
        frame_img = QFrame()
        frame_img.setFixedSize(100, 100)
        frame_img.setStyleSheet("background: #EEE; border-radius: 50px; border: 2px solid #FC7CE2;")
        lay_img = QVBoxLayout(frame_img)
        initial = data_dict.get("Nombre", "?")[0]
        lbl_img = QLabel(initial)
        lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_img.setStyleSheet("font-size: 40px; color: #FC7CE2; font-weight: bold; border: none;")
        lay_img.addWidget(lbl_img)
        
        self.left_data_layout.addWidget(frame_img, alignment=Qt.AlignmentFlag.AlignCenter)
        self.left_data_layout.addSpacing(20)

        # Campos
        campos_orden = ["Nombre", "ID Paciente", "Edad", "Peso", "Especie", "Raza", "Sexo"]
        for key in campos_orden:
            if key in data_dict:
                lbl_k = QLabel(f"{key}:")
                lbl_k.setProperty("class", "label-key")
                lbl_v = QLabel(str(data_dict[key]))
                lbl_v.setProperty("class", "label-value")
                self.left_data_layout.addWidget(lbl_k)
                self.left_data_layout.addWidget(lbl_v)
        
        self.left_data_layout.addStretch()

    def renderizar_panel_derecho(self, lista_bloques):
        self.limpiar_panel_derecho()

        # Contenedor Marco
        board = QFrame()
        board.setObjectName("InfoBoard")
        board.setMaximumWidth(550) 
        
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)

        # Header Board
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.9));
            border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom: none;
        """)
        head_lay = QHBoxLayout(header)
        lbl_tit = QLabel("Resumen Clínico")
        lbl_tit.setStyleSheet("color: white; font-weight: bold; font-size: 16px; border: none; background: transparent;")
        head_lay.addWidget(lbl_tit)
        board_lay.addWidget(header)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; } QWidget { background: white; }")

        content_widget = QWidget()
        content_lay = QVBoxLayout(content_widget)
        content_lay.setContentsMargins(20, 20, 20, 20)
        content_lay.setSpacing(15)

        for bloque in lista_bloques:
            card = QFrame()
            card.setProperty("class", "info-block")
            card_lay = QVBoxLayout(card)
            card_lay.setContentsMargins(15, 10, 15, 10)
            
            l_tit = QLabel(bloque['titulo'])
            l_tit.setProperty("class", "info-title")
            
            l_txt = QLabel(bloque['texto'])
            l_txt.setProperty("class", "info-content")
            l_txt.setWordWrap(True)

            card_lay.addWidget(l_tit)
            card_lay.addWidget(l_txt)
            content_lay.addWidget(card)

        content_lay.addStretch()
        scroll.setWidget(content_widget)
        board_lay.addWidget(scroll)

        self.right_info_layout.addWidget(board)

    def limpiar_panel_derecho(self):
        while self.right_info_layout.count():
            item = self.right_info_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def limpiar_todo(self):
        while self.left_data_layout.count():
            item = self.left_data_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self.limpiar_panel_derecho()

    # ==========================================
    # --- FUNCIONES DE BASE DE DATOS (BD) ---
    # ==========================================
    
    def db_get_info_basica(self, id_mascota):
        """
        TODO: Reemplazar con tu consulta SQL real.
        Ej: cursor.execute("SELECT nombre, raza, ... FROM mascota WHERE id=%s", (id_mascota,))
        """
        # --- SIMULACIÓN ---
        # Si el ID es 1092 devolvemos datos, si no, None
        if id_mascota == "1092":
            return {
                "Nombre": "Max",
                "ID Paciente": f"PET-{id_mascota}",
                "Edad": "4 Años",
                "Peso": "12.5 kg",
                "Especie": "Canino",
                "Raza": "Golden Retriever",
                "Sexo": "Macho"
            }
        return None

    def db_get_historial_clinico(self, id_mascota):
        """
        TODO: Reemplazar con consulta SQL a tabla de consultas/historial.
        Retornar lista de diccionarios.
        """
        # --- SIMULACIÓN ---
        return [
            {
                "titulo": "Motivo de Consulta (Reciente)",
                "texto": "El paciente presenta decaimiento general y falta de apetito. Temperatura levemente elevada."
            },
            {
                "titulo": "Antecedentes",
                "texto": "Vacunación quíntuple vigente. Sin alergias conocidas."
            },
            {
                "titulo": "Plan Médico",
                "texto": "1. Realizar hemograma.\n2. Administrar antipirético."
            }
        ]

    # ==========================================
    # --- UTILIDADES ---
    # ==========================================
    
    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def navegar(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        # Aquí puedes importar tus otras ventanas y mostrarlas

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())