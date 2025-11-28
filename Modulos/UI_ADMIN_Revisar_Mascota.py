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
                             QHBoxLayout, QPushButton, QLabel, QFrame, QMessageBox,
                             QScrollArea, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Revisar Mascota")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS ---
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC);
            }
            QWidget#WhitePanel {
                background-color: white;
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                /* Margen derecho reducido en el código Python */
                margin: 20px 0px 20px 0px; 
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif; color: #333;
            }
            /* Menú Lateral */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px; color: white;
                font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white;
            }
            QPushButton.sub-btn {
                text-align: left; padding-left: 40px;
                border-radius: 10px; color: #F0F0F0;
                background-color: rgba(0, 0, 0, 0.05); height: 35px;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
            
            /* Panel Info (Compatible con Hyprland) */
            QFrame#InfoBoard {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
            }
            QFrame.info-block {
                background-color: #FAFAFA;
                border-radius: 8px;
                border-left: 5px solid #FC7CE2;
            }
            QLabel.info-title { font-weight: bold; color: #FC7CE2; text-transform: uppercase; font-size: 13px; }
            QLabel.info-content { color: #444; font-size: 15px; margin-top: 2px; }
        """)

        # Inicialización de UI
        self.setup_sidebar()
        self.setup_main_panel()

        # --- CARGAR DATOS ---
        self.cargar_datos_completo()

    # ==========================================
    # --- 1. ESTRUCTURA VISUAL (UI) ---
    # ==========================================

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # Logo Placeholder
        lbl_logo = QLabel("YUNO VET")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        self.sidebar_layout.addWidget(lbl_logo)

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
        btn_logout.setStyleSheet("QPushButton { border: 2px solid white; border-radius: 15px; padding: 10px; color: white; font-weight: bold; background: transparent; } QPushButton:hover { background: rgba(255,255,255,0.2); }")
        btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)

        self.main_layout.addWidget(self.sidebar)

    def setup_accordion_group(self, title, options):
        btn = QPushButton(title)
        btn.setProperty("class", "menu-btn")
        self.sidebar_layout.addWidget(btn)
        frame = QFrame()
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(0, 0, 0, 10)
        for opt in options:
            sub = QPushButton(opt)
            sub.setProperty("class", "sub-btn")
            lay.addWidget(sub)
        frame.hide()
        self.sidebar_layout.addWidget(frame)
        btn.clicked.connect(lambda: frame.setVisible(not frame.isVisible()))

    def setup_main_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        
        # AJUSTE 1: Margen derecho reducido a 10 para pegar el contenido al borde
        # (Izquierda, Arriba, Derecha, Abajo)
        self.white_layout.setContentsMargins(40, 40, 10, 40)

        # Header
        header = QHBoxLayout()
        lbl = QLabel("Expediente de Mascota")
        lbl.setStyleSheet("font-size: 32px; font-weight: bold;")
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(40, 40)
        btn_close.clicked.connect(self.close)
        btn_close.setStyleSheet("background: #f0f0f0; border-radius: 20px; font-size: 20px; border: none;")
        
        header.addWidget(lbl)
        header.addStretch()
        header.addWidget(btn_close)
        self.white_layout.addLayout(header)
        self.white_layout.addSpacing(20)

        # Contenido dividido
        content = QHBoxLayout()
        # Aumentamos un poco el espacio entre las dos columnas principales
        content.setSpacing(50) 

        # Lado Izquierdo: Widget contenedor para datos básicos
        self.left_data_widget = QWidget()
        self.left_data_layout = QVBoxLayout(self.left_data_widget)
        self.left_data_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content.addWidget(self.left_data_widget, stretch=2) # Stretch ajustado

        # Lado Derecho: Widget contenedor para historial/info
        self.right_info_widget = QWidget()
        self.right_info_layout = QVBoxLayout(self.right_info_widget)
        
        # AJUSTE 2: Alinear el contenido de esta columna a la Derecha y al Centro Vertical
        self.right_info_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        content.addWidget(self.right_info_widget, stretch=3) # Stretch ajustado

        self.white_layout.addLayout(content)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- 2. RENDERIZADO DE DATOS ---
    # ==========================================

    def renderizar_datos_izquierda(self, data_dict):
        """Recibe un diccionario y crea los labels en el panel izquierdo."""
        while self.left_data_layout.count():
            item = self.left_data_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        # Foto/Inicial
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
        self.left_data_layout.addSpacing(30)

        # Generar Labels
        style_key = "font-size: 16px; color: #888; margin-bottom: 2px;"
        style_val = "font-size: 20px; color: #333; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #EEE; padding-bottom: 5px;"

        campos_orden = ["Nombre", "ID Paciente", "Edad", "Peso", "Especie", "Raza", "Sexo"]
        
        for key in campos_orden:
            if key in data_dict:
                lbl_k = QLabel(f"{key}:")
                lbl_k.setStyleSheet(style_key)
                lbl_v = QLabel(str(data_dict[key]))
                lbl_v.setStyleSheet(style_val)
                self.left_data_layout.addWidget(lbl_k)
                self.left_data_layout.addWidget(lbl_v)
        
        self.left_data_layout.addStretch()

    def renderizar_panel_derecho(self, lista_bloques):
        """Renderiza el panel derecho optimizado."""
        while self.right_info_layout.count():
            item = self.right_info_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        # Contenedor Marco
        board = QFrame()
        board.setObjectName("InfoBoard")
        # Ancho máximo para que no se estire demasiado en pantallas grandes,
        # manteniendo la información "centrada" visualmente en su bloque.
        board.setMaximumWidth(550) 
        
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)

        # Header degradado
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.9));
            border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom: none;
        """)
        head_lay = QHBoxLayout(header)
        lbl_tit = QLabel("Resumen Clínico")
        lbl_tit.setStyleSheet("color: white; font-weight: bold; font-size: 18px; border: none; background: transparent;")
        head_lay.addWidget(lbl_tit)
        board_lay.addWidget(header)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; } QWidget { background: white; }")

        content_widget = QWidget()
        content_lay = QVBoxLayout(content_widget)
        content_lay.setContentsMargins(25, 25, 25, 25)
        content_lay.setSpacing(15)

        # Crear tarjetas dinámicamente
        for bloque in lista_bloques:
            card = QFrame()
            card.setProperty("class", "info-block")
            card_lay = QVBoxLayout(card)
            card_lay.setContentsMargins(15, 12, 15, 12)
            
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

        # Al añadirlo, ya no necesitamos especificar alineación aquí porque
        # el layout padre (right_info_layout) ya tiene la alineación configurada.
        self.right_info_layout.addWidget(board)

    # ==========================================
    # --- 3. MÉTODOS DE BASE DE DATOS (PLACEHOLDERS) ---
    # ==========================================
    
    def cargar_datos_completo(self):
        """Función orquestadora que obtiene datos y actualiza la UI."""
        id_mascota_actual = 1092 
        
        # 1. Obtener datos crudos
        info_basica = self.db_get_info_basica(id_mascota_actual)
        info_clinica = self.db_get_historial_clinico(id_mascota_actual)

        # 2. Renderizar
        if info_basica:
            self.renderizar_datos_izquierda(info_basica)
        
        if info_clinica:
            self.renderizar_panel_derecho(info_clinica)

    def db_get_info_basica(self, id_mascota):
        # Simulación de retorno DB
        return {
            "Nombre": "Max",
            "ID Paciente": f"PET-{id_mascota}",
            "Edad": "4 Años",
            "Peso": "12.5 kg",
            "Especie": "Canino",
            "Raza": "Golden Retriever",
            "Sexo": "Macho"
        }

    def db_get_historial_clinico(self, id_mascota):
        # Simulación de retorno DB
        return [
            {
                "titulo": "Motivo de Consulta (Reciente)",
                "texto": "El paciente presenta decaimiento general y falta de apetito. Temperatura levemente elevada."
            },
            {
                "titulo": "Antecedentes",
                "texto": "Vacunación quíntuple vigente. Sin alergias medicamentosas conocidas."
            },
            {
                "titulo": "Signos Vitales",
                "texto": "Temp: 39.2°C | FC: 110 lpm | FR: 24 rpm | Mucosas: Rosadas."
            },
            {
                "titulo": "Plan Médico",
                "texto": "1. Realizar hemograma.\n2. Administrar antipirético.\n3. Observación 24h."
            }
        ]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())