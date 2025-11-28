import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# Se asume que 'db_connection.py' y 'Conexion' están disponibles en el path.
# Para este ejemplo, mantendremos la estructura de importación del usuario.
try:
    # Ajuste de ruta para el entorno de ejecución
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    if project_root not in sys.path:
        sys.path.append(project_root)
    if current_dir not in sys.path:
        sys.path.append(current_dir)
        
    from db_connection import Conexion
except ImportError:
    # Manejo de error si la conexión no se puede importar
    class Conexion:
        def consultar_registro(self, tabla, id_columna, id_valor, columnas, joins):
            print("AVISO: Clase Conexion no disponible. Usando Mock Data.")
            if id_valor == '101':
                # Datos simulados para una cita exitosa
                return ('2025-12-20', '10:30:00', 'Chequeo anual y vacuna', 'Confirmada', 
                        'Milo', 'Juan', 'Pérez', 'Dr. Mateo', 'García')
            return None
    
    
class MainWindow(QMainWindow):
    # Inicialización de la conexión. Usará el mock si la importación falla.
    conexion1 = Conexion()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Revisar Cita")
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
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
                transition: all 0.3s;
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
                transition: all 0.3s;
            }
            QPushButton.sub-btn:hover {
                color: white;
                background-color: rgba(255, 255, 255, 0.3);
                font-weight: bold;
            }
            /* Estilo de Campo de Búsqueda */
            #SearchInput {
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 8px 15px;
                font-size: 16px;
                color: #333;
                background-color: #F9F9F9;
            }
            /* Estilo de Botón de Búsqueda */
            #SearchButton {
                background-color: #7CEBFC; /* Azul Claro */
                color: #333;
                font-weight: bold;
                font-size: 16px;
                border-radius: 10px;
                border: 1px solid #5CD0E3;
            }
            #SearchButton:hover { 
                background-color: #5CD0E3; 
                color: white;
            }
            /* Estilo Campos de Lectura */
            #ReadonlyInput {
                background-color: #F0F0F0;
                border: 1px solid #DDD;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 18px;
                color: #555;
                height: 45px;
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
        lbl_header = QLabel("Revisar Cita")
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

        # Barra de Búsqueda
        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        # Contenedor Horizontal para Datos + Panel Info
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        # --- A. LISTA DE DATOS (Izquierda) ---
        self.setup_details_form(content_layout)

        # --- B. PANEL DE INFORMACIÓN (Derecha - Motivo) ---
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        
        # --- ESPACIADOR INFERIOR (Centrado) ---
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

        # --- LOGO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))

        # Se utiliza una ruta relativa robusta para la imagen
        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)

        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                lbl_logo.setText("YUNO VET (Logo no cargado)")
        else:
            lbl_logo.setText("YUNO VET (Placeholder)")

        self.sidebar_layout.addWidget(lbl_logo)
        
        # Setup Accordion Groups
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
            # Conexión mejorada usando functools.partial si fuera necesario, 
            # pero lambda con argumentos default es suficiente aquí
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.abrir_ventana(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    # --- GESTOR DE VENTANAS ---
    def abrir_ventana(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        try:
            # Importaciones dentro de la función para evitar errores si no existen los archivos
            if categoria == "Citas":
                if opcion == "Agendar":
                    from UI_REP_Crear_cita import MainWindow as Agendar_cita
                    self.ventana = Agendar_cita()
                    self.ventana.show()
                    self.close()
                elif opcion == "Visualizar":
                    # Ya estamos aquí, no hacemos nada
                    return 
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
                    from UI_REP_Modificar_cliente import MainWindow as Modificar_cliente
                    self.ventana = Modificar_cliente()
                    self.ventana.show()
                    self.close()
                    
        except ImportError as e:
            QMessageBox.warning(self, "Error de Navegación", f"No se pudo abrir la ventana solicitada.\nFalta el archivo: {e.name}.py")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al intentar abrir la ventana: {e}")

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_search = QLabel("ID Cita:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        
        self.inp_search = QLineEdit()
        self.inp_search.setObjectName("SearchInput")
        self.inp_search.setPlaceholderText("Ingresa el ID de la cita a revisar (Ej. 101 para prueba)")
        self.inp_search.setFixedWidth(300)
        
        btn_search = QPushButton("Buscar")
        btn_search.setObjectName("SearchButton")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setFixedSize(120, 40)
        btn_search.clicked.connect(self.buscar_cita)
        
        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.inp_search)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_container)

    def setup_details_form(self, parent_layout):
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        label_style = "font-size: 20px; color: black; font-weight: 500;"

        def add_row(row, label_text, attr_name):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            inp = QLineEdit()
            inp.setReadOnly(True)
            inp.setText("---")
            inp.setObjectName("ReadonlyInput")
            setattr(self, attr_name, inp)
            grid_layout.addWidget(lbl, row, 0)
            grid_layout.addWidget(inp, row, 1)

        add_row(0, "Fecha:", "inp_fecha")
        add_row(1, "Hora:", "inp_hora")
        add_row(2, "Estado:", "inp_estado")
        add_row(3, "Mascota:", "inp_mascota")
        add_row(4, "Cliente:", "inp_cliente")
        add_row(5, "Veterinario:", "inp_vet")

        grid_layout.setColumnStretch(1, 1)
        parent_layout.addWidget(form_widget, stretch=2)

    def setup_info_board(self, parent_layout):
        board_container = QFrame()
        board_container.setFixedWidth(350)
        board_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 15px; /* Ligeramente más redondeado */
            }
        """)
        
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8));
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-bottom: none;
        """)
        header_layout = QVBoxLayout(header_frame)
        lbl_info_title = QLabel("Motivo de la Cita")
        lbl_info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info_title.setStyleSheet("color: white; font-size: 20px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(lbl_info_title)

        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 15px; border-bottom-right-radius: 15px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        self.lbl_motivo_text = QLabel("Ingrese un ID y presione 'Buscar' para ver los detalles...")
        self.lbl_motivo_text.setWordWrap(True)
        self.lbl_motivo_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.lbl_motivo_text.setStyleSheet("color: #555; font-size: 16px; border: none; line-height: 1.5; padding: 0;")
        
        content_layout.addWidget(self.lbl_motivo_text)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)

        parent_layout.addWidget(board_container, stretch=1)

    # --- FUNCIÓN: BUSCAR CITA ---
    def buscar_cita(self):
        id_cita = self.inp_search.text().strip()
        self.limpiar_datos() # Limpia antes de intentar buscar

        if not id_cita:
            QMessageBox.warning(self, "Aviso", "Ingresa un ID de cita.")
            return
        
        if not id_cita.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número entero.")
            return

        print(f"Consultando cita ID: {id_cita}")
        try:
            # Columnas a seleccionar de la base de datos (IMPORTANTE MANTENER EL ORDEN)
            columnas = [
                "cita.fecha",           # 0
                "cita.hora",            # 1
                "cita.motivo",          # 2
                "cita.estado",          # 3
                "mascota.nombre",       # 4
                "cliente.nombre",       # 5 (Nombre Cliente)
                "cliente.apellido",     # 6 (Apellido Cliente)
                "usuario.nombre",       # 7 (Nombre Veterinario)
                "usuario.apellido"      # 8 (Apellido Veterinario)
            ]

            
            # JOINS para obtener los nombres completos
            joins = """
                JOIN mascota ON cita.fk_mascota = mascota.id_mascota
                JOIN cliente ON mascota.fk_cliente = cliente.id_cliente
                JOIN veterinario ON cita.fk_veterinario = veterinario.id_veterinario
                JOIN usuario ON veterinario.fk_usuario = usuario.id_usuario
            """
            
            registro = self.conexion1.consultar_registro(
                tabla='cita', 
                id_columna='cita.id_cita', 
                id_valor=id_cita, 
                columnas=columnas,
                joins=joins
            )
            
            if registro:
                # Asignación de datos del registro
                self.inp_fecha.setText(str(registro[0]))
                self.inp_hora.setText(str(registro[1]))
                self.lbl_motivo_text.setText(str(registro[2]))
                self.inp_estado.setText(str(registro[3]))
                
                self.inp_mascota.setText(str(registro[4]))
                self.inp_cliente.setText(f"{registro[5]} {registro[6]}")
                
                # Formato Dr. Nombre Apellido para el veterinario
                nombre_vet = f"{registro[7]} {registro[8]}" if len(registro) > 8 else str(registro[7])
                self.inp_vet.setText(f"Dr. {nombre_vet.strip()}")
                
                # Muestra el mensaje de éxito
                QMessageBox.information(self, "Cita Encontrada", "Cita cargada exitosamente.")
            else:
                self.limpiar_datos()
                QMessageBox.warning(self, "No Encontrado", f"No existe cita con el ID {id_cita}.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error de Búsqueda", f"Error al buscar la cita: {e}")
            self.limpiar_datos()

    def limpiar_datos(self):
        self.inp_fecha.setText("---")
        self.inp_hora.setText("---")
        self.inp_estado.setText("---")
        self.inp_mascota.setText("---")
        self.inp_cliente.setText("---")
        self.inp_vet.setText("---")
        self.lbl_motivo_text.setText("Ingrese un ID y presione 'Buscar' para ver los detalles...")

if __name__ == "__main__":
    # La clase 'Conexion' debe estar disponible, si no, el mock se activa automáticamente.
    # Para probar sin BD, ingrese '101' en el campo de ID.
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())