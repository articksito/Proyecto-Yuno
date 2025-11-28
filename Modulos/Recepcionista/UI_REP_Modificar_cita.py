# UI_REP_Modificar_cita.py  (versión corregida)
import sys
import os
from datetime import datetime, date, time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QDateEdit, QTimeEdit, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont, QPixmap

# --- GESTIÓN DE IMPORTACIÓN DE LA CONEXIÓN DB Y MENU PRINCIPAL ---
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    if project_root not in sys.path:
        sys.path.append(project_root)

    # Importar la conexión real
    from db_connection import Conexion

    # Importar el menú principal real — tu me dijiste que el archivo del menu se llama UI_REP_main.py
    from UI_REP_main import MainWindow as MenuPrincipal

except ImportError as e:
    # Si falla la importación, usamos mocks para desarrollo local sin BD ni menú real
    print(f"Advertencia: No se pudo importar la conexión real o el menú principal: {e}")

    class MockConexion:
        def consultar_registro(self, tabla, id_columna, id_valor, columnas):
            # Simula una fila para ID '101' (útil para pruebas)
            if str(id_valor) == '101':
                return (date(2025, 12, 1), time(10, 0, 0), "Vacunación anual", "Pendiente", 5, 20)
            return None

        def editar_registro(self, id, datos, tabla, id_columna):
            print(f"Mock DB: Editando registro {id} en {tabla} con datos {datos}")
            return True

    Conexion = MockConexion

    class MenuPrincipal(QMainWindow):
        def __init__(self, nombre_usuario="Usuario"):
            super().__init__()
            self.setWindowTitle(f"Menú Principal - Mock ({nombre_usuario})")
            self.resize(800, 600)
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            layout.addWidget(QLabel("¡Estás en el Menú Principal (Mock)!"))

