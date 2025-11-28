import sys
import os

# --- 1. CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Ajuste para subir niveles correctamente
if 'Veterinaro' in current_dir:
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
else:
    project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# Importamos la clase de funciones
try:
    from funciones_vete import FuncinesVete
except ImportError:
    pass 

from db_connection import Conexion

class VentanaRevisarReceta(QMainWindow):
    def __init__(self, nombre_usuario):
        super().__init__()
        
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Sistema Veterinario Yuno - Historial de Recetas")
        self.resize(1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS VISUALES ---
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
            
            /* Inputs Solo Lectura */
            QLineEdit[readOnly="true"], QTextEdit[readOnly="true"] {
                background-color: #F0F0F0; border: 1px solid #DDD; border-radius: 10px;
                padding: 5px 15px; font-size: 16px; color: #555;
            }
            /* Inputs de Busqueda */
            QLineEdit {
                background-color: white; border: 2px solid #ddd; border-radius: 10px;
                padding: 8px; font-size: 16px;
            }

            /* BOTONES MENU PRINCIPAL */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px;
                color: white; font-family: 'Segoe UI', sans-serif; font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF;
            }

            /* SUB-BOTONES */
            QPushButton.sub-btn {
                text-align: left; padding-left: 40px; border-radius: 10px;
                color: #F0F0F0; font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: normal;
                background-color: rgba(0, 0, 0, 0.05); height: 35px; margin-bottom: 2px;
                margin-left: 10px; margin-right: 10px; border: none;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
            
            /* Botón Logout */
            QPushButton.logout-btn {
                text-align: center; border: 2px solid white; 
                border-radius: 15px; padding: 10px; margin-top: 20px;
                font-size: 14px; color: white; font-weight: bold;
                background-color: transparent;
            }
            QPushButton.logout-btn:hover { background-color: rgba(255, 255, 255, 0.2); }
            
            /* Labels de datos */
            QLabel.label-key { font-size: 18px; color: #666; font-weight: normal; }
            QLabel.label-value { font-size: 22px; color: #000; font-weight: bold; padding-bottom: 5px; border-bottom: 1px solid #EEE; }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ============================================================
    #  SIDEBAR
    # ============================================================
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
        # Sube a Modulos -> FILES -> logo_yuno.png
        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)

        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")

        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)
        
        # --- MENÚS DESPLEGABLES COMPLETOS ---
        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro", "Agregar medicina a receta"])
        self.setup_accordion_group("Extra", ["Visualizar mascotas", "Visualizar medicamento", "Agregar notas para internar"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setProperty("class", "logout-btn")
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
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.router_ventanas(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def router_ventanas(self, categoria, opcion):
        print(f"Navegando: {categoria} -> {opcion}")
        try:
            # CONSULTAS
            if categoria == "Consultas":
                if opcion == "Crear Consulta":
                    from UI_Realizar_consulta import VentanaConsulta
                    self.ventana = VentanaConsulta(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Ver Registro":
                    from UI_Revisar_consulta import VentanaRevisarConsulta
                    self.ventana = VentanaRevisarConsulta(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

            # --- RECETAS ---
            elif categoria == "Recetas":
                if opcion == "Crear Receta":
                    from UI_Registrar_receta import VentanaReceta 
                    self.ventana = VentanaReceta(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Ver Registro":
                    from UI_Revisar_recetas import VentanaRevisarReceta
                    self.ventana = VentanaRevisarReceta(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Agregar medicina a receta":
                    from UI_Agregar_MReceta import VentanaAgregarMedicamento
                    self.ventana=VentanaAgregarMedicamento(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

            # --- EXTRA (NUEVO) ---
            elif categoria == "Extra":
                if opcion == "Visualizar mascotas":
                    from UI_RevisarMascota_Vete import VentanaRevisarMascota
                    self.ventana = VentanaRevisarMascota(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                
                elif opcion == "Visualizar medicamento":
                    from UI_RevisarMedicamento import VentanaRevisarMedicamento
                    self.ventana = VentanaRevisarMedicamento(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                
                elif opcion == "Agregar notas para internar":
                    # AQUI CONECTAS TU CLASE
                    QMessageBox.information(self, "Construcción", "Aquí iría Notas de Internación.")

        except ImportError as e:
            QMessageBox.warning(self, "Error", f"Falta archivo: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")

    # ============================================================
    #  PANEL CENTRAL (VISUALIZAR RECETA)
    # ============================================================
    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Historial de Recetas")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("✕")
        btn_back.setFixedSize(40, 40)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; border-radius: 20px; font-size: 20px; color: #666; border: none; }
            QPushButton:hover { background-color: #ffcccc; color: #cc0000; }
        """)
        btn_back.clicked.connect(self.volver_al_menu)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_back)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(30)

        # --- BARRA DE BÚSQUEDA ---
        self.setup_search_bar()
        self.white_layout.addSpacing(30)

        # --- CONTENEDOR DE DATOS ---
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        # IZQUIERDA: Datos Básicos (Solo ID Consulta ahora)
        self.setup_details_form(content_layout)

        # DERECHA: Indicaciones
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addStretch(2)

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_search = QLabel("ID Receta:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Ingrese ID...")
        self.inp_search.setFixedWidth(300)
        
        btn_search = QPushButton("Buscar")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setFixedSize(120, 40)
        btn_search.setStyleSheet("background-color: #7CEBFC; color: #333; font-weight: bold; border-radius: 10px; border: 1px solid #5CD0E3;")
        btn_search.clicked.connect(self.buscar_receta)
        
        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.inp_search)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_container)

    def setup_details_form(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(30)

        lbl_style = "font-size: 18px; font-weight: 500;"

        # --- SOLO MOSTRAMOS ID CONSULTA (Sin Fecha) ---
        self.lbl_consulta = self.crear_fila_datos("ID Consulta Asociada:", "---", grid, 0)

        # Empujar hacia arriba
        grid.setRowStretch(1, 1)
        parent_layout.addWidget(form_widget, stretch=2)

    def crear_fila_datos(self, titulo, valor_inicial, grid, row):
        lbl_tit = QLabel(titulo)
        lbl_tit.setProperty("class", "label-key")
        
        inp = QLineEdit()
        inp.setReadOnly(True)
        inp.setText(valor_inicial)
        
        grid.addWidget(lbl_tit, row, 0)
        grid.addWidget(inp, row, 1)
        
        return inp

    def setup_info_board(self, parent_layout):
        board_container = QFrame()
        board_container.setFixedWidth(400)
        board_container.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 10px;")
        
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FC7CE2, stop:1 #7CEBFC); border-top-left-radius: 10px; border-top-right-radius: 10px;")
        hl = QVBoxLayout(header)
        lbl = QLabel("Indicaciones / Medicamentos")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none; background: transparent;")
        hl.addWidget(lbl)

        self.txt_indicaciones_view = QTextEdit()
        self.txt_indicaciones_view.setReadOnly(True)
        self.txt_indicaciones_view.setStyleSheet("border: none; padding: 15px; font-size: 16px; color: #555;")
        self.txt_indicaciones_view.setText("Ingrese un ID para ver los detalles...")

        board_layout.addWidget(header)
        board_layout.addWidget(self.txt_indicaciones_view)

        parent_layout.addWidget(board_container, stretch=1)

    # ============================================================
    #  LÓGICA DB
    # ============================================================
    def volver_al_menu(self):
        try:
            from UI_Veterinario import VeterinarioMenu 
            self.menu = VeterinarioMenu(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            self.close()

    def buscar_receta(self):
        id_receta = self.inp_search.text().strip()

        if not id_receta.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número.")
            return

        try:
            # USANDO FuncinesVete (Como pediste para los otros módulos)
            from funciones_vete import FuncinesVete
            funcion = FuncinesVete()

            # Columnas: fk_consulta, indicaciones
            columnas = ('fk_consulta', 'indicaciones')
            
            resultado = funcion.buscarId_unico(columnas, id_receta, table='receta')

            if resultado:
                # 0: fk_consulta, 1: indicaciones
                consulta_val = resultado[0]
                self.lbl_consulta.setText(str(consulta_val) if consulta_val else "Sin vínculo")
                self.txt_indicaciones_view.setText(str(resultado[1]))
                
                QMessageBox.information(self, "Encontrado", "Receta cargada correctamente.")
            else:
                self.limpiar_datos()
                QMessageBox.warning(self, "No Encontrado", "No existe una receta con ese ID.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar:\n{e}")

    def limpiar_datos(self):
        self.lbl_consulta.setText("---")
        self.txt_indicaciones_view.setText("---")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = VentanaRevisarReceta()
    window.show()
    sys.exit(app.exec())