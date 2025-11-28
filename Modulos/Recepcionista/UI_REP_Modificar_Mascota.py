import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap

# Configuración del path para imports relativos
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Importar conexión a la base de datos y el Menú Principal
try:
    from db_connection import Conexion
    # 🛑 Importar el Menú Principal para el retorno
    from UI_Menu_Principal import MainWindow as MenuPrincipal 
except ImportError as e:
    # Definición de clases Mock para evitar fallos si no se encuentran los archivos
    print(f"Error de importación: {e.name}")
    class Conexion:
        def consultar_registro(self, *args): return None
        def editar_registro(self, *args): return True
    class MenuPrincipal(QMainWindow):
        def __init__(self, nombre_usuario=""):
            super().__init__()
            self.setWindowTitle("MENU PRINCIPAL (MOCK)")
            self.resize(500, 300)
            self.setCentralWidget(QLabel("Ventana de Menú Principal (MOCK)"))


class MainWindow(QMainWindow):
    # Instancia de la conexión a la DB
    conexion1 = Conexion()

    def __init__(self, nombre_usuario="Recepcionista"): # Se añade nombre_usuario para consistencia
        super().__init__()
        
        self.nombre_usuario = nombre_usuario
        self.ventana = None
        # Variable para almacenar el ID de la mascota actualmente cargada
        self.mascota_id_cargada = None

        self.setWindowTitle(f"Sistema Veterinario Yuno - Modificar Mascota ({self.nombre_usuario})")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal (Horizontal)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS (Mismo código CSS del original) ---
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

        # --- 1. BARRA LATERAL ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Modificar Mascota")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        # 🛑 Botón Volver (btn_back) ELIMINADO de aquí.

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        # 🛑 header_layout.addWidget(btn_back) ELIMINADO

        self.white_layout.addLayout(header_layout)
        
        # Espaciador superior para centrar
        self.white_layout.addStretch(1)

        # Contenedor Formulario
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        self.setup_edit_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        
        # Espacio entre form y botón
        self.white_layout.addSpacing(30)
        
        # Botón Guardar
        self.setup_save_button()

        # Espaciador inferior para centrar
        self.white_layout.addStretch(2)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

        # Inicializar UI deshabilitada hasta que se cargue una mascota
        self.set_form_editable(False)

    # --- MÉTODO PARA VOLVER AL MENÚ PRINCIPAL ---
    def return_to_menu(self):
        """Muestra la ventana del menú principal (UI_Menu_Principal) y cierra la actual."""
        try:
            # Recrea el menú principal con el nombre de usuario de la sesión
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error de Navegación", f"No se pudo cargar el Menú Principal.\nDetalle: {e}")
            self.close()

    def set_form_editable(self, enabled):
        """Habilita o deshabilita los campos del formulario de edición."""
        self.inp_nombre.setEnabled(enabled)
        self.inp_edad.setEnabled(enabled)
        self.inp_peso.setEnabled(enabled)
        self.inp_especie.setEnabled(enabled)
        self.inp_raza.setEnabled(enabled)
        self.inp_cliente.setEnabled(enabled)
        # Buscar siempre debe estar activo
        self.findChild(QPushButton, "btn_guardar").setEnabled(enabled)


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
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")

        self.sidebar_layout.addWidget(lbl_logo)
        
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"]) # Se añade Visualizar para mantener consistencia
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"]) # Se añade Visualizar para mantener consistencia

        self.sidebar_layout.addStretch()

        # 🛑 Botón Modificado: Ahora es "Volver al Menú"
        btn_logout = QPushButton("↶ Volver al Menú")
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
        # 🛑 Conectar al retorno al menú
        btn_logout.clicked.connect(self.return_to_menu)
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
        
        # Si la opción es Modificar Mascota y ya estamos aquí, no hacemos nada.
        if categoria == "Mascotas" and opcion == "Modificar":
            return 
            
        target_window = None

        try:
            # Pasa siempre el nombre_usuario a la nueva ventana
            if categoria == "Citas":
                if opcion == "Agendar":
                    from UI_REP_Crear_cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_REP_Revisar_Cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)

            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    from UI_REP_Registrar_mascota import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_REP_Revisar_Mascota import MainWindow as Win # Asume este nombre
                    target_window = Win(self.nombre_usuario)
                # La opción Modificar ya está abierta

            elif categoria == "Clientes":
                if opcion == "Registrar":
                    from UI_REP_Registra_cliente import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_REP_Revisar_cliente import MainWindow as Win # Asume este nombre
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cliente import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                    
            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close()
            
        except ImportError as e:
            QMessageBox.warning(self, "Error de Navegación", f"No se pudo abrir la ventana solicitada.\nFalta el archivo: **{e.name}**")
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
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
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

        # --- Campos ---
        
        # 1. ID Mascota (Búsqueda)
        lbl_id = QLabel("Id mascota:")
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
        btn_buscar.clicked.connect(self.buscar_mascota)

        # 2. Nombre
        lbl_nombre = QLabel("Nombre:")
        lbl_nombre.setStyleSheet(label_style)
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setStyleSheet(input_style)

        # 3. Edad
        lbl_edad = QLabel("Edad (Años):")
        lbl_edad.setStyleSheet(label_style)
        self.inp_edad = QLineEdit()
        self.inp_edad.setPlaceholderText("Ej: 4")
        self.inp_edad.setStyleSheet(input_style)
        self.inp_edad.setInputMask("99") # Permite hasta 2 dígitos numéricos

        # 4. Peso
        lbl_peso = QLabel("Peso (Kg):")
        lbl_peso.setStyleSheet(label_style)
        self.inp_peso = QLineEdit()
        self.inp_peso.setPlaceholderText("Ej: 12.5")
        self.inp_peso.setStyleSheet(input_style)
        
        # 5. Especie
        lbl_especie = QLabel("Especie:")
        lbl_especie.setStyleSheet(label_style)
        self.inp_especie = QComboBox()
        self.inp_especie.addItems(["Perro", "Gato", "Ave", "Roedor", "Otro"])
        self.inp_especie.setStyleSheet(input_style)

        # 6. Raza
        lbl_raza = QLabel("Raza:")
        lbl_raza.setStyleSheet(label_style)
        self.inp_raza = QLineEdit()
        self.inp_raza.setStyleSheet(input_style)

        # 7. ID Dueño (Editable)
        lbl_cliente = QLabel("Id dueño:")
        lbl_cliente.setStyleSheet(label_style)
        self.inp_cliente = QLineEdit()
        self.inp_cliente.setPlaceholderText("ID del cliente")
        self.inp_cliente.setStyleSheet(input_style)

        # --- CONEXIÓN PARA PREVIEW ---
        self.inp_nombre.textChanged.connect(self.update_preview)
        self.inp_edad.textChanged.connect(self.update_preview)
        self.inp_peso.textChanged.connect(self.update_preview)
        self.inp_raza.textChanged.connect(self.update_preview)
        self.inp_cliente.textChanged.connect(self.update_preview)
        self.inp_especie.currentTextChanged.connect(self.update_preview)

        # Añadir al Grid
        # Fila 0: Búsqueda
        input_busqueda_layout = QHBoxLayout()
        input_busqueda_layout.addWidget(self.inp_id)
        input_busqueda_layout.addWidget(btn_buscar)
        input_busqueda_layout.setContentsMargins(0,0,0,0)
        
        grid_layout.addWidget(lbl_id, 0, 0)
        grid_layout.addLayout(input_busqueda_layout, 0, 1, 1, 2) # Ocupa dos columnas

        grid_layout.addWidget(lbl_nombre, 1, 0)
        grid_layout.addWidget(self.inp_nombre, 1, 1, 1, 2)

        grid_layout.addWidget(lbl_edad, 2, 0)
        grid_layout.addWidget(self.inp_edad, 2, 1)

        grid_layout.addWidget(lbl_peso, 3, 0)
        grid_layout.addWidget(self.inp_peso, 3, 1)

        grid_layout.addWidget(lbl_especie, 4, 0)
        grid_layout.addWidget(self.inp_especie, 4, 1)

        grid_layout.addWidget(lbl_raza, 5, 0)
        grid_layout.addWidget(self.inp_raza, 5, 1)

        grid_layout.addWidget(lbl_cliente, 6, 0)
        grid_layout.addWidget(self.inp_cliente, 6, 1)

        grid_layout.setRowStretch(7, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_board(self, parent_layout):
        # Panel derecho
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

        # Header
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

        # Contenido (Ficha Resumen)
        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        lbl_preview = QLabel("Ficha de Mascota")
        lbl_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_preview.setStyleSheet("color: #888; font-size: 14px; font-weight: bold; margin-bottom: 10px;")

        # Nombre
        self.lbl_prev_nombre = QLabel("Nombre Mascota")
        self.lbl_prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_nombre.setWordWrap(True)
        self.lbl_prev_nombre.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 15px;")

        # ID Dueño Resaltado
        self.lbl_prev_dueno = QLabel("Dueño ID: --")
        self.lbl_prev_dueno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_dueno.setStyleSheet("""
            font-size: 18px; 
            color: #2c3e50; 
            font-weight: bold; 
            background-color: #ecf0f1; 
            padding: 10px; 
            border-radius: 5px;
        """)

        # Detalles
        self.lbl_prev_detalles = QLabel("Especie - Raza")
        self.lbl_prev_detalles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_detalles.setStyleSheet("font-size: 16px; color: #555; margin-top: 15px;")

        # Stats
        self.lbl_prev_stats = QLabel("Edad: -- | Peso: --")
        self.lbl_prev_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_stats.setStyleSheet("font-size: 14px; color: #888; margin-top: 5px;")

        content_layout.addWidget(lbl_preview)
        content_layout.addWidget(self.lbl_prev_nombre)
        content_layout.addWidget(self.lbl_prev_dueno)
        content_layout.addWidget(self.lbl_prev_detalles)
        content_layout.addWidget(self.lbl_prev_stats)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)

        parent_layout.addWidget(board_container, stretch=1)

    def setup_save_button(self):
        btn_save = QPushButton("Guardar Cambios")
        btn_save.setObjectName("btn_guardar") # Añadir ObjectName para controlar la habilitación
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
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
        btn_save.clicked.connect(self.guardar_cambios)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_save)
        btn_container.addStretch()
        
        self.white_layout.addLayout(btn_container)

    # --- ACTUALIZACIÓN PREVIEW ---
    def update_preview(self):
        nombre = self.inp_nombre.text().strip()
        id_cliente = self.inp_cliente.text().strip()
        especie = self.inp_especie.currentText()
        raza = self.inp_raza.text().strip()
        edad = self.inp_edad.text().strip()
        peso = self.inp_peso.text().strip()

        self.lbl_prev_nombre.setText(nombre if nombre else "Nombre Mascota")
        self.lbl_prev_dueno.setText(f"Dueño ID: {id_cliente}" if id_cliente else "Dueño ID: --")
        self.lbl_prev_detalles.setText(f"{especie} - {raza}" if raza else f"{especie}")
        
        # Validar si edad y peso son convertibles a float/int antes de mostrarlos
        try:
            edad_val = int(edad)
            edad_txt = f"{edad_val} años" if edad_val > 0 else "Edad: 0"
        except ValueError:
            edad_txt = "Edad: -- (Inválida)" if edad else "Edad: --"
            
        try:
            peso_val = float(peso)
            peso_txt = f"{peso_val:.1f} kg"
        except ValueError:
            peso_txt = "Peso: -- (Inválido)" if peso else "Peso: --"

        self.lbl_prev_stats.setText(f"{edad_txt} | {peso_txt}")

    # --- FUNCIÓN: BUSCAR MASCOTA ---
    def buscar_mascota(self):
        id_mascota_str = self.inp_id.text().strip()
        self.mascota_id_cargada = None # Limpiar ID anterior
        self.set_form_editable(False) # Deshabilitar formulario

        if not id_mascota_str:
            QMessageBox.warning(self, "Aviso", "Ingresa un ID de mascota para buscar.")
            return
        
        if not id_mascota_str.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser numérico.")
            return

        try:
            id_mascota = int(id_mascota_str)
            print(f"Buscando mascota ID: {id_mascota}")

            # Columnas a recuperar (deben coincidir con el orden del registro)
            columnas = ['nombre', 'edad', 'peso', 'especie', 'raza', 'fk_cliente']
            # Asumimos que consultar_registro devuelve una tupla o None
            registro = self.conexion1.consultar_registro('mascota', 'id_mascota', id_mascota, columnas)
            
            if registro:
                self.inp_nombre.setText(str(registro[0]))
                self.inp_edad.setText(str(registro[1]))
                self.inp_peso.setText(f"{registro[2]:.1f}") # Formatear peso a 1 decimal
                self.inp_especie.setCurrentText(str(registro[3]))
                self.inp_raza.setText(str(registro[4]))
                self.inp_cliente.setText(str(registro[5]))
                
                # Almacenar el ID de la mascota cargada y habilitar la edición
                self.mascota_id_cargada = id_mascota
                self.set_form_editable(True) 
                self.update_preview()
                
                QMessageBox.information(self, "Encontrado", "Datos de la mascota cargados. Ahora puedes modificar.")
            else:
                QMessageBox.warning(self, "No encontrado", "No existe una mascota con ese ID.")
                self.limpiar_campos_formulario()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar en la base de datos: {e}")

    # --- FUNCIÓN: LIMPIAR CAMPOS ---
    def limpiar_campos_formulario(self):
        """Limpia todos los campos de entrada de datos."""
        self.inp_nombre.clear()
        self.inp_edad.clear()
        self.inp_peso.clear()
        self.inp_raza.clear()
        self.inp_cliente.clear()
        self.inp_especie.setCurrentIndex(0) # Pone el primer ítem
        self.update_preview()
        self.set_form_editable(False) # Deshabilitar edición

    # --- FUNCIÓN: GUARDAR CAMBIOS ---
    def guardar_cambios(self):
        id_mascota_a_modificar = self.mascota_id_cargada
        
        if id_mascota_a_modificar is None:
            QMessageBox.warning(self, "Error", "Primero debes buscar y cargar una mascota por ID.")
            return

        # Recolectar datos
        nombre = self.inp_nombre.text().strip()
        edad_str = self.inp_edad.text().strip()
        peso_str = self.inp_peso.text().strip()
        especie = self.inp_especie.currentText()
        raza = self.inp_raza.text().strip()
        id_cliente = self.inp_cliente.text().strip()

        # Validación de campos obligatorios
        if not nombre or not id_cliente:
             QMessageBox.warning(self, "Aviso", "Nombre e ID Dueño son campos obligatorios.")
             return
        
        if not id_cliente.isdigit():
            QMessageBox.warning(self, "Error", "El ID de Dueño debe ser un número entero.")
            return

        # Validación de tipos de datos (Edad y Peso)
        try:
            # Si el campo está vacío, asumimos 0 o None si la columna lo permite.
            edad = int(edad_str) if edad_str else 0
            peso = float(peso_str) if peso_str else 0.0
        except ValueError:
            QMessageBox.warning(self, "Error de Datos", "Edad debe ser un número entero y Peso un número (decimal permitido).")
            return

        # Datos a actualizar en la DB
        datos = {
            "nombre": nombre,
            "edad": edad,
            "peso": peso,
            "especie": especie,
            "raza": raza,
            "fk_cliente": int(id_cliente) # Convertir a int para la DB
        }

        try:
            # Usar la ID de la mascota cargada para la edición
            exito = self.conexion1.editar_registro(id_mascota_a_modificar, datos, 'mascota', 'id_mascota')
            
            if exito:
                QMessageBox.information(self, "Éxito", f"Mascota con ID {id_mascota_a_modificar} actualizada correctamente.")
                self.limpiar_campos_formulario()
                self.inp_id.clear() # Limpiar también el campo de búsqueda
            else:
                QMessageBox.warning(self, "Error de DB", "La base de datos reportó un fallo en la actualización. (Verificar log de conexión)")

        except Exception as e:
            error_msg = str(e).lower()
            # Intenta capturar errores comunes de SQL como la llave foránea
            if "foreign key" in error_msg or "cliente" in error_msg:
                 QMessageBox.warning(self, "Error Dueño", f"El ID de dueño '{id_cliente}' no existe en la base de datos de clientes.")
            else:
                QMessageBox.critical(self, "Fallo al Guardar", f"Ocurrió un error inesperado al guardar: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    # 🛑 Se pasa un nombre de usuario de prueba para consistencia
    window = MainWindow("Recepcionista Prueba") 
    window.show()
    sys.exit(app.exec())