import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, 
                             QMessageBox, QFrame, QTreeWidget, QTreeWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# Intentar importar conexión
try:
    from db_connection import Conexion
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Veterinario Yuno - Hospitalización")
        self.resize(1280, 720)

        # Inicializar conexión
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
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QWidget#Sidebar { background-color: transparent; }
            QLabel { font-family: 'Segoe UI'; color: #333; font-size: 16px; font-weight: bold; }
            
            /* Inputs */
            QLineEdit, QTextEdit {
                background-color: rgba(241, 131, 227, 0.15); 
                border: 1px solid #DDD; border-radius: 10px; 
                padding: 10px; font-size: 16px; color: #333;
            }
            QLineEdit:focus, QTextEdit:focus { border: 1px solid #b67cfc; background-color: white; }
            
            /* Sidebar Styles */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px; color: white; font-family: 'Segoe UI', sans-serif;
                font-weight: bold; font-size: 18px; background-color: rgba(255, 255, 255, 0.1);
                height: 50px; margin-bottom: 5px;
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
        """)

        # --- Sidebar ---
        self.setup_sidebar()

        # --- PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(80, 40, 80, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Internar Paciente")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0; color: #555; border-radius: 20px; 
                padding: 10px 20px; font-weight: bold; border: none; font-size: 14px;
            }
            QPushButton:hover { background-color: #E0E0E0; color: #333; }
        """)
        # CONEXIÓN AL MENU
        btn_back.clicked.connect(self.regresar_menu)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_back)
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(40)

        # --- FORMULARIO CENTRADO ---
        self.white_layout.addWidget(QLabel("ID de la Consulta:"))
        self.inp_id_consulta = QLineEdit()
        self.inp_id_consulta.setPlaceholderText("Ej. 102")
        self.white_layout.addWidget(self.inp_id_consulta)
        
        self.white_layout.addSpacing(20)

        self.white_layout.addWidget(QLabel("Observaciones / Motivo de Internamiento:"))
        self.inp_obs = QTextEdit()
        self.inp_obs.setPlaceholderText("Describa el estado del paciente, medicación requerida y razones para internarlo...")
        self.white_layout.addWidget(self.inp_obs)

        self.white_layout.addSpacing(40)

        # Botón Confirmar
        btn_internar = QPushButton("CONFIRMAR INTERNAMIENTO")
        btn_internar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_internar.setFixedHeight(60)
        btn_internar.setStyleSheet("""
            QPushButton { background-color: #b67cfc; color: white; font-size: 20px; font-weight: bold; border-radius: 15px; }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_internar.clicked.connect(self.internar_mascota)
        self.white_layout.addWidget(btn_internar)
        self.white_layout.addStretch()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def internar_mascota(self):
        id_consulta = self.inp_id_consulta.text()
        obs = self.inp_obs.toPlainText()

        if not id_consulta or not obs:
            QMessageBox.warning(self, "Alerta", "Todos los campos son obligatorios.")
            return

        if not DB_AVAILABLE:
            QMessageBox.critical(self, "Error", "No hay conexión a la base de datos.")
            return

        try:
            # Insertar en tabla hospitalizacion
            datos = (obs, int(id_consulta))
            columnas = ('observaciones', 'fk_consulta')
            self.conexion1.insertar_datos('hospitalizacion', datos, columnas)
            
            QMessageBox.information(self, "Éxito", "Paciente internado correctamente.")
            self.inp_id_consulta.clear()
            self.inp_obs.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al internar: {e}")

    # --- BARRA LATERAL ---
    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # --- LOGO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 1. Obtener la ruta donde está guardado ESTE archivo .py (Enfermero)
        directorio_actual = os.path.dirname(os.path.abspath(__file__))

        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)

        # 3. Cargar imagen
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                # Si la imagen existe pero está corrupta
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        else:
            # Si no encuentra la imagen
            print(f"No se encontró el logo en: {ruta_logo}")
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
            
        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # Menús desplegables (Igual que en Menú Principal)
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

    # --- NAVEGACIÓN ---
    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import EnfermeroMain as MenuEnfermera
            self.menu = MenuEnfermera()
            self.menu.show()
            self.close()
        except ImportError:
            QMessageBox.warning(self, "Error", "No se encuentra el menú de enfermera.")

    # --- FUNCION DE NAVEGACIÓN DIRECTA (ROUTER) ---
    def abrir_ventana(self, categoria, opcion):
        try:
            target_window = None

            # 1. ENRUTAMIENTO
            if categoria == "Citas" and opcion == "Visualizar":
                from UI_Cita_Enfermera import MainWindow as Win
                target_window = Win()
            
            elif categoria == "Mascotas" and opcion == "Visualizar":
                from UI_Revisar_Mascota_Enfermera import MainWindow as Win
                target_window = Win()
            
            elif categoria == "Inventario":
                if opcion == "Farmacia":
                    from UI_Farmacia import MainWindow as Win
                    target_window = Win()
                elif opcion == "Hospitalización":
                    pass # Ya estamos aquí
            
            elif categoria == "Expediente" and opcion == "Diagnóstico":
                from UI_Diagnostico import MainWindow as Win
                target_window = Win()

            # 2. EJECUCIÓN
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec())