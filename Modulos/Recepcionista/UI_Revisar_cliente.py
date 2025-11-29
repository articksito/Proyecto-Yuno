import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- IMPORTACIONES ---
try:
    from UI_REP_main import MainWindow as MenuPrincipal
except ImportError:
    class MenuPrincipal(QMainWindow):
        def __init__(self, u): super().__init__(); self.show()

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.ventana = None 

        self.setWindowTitle("Sistema Veterinario Yuno - Revisar Cliente")
        
        # 1. TAMAÑO MÍNIMO (Igual que en Mascotas para evitar el error de miniatura)
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
                font-family: 'Segoe UI', sans-serif;
                color: #333;
            }
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
            /* Estilos de Datos */
            QLabel.label-key {
                font-size: 18px; color: #666; font-weight: normal; margin-bottom: 2px;
            }
            QLabel.label-value {
                font-size: 22px; color: #000; font-weight: bold; padding-bottom: 10px; border-bottom: 1px solid #EEE;
            }
        """)

        # 1. Barra Lateral
        self.setup_sidebar()

        # 2. Panel Blanco
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        # Márgenes optimizados
        self.white_layout.setContentsMargins(50, 30, 50, 30)

        # Header (Solo título)
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Revisar Cliente")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # Contenedor Principal de Datos
        content_layout = QHBoxLayout()
        content_layout.setSpacing(50)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Alineación superior clave

        # Columna Izquierda (Datos Cliente)
        self.setup_client_data(content_layout)

        # Columna Derecha (Foto + Notas)
        self.setup_right_panel(content_layout)

        self.white_layout.addLayout(content_layout)
        self.white_layout.addStretch() 

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # --- NAVEGACIÓN ---
    def return_to_menu(self):
        try:
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except Exception as e:
            print(f"Error al volver al menú: {e}")
            self.close()

    def abrir_ventana(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        
        if categoria == "Clientes" and opcion == "Visualizar": return 

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

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        # Margen inferior ajustado (30) para asegurar visibilidad del botón volver
        self.sidebar_layout.setContentsMargins(20, 40, 20, 30) 
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

        self.sidebar_layout.addStretch()

        # Botón Volver al Menú
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setStyleSheet("""
            QPushButton {
                border: 2px solid white; 
                border-radius: 15px; 
                padding: 10px; 
                margin-top: 10px;
                font-size: 14px; 
                color: white; 
                font-weight: bold; 
                background-color: transparent;
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
        btn_main.clicked.connect(lambda: frame.setVisible(not frame.isVisible()))

    def setup_client_data(self, parent_layout):
        data_widget = QWidget()
        data_layout = QVBoxLayout(data_widget)
        data_layout.setSpacing(15)
        data_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Datos de ejemplo del Cliente
        client_data = [
            ("ID Cliente:", "CLI-8832"),
            ("Nombre:", "Juan"),
            ("Apellido:", "Pérez"),
            ("Correo:", "juan.perez@mail.com"),
            ("Dirección:", "Av. Siempre Viva 123"),
            ("Teléfono:", "555-0199")
        ]

        for key, value in client_data:
            lbl_k = QLabel(key)
            lbl_k.setProperty("class", "label-key")
            lbl_v = QLabel(value)
            lbl_v.setProperty("class", "label-value")
            data_layout.addWidget(lbl_k)
            data_layout.addWidget(lbl_v)

        parent_layout.addWidget(data_widget, stretch=3)

    def setup_right_panel(self, parent_layout):
        """Configura el panel derecho con la Foto arriba y la Info abajo."""
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setSpacing(20)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- 1. SECCIÓN FOTO (ARRIBA) ---
        photo_container = QWidget()
        photo_layout = QVBoxLayout(photo_container)
        photo_layout.setContentsMargins(0,0,0,0)
        photo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Círculo Gris (Placeholder de Foto de Cliente)
        lbl_photo = QLabel("👤") 
        lbl_photo.setFixedSize(140, 140)
        lbl_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_photo.setStyleSheet("""
            background-color: #E0E0E0; 
            border-radius: 70px;
            font-size: 60px;
            color: #999;
        """)
        
        lbl_photo_text = QLabel("Foto de Perfil")
        lbl_photo_text.setStyleSheet("color: #888; font-size: 14px; margin-top: 10px; font-weight: bold;")
        lbl_photo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        photo_layout.addWidget(lbl_photo)
        photo_layout.addWidget(lbl_photo_text)
        
        right_layout.addWidget(photo_container)

        # --- 2. SECCIÓN INFO BOARD (ABAJO) ---
        board_container = QFrame()
        board_container.setFixedWidth(350)
        board_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 10px;
            }
        """)
        
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(0)

        # Header Degradado
        header_frame = QFrame()
        header_frame.setFixedHeight(50)
        header_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8));
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom: none;
        """)
        header_layout = QVBoxLayout(header_frame)
        lbl_info_title = QLabel("Información")
        lbl_info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(lbl_info_title)

        # Contenido Notas
        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_text = QLabel(
            "Cliente frecuente desde 2021.\n"
            "Mascotas: 2 (Firulais, Michi).\n"
            "Pagos al día."
        )
        lbl_text.setWordWrap(True)
        lbl_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        lbl_text.setStyleSheet("font-size: 16px; color: #555; margin-top: 5px;")

        content_layout.addWidget(lbl_text)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)

        right_layout.addWidget(board_container)
        
        parent_layout.addWidget(right_container, stretch=2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())