import sys
import os
from datetime import datetime
from functools import partial 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap

# --- AJUSTE DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path: sys.path.append(current_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)

# --- MOCK DE VENTANA DE LOGIN PARA PRUEBAS ---
# Para que el botón de Cerrar Sesión funcione sin el archivo real
try:
    # 🛑 IMPORTACIÓN DE LA VENTANA DE LOGIN REAL
    # Asume que la ventana de login se llama UI_Login.py y la clase LoginWindow
    from UI_Login import LoginWindow 
except ImportError:
    print("Advertencia: No se encontró UI_Login.py. Usando MockLoginWindow.")
    class LoginWindow(QMainWindow):
        """Clase Mock para probar el flujo de Cerrar Sesión."""
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Ventana de Inicio de Sesión (Mock)")
            self.resize(500, 300)
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.addWidget(QLabel("Volviste a la Pantalla de Login"))
            self.setCentralWidget(widget)


class MainWindow(QMainWindow):
    # 1. RECIBIMOS EL NOMBRE 
    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        
        # 2. GUARDAMOS LA SESIÓN
        self.nombre_usuario = nombre_usuario
        self.login_window = None # Atributo para guardar la referencia de la ventana de login si se usa

        self.setWindowTitle(f"Sistema Veterinario Yuno - Menú Principal ({self.nombre_usuario})")
        self.resize(1280, 720)

        # Datos para mostrar en pantalla
        self.user_data = {
            "nombre": self.nombre_usuario,
            "puesto": "Recepcionista",
        }

        # ... (Resto del setup inicial - Mantenido) ...
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES (Mantenidos) ---
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QLabel { font-family: 'Segoe UI', sans-serif; }
            QPushButton.menu-btn { text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; color: white; font-family: 'Segoe UI', sans-serif; font-weight: bold; font-size: 18px; background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px; }
            QPushButton.menu-btn:hover { background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; }
            QPushButton.sub-btn { text-align: left; font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: normal; padding-left: 40px; border-radius: 10px; color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05); height: 35px; margin-bottom: 2px; margin-left: 10px; margin-right: 10px; }
            QPushButton.sub-btn:hover { color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; }
        """)

        # --- 1. BARRA LATERAL ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO (CONTENIDO) ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        
        self.content_layout = QVBoxLayout(self.white_panel)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.setSpacing(20)

        self.setup_central_info()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)
        
        # Atributo para mantener referencia a la nueva ventana abierta
        self.ventana = None

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # LOGO (Mantenido)
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_logo = os.path.join(parent_dir, "FILES", "logo_yuno.png")
        
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
        self.sidebar_layout.addSpacing(20)
        
        # MENÚS DESPLEGABLES (Mantenidos)
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        # Asumo que "Visualizar" y "Modificar" están mapeados a diferentes archivos.
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])

        self.sidebar_layout.addStretch()

        # BOTÓN CERRAR SESIÓN
        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("QPushButton { text-align: center; border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 20px; font-size: 14px; color: white; font-weight: bold; background-color: transparent; } QPushButton:hover { background-color: rgba(255,255,255,0.2); }")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 🛑 CORRECCIÓN CLAVE: Conectar a la nueva función de logout
        btn_logout.clicked.connect(self.logout_to_login) 
        
        self.sidebar_layout.addWidget(btn_logout)

    # --- NUEVA FUNCIÓN PARA EL LOGOUT ---
    def logout_to_login(self):
        """Abre la ventana de Login y cierra la ventana actual (Menu Principal)."""
        try:
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error de Logout", 
                                 f"No se pudo cargar la pantalla de inicio de sesión. Cerrando aplicación. Detalle: {e}")
            self.close() # Cierra solo el menú como fallback.

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
            
            # Conectamos con el enrutador usando functools.partial
            btn_sub.clicked.connect(partial(self.router_ventanas, title, opt_text))
            
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    # ... (setup_central_info y update_time se mantienen) ...
    def setup_central_info(self):
        info_container = QFrame()
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(15)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_title = QLabel("Bienvenid@")
        lbl_title.setStyleSheet("color: #888; font-size: 24px; letter-spacing: 2px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_name = QLabel(self.user_data['nombre'])
        lbl_name.setStyleSheet("color: #5f2c82; font-size: 56px; font-weight: bold;")
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_role = QLabel(self.user_data['puesto'])
        lbl_role.setStyleSheet("color: #FC7CE2; font-size: 20px; font-weight: 600;")
        lbl_role.setAlignment(Qt.AlignmentFlag.AlignCenter)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedWidth(120)
        line.setStyleSheet("background-color: #DDD; margin: 25px 0;")
        
        self.lbl_time = QLabel()
        self.lbl_time.setStyleSheet("color: #555; font-size: 80px; font-weight: 300; font-family: 'Segoe UI Light';")
        self.lbl_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        info_layout.addWidget(lbl_title)
        info_layout.addWidget(lbl_name)
        info_layout.addWidget(lbl_role)
        
        line_layout = QHBoxLayout()
        line_layout.addStretch()
        line_layout.addWidget(line)
        line_layout.addStretch()
        info_layout.addLayout(line_layout)
        info_layout.addWidget(self.lbl_time)
        self.content_layout.addWidget(info_container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.lbl_time.setText(current_time)


    # =========================================================================
    #                    ZONA DE NAVEGACIÓN (ENRUTADOR)
    # =========================================================================
    def router_ventanas(self, categoria, opcion):
        print(f"Abriendo: {categoria} -> {opcion}") 
        target_window = None

        try:
            # --- SECCIÓN CITAS ---
            if categoria == "Citas":
                if opcion == "Agendar":
                    from UI_REP_Crear_cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_REP_Revisar_Cita import MainWindow as Win
                    # Nota: Si Revisar Cita usa el nombre, pásalo
                    target_window = Win(self.nombre_usuario) 
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)

            # --- SECCIÓN MASCOTAS ---
            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    from UI_REP_Registrar_mascota import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_Revisar_Mascota import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    # Asumiendo un nombre de archivo para Modificar mascota
                    from UI_REP_Modificar_Mascota import MainWindow as Win 
                    target_window = Win(self.nombre_usuario)

            # --- SECCIÓN CLIENTES ---
            elif categoria == "Clientes":
                if opcion == "Registrar":
                    from UI_REP_Registra_cliente import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_Revisar_cliente import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cliente import MainWindow as Win
                    target_window = Win(self.nombre_usuario)

            # --- ABRIR LA VENTANA ---
            if target_window:
                self.ventana = target_window
                self.ventana.show()
                # Cerramos el menú principal
                self.close() 
            else:
                QMessageBox.warning(self, "Aviso", f"La opción '{opcion}' no tiene una ventana asignada aún o la categoría no existe.")

        except ImportError as e:
            QMessageBox.critical(self, "Error de Archivo", f"No se encuentra el archivo: **{e.name}**\nVerifica que el nombre del archivo coincida (incluyendo mayúsculas/minúsculas) y que la configuración de rutas es correcta.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la ventana.\nDetalle: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow("Recepcionista TEST")
    window.show()
    sys.exit(app.exec())