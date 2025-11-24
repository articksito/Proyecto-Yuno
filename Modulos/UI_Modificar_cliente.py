import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QFileDialog, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap

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
        lbl_header = QLabel("Modificar cliente")
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
        layout_options.setSpacing(2)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # CONEXIÓN DE BOTONES
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
                    from UI_Crear_cita import MainWindow as Agendar_cita
                    self.ventana = Agendar_cita()
                    self.ventana.show()
                    self.close()
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

        # Estilo de Inputs
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
        
        # 1. ID Cliente (Ahora con Botón Buscar)
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
        grid_layout.addWidget(btn_buscar, 0, 2) # Botón buscar añadido
        
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

        # Contenido (Foto de perfil)
        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.img_placeholder = QLabel("👤")
        self.img_placeholder.setFixedSize(200, 200)
        self.img_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_placeholder.setStyleSheet("""
            background-color: #F5F5F5;
            border: 2px dashed #CCC;
            border-radius: 100px;
            font-size: 60px;
            color: #CCC;
        """)
        
        btn_upload = QPushButton("Cambiar Foto")
        btn_upload.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_upload.setStyleSheet("""
            QPushButton {
                background-color: #7CEBFC;
                color: #333;
                border-radius: 15px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #6bdcf0; }
        """)
        btn_upload.clicked.connect(self.upload_photo)

        lbl_notas = QLabel("Notas:")
        lbl_notas.setStyleSheet("font-weight: bold; margin-top: 10px; color: #333;")
        
        # Hacemos self.txt_notas accesible para guardar/leer
        self.txt_notas = QTextEdit()
        self.txt_notas.setPlaceholderText("Notas adicionales sobre el cliente...")
        self.txt_notas.setFixedHeight(80)
        self.txt_notas.setStyleSheet("border: 1px solid #DDD; border-radius: 5px; background-color: #FAFAFA;")

        content_layout.addWidget(self.img_placeholder)
        content_layout.addSpacing(10)
        content_layout.addWidget(btn_upload)
        content_layout.addWidget(lbl_notas)
        content_layout.addWidget(self.txt_notas)
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

    def upload_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto", "", "Images (*.png *.xpm *.jpg)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.img_placeholder.setPixmap(pixmap.scaled(self.img_placeholder.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.img_placeholder.setStyleSheet("border: none; border-radius: 100px;")

    # --- LÓGICA DE BÚSQUEDA ---
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
            # Asumimos las columnas de tu tabla 'cliente'
            columnas = ['nombre', 'apellido', 'correo', 'direccion', 'telefono', 'notas']
            
            # Ajusta 'cliente' y 'id_cliente' según tu esquema real
            registro = self.conexion1.consultar_registro('cliente', 'id_cliente', id_cliente, columnas)
            
            if registro:
                # registro: (nombre, apellido, correo, direccion, telefono, notas)
                self.inp_nombre.setText(str(registro[0]))
                self.inp_apellido.setText(str(registro[1]))
                self.inp_correo.setText(str(registro[2]))
                self.inp_direccion.setText(str(registro[3]))
                self.inp_telefono.setText(str(registro[4]))
                
                # Notas (si existe la columna, sino ignora)
                if len(registro) > 5:
                    self.txt_notas.setText(str(registro[5]))
                
                QMessageBox.information(self, "Encontrado", "Datos del cliente cargados.")
            else:
                QMessageBox.warning(self, "No encontrado", "No existe un cliente con ese ID.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar: {e}")

    # --- LÓGICA DE GUARDADO ---
    def guardar_cambios(self):
        id_cliente = self.inp_id.text().strip()
        
        if not id_cliente:
            QMessageBox.warning(self, "Error", "Primero busca un cliente por ID.")
            return

        datos = {
            "nombre": self.inp_nombre.text().strip(),
            "apellido": self.inp_apellido.text().strip(),
            "correo": self.inp_correo.text().strip(),
            "direccion": self.inp_direccion.text().strip(),
            "telefono": self.inp_telefono.text().strip(),
            "notas": self.txt_notas.toPlainText().strip()
        }

        if not datos["nombre"] or not datos["apellido"]:
             QMessageBox.warning(self, "Aviso", "El nombre y apellido son obligatorios.")
             return

        try:
            exito = self.conexion1.editar_registro(id_cliente, datos, 'cliente', 'id_cliente')
            if exito:
                QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo al guardar: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())