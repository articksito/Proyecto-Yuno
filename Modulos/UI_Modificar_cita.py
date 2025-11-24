import sys
# Importamos date y time explicitamente para las validaciones
from datetime import datetime, date, time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QDateEdit, QTimeEdit, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont, QPixmap
import os

from db_connection import Conexion
from UI_Crear_cita import MainWindow as Agendar_cita
from UI_Registrar_mascota import MainWindow as Registrar_mascota
from UI_Revisar_Mascota import MainWindow as Modificar_mascota
from UI_Registra_cliente import MainWindow as Regsitrar_dueno
from UI_Revisar_cliente import MainWindow as Modficiar_dueno

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Modificar Cita")
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
            QLabel#Logo {
                color: white; 
                font-size: 36px; 
                font-weight: bold; 
                margin-bottom: 30px;
            }
            QPushButton.menu-btn {
                text-align: left;
                padding-left: 20px;
                border: none;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 18px;
                background-color: transparent;
                height: 40px;
            }
            QPushButton.menu-btn:hover {
                color: #E0E0E0;
                background-color: rgba(255, 255, 255, 0.1);
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
            QPushButton.sub-btn {
                text-align: left;
                border: none;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: normal;
                padding-left: 50px;
                color: #F0F0F0;
                background-color: transparent;
                height: 30px;
            }
            QPushButton.sub-btn:hover {
                color: #333;
                background-color: rgba(255, 255, 255, 0.2);
                font-weight: bold;
            }
        """)

        self.setup_sidebar()

        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Modificar cita")
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
        self.white_layout.addSpacing(20)

        # Contenedor Formulario
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        self.setup_edit_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        
        self.setup_save_button()
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ruta_logo = "logo.png" 
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
        
        # Agregamos "Agendar" para poder regresar a la pantalla de crear
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar"])
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
        layout_options.setSpacing(2)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # --- CONEXIÓN DE BOTONES ---
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.abrir_ventana(cat, opt))
            
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    # --- NUEVA FUNCIÓN: GESTOR DE VENTANAS ---
    def abrir_ventana(self, categoria, opcion):
        """
        Navegación entre ventanas. Importamos dentro de la función para evitar
        errores de importación circular.
        """
        print(f"Navegando a: {categoria} -> {opcion}")

        try:
            # Lógica para CITAS
            if categoria == "Citas":
                if opcion == "Agendar":
                    self.ventana = Agendar_cita()
                    self.ventana.show()
                    self.close()

            # Lógica para MASCOTAS
            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    self.ventana = Registrar_mascota()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    self.ventana = Modificar_mascota()
                    self.ventana.show()
                    self.close()

            # Lógica para CLIENTES
            elif categoria == "Clientes":
                if opcion == "Registrar":
                    self.ventana = Regsitrar_dueno()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    self.ventana = Modficiar_dueno()
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

    def setup_edit_form(self, parent_layout):
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

        # 1. ID para BUSCAR
        lbl_id = QLabel("ID de la cita:")
        lbl_id.setStyleSheet(label_style)
        
        self.inp_id = QLineEdit()
        self.inp_id.setPlaceholderText("Ingresa ID para buscar")
        self.inp_id.setStyleSheet(input_style)
        
        btn_buscar = QPushButton("Buscar")
        btn_buscar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_buscar.setFixedSize(100, 45)
        btn_buscar.setStyleSheet("""
            QPushButton {
                background-color: #7CEBFC;
                color: #333;
                font-weight: bold;
                border-radius: 10px;
                border: 1px solid #5CD0E3;
            }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_buscar.clicked.connect(self.buscar_cita)

        # 2. Fecha
        lbl_fecha = QLabel("Fecha de la cita:")
        lbl_fecha.setStyleSheet(label_style)
        self.inp_fecha = QDateEdit()
        self.inp_fecha.setCalendarPopup(True)
        self.inp_fecha.setDate(datetime.now().date())
        self.inp_fecha.setStyleSheet(input_style)

        # 3. Hora
        lbl_hora = QLabel("Hora de la cita:")
        lbl_hora.setStyleSheet(label_style)
        self.inp_hora = QTimeEdit()
        self.inp_hora.setTime(datetime.now().time())
        self.inp_hora.setStyleSheet(input_style)

        # 4. Motivo
        lbl_motivo = QLabel("Motivo:")
        lbl_motivo.setStyleSheet(label_style)
        self.inp_motivo = QLineEdit()
        self.inp_motivo.setStyleSheet(input_style)

        # 5. Estado
        lbl_estado = QLabel("Estado:")
        lbl_estado.setStyleSheet(label_style)
        self.inp_estado = QComboBox()
        self.inp_estado.addItems(["Pendiente", "Confirmada", "Cancelada", "Completada"])
        self.inp_estado.setStyleSheet(input_style)

        # 6. ID Mascota
        lbl_mascota = QLabel("Id de la mascota:")
        lbl_mascota.setStyleSheet(label_style)
        self.inp_mascota = QLineEdit()
        self.inp_mascota.setStyleSheet(input_style)

        # 7. ID Veterinario
        lbl_vet = QLabel("Id del veterinario:")
        lbl_vet.setStyleSheet(label_style)
        self.inp_vet = QLineEdit()
        self.inp_vet.setStyleSheet(input_style)

        grid_layout.addWidget(lbl_id, 0, 0)
        grid_layout.addWidget(self.inp_id, 0, 1)
        grid_layout.addWidget(btn_buscar, 0, 2)

        grid_layout.addWidget(lbl_fecha, 1, 0)
        grid_layout.addWidget(self.inp_fecha, 1, 1)

        grid_layout.addWidget(lbl_hora, 2, 0)
        grid_layout.addWidget(self.inp_hora, 2, 1)

        grid_layout.addWidget(lbl_motivo, 3, 0)
        grid_layout.addWidget(self.inp_motivo, 3, 1)

        grid_layout.addWidget(lbl_estado, 4, 0)
        grid_layout.addWidget(self.inp_estado, 4, 1)

        grid_layout.addWidget(lbl_mascota, 5, 0)
        grid_layout.addWidget(self.inp_mascota, 5, 1)

        grid_layout.addWidget(lbl_vet, 6, 0)
        grid_layout.addWidget(self.inp_vet, 6, 1)

        grid_layout.setRowStretch(7, 1)
        parent_layout.addWidget(form_widget, stretch=2)

    def setup_info_board(self, parent_layout):
        board_container = QFrame()
        board_container.setFixedWidth(300)
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

        header_frame = QFrame()
        header_frame.setFixedHeight(60)
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

        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        self.lbl_info_extra = QLabel("Ingresa un ID y presiona 'Buscar' para cargar los datos.")
        self.lbl_info_extra.setWordWrap(True)
        self.lbl_info_extra.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.lbl_info_extra.setStyleSheet("color: #555; font-size: 14px; border: none;")
        
        content_layout.addWidget(self.lbl_info_extra)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)

        parent_layout.addWidget(board_container, stretch=1)

    def setup_save_button(self):
        btn_save = QPushButton("Guardar Cambios")
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
        
        btn_save.clicked.connect(self.guardar_cambios)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_save)
        btn_container.addStretch()
        
        self.white_layout.addLayout(btn_container)

    # --- FUNCIÓN 1: BUSCAR CITA Y LLENAR CAMPOS ---
    def buscar_cita(self):
        id_cita = self.inp_id.text().strip()
        
        # Validar que no esté vacío y que sea número
        if not id_cita:
            QMessageBox.warning(self, "Aviso", "Por favor ingresa un ID para buscar.")
            return
        
        if not id_cita.isdigit():
            QMessageBox.warning(self, "Formato Incorrecto", "El ID de la cita debe ser un número entero.")
            return

        print(f"Buscando cita con ID: {id_cita}")
        
        try:
            # Columnas exactas que espera el formulario
            columnas = ['fecha', 'hora', 'motivo', 'estado', 'fk_mascota', 'fk_veterinario']
            
            registro = self.conexion1.consultar_registro('cita', 'id_cita', id_cita, columnas)
            
            if registro:
                # registro es una tupla: (fecha, hora, motivo, estado, mascota, vet)
                fecha_bd = registro[0] 
                hora_bd = registro[1]

                # --- CONVERSIÓN DE FECHA ROBUSTA ---
                if isinstance(fecha_bd, date): # Objeto python date
                    q_date = QDate(fecha_bd.year, fecha_bd.month, fecha_bd.day)
                    self.inp_fecha.setDate(q_date)
                elif isinstance(fecha_bd, str): # Cadena
                    self.inp_fecha.setDate(QDate.fromString(fecha_bd, "yyyy-MM-dd"))
                
                # --- CONVERSIÓN DE HORA ROBUSTA ---
                if isinstance(hora_bd, time): # Objeto python time
                    q_time = QTime(hora_bd.hour, hora_bd.minute, hora_bd.second)
                    self.inp_hora.setTime(q_time)
                elif isinstance(hora_bd, str): # Cadena
                    self.inp_hora.setTime(QTime.fromString(hora_bd, "HH:mm:ss"))

                # 3. Textos
                self.inp_motivo.setText(str(registro[2]))
                self.inp_estado.setCurrentText(str(registro[3]))
                self.inp_mascota.setText(str(registro[4]))
                self.inp_vet.setText(str(registro[5]))
                
                self.lbl_info_extra.setText(f"Cita #{id_cita} cargada correctamente.\nPuedes modificar los datos.")
            else:
                QMessageBox.warning(self, "No encontrado", f"No se encontró ninguna cita con ID: {id_cita}")
                self.lbl_info_extra.setText("ID no encontrado.")

        except Exception as e:
            # Mostramos el error exacto para depuración
            QMessageBox.critical(self, "Error al buscar", f"Detalle del error:\n{e}")

    # --- FUNCIÓN 2: GUARDAR CAMBIOS ---
    def guardar_cambios(self):
        id_cita = self.inp_id.text().strip()
        
        if not id_cita:
            QMessageBox.warning(self, "Error", "Busca una cita primero (ingresa ID).")
            return

        # 1. Recolectar datos del formulario
        datos = {
            "fecha": self.inp_fecha.date().toString("yyyy-MM-dd"),
            "hora": self.inp_hora.time().toString("HH:mm:ss"),
            "motivo": self.inp_motivo.text().strip(),
            "estado": self.inp_estado.currentText(),
            "fk_mascota": self.inp_mascota.text().strip(),
            "fk_veterinario": self.inp_vet.text().strip()
        }

        # 2. Validaciones básicas
        if not datos["motivo"] or not datos["fk_mascota"] or not datos["fk_veterinario"]:
            QMessageBox.warning(self, "Campos vacíos", "Todos los campos (Motivo, Mascota, Veterinario) son obligatorios.")
            return

        print(f"Actualizando cita {id_cita}...")

        # 3. Llamada a la BD
        try:
            exito = self.conexion1.editar_registro(
                id=id_cita, 
                datos=datos, 
                tabla='cita', 
                id_columna='id_cita' # Ajusta si tu PK es diferente
            )
            
            if exito:
                QMessageBox.information(self, "Éxito", "Cita modificada correctamente.")
                self.lbl_info_extra.setText("Cambios guardados exitosamente.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar (verifica el ID).")

        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Ocurrió un error al actualizar: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())