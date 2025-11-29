import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QGridLayout, QDateEdit, QTimeEdit, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# --- AJUSTE DE RUTAS GENERAL ---
# La clave es establecer una ruta base correcta para que todas las ventanas la usen.
current_dir = os.path.dirname(os.path.abspath(__file__))
# Asumo que la carpeta del proyecto (que contiene 'db_connection' y las otras UIs) es el padre.
# Si tu estructura es: Proyecto-Yuno/db_connection.py, Proyecto-Yuno/Citas/UI_REP_Agendar_Cita.py
# El directorio padre (parent_dir) es 'Proyecto-Yuno'.
parent_dir = os.path.dirname(current_dir) # CORRECCIÓN: Subimos un nivel (de 'Citas' a 'Proyecto-Yuno')
if current_dir not in sys.path: sys.path.append(current_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)

# Intentamos importar la conexión
try:
    from db_connection import Conexion
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("ADVERTENCIA: No se pudo importar la conexión a la base de datos (db_connection).")


class MainWindow(QMainWindow):

    # 1. RECIBIMOS EL NOMBRE DE USUARIO
    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()

        # 2. GUARDAMOS LA SESIÓN (PERSISTENCIA)
        self.nombre_usuario = nombre_usuario
        self.setWindowTitle(f"Sistema Veterinario Yuno - Agendar Cita ({self.nombre_usuario})")

        self.resize(1280, 720)

        # Instancia de conexión segura
        if DB_AVAILABLE:
            self.conexion1 = Conexion()

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES (Igual al de Enfermería) ---
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

        # --- 1. BARRA LATERAL ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Agendar Cita")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")

        # CONEXIÓN: Regresar al menú principal

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()

        self.white_layout.addLayout(header_layout)
        self.white_layout.addStretch(1)

        # Contenedor Horizontal para Formulario + Panel Info
        form_container = QWidget()
        form_layout = QHBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(40)

        self.setup_form(form_layout)
        self.setup_info_board(form_layout)

        self.white_layout.addWidget(form_container)
        self.white_layout.addSpacing(30)

        self.setup_save_button()
        self.white_layout.addStretch(2)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # --- LOGO (CORRECCIÓN 1: Detección de Logo) ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Asumo que la carpeta 'FILES' está en el directorio del proyecto (parent_dir)
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
            print(f"ADVERTENCIA: Logo no encontrado en la ruta: {ruta_logo}") # Para debugging

        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # --- MENÚ DE RECEPCIONISTA (Basado en tus archivos) ---
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Volver al Menú")
        btn_logout.setStyleSheet("QPushButton { text-align: center; border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 20px; font-size: 14px; color: white; font-weight: bold; background-color: transparent; } QPushButton:hover { background-color: rgba(255,255,255,0.2); }")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)

        # CONEXIÓN: Regresar al menú
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
        layout_options.setSpacing(5)

        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)

            # Pasamos categoria y opcion
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.abrir_ventana(t, o))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    # --- LÓGICA DE NAVEGACIÓN Y PERSISTENCIA DE USUARIO (Router) ---

    # CORRECCIÓN 2: Aseguramos la importación del MainMenu fuera del método
    # La solución más limpia es importar los módulos al inicio o dentro del método,
    # pero para evitar errores de importación circular o fallos si el archivo
    # no existe, lo mantenemos con `try...except`.

    def regresar_menu(self):
        try:
            # Importar el menú principal de Recepcionista (Asumo que está en la carpeta padre)
            from UI_REP_main import MainWindow as MenuRecepcionista
            # CORRECCIÓN 3: Al crear la nueva ventana, debemos guardarla en una referencia del objeto
            # principal o de la aplicación, NO como una variable local dentro del método.
            # Si se deja como variable local, el recolector de basura (garbage collector) de Python
            # la cerrará inmediatamente. 'self.menu' es una referencia fuerte.
            self.menu_principal = MenuRecepcionista(self.nombre_usuario)
            self.menu_principal.show()
            self.close()
        except ImportError:
            QMessageBox.warning(self, "Error", "No se encuentra el archivo principal del menú 'UI_REP_main.py'.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al volver al menú: {e}")

    def abrir_ventana(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        try:
            target_window_class = None

            # --- RUTAS DE CITAS ---
            if categoria == "Citas":
                if opcion == "Agendar":
                    return # Ya estamos aquí, no hacemos nada
                elif opcion == "Visualizar":
                    from UI_REP_Revisar_Cita import MainWindow as Win
                    target_window_class = Win
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cita import MainWindow as Win
                    target_window_class = Win

            # --- RUTAS DE MASCOTAS ---
            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    from UI_REP_Registrar_mascota import MainWindow as Win
                    target_window_class = Win
                elif opcion == "Visualizar":
                    from UI_Revisar_Mascota import MainWindow as Win
                    target_window_class = Win
                elif opcion == "Modificar":
                    from UI_REP_Modificar_Mascota import MainWindow as Win
                    target_window_class = Win

            # --- RUTAS DE CLIENTES ---
            elif categoria == "Clientes":
                if opcion == "Registrar":
                    from UI_REP_Registra_cliente import MainWindow as Win
                    target_window_class = Win
                elif opcion == "Visualizar":
                    from UI_Revisar_cliente import MainWindow as Win
                    target_window_class = Win
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cliente import MainWindow as Win
                    target_window_class = Win

            # --- ABRIR LA VENTANA (CORRECCIÓN 3: Referencia fuerte) ---
            if target_window_class:
                # Creamos la instancia y la guardamos en una referencia fuerte (self.ventana_activa)
                self.ventana_activa = target_window_class(self.nombre_usuario)
                self.ventana_activa.show()
                self.close()

        except ImportError as e:
            QMessageBox.warning(self, "Error de Archivo (ImportError)", f"No se pudo encontrar el archivo solicitado.\n\nVerifica que exista y se llame:\n {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {e}")

    # --- RESTO DE FUNCIONES (sin modificar) ---
    def setup_form(self, parent_layout):
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        input_style = """
            QLineEdit, QDateEdit, QTimeEdit, QComboBox {
                background-color: rgba(241, 131, 227, 0.35);
                border: none; border-radius: 10px; padding: 5px 15px;
                font-size: 18px; color: #333; height: 45px;
            }
            QComboBox::drop-down { border: 0px; }
        """
        label_style = "font-size: 20px; color: black; font-weight: 400;"

        # Campos
        lbl_fecha = QLabel("Fecha de la cita:")
        lbl_fecha.setStyleSheet(label_style)
        self.inp_fecha = QDateEdit()
        self.inp_fecha.setCalendarPopup(True)
        self.inp_fecha.setDate(datetime.now().date())
        self.inp_fecha.setStyleSheet(input_style)

        lbl_hora = QLabel("Hora de la cita:")
        lbl_hora.setStyleSheet(label_style)
        self.inp_hora = QTimeEdit()
        self.inp_hora.setTime(datetime.now().time())
        self.inp_hora.setStyleSheet(input_style)

        lbl_motivo = QLabel("Motivo:")
        lbl_motivo.setStyleSheet(label_style)
        self.inp_motivo = QLineEdit()
        self.inp_motivo.setStyleSheet(input_style)

        lbl_estado = QLabel("Estado:")
        lbl_estado.setStyleSheet(label_style)
        self.inp_estado = QComboBox()
        self.inp_estado.addItems(["Pendiente", "Confirmada", "Cancelada", "Completada"])
        self.inp_estado.setStyleSheet(input_style)

        lbl_mascota = QLabel("ID Mascota:")
        lbl_mascota.setStyleSheet(label_style)
        self.inp_mascota = QLineEdit()
        self.inp_mascota.setPlaceholderText("Ej: 1")
        self.inp_mascota.setStyleSheet(input_style)

        lbl_vet = QLabel("ID Veterinario:")
        lbl_vet.setStyleSheet(label_style)
        self.inp_vet = QLineEdit()
        self.inp_vet.setPlaceholderText("Ej: 1")
        self.inp_vet.setStyleSheet(input_style)

        grid_layout.addWidget(lbl_fecha, 0, 0)
        grid_layout.addWidget(self.inp_fecha, 0, 1)
        grid_layout.addWidget(lbl_hora, 1, 0)
        grid_layout.addWidget(self.inp_hora, 1, 1)
        grid_layout.addWidget(lbl_motivo, 2, 0)
        grid_layout.addWidget(self.inp_motivo, 2, 1)
        grid_layout.addWidget(lbl_estado, 3, 0)
        grid_layout.addWidget(self.inp_estado, 3, 1)
        grid_layout.addWidget(lbl_mascota, 4, 0)
        grid_layout.addWidget(self.inp_mascota, 4, 1)
        grid_layout.addWidget(lbl_vet, 5, 0)
        grid_layout.addWidget(self.inp_vet, 5, 1)

        grid_layout.setRowStretch(6, 1)
        parent_layout.addWidget(form_widget, stretch=2)

    def setup_info_board(self, parent_layout):
        board_container = QFrame()
        board_container.setFixedWidth(300)
        board_container.setStyleSheet("QFrame { background-color: white; border: 1px solid #DDD; border-radius: 5px; }")

        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8)); border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom: none;")

        header_layout = QVBoxLayout(header_frame)
        lbl_info_title = QLabel("Información")
        lbl_info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(lbl_info_title)

        content_area = QLabel("Asegúrese de verificar\nel ID de la mascota\ny el veterinario antes\nde guardar.")
        content_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_area.setStyleSheet("color: #888; font-size: 14px; border: none; padding: 20px;")

        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_area)
        board_layout.addStretch()

        parent_layout.addWidget(board_container, stretch=1)

    def setup_save_button(self):
        btn_save = QPushButton("Guardar Cita")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedSize(250, 60)
        btn_save.setStyleSheet("QPushButton { background-color: #b67cfc; color: white; font-size: 24px; font-weight: bold; border-radius: 30px; } QPushButton:hover { background-color: #a060e8; } QPushButton:pressed { background-color: #8a4cd0; }")

        btn_save.clicked.connect(self.guardar_datos)

        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_save)
        btn_container.addStretch()

        self.white_layout.addLayout(btn_container)

    def guardar_datos(self):
        if not DB_AVAILABLE:
            QMessageBox.critical(self, "Error", "No hay conexión a la base de datos.")
            return

        fecha_str = self.inp_fecha.date().toString("yyyy-MM-dd")
        hora_str = self.inp_hora.time().toString("HH:mm:ss")
        motivo = self.inp_motivo.text().strip()
        estado = self.inp_estado.currentText()
        id_mascota = self.inp_mascota.text().strip()
        id_veterinario = self.inp_vet.text().strip()

        if not motivo or not id_mascota or not id_veterinario:
            QMessageBox.warning(self, "Aviso", "Complete Motivo, ID Mascota e ID Veterinario.")
            return

        datos = (fecha_str, hora_str, estado, motivo, id_mascota, id_veterinario)
        columnas = ('fecha', 'hora', 'estado', 'motivo', 'fk_mascota', 'fk_veterinario')

        try:
            nuevo_id = self.conexion1.insertar_datos('cita', datos, columnas)
            if nuevo_id:
                QMessageBox.information(self, "Éxito", f"Cita ID {nuevo_id} creada correctamente.")
                self.inp_motivo.clear()
                self.inp_mascota.clear()
                self.inp_vet.clear()
            else:
                 QMessageBox.warning(self, "Error", "La base de datos no devolvió un nuevo ID. Revise la inserción.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("Recepcionista TEST")
    window.show()
    sys.exit(app.exec())