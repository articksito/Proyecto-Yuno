import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                            QGridLayout, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap

# Importar conexión
from db_connection import Conexion

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Modificar Cliente")
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

        # --- 2. PANEL BLANCO (Derecha - Modificar Cliente) ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header con Título y Botón Volver
        header_layout = QHBoxLayout()
        
        lbl_header = QLabel("Modificar cliente")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                color: #555;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
                color: #333;
            }
        """)
        btn_back.clicked.connect(self.close)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_back)

        self.white_layout.addLayout(header_layout)
        
        # --- ESPACIADOR SUPERIOR (Centrado) ---
        self.white_layout.addStretch(1)

        # Contenedor Horizontal para Formulario + Panel Info
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        # --- A. FORMULARIO DE EDICIÓN (Izquierda) ---
        self.setup_edit_form(content_layout)

        # --- B. PANEL DE INFORMACIÓN (Derecha) ---
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        
        # Espacio entre form y botón
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
        self.sidebar_layout.setSpacing(5)

        # --- LOGO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))

        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)

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
            if categoria == "Citas":
                if opcion == "Agendar":
                    from UI_REP_Crear_cita import MainWindow as Agendar_cita
                    self.ventana = Agendar_cita()
                    self.ventana.show()
                    self.close()
                elif opcion == "Visualizar":
                    from UI_REP_Revisar_Cita import MainWindow as Visualizar_cita
                    self.ventana = Visualizar_cita()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cita import MainWindow as Modificar_cita
                    self.ventana = Modificar_cita()
                    self.ventana.show()
                    self.close()

            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    from UI_REP_Registrar_mascota import MainWindow as Registrar_mascota
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
                    from UI_REP_Registra_cliente import MainWindow as Regsitrar_dueno
                    self.ventana = Regsitrar_dueno()
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    pass # Ya estamos aquí
                    
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

        # Estilo de Inputs Editables
        input_style = """
            QLineEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 18px;
                color: #333;
                height: 45px;
            }
        """
        label_style = "font-size: 24px; color: black; font-weight: 400;"

        # --- Campos ---
        
        # 1. ID Cliente (Campo de Búsqueda)
        lbl_id = QLabel("Id cliente:")
        lbl_id.setStyleSheet(label_style)
        self.inp_id = QLineEdit()
        self.inp_id.setPlaceholderText("Buscar ID...")
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
        btn_buscar.clicked.connect(self.buscar_cliente)

        # 2. Nombre
        lbl_nombre = QLabel("Nombre:")
        lbl_nombre.setStyleSheet(label_style)
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setStyleSheet(input_style)

        # 3. Apellido
        lbl_apellido = QLabel("Apellido:")
        lbl_apellido.setStyleSheet(label_style)
        self.inp_apellido = QLineEdit()
        self.inp_apellido.setStyleSheet(input_style)

        # 4. Correo
        lbl_correo = QLabel("Correo:")
        lbl_correo.setStyleSheet(label_style)
        self.inp_correo = QLineEdit()
        self.inp_correo.setStyleSheet(input_style)

        # 5. Dirección
        lbl_direccion = QLabel("Dirección:")
        lbl_direccion.setStyleSheet(label_style)
        self.inp_direccion = QLineEdit()
        self.inp_direccion.setStyleSheet(input_style)

        # 6. Teléfono
        lbl_telefono = QLabel("Teléfono:")
        lbl_telefono.setStyleSheet(label_style)
        self.inp_telefono = QLineEdit()
        self.inp_telefono.setStyleSheet(input_style)

        # Añadir al Grid
        grid_layout.addWidget(lbl_id, 0, 0)
        grid_layout.addWidget(self.inp_id, 0, 1)
        grid_layout.addWidget(btn_buscar, 0, 2)
        
        grid_layout.addWidget(lbl_nombre, 1, 0)
        grid_layout.addWidget(self.inp_nombre, 1, 1)

        grid_layout.addWidget(lbl_apellido, 2, 0)
        grid_layout.addWidget(self.inp_apellido, 2, 1)

        grid_layout.addWidget(lbl_correo, 3, 0)
        grid_layout.addWidget(self.inp_correo, 3, 1)

        grid_layout.addWidget(lbl_direccion, 4, 0)
        grid_layout.addWidget(self.inp_direccion, 4, 1)

        grid_layout.addWidget(lbl_telefono, 5, 0)
        grid_layout.addWidget(self.inp_telefono, 5, 1)

        grid_layout.setRowStretch(6, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_board(self, parent_layout):
        # Panel derecho para INFORMACIÓN EXTRA
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

        # Header degradado
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

        # Contenido (SOLO NOTAS - VISUAL)
        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        lbl_notas = QLabel("Observaciones / Historial:")
        lbl_notas.setStyleSheet("font-weight: bold; font-size: 16px; color: #333; margin-bottom: 5px;")
        
        self.txt_notas = QTextEdit()
        self.txt_notas.setPlaceholderText("Espacio para notas locales (No se guardan en BD)...")
        self.txt_notas.setStyleSheet("""
            border: 1px solid #DDD; 
            border-radius: 5px; 
            background-color: #FAFAFA; 
            font-size: 14px;
            padding: 10px;
        """)

        content_layout.addWidget(lbl_notas)
        content_layout.addWidget(self.txt_notas)
        
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

    # --- FUNCIÓN: BUSCAR CLIENTE ---
    def buscar_cliente(self):
        id_cliente = self.inp_id.text().strip()
        
        if not id_cliente:
            QMessageBox.warning(self, "Aviso", "Ingresa un ID de cliente para buscar.")
            return
        
        if not id_cliente.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser numérico.")
            return

        print(f"Buscando cliente ID: {id_cliente}")
        try:
            # Columnas a traer de la BD (Sin 'notas')
            columnas = ['nombre', 'apellido', 'correo', 'direccion', 'telefono']
            
            registro = self.conexion1.consultar_registro('cliente', 'id_cliente', id_cliente, columnas)
            
            if registro:
                self.inp_nombre.setText(str(registro[0]))
                self.inp_apellido.setText(str(registro[1]))
                self.inp_correo.setText(str(registro[2]))
                self.inp_direccion.setText(str(registro[3]))
                self.inp_telefono.setText(str(registro[4]))
                
                # Limpiamos notas ya que no vienen de BD
                self.txt_notas.clear()
                
                QMessageBox.information(self, "Encontrado", "Datos del cliente cargados correctamente.")
            else:
                QMessageBox.warning(self, "No encontrado", "No existe un cliente con ese ID.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar: {e}")

    # --- FUNCIÓN: GUARDAR CAMBIOS ---
    def guardar_cambios(self):
        id_cliente = self.inp_id.text().strip()
        
        if not id_cliente:
            QMessageBox.warning(self, "Error", "Primero busca un cliente por ID para modificar.")
            return

        # Recolectar datos
        nombre = self.inp_nombre.text().strip()
        apellido = self.inp_apellido.text().strip()
        correo = self.inp_correo.text().strip()
        direccion = self.inp_direccion.text().strip()
        telefono_str = self.inp_telefono.text().strip()
        
        # Notas no se guarda en BD

        if not nombre or not apellido:
             QMessageBox.warning(self, "Aviso", "El nombre y apellido son obligatorios.")
             return

        # Convertir teléfono a entero (BigInt) si es necesario
        try:
            telefono_num = int(telefono_str) if telefono_str else None
        except ValueError:
            QMessageBox.warning(self, "Error", "El teléfono debe ser numérico.")
            return

        # Diccionario de datos a actualizar (SIN 'notas')
        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "direccion": direccion,
            "telefono": telefono_num
        }

        try:
            # Aseguramos usar editar_registro
            exito = self.conexion1.editar_registro(id_cliente, datos, 'cliente', 'id_cliente')
            if exito:
                QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar el registro.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo al guardar: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())