class MainWindow(QMainWindow):
    # instancia (puede ser real o mock según import)
    conexion1 = Conexion()

    # --- Nota clave: aceptar nombre_usuario para compatibilidad con el resto del sistema ---
    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle(f"Sistema Veterinario Yuno - Modificar Cita ({self.nombre_usuario})")
        self.resize(1280, 720)

        self.cita_cargada = False
        self.ventana_menu = None
        self.ventana = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- STYLES (mantenidos) ---
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC);
            }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel {
                background-color: white;
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                margin: 20px 20px 20px 0px; 
            }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            QPushButton.menu-btn { text-align: left; padding-left: 20px; border: 1px solid rgba(255,255,255,0.3); border-radius: 15px; color: white; font-weight: bold; font-size: 18px; background-color: rgba(255,255,255,0.1); height: 50px; margin-bottom: 5px; }
            QPushButton.menu-btn:hover { background-color: rgba(255,255,255,0.25); border: 1px solid white; color: #FFF; }
            QPushButton.sub-btn { text-align: left; font-size: 16px; padding-left: 40px; border-radius: 10px; color: #F0F0F0; background-color: rgba(0,0,0,0.05); height: 35px; margin-bottom: 2px; margin-left: 10px; margin-right: 10px; }
            QPushButton.sub-btn:hover { color: white; background-color: rgba(255,255,255,0.3); font-weight: bold; }
            QLineEdit:disabled, QDateEdit:disabled, QTimeEdit:disabled, QComboBox:disabled { background-color: #F0F0F0; color: #999; border: 1px solid #DDD; }
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
            QPushButton { background-color: #f0f0f0; border-radius: 20px; font-size: 20px; color: #666; border: none; }
            QPushButton:hover { background-color: #ffcccc; color: #cc0000; }
        """)
        # mantiene cerrar rápido (pero hay botón en sidebar para volver al menú)
        btn_close_view.clicked.connect(self.close)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close_view)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addStretch(1)

        # Contenedor formulario + info
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        # -- Aquí estaban tus métodos: setup_edit_form y setup_info_board --
        self.setup_edit_form(content_layout)
        self.setup_info_board(content_layout)

        self.set_form_enabled(False)

        self.white_layout.addWidget(content_container)
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

        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ruta del logo más robusta: usar parent dir donde suele existir carpeta FILES
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        ruta_logo = os.path.join(parent_dir, "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)

        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                lbl_logo.setText("YUNO VET (Logo no cargado)")
        else:
            lbl_logo.setText("YUNO VET (Logo no encontrado)")

        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # Menú acordeón
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Modificar"])

        self.sidebar_layout.addStretch()

        # BOTÓN: Regresar al Menú (en lugar de 'Cerrar Sesión')
        btn_logout = QPushButton("↶ Volver al Menú")
        btn_logout.setStyleSheet("""
            QPushButton { text-align: center; border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 20px; font-size: 14px; color: white; font-weight: bold; background-color: transparent; }
            QPushButton:hover { background-color: rgba(255,255,255,0.2); }
        """)
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.volver_a_menu_principal)
        self.sidebar_layout.addWidget(btn_logout)

    def volver_a_menu_principal(self):
        try:
            self.ventana_menu = MenuPrincipal(self.nombre_usuario)
            self.ventana_menu.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error al volver", f"No se pudo abrir el Menú Principal: {e}")
            self.close()

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
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.abrir_ventana(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def abrir_ventana(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        try:
            if categoria == "Citas":
                if opcion == "Agendar":
                    from UI_REP_Crear_cita import MainWindow as Agendar_cita
                    self.ventana = Agendar_cita(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_REP_Revisar_Cita import MainWindow as Visualizar_cita
                    self.ventana = Visualizar_cita(self.nombre_usuario)
                elif opcion == "Modificar":
                    # ya estamos en modificar aquí
                    return
            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    from UI_REP_Registrar_mascota import MainWindow as Registrar_mascota
                    self.ventana = Registrar_mascota(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_Mascota import MainWindow as Modificar_mascota
                    self.ventana = Modificar_mascota(self.nombre_usuario)
            elif categoria == "Clientes":
                if opcion == "Registrar":
                    from UI_REP_Registra_cliente import MainWindow as Regsitrar_dueno
                    self.ventana = Regsitrar_dueno(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cliente import MainWindow as Modificar_cliente
                    self.ventana = Modificar_cliente(self.nombre_usuario)

            if self.ventana:
                self.ventana.show()
                self.close()
            else:
                QMessageBox.warning(self, "Aviso", f"Opción no implementada: {categoria} -> {opcion}")

        except ImportError as e:
            QMessageBox.critical(self, "Error de Módulo", f"No se encontró el archivo/clase: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al intentar abrir la ventana: {e}")

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def set_form_enabled(self, enabled):
        self.inp_fecha.setEnabled(enabled)
        self.inp_hora.setEnabled(enabled)
        self.inp_motivo.setEnabled(enabled)
        self.inp_estado.setEnabled(enabled)
        self.inp_mascota.setEnabled(enabled)
        self.inp_vet.setEnabled(enabled)

    def reset_form(self):
        self.inp_id.clear()
        self.inp_fecha.setDate(QDate.currentDate())
        self.inp_hora.setTime(QTime.currentTime())
        self.inp_motivo.clear()
        self.inp_estado.setCurrentIndex(0)
        self.inp_mascota.clear()
        self.inp_vet.clear()
        self.lbl_info_extra.setText("Ingresa un ID y presiona 'Buscar' para cargar los datos.")
        self.cita_cargada = False
        self.set_form_enabled(False)
        self.inp_id.setFocus()

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

        lbl_id = QLabel("ID de la cita:")
        lbl_id.setStyleSheet(label_style)
        self.inp_id = QLineEdit()
        self.inp_id.setPlaceholderText("Ingresa ID para buscar (e.g., 101)")
        self.inp_id.setStyleSheet(input_style)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_buscar.setFixedSize(100, 45)
        btn_buscar.setStyleSheet("""
            QPushButton { background-color: #7CEBFC; color: #333; font-weight: bold; border-radius: 10px; border: 1px solid #5CD0E3; }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_buscar.clicked.connect(self.buscar_cita)

        lbl_fecha = QLabel("Fecha de la cita:")
        lbl_fecha.setStyleSheet(label_style)
        self.inp_fecha = QDateEdit()
        self.inp_fecha.setCalendarPopup(True)
        self.inp_fecha.setDate(QDate.currentDate())
        self.inp_fecha.setStyleSheet(input_style)

        lbl_hora = QLabel("Hora de la cita:")
        lbl_hora.setStyleSheet(label_style)
        self.inp_hora = QTimeEdit()
        self.inp_hora.setTime(QTime.currentTime())
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

        lbl_mascota = QLabel("Id de la mascota:")
        lbl_mascota.setStyleSheet(label_style)
        self.inp_mascota = QLineEdit()
        self.inp_mascota.setStyleSheet(input_style)

        lbl_vet = QLabel("Id del veterinario:")
        lbl_vet.setStyleSheet(label_style)
        self.inp_vet = QLineEdit()
        self.inp_vet.setStyleSheet(input_style)

        grid_layout.addWidget(lbl_id, 0, 0)
        grid_layout.addWidget(self.inp_id, 0, 1)
        grid_layout.addWidget(btn_buscar, 0, 2)

        grid_layout.addWidget(lbl_fecha, 1, 0)
        grid_layout.addWidget(self.inp_fecha, 1, 1, 1, 2)

        grid_layout.addWidget(lbl_hora, 2, 0)
        grid_layout.addWidget(self.inp_hora, 2, 1, 1, 2)

        grid_layout.addWidget(lbl_motivo, 3, 0)
        grid_layout.addWidget(self.inp_motivo, 3, 1, 1, 2)

        grid_layout.addWidget(lbl_estado, 4, 0)
        grid_layout.addWidget(self.inp_estado, 4, 1, 1, 2)

        grid_layout.addWidget(lbl_mascota, 5, 0)
        grid_layout.addWidget(self.inp_mascota, 5, 1, 1, 2)

        grid_layout.addWidget(lbl_vet, 6, 0)
        grid_layout.addWidget(self.inp_vet, 6, 1, 1, 2)

        grid_layout.setColumnStretch(1, 1)
        grid_layout.setRowStretch(7, 1)
        parent_layout.addWidget(form_widget, stretch=2)

    def setup_info_board(self, parent_layout):
        board_container = QFrame()
        board_container.setFixedWidth(300)
        board_container.setStyleSheet("""
            QFrame { background-color: white; border: 1px solid #DDD; border-radius: 10px; }
        """)
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252,124,226,0.8));
            border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom: none;
        """)
        header_layout = QVBoxLayout(header_frame)
        lbl_info_title = QLabel("Información")
        lbl_info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(lbl_info_title)

        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)

        self.lbl_info_extra = QLabel("Ingresa un ID y presiona 'Buscar' para cargar los datos.")
        self.lbl_info_extra.setWordWrap(True)
        self.lbl_info_extra.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.lbl_info_extra.setStyleSheet("color: #555; font-size: 14px;")

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
            QPushButton { background-color: #b67cfc; color: white; font-size: 24px; font-weight: bold; border-radius: 30px; }
            QPushButton:hover { background-color: #a060e8; } QPushButton:pressed { background-color: #8a4cd0; }
        """)
        btn_save.clicked.connect(self.guardar_cambios)

        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_save)
        btn_container.addStretch()
        self.white_layout.addLayout(btn_container)

    def buscar_cita(self):
        id_cita = self.inp_id.text().strip()
        self.cita_cargada = False

        if not id_cita:
            QMessageBox.warning(self, "Aviso", "Por favor ingresa un ID para buscar.")
            self.set_form_enabled(False)
            return

        if not id_cita.isdigit():
            QMessageBox.warning(self, "Formato Incorrecto", "El ID de la cita debe ser un número entero.")
            self.set_form_enabled(False)
            return

        try:
            columnas = ['fecha', 'hora', 'motivo', 'estado', 'fk_mascota', 'fk_veterinario']
            registro = self.conexion1.consultar_registro('cita', 'id_cita', id_cita, columnas)

            if registro:
                fecha_bd = registro[0]
                hora_bd = registro[1]

                if isinstance(fecha_bd, date):
                    q_date = QDate(fecha_bd.year, fecha_bd.month, fecha_bd.day)
                    self.inp_fecha.setDate(q_date)
                elif isinstance(fecha_bd, str):
                    q_date = QDate.fromString(fecha_bd, "yyyy-MM-dd")
                    if q_date.isValid():
                        self.inp_fecha.setDate(q_date)

                if isinstance(hora_bd, time):
                    q_time = QTime(hora_bd.hour, hora_bd.minute, hora_bd.second)
                    self.inp_hora.setTime(q_time)
                elif isinstance(hora_bd, str):
                    q_time = QTime.fromString(hora_bd, "HH:mm:ss")
                    if q_time.isValid():
                        self.inp_hora.setTime(q_time)

                self.inp_motivo.setText(str(registro[2]))
                estado_texto = str(registro[3])
                index = self.inp_estado.findText(estado_texto, Qt.MatchFlag.MatchExactly)
                if index >= 0:
                    self.inp_estado.setCurrentIndex(index)
                else:
                    self.inp_estado.setCurrentIndex(0)

                self.inp_mascota.setText(str(registro[4]))
                self.inp_vet.setText(str(registro[5]))

                self.lbl_info_extra.setText(
                    f"Cita #{id_cita} cargada correctamente.\nMotivo original: {registro[2]}\nMascota ID: {registro[4]}, Vet ID: {registro[5]}"
                )
                self.cita_cargada = True
                self.set_form_enabled(True)
            else:
                QMessageBox.warning(self, "No encontrado", f"No se encontró ninguna cita con ID: {id_cita}")
                self.lbl_info_extra.setText("ID no encontrado. Intenta de nuevo.")
                self.set_form_enabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Error al buscar", f"Ocurrió un error al intentar cargar la cita. Detalle: {e}")
            self.set_form_enabled(False)

    def guardar_cambios(self):
        id_cita_str = self.inp_id.text().strip()
        if not self.cita_cargada:
            QMessageBox.warning(self, "Error", "Busca y carga una cita primero para poder guardar cambios.")
            return
        if not id_cita_str.isdigit():
            QMessageBox.warning(self, "Error de ID", "El ID de la cita en el campo de búsqueda debe ser un número entero.")
            return
        id_cita = id_cita_str

        datos = {
            "fecha": self.inp_fecha.date().toString("yyyy-MM-dd"),
            "hora": self.inp_hora.time().toString("HH:mm:ss"),
            "motivo": self.inp_motivo.text().strip(),
            "estado": self.inp_estado.currentText(),
            "fk_mascota": self.inp_mascota.text().strip(),
            "fk_veterinario": self.inp_vet.text().strip()
        }

        if not datos["motivo"] or not datos["fk_mascota"] or not datos["fk_veterinario"]:
            QMessageBox.warning(self, "Campos vacíos", "Todos los campos (Motivo, Mascota, Veterinario) son obligatorios.")
            return
        try:
            int(datos["fk_mascota"])
            int(datos["fk_veterinario"])
        except ValueError:
            QMessageBox.warning(self, "Error de Formato", "Los IDs de Mascota y Veterinario deben ser números enteros.")
            return

        try:
            exito = self.conexion1.editar_registro(id=id_cita, datos=datos, tabla='cita', id_columna='id_cita')
            if exito:
                QMessageBox.information(self, "Éxito", "Cita modificada correctamente.")
                self.reset_form()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la cita (verifica el ID o la conexión a la BD).")
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Ocurrió un error al actualizar: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow("Recepcionista TEST")
    window.show()
    sys.exit(app.exec())
