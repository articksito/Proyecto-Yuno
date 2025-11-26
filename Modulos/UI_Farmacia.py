import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QTreeWidget, QTreeWidgetItem, QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# Intentar importar conexión
try:
    from db_connection import Conexion
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Veterinario Yuno - Farmacia")
        self.resize(1280, 720)

        # Inicializar conexión
        if DB_AVAILABLE:
            self.conexion1 = Conexion()

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
            QWidget#WhitePanel {
                background-color: white;
                border-top-left-radius: 30px; border-bottom-left-radius: 30px;
                margin: 20px 20px 20px 0px; 
            }
            QWidget#Sidebar { background-color: transparent; }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            
            /* Inputs del Formulario */
            QLineEdit {
                background-color: rgba(241, 131, 227, 0.15); 
                border: 1px solid #DDD; border-radius: 10px; 
                padding: 5px 15px; font-size: 14px; color: #333; height: 35px;
            }
            QLineEdit:focus { border: 1px solid #b67cfc; background-color: white; }

            /* Tabla */
            QTreeWidget { border: 1px solid #DDD; border-radius: 10px; font-family: 'Segoe UI'; font-size: 14px; }
            QHeaderView::section { background-color: #b67cfc; color: white; padding: 5px; border: none; font-weight: bold; }
            
            /* Botones del Sidebar */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px; color: white; font-family: 'Segoe UI', sans-serif;
                font-weight: bold; font-size: 18px; background-color: rgba(255, 255, 255, 0.1);
                height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF;
            }
            QPushButton.sub-btn {
                text-align: left; font-family: 'Segoe UI', sans-serif; font-size: 16px;
                font-weight: normal; padding-left: 40px; border-radius: 10px;
                color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05);
                height: 35px; margin-bottom: 2px; margin-left: 10px; margin-right: 10px;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
        """)

        # --- Sidebar ---
        self.setup_sidebar()

        # --- PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(40, 30, 40, 30)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Gestión de Farmacia")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0; color: #555; border-radius: 20px; 
                padding: 10px 20px; font-weight: bold; border: none; font-size: 14px;
            }
            QPushButton:hover { background-color: #E0E0E0; color: #333; }
        """)
        # CONEXIÓN AL MENU ENFERMERA
        btn_back.clicked.connect(self.regresar_menu)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_back)
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(10)

        # --- CONTENIDO DIVIDIDO ---
        content_layout = QHBoxLayout()
        
        # Lado Izquierdo: Formulario
        form_container = QFrame()
        form_layout = QVBoxLayout(form_container)
        self.setup_form(form_layout)
        
        # Lado Derecho: Tabla + Búsqueda
        table_container = QFrame()
        table_layout = QVBoxLayout(table_container)
        
        # Agregamos la barra de búsqueda antes de la tabla
        self.setup_search_bar(table_layout) 
        self.setup_table(table_layout)

        content_layout.addWidget(form_container, stretch=1)
        content_layout.addSpacing(30)
        content_layout.addWidget(table_container, stretch=2)

        self.white_layout.addLayout(content_layout)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)
        
        # Cargar datos al iniciar
        self.cargar_tabla()

    # --- BARRA LATERAL (Estandarizada) ---
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
        
        # 1. Obtener la ruta donde está guardado ESTE archivo .py
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        
        # 2. Construir la ruta exacta a la carpeta FILES -> logo_yuno.png
        ruta_logo = os.path.join(directorio_actual, "FILES", "logo_yuno.png")

        # 3. Cargar imagen
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        else:
            print(f"No se encontró el logo en: {ruta_logo}")
            lbl_logo.setText("YUNO VET")
            
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # Menús
        self.setup_accordion_group("Citas", ["Visualizar"])
        self.setup_accordion_group("Mascotas", ["Visualizar"])
        self.setup_accordion_group("Inventario", ["Farmacia", "Hospitalización"])
        self.setup_accordion_group("Expediente", ["Diagnóstico"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Volver al Menú")
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
        layout_options.setSpacing(2)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # --- CONEXIÓN DE NAVEGACIÓN DIRECTA ---
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.abrir_ventana(t, o))
            
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    # --- BARRA DE BÚSQUEDA ---
    def setup_search_bar(self, layout):
        search_frame = QFrame()
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(0, 0, 0, 10)

        self.inp_search_id = QLineEdit()
        self.inp_search_id.setPlaceholderText("Buscar por ID de Medicamento...")
        self.inp_search_id.setStyleSheet("""
            QLineEdit { background-color: #F9F9F9; border: 2px solid #EEE; }
            QLineEdit:focus { border: 2px solid #b67cfc; }
        """)

        btn_search = QPushButton("Buscar")
        btn_search.setFixedSize(100, 35)
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("""
            QPushButton { background-color: #b67cfc; color: white; border-radius: 10px; font-weight: bold; }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_search.clicked.connect(self.buscar_medicamento_id)

        search_layout.addWidget(self.inp_search_id)
        search_layout.addWidget(btn_search)
        
        layout.addWidget(search_frame)

    # --- FORMULARIO Y TABLA ---
    def setup_form(self, layout):
        lbl_titulo = QLabel("Registrar Medicamento")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px; color: #5f2c82;")
        layout.addWidget(lbl_titulo)

        # Campos
        self.inp_nombre = QLineEdit(); self.inp_nombre.setPlaceholderText("Nombre Medicina")
        self.inp_tipo = QLineEdit(); self.inp_tipo.setPlaceholderText("Tipo (ej. Antibiótico)")
        self.inp_comp = QLineEdit(); self.inp_comp.setPlaceholderText("Composición (mg)")
        self.inp_dosis = QLineEdit(); self.inp_dosis.setPlaceholderText("Dosis Recomendada")
        self.inp_via = QLineEdit(); self.inp_via.setPlaceholderText("Vía Admin. (ej. Oral)")

        layout.addWidget(QLabel("Nombre:")); layout.addWidget(self.inp_nombre)
        layout.addWidget(QLabel("Tipo:")); layout.addWidget(self.inp_tipo)
        layout.addWidget(QLabel("Composición:")); layout.addWidget(self.inp_comp)
        layout.addWidget(QLabel("Dosis:")); layout.addWidget(self.inp_dosis)
        layout.addWidget(QLabel("Vía Admin:")); layout.addWidget(self.inp_via)
        
        layout.addStretch()
        
        btn_add = QPushButton("Agregar al Inventario")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFixedHeight(50)
        btn_add.setStyleSheet("""
            QPushButton { background-color: #b67cfc; color: white; font-size: 16px; font-weight: bold; border-radius: 10px; }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_add.clicked.connect(self.agregar_medicamento)
        layout.addWidget(btn_add)

    def setup_table(self, layout):
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["ID", "Nombre", "Tipo", "Comp.", "Dosis", "Vía"])
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tree)
        
        btn_refresh = QPushButton("🔄 Mostrar Todos")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setStyleSheet("background: transparent; color: #555; font-weight: bold; text-align: right; margin-top: 5px;")
        btn_refresh.clicked.connect(self.cargar_tabla)
        layout.addWidget(btn_refresh)

    # --- LÓGICA DE BASE DE DATOS ---
    def agregar_medicamento(self):
        nombre = self.inp_nombre.text()
        tipo = self.inp_tipo.text()
        comp = self.inp_comp.text()
        dosis = self.inp_dosis.text()
        via = self.inp_via.text()

        if not nombre or not tipo:
            QMessageBox.warning(self, "Error", "El nombre y tipo son obligatorios.")
            return

        try:
            datos = (nombre, tipo, comp, dosis, via)
            # Usamos comillas dobles para la columna especial "composicion(mg)" si es necesario en tu BD
            columnas = ('nombre', 'tipo', '"composicion(mg)"', 'dosis_recomendada', 'via_administracion')
            self.conexion1.insertar_datos('medicamento', datos, columnas)
            QMessageBox.information(self, "Éxito", "Medicamento agregado correctamente.")
            self.limpiar_form()
            self.cargar_tabla()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {e}")

    def cargar_tabla(self):
        if not DB_AVAILABLE: return
        self.tree.clear()
        try:
            filas = self.conexion1.Select_users(table='medicamento')
            for fila in filas:
                item = QTreeWidgetItem([str(x) for x in fila])
                self.tree.addTopLevelItem(item)
        except Exception as e:
            print(f"Error cargando tabla: {e}")

    def buscar_medicamento_id(self):
        id_med = self.inp_search_id.text().strip()
        
        if not id_med:
            QMessageBox.warning(self, "Aviso", "Por favor ingresa un ID.")
            return
        
        if not DB_AVAILABLE: 
            return

        print(f"--- BUSCANDO MANUALMENTE EL ID: {id_med} ---")

        try:
            self.tree.clear()
            encontrado = False
            
            todos_los_meds = self.conexion1.Select_users(table='medicamento')
            
            for fila in todos_los_meds:
                id_actual_bd = str(fila[0])
                if id_actual_bd == id_med:
                    item = QTreeWidgetItem([str(x) for x in fila])
                    self.tree.addTopLevelItem(item)
                    encontrado = True
                    break 
            
            if encontrado:
                QMessageBox.information(self, "Éxito", f"Medicamento {id_med} encontrado.")
            else:
                QMessageBox.warning(self, "Sin resultados", f"El ID {id_med} no existe.")
                self.cargar_tabla()
                
        except Exception as e:
             print(f"ERROR: {e}")
             QMessageBox.critical(self, "Error", f"Ocurrió un error al buscar: {e}")

    def limpiar_form(self):
        self.inp_nombre.clear()
        self.inp_tipo.clear()
        self.inp_comp.clear()
        self.inp_dosis.clear()
        self.inp_via.clear()

    # --- NAVEGACIÓN ---
    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import MainWindow as MenuEnfermera
            self.menu = MenuEnfermera()
            self.menu.show()
            self.close()
        except ImportError:
            QMessageBox.warning(self, "Error", "No se encuentra el menú de enfermera.")

    # --- FUNCION DE NAVEGACIÓN DIRECTA (ROUTER) ---
    def abrir_ventana(self, categoria, opcion):
        try:
            target_window = None

            # 1. ENRUTAMIENTO
            if categoria == "Citas" and opcion == "Visualizar":
                from UI_Cita_Enfermera import MainWindow as Win
                target_window = Win()
            
            elif categoria == "Mascotas" and opcion == "Visualizar":
                from UI_Revisar_Mascota_Enfermera import MainWindow as Win
                target_window = Win()
            
            elif categoria == "Inventario":
                if opcion == "Farmacia":
                    pass # Ya estamos aquí
                elif opcion == "Hospitalización":
                    from UI_Hospitalizacion import MainWindow as Win
                    target_window = Win()
            
            elif categoria == "Expediente" and opcion == "Diagnóstico":
                from UI_Diagnostico import MainWindow as Win
                target_window = Win()

            # 2. EJECUCIÓN
            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close() 
            
        except ImportError as e:
            QMessageBox.warning(self, "Error", f"No se encuentra el archivo de destino.\n{e}")
        except Exception as e:
            print(f"Error navegando: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())