import sys
import os

# --- CONFIGURACIÓN DE RUTAS PARA IMPORTACIONES ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)


from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QMessageBox, QComboBox, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIntValidator, QDoubleValidator

# Si tienes un archivo db_connection.py, descomenta:
# from db_connection import Conexion

class MainWindow(QMainWindow):
    # conexion1 = Conexion() # Descomentar para producción

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Modificar Mascota")
        self.resize(1280, 720)
        
        # Variable para saber qué ID estamos editando
        self.current_mascota_id = None

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

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
                font-family: 'Segoe UI', sans-serif; color: #333;
            }
            
            /* --- MENÚ LATERAL --- */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px; color: white;
                font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF;
            }
            QPushButton.sub-btn {
                text-align: left; font-family: 'Segoe UI', sans-serif;
                font-size: 16px; font-weight: normal; padding-left: 40px;
                border-radius: 10px; color: #F0F0F0;
                background-color: rgba(0, 0, 0, 0.05); height: 35px;
                margin-bottom: 2px; margin-left: 10px; margin-right: 10px;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }

            /* --- INPUTS Y FORMULARIO --- */
            QLineEdit, QComboBox {
                background-color: rgba(241, 131, 227, 0.15); 
                border: 1px solid rgba(241, 131, 227, 0.5);
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 16px;
                color: #333;
                height: 40px;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: white;
                border: 2px solid #FC7CE2;
            }
            QComboBox::drop-down { border: 0px; }
            
            /* --- PANEL DERECHO (INFO) --- */
            QFrame#InfoBoard {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 12px;
            }
        """)

        # --- 1. BARRA LATERAL ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO ---
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- SETUP UI ---
    # ==========================================

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # --- LOGO ROBUSTO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)

        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled)
            else:
                lbl_logo.setText("YUNO VET")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # --- MENÚ LATERAL (Lista Especificada) ---
        self.setup_accordion_group("Cita", ["Visualizar"])
        self.setup_accordion_group("Consulta", ["Visualizar"])
        self.setup_accordion_group("Mascota", ["Visualizar"])
        self.setup_accordion_group("Cliente", ["Visualizar"])
        self.setup_accordion_group("Hospitalizacion", ["Visualizar"])
        self.setup_accordion_group("Medicamentos", ["Visualizar", "Agregar"])
        self.setup_accordion_group("Usuarios", ["Agregar", "Modificar", "Visualizar"])
        self.setup_accordion_group("Especialidad", ["Agregar", "Modificar"])

        self.sidebar_layout.addStretch()

        # Botón Salir
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
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.navegar(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        # Margen derecho reducido para pegar el contenido
        self.white_layout.setContentsMargins(40, 40, 20, 40)

        # 1. Header
        header = QHBoxLayout()
        lbl_header = QLabel("Modificar Mascota")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-size: 16px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #E0E0E0; color: #333; }
        """)
        btn_back.clicked.connect(self.close)

        header.addWidget(lbl_header)
        header.addStretch()
        header.addWidget(btn_back)
        self.white_layout.addLayout(header)
        self.white_layout.addSpacing(10)

        # 2. Barra de Búsqueda (Arriba)
        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        # 3. Contenedor Principal (Dividido)
        content_split = QHBoxLayout()
        content_split.setSpacing(40)

        # --- A. Izquierda: Formulario Editable ---
        self.setup_form_left(content_split)

        # --- B. Derecha: Preview Info ---
        self.setup_info_right(content_split)

        self.white_layout.addLayout(content_split)
        
        # 4. Botón Guardar (Abajo)
        self.setup_save_button()

        self.white_layout.addStretch()

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_search = QLabel("ID Mascota:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        
        self.inp_search_id = QLineEdit()
        self.inp_search_id.setPlaceholderText("Ej: 1092")
        self.inp_search_id.setFixedWidth(200)
        self.inp_search_id.setValidator(QIntValidator()) # Solo números
        self.inp_search_id.setStyleSheet("""
            QLineEdit { border: 2px solid #ddd; border-radius: 10px; padding: 8px 15px; font-size: 16px; color: #333; background-color: #F9F9F9; }
        """)
        
        btn_search = QPushButton("Buscar")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setFixedSize(120, 40)
        btn_search.setStyleSheet("""
            QPushButton { background-color: #7CEBFC; color: #333; font-weight: bold; font-size: 16px; border-radius: 10px; border: 1px solid #5CD0E3; }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_search.clicked.connect(self.buscar_mascota)
        
        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.inp_search_id)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_container)

    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        label_style = "font-size: 18px; font-weight: 500; color: #444;"

        # Campos
        self.inp_nombre = QLineEdit()
        self.inp_edad = QLineEdit()
        self.inp_edad.setValidator(QIntValidator())
        self.inp_peso = QLineEdit()
        self.inp_peso.setValidator(QDoubleValidator())
        
        self.inp_especie = QComboBox()
        self.inp_especie.addItems(["Canino", "Felino", "Ave", "Roedor", "Otro"])
        
        self.inp_raza = QLineEdit()
        
        self.inp_dueno = QLineEdit() # ID del dueño
        self.inp_dueno.setValidator(QIntValidator())
        self.inp_dueno.setPlaceholderText("ID Cliente")

        # Conectar señales para Live Preview
        self.inp_nombre.textChanged.connect(self.update_preview)
        self.inp_edad.textChanged.connect(self.update_preview)
        self.inp_peso.textChanged.connect(self.update_preview)
        self.inp_especie.currentTextChanged.connect(self.update_preview)
        self.inp_raza.textChanged.connect(self.update_preview)
        self.inp_dueno.textChanged.connect(self.update_preview)

        # Agregar al Grid
        # (Label, Row, Col)
        grid.addWidget(QLabel("Nombre:", styleSheet=label_style), 0, 0)
        grid.addWidget(self.inp_nombre, 0, 1)

        grid.addWidget(QLabel("Edad (Años):", styleSheet=label_style), 1, 0)
        grid.addWidget(self.inp_edad, 1, 1)

        grid.addWidget(QLabel("Peso (Kg):", styleSheet=label_style), 2, 0)
        grid.addWidget(self.inp_peso, 2, 1)

        grid.addWidget(QLabel("Especie:", styleSheet=label_style), 3, 0)
        grid.addWidget(self.inp_especie, 3, 1)

        grid.addWidget(QLabel("Raza:", styleSheet=label_style), 4, 0)
        grid.addWidget(self.inp_raza, 4, 1)

        grid.addWidget(QLabel("ID Dueño:", styleSheet=label_style), 5, 0)
        grid.addWidget(self.inp_dueno, 5, 1)

        # Deshabilitar al inicio
        form_widget.setEnabled(False)
        self.form_widget = form_widget # Guardar referencia para habilitar después

        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_right(self, parent_layout):
        board = QFrame()
        board.setObjectName("InfoBoard")
        board.setMaximumWidth(400)
        
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)

        # Header Board
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.9));
            border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: none;
        """)
        head_lay = QHBoxLayout(header)
        lbl_tit = QLabel("Vista Previa")
        lbl_tit.setStyleSheet("color: white; font-weight: bold; font-size: 16px; border: none; background: transparent;")
        head_lay.addWidget(lbl_tit, alignment=Qt.AlignmentFlag.AlignCenter)
        board_lay.addWidget(header)

        # Contenido
        content = QWidget()
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(20, 30, 20, 30)
        content_lay.setSpacing(10)
        content_lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Foto Placeholder
        lbl_pic = QLabel("🐾")
        lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_pic.setStyleSheet("font-size: 50px; background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        content_lay.addWidget(lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Datos Preview
        self.prev_nombre = QLabel("Nombre Mascota")
        self.prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_nombre.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.prev_detalle = QLabel("Especie | Raza")
        self.prev_detalle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_detalle.setStyleSheet("font-size: 16px; color: #666;")

        self.prev_dueno = QLabel("Dueño ID: --")
        self.prev_dueno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_dueno.setStyleSheet("font-size: 14px; font-weight: bold; color: #FC7CE2; background: #FFF0F5; padding: 5px; border-radius: 5px; margin-top: 5px;")

        self.prev_stats = QLabel("Edad: -- | Peso: --")
        self.prev_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_stats.setStyleSheet("font-size: 14px; color: #888; margin-top: 10px;")

        content_lay.addWidget(self.prev_nombre)
        content_lay.addWidget(self.prev_detalle)
        content_lay.addWidget(self.prev_dueno)
        content_lay.addWidget(self.prev_stats)
        content_lay.addStretch()

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    def setup_save_button(self):
        container = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_guardar.setFixedSize(250, 55)
        self.btn_guardar.setEnabled(False) # Deshabilitado al inicio
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #b67cfc; color: white; font-size: 20px; font-weight: bold; border-radius: 27px;
            }
            QPushButton:hover { background-color: #a060e8; }
            QPushButton:disabled { background-color: #cccccc; color: #666; }
        """)
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        
        container.addStretch()
        container.addWidget(self.btn_guardar)
        container.addStretch()
        self.white_layout.addLayout(container)

    # ==========================================
    # --- LOGICA ---
    # ==========================================

    def update_preview(self):
        nom = self.inp_nombre.text()
        esp = self.inp_especie.currentText()
        raz = self.inp_raza.text()
        due = self.inp_dueno.text()
        eda = self.inp_edad.text()
        pes = self.inp_peso.text()

        self.prev_nombre.setText(nom if nom else "Nombre Mascota")
        self.prev_detalle.setText(f"{esp} | {raz if raz else 'Raza'}")
        self.prev_dueno.setText(f"Dueño ID: {due}" if due else "Dueño ID: --")
        self.prev_stats.setText(f"Edad: {eda if eda else '-'} | Peso: {pes if pes else '-'} kg")

    def buscar_mascota(self):
        id_busqueda = self.inp_search_id.text().strip()
        if not id_busqueda:
            QMessageBox.warning(self, "Error", "Ingresa un ID válido.")
            return

        print(f"Buscando mascota {id_busqueda}...")
        
        # 1. Consultar BD
        datos = self.db_consultar_mascota(id_busqueda)
        
        if datos:
            self.current_mascota_id = id_busqueda
            
            # 2. Llenar campos
            self.inp_nombre.setText(str(datos.get("nombre", "")))
            self.inp_edad.setText(str(datos.get("edad", "")))
            self.inp_peso.setText(str(datos.get("peso", "")))
            self.inp_raza.setText(str(datos.get("raza", "")))
            self.inp_dueno.setText(str(datos.get("fk_cliente", "")))
            
            idx = self.inp_especie.findText(datos.get("especie", ""), Qt.MatchFlag.MatchFixedString)
            if idx >= 0: self.inp_especie.setCurrentIndex(idx)

            # 3. Habilitar edición
            self.form_widget.setEnabled(True)
            self.btn_guardar.setEnabled(True)
            self.update_preview()
            
            QMessageBox.information(self, "Éxito", "Mascota encontrada. Puedes editar los datos.")
        else:
            QMessageBox.warning(self, "No encontrado", "No existe una mascota con ese ID.")
            self.form_widget.setEnabled(False)
            self.btn_guardar.setEnabled(False)
            self.current_mascota_id = None

    def guardar_cambios(self):
        if not self.current_mascota_id: return

        # Recolectar datos
        datos_nuevos = {
            "nombre": self.inp_nombre.text(),
            "edad": self.inp_edad.text(),
            "peso": self.inp_peso.text(),
            "especie": self.inp_especie.currentText(),
            "raza": self.inp_raza.text(),
            "fk_cliente": self.inp_dueno.text()
        }

        # Validaciones básicas
        if not datos_nuevos["nombre"] or not datos_nuevos["fk_cliente"]:
            QMessageBox.warning(self, "Error", "El nombre y el ID del dueño son obligatorios.")
            return

        # Actualizar BD
        exito = self.db_actualizar_mascota(self.current_mascota_id, datos_nuevos)
        
        if exito:
            QMessageBox.information(self, "Guardado", "Los cambios han sido guardados correctamente.")
            # Opcional: Limpiar o mantener
            self.form_widget.setEnabled(False)
            self.btn_guardar.setEnabled(False)
            self.inp_search_id.clear()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la información.")

    # ==========================================
    # --- FUNCIONES BD (PLACEHOLDERS) ---
    # ==========================================

    def db_consultar_mascota(self, id_mascota):
        """
        TODO: Reemplazar con: 
        cursor.execute("SELECT * FROM mascota WHERE id_mascota = %s", (id_mascota,))
        """
        # Simulacion
        if id_mascota == "1092":
            return {
                "nombre": "Max",
                "edad": 4,
                "peso": 12.5,
                "especie": "Canino",
                "raza": "Golden Retriever",
                "fk_cliente": 55
            }
        return None

    def db_actualizar_mascota(self, id_mascota, datos):
        """
        TODO: Reemplazar con UPDATE mascota SET ... WHERE id_mascota = ...
        """
        print(f"Actualizando ID {id_mascota} con: {datos}")
        return True

    # ==========================================
    # --- UTILIDADES ---
    # ==========================================
    
    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def navegar(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        # Lógica de importación de ventanas

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())