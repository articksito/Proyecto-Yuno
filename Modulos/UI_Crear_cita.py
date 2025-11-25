import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QDateEdit, QTimeEdit, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# Importar conexión
from db_connection import Conexion

class MainWindow(QMainWindow):
    # Instancia de conexión
    conexion1 = Conexion()
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Agendar Cita")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal (Horizontal)
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
            /* Estilo Botones Menú Principal */
            QPushButton.menu-btn {
                text-align: left;
                padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1);
                height: 50px;
                margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid white;
                color: #FFF;
            }
            /* Estilo Sub-botones */
            QPushButton.sub-btn {
                text-align: left;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: normal;
                padding-left: 40px;
                border-radius: 10px;
                color: #F0F0F0;
                background-color: rgba(0, 0, 0, 0.05);
                height: 35px;
                margin-bottom: 2px;
                margin-left: 10px;
                margin-right: 10px;
            }
            QPushButton.sub-btn:hover {
                color: white;
                background-color: rgba(255, 255, 255, 0.3);
                font-weight: bold;
            }
        """)

        # --- 1. BARRA LATERAL (Izquierda) ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO (Derecha - Formulario) ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header con Título y Botón Cerrar
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Agendar cita")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_close_view = QPushButton("✕")
        btn_close_view.setFixedSize(40, 40)
        btn_close_view.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close_view.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border-radius: 20px;
                font-size: 20px;
                color: #666;
                border: none;
            }
            QPushButton:hover {
                background-color: #ffcccc;
                color: #cc0000;
            }
        """)
        btn_close_view.clicked.connect(self.close)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close_view)

        self.white_layout.addLayout(header_layout)
        
        # --- ESPACIADOR SUPERIOR (Centrado) ---
        self.white_layout.addStretch(1)

        # Contenedor Horizontal para Formulario + Panel Info
        form_container = QWidget()
        form_layout = QHBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(40)

        # --- A. EL FORMULARIO ---
        self.setup_form(form_layout)

        # --- B. PANEL DE INFORMACIÓN (Derecha) ---
        self.setup_info_board(form_layout)

        self.white_layout.addWidget(form_container)
        
        # Espacio
        self.white_layout.addSpacing(30)
        
        # Botón Guardar
        self.setup_save_button()

        # --- ESPACIADOR INFERIOR (Centrado) ---
        self.white_layout.addStretch(2)

        # Agregar al layout principal
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        # --- LOGO (IMAGEN) ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ruta_logo = "Modulos/FILES/logo_yuno.png"
        
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                lbl_logo.setText("YUNO VET")
        else:
            lbl_logo.setText("YUNO VET")

        self.sidebar_layout.addWidget(lbl_logo)
        
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Modificar"])

        self.sidebar_layout.addStretch()

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
            # Conexión de botones
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.abrir_ventana(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    # --- GESTOR DE VENTANAS ---
    def abrir_ventana(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        try:
            # Importaciones locales
            if categoria == "Citas":
                if opcion == "Agendar":
                    pass # Ya estamos aquí
                elif opcion == "Visualizar":
                    from UI_Revisar_Cita import MainWindow as Visualizar_cita
                    self.ventana = Visualizar_cita()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_Modificar_cita import MainWindow as Modificar_cita
                    self.ventana = Modificar_cita()
                    self.ventana.show()
                    self.close()

            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    from UI_Registrar_mascota import MainWindow as Registrar_mascota
                    self.ventana = Registrar_mascota()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_Revisar_Mascota import MainWindow as Modificar_mascota
                    self.ventana = Modificar_mascota()
                    self.ventana.show()
                    self.close()

            elif categoria == "Clientes":
                if opcion == "Registrar":
                    from UI_Registra_cliente import MainWindow as Regsitrar_dueno
                    self.ventana = Regsitrar_dueno()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_Modificar_cliente import MainWindow as Modificar_cliente
                    self.ventana = Modificar_cliente()
                    self.ventana.show()
                    self.close()
                    
        except ImportError as e:
            QMessageBox.warning(self, "Error de Navegación", f"No se pudo abrir la ventana solicitada.\nFalta el archivo: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al intentar abrir la ventana: {e}")

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def setup_form(self, parent_layout):
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        input_style = """
            QLineEdit, QDateEdit, QTimeEdit, QComboBox {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 18px;
                color: #333;
                height: 45px;
            }
            QComboBox::drop-down { border: 0px; }
        """
        label_style = "font-size: 24px; color: black; font-weight: 400;"

        # --- Campos del Formulario ---
        
        # 1. Fecha de la cita
        lbl_fecha = QLabel("Fecha de la cita:")
        lbl_fecha.setStyleSheet(label_style)
        self.inp_fecha = QDateEdit()
        self.inp_fecha.setCalendarPopup(True)
        self.inp_fecha.setDate(datetime.now().date())
        self.inp_fecha.setStyleSheet(input_style)

        # 2. Hora de la cita
        lbl_hora = QLabel("Hora de la cita:")
        lbl_hora.setStyleSheet(label_style)
        self.inp_hora = QTimeEdit()
        self.inp_hora.setTime(datetime.now().time())
        self.inp_hora.setStyleSheet(input_style)

        # 3. Motivo
        lbl_motivo = QLabel("Motivo:")
        lbl_motivo.setStyleSheet(label_style)
        self.inp_motivo = QLineEdit()
        self.inp_motivo.setStyleSheet(input_style)

        # 4. Estado
        lbl_estado = QLabel("Estado:")
        lbl_estado.setStyleSheet(label_style)
        self.inp_estado = QComboBox()
        self.inp_estado.addItems(["Pendiente", "Confirmada", "Cancelada", "Completada"])
        self.inp_estado.setStyleSheet(input_style)

        # 5. Id de la mascota
        lbl_mascota = QLabel("Id de la mascota:")
        lbl_mascota.setStyleSheet(label_style)
        self.inp_mascota = QLineEdit()
        self.inp_mascota.setPlaceholderText("Ej: PET-1024")
        self.inp_mascota.setStyleSheet(input_style)

        # 6. Id del veterinario
        lbl_vet = QLabel("Id del veterinario:")
        lbl_vet.setStyleSheet(label_style)
        self.inp_vet = QLineEdit()
        self.inp_vet.setPlaceholderText("Ej: VET-007")
        self.inp_vet.setStyleSheet(input_style)

        # Agregar al Grid
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
        board_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 5px;
            }
        """)
        
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8));
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            border-bottom: none;
        """)
        header_layout = QVBoxLayout(header_frame)
        lbl_info_title = QLabel("Información")
        lbl_info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(lbl_info_title)

        content_area = QLabel("Detalles adicionales\naquí...")
        content_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_area.setStyleSheet("color: #888; font-size: 14px; border: none;")
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_area)
        board_layout.addStretch()

        parent_layout.addWidget(board_container, stretch=1)

    def setup_save_button(self):
        btn_save = QPushButton("Guardar")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedSize(250, 60)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #b67cfc;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 30px; 
            }
            QPushButton:hover {
                background-color: #a060e8;
            }
            QPushButton:pressed {
                background-color: #8a4cd0;
            }
        """)
        
        btn_save.clicked.connect(self.guardar_datos)

        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_save)
        btn_container.addStretch()
        
        self.white_layout.addLayout(btn_container)

    # --- LÓGICA DE GUARDADO ---
    def guardar_datos(self):
        # 1. Obtener datos
        fecha_str = self.inp_fecha.date().toString("yyyy-MM-dd")
        hora_str = self.inp_hora.time().toString("HH:mm:ss")
        motivo = self.inp_motivo.text().strip()
        estado = self.inp_estado.currentText()
        id_mascota = self.inp_mascota.text().strip()
        id_veterinario = self.inp_vet.text().strip()

        # 2. VALIDACIÓN: Ningún campo importante vacío
        if not motivo or not id_mascota or not id_veterinario:
            QMessageBox.warning(self, "Campos vacíos", "Por favor complete todos los campos (Motivo, ID Mascota e ID Veterinario).")
            return

        # 3. Empaquetar datos para la BD
        datos = (fecha_str, hora_str, estado, motivo, id_mascota, id_veterinario)
        columnas = ('fecha', 'hora', 'estado', 'motivo', 'fk_mascota', 'fk_veterinario')
        table = 'cita'

        # 4. INTENTO DE CONEXIÓN CON TRY-EXCEPT
        try:
            print("Enviando datos a la base de datos:", datos)
            
            nuevo_id = self.conexion1.insertar_datos(table, datos, columnas)
            
            # Éxito: Mostramos el ID retornado
            QMessageBox.information(self, "Éxito", f"Cita guardada correctamente.\n\nID de la cita generada: {nuevo_id}")
            
            # Limpiar campos después de guardar
            self.inp_motivo.clear()
            self.inp_mascota.clear()
            self.inp_vet.clear()

        except Exception as e:
            # Convertimos el error a string para analizarlo
            error_message = str(e)
            print(f"Error capturado: {error_message}")
            
            # Detectamos si es un error de Foreign Key
            if "foreign key constraint" in error_message or "violates foreign key" in error_message:
                QMessageBox.warning(self, "Veterinario/Mascota no existe", "El ID del Veterinario o de la Mascota ingresado NO existe en la base de datos.\nPor favor verifique los datos.")
            else:
                QMessageBox.critical(self, "Error de Base de Datos", f"No se pudo guardar la cita.\nDetalle: {error_message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())