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
                             QHBoxLayout, QPushButton, QLabel, QFrame, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QColor, QBrush

from db_connection import Conexion

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Gestión de Pacientes (Admin)")
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
            
            /* --- ESTILO TABLA --- */
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 15px;
                gridline-color: transparent; 
                font-size: 14px;
                selection-background-color: #E1BEE7; 
                selection-color: #333;
                alternate-background-color: #FAFAFA; 
                outline: 0;
            }
            QHeaderView::section {
                background-color: #7CEBFC; 
                color: #444;
                font-weight: bold;
                border: none;
                padding: 12px;
                font-size: 15px;
                font-family: 'Segoe UI';
            }
            QHeaderView::section:first { border-top-left-radius: 15px; }
            QHeaderView::section:last { border-top-right-radius: 15px; }
            
            QTableWidget::item {
                padding: 5px 10px;
                border-bottom: 1px solid #F0F0F0; 
            }
            
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #CCC;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover { background: #BBB; }
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
        lbl_header = QLabel("Listado de Pacientes")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        # Botón Refrescar
        btn_refresh = QPushButton("↻ Actualizar")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFixedSize(120, 40)
        btn_refresh.setStyleSheet("""
            QPushButton { 
                background-color: #7CEBFC; 
                color: #444; 
                border-radius: 10px; 
                font-weight: bold; 
                border: 1px solid #5CD0E3; 
            }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_refresh.clicked.connect(self.cargar_datos_tabla)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_refresh)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # Tabla de Pacientes
        self.setup_table()

        # Cargar datos iniciales
        self.cargar_datos_tabla()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

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
        
        ruta_logo = "logo.png" 
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
        self.sidebar_layout.addSpacing(20)

        # --- MENU (Específico de Admin) ---
        self.setup_accordion_group("Administrar", ["Pacientes", "Clientes", "Citas"])
        self.setup_accordion_group("Usuarios", ["Crear", "Modificar", "Consultar"])
        self.setup_accordion_group("Medicamentos", ["Agregar", "Modificar"])

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
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.abrir_ventana(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    # --- GESTOR DE VENTANAS ---
    def abrir_ventana(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        try:
            # --- ADMINISTRAR ---
            if categoria == "Administrar":
                if opcion == "Pacientes":
                    pass # Ya estamos aquí
                elif opcion == "Clientes":
                    from UI_Modificar_cliente import MainWindow as ClientesWindow
                    self.ventana = ClientesWindow()
                    self.ventana.show()
                    self.close()
                elif opcion == "Citas":
                    from UI_Revisar_Cita import MainWindow as CitasWindow
                    self.ventana = CitasWindow()
                    self.ventana.show()
                    self.close()
            
            # Puedes agregar el resto de la lógica de navegación aquí
            
        except ImportError as e:
            QMessageBox.warning(self, "Error", f"No se encontró la ventana: {e.name}")

    def setup_table(self):
        # Columnas: ID, Nombre, Especie, Raza, Observaciones, Acciones
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Especie", "Raza", "Observaciones", "Acciones"])
        
        # Configuración visual
        self.table.setShowGrid(False) 
        self.table.setAlternatingRowColors(True) 
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus) 
        
        # Ajuste de cabeceras
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed) # ID fijo
        self.table.setColumnWidth(0, 80)
        
        # CAMBIO: Nombre fijo y más pequeño para dar espacio a Observaciones
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed) 
        self.table.setColumnWidth(1, 150) 
        
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch) # Obs flexible
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed) # Botón fijo
        self.table.setColumnWidth(5, 100)
        
        # Altura de filas
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.verticalHeader().setVisible(False)

        # Comportamiento
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.white_layout.addWidget(self.table)

    def cargar_datos_tabla(self):
        """Obtiene datos de la BD y rellena la tabla"""
        self.table.setRowCount(0)
        
        pacientes = self.conexion1.obtener_todos_pacientes()

        for row_idx, data in enumerate(pacientes):
            self.table.insertRow(row_idx)
            
            # data = (id_mascota, nombre, especie, raza, padecimientos)
            
            # Insertar textos centrados
            item_id = QTableWidgetItem(str(data[0]))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 0, item_id)
            
            # CAMBIO: Nombre centrado
            item_nombre = QTableWidgetItem(str(data[1]))
            item_nombre.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 1, item_nombre)
            
            item_esp = QTableWidgetItem(str(data[2]))
            item_esp.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 2, item_esp)
            
            item_raza = QTableWidgetItem(str(data[3]))
            item_raza.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 3, item_raza)
            
            # Observaciones (No agregado todavia)
            # obs = str(data[4]) if data[4] else ""
            # item_obs = QTableWidgetItem(obs)
            # item_obs.setToolTip(obs)
            # self.table.setItem(row_idx, 4, item_obs)

            # Insertar Botón Editar
            btn_edit = QPushButton("Editar")
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.setStyleSheet("""
                QPushButton {
                    background-color: #AB47BC; /* Violeta */
                    color: white;
                    border-radius: 8px;
                    font-weight: bold;
                    padding: 6px;
                    font-size: 12px;
                }
                QPushButton:hover { background-color: #BA68C8; }
            """)
            
            # Conectamos el botón
            btn_edit.clicked.connect(lambda checked=False, id_mascota=data[0]: self.abrir_modificar_mascota(id_mascota))
            
            # Contenedor para centrar el botón
            cell_widget = QWidget()
            layout_cell = QHBoxLayout(cell_widget)
            layout_cell.setContentsMargins(5, 5, 5, 5)
            layout_cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_cell.addWidget(btn_edit)
            
            self.table.setCellWidget(row_idx, 5, cell_widget)


    def abrir_modificar_mascota(self, id_mascota):
        print(f"Abriendo modificar mascota para ID: {id_mascota}")
        try:
            from UI_Revisar_Mascota import MainWindow as ModificarMascota
            self.ventana = ModificarMascota() 
            self.ventana.inp_id.setText(str(id_mascota)) # Prellenar el campo ID
            self.ventana.buscar_mascota() # Ejecutar búsqueda automática
            self.ventana.show()
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la ventana de modificación: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())