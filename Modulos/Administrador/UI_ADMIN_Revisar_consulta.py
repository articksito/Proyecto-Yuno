import sys
import os

# --- CONFIGURACIÓN DE RUTAS ---
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
from PyQt6.QtGui import QFont, QPixmap

from db_connection import Conexion

class VentanaRevisarConsulta(QMainWindow):
    def __init__(self, nombre_usuario="Admin"):
        super().__init__()

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Sistema Veterinario Yuno - Historial de Consultas (Admin)")
        self.resize(1280, 720)

        # Conexión DB
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error al conectar BD: {e}")

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal (Horizontal)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES (Igual que Paciente) ---
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
            /* Botones Menú */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px; color: white; font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover { background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; }
            
            /* Sub-botones */
            QPushButton.sub-btn {
                text-align: left; font-size: 16px; padding-left: 40px; border-radius: 10px;
                color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05); height: 35px;
                margin-bottom: 2px; margin-left: 10px; margin-right: 10px;
            }
            QPushButton.sub-btn:hover { color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; }
            
            /* Tabla */
            QTableWidget {
                background-color: white; border: 1px solid #E0E0E0; border-radius: 15px;
                gridline-color: transparent; font-size: 14px;
                selection-background-color: #E1BEE7; selection-color: #333;
                alternate-background-color: #FAFAFA; outline: 0;
            }
            QHeaderView::section {
                background-color: #7CEBFC; color: #444; font-weight: bold; border: none;
                padding: 12px; font-size: 15px; font-family: 'Segoe UI';
            }
            QHeaderView::section:first { border-top-left-radius: 15px; }
            QHeaderView::section:last { border-top-right-radius: 15px; }
            
            QScrollBar:vertical {
                border: none; background: #F5F5F5; width: 10px; border-radius: 5px;
            }
            QScrollBar::handle:vertical { background: #CCC; min-height: 20px; border-radius: 5px; }
            QScrollBar::handle:vertical:hover { background: #BBB; }
            
            /* Logout */
            QPushButton.logout-btn {
                text-align: center; border: 2px solid white; border-radius: 15px;
                padding: 10px; margin-top: 20px; font-size: 14px; color: white;
                font-weight: bold; background-color: transparent;
            }
            QPushButton.logout-btn:hover { background-color: rgba(255, 255, 255, 0.2); }
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
        lbl_header = QLabel("Historial de Consultas")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        # Botón Volver
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-size: 16px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #E0E0E0; color: #333; }
        """)
        btn_back.clicked.connect(self.volver_al_menu)

        # Botón Refrescar
        btn_refresh = QPushButton("↻ Actualizar")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFixedSize(120, 40)
        btn_refresh.setStyleSheet("""
            QPushButton { 
                background-color: #7CEBFC; color: #444; border-radius: 10px; 
                font-weight: bold; border: 1px solid #5CD0E3; 
            }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_refresh.clicked.connect(self.cargar_datos_tabla)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_refresh)
        header_layout.addSpacing(10)
        header_layout.addWidget(btn_back)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # Tabla de Consultas
        self.setup_table()

        # Cargar datos iniciales
        self.cargar_datos_tabla()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- SIDEBAR Y NAVEGACIÓN ---
    # ==========================================
    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # Logo
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
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

        # Menú
        self.setup_accordion_group("Cita", ["Visualizar"])
        self.setup_accordion_group("Consulta", ["Visualizar"])
        self.setup_accordion_group("Mascota", ["Visualizar", "Modificar"])
        self.setup_accordion_group("Cliente", ["Visualizar"])
        self.setup_accordion_group("Hospitalizacion", ["Visualizar"])
        self.setup_accordion_group("Medicamentos", ["Visualizar", "Agregar"])
        self.setup_accordion_group("Usuarios", ["Agregar", "Modificar", "Visualizar"])
        self.setup_accordion_group("Especialidad", ["Agregar", "Modificar"])

        self.sidebar_layout.addStretch()
        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setProperty("class", "logout-btn")
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

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def navegar(self, categoria, opcion):
        if categoria == "Consulta" and opcion == "Visualizar":
             return 
        try:
            # Lógica de navegación estándar
            if categoria == "Cita" and opcion == "Visualizar":
                from UI_ADMIN_Revisar_cita import MainWindow as UI_Revisar_Cita
                self.ventana = UI_Revisar_Cita(self.nombre_usuario)
            elif categoria == "Mascota" and opcion == "Visualizar":
                from UI_ADMIN_Revisar_Paciente import MainWindow as UI_Mascota
                self.ventana = UI_Mascota(self.nombre_usuario)
            elif categoria == "Mascota" and opcion == "Modificar":
                from UI_Admin_Modificar_Mascota import MainWindow as UI_Modificar_Mascota
                self.ventana = UI_Modificar_Mascota(self.nombre_usuario)
            elif categoria == "Cliente" and opcion == "Visualizar":
                from UI_ADMIN_Visualizar_cliente import MainWindow as UI_Modificar_cliente
                self.ventana = UI_Modificar_cliente(self.nombre_usuario)
            elif categoria == "Hospitalizacion" and opcion == "Visualizar":
                from UI_ADMIN_RevisarHospitalizacion import VentanaRevisarHospitalizacion
                self.ventana = VentanaRevisarHospitalizacion(self.nombre_usuario)
            elif categoria == "Medicamentos":
                if opcion == "Visualizar":
                    from UI_ADMIN_Revisar_medicina import VentanaRevisarMedicina
                    self.ventana = VentanaRevisarMedicina(self.nombre_usuario)
                elif opcion == "Agregar":
                    from UI_ADMIN_Agregar_medicina import MainWindow as AddMed
                    self.ventana = AddMed(self.nombre_usuario)
            elif categoria == "Usuarios":
                if opcion == "Agregar":
                    from UI_ADMIN_Agregar_usuario import VentanaAgregarUsuario
                    self.ventana = VentanaAgregarUsuario(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_ADMIN_Modificar_usuario import VentanaModificarUsuario
                    self.ventana = VentanaModificarUsuario(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_ADMIN_Revisar_usuario import VentanaRevisarUsuario
                    self.ventana = VentanaRevisarUsuario(self.nombre_usuario)
            elif categoria == "Especialidad":
                if opcion == "Agregar":
                    from UI_ADMIN_Agregar_Especialidad import VentanaAgregarEspecialidad
                    self.ventana = VentanaAgregarEspecialidad(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_ADMIN_Modificar_especialidad import VentanaModificarEspecialidad
                    self.ventana = VentanaModificarEspecialidad(self.nombre_usuario)

            if hasattr(self, 'ventana') and self.ventana:
                self.ventana.show()
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al navegar: {e}")

    # ==========================================
    # --- TABLA Y DATOS ---
    # ==========================================

    def setup_table(self):
        # Columnas específicas para CONSULTA
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Fecha", "Hora", "Mascota", "Veterinario", "Motivo"])
        
        # Configuración visual
        self.table.setShowGrid(False) 
        self.table.setAlternatingRowColors(True) 
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus) 
        
        # Ajuste de cabeceras
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed) # ID
        self.table.setColumnWidth(0, 60)
        
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed) # Fecha
        self.table.setColumnWidth(1, 120)

        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed) # Hora
        self.table.setColumnWidth(2, 100)
        
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # Mascota
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Veterinario
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch) # Motivo
        
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(50)

        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.white_layout.addWidget(self.table)

    def cargar_datos_tabla(self):
        """Obtiene datos de la BD y rellena la tabla"""
        self.table.setRowCount(0)
        
        try:
            # Query con JOINS para obtener nombres legibles
            # Se asume que Veterinario tiene fk_usuario para obtener su nombre real
            query = """
                SELECT 
                    c.id_consulta, 
                    c.fecha, 
                    c.hora, 
                    m.nombre AS nombre_mascota, 
                    u.nombre AS nombre_veterinario,
                    c.motivo
                FROM consulta c
                JOIN mascota m ON c.fk_mascota = m.id_mascota
                JOIN veterinario v ON c.fk_veterinario = v.id_veterinario
                JOIN usuario u ON v.fk_usuario = u.id_usuario
                ORDER BY c.fecha DESC, c.hora DESC
            """
            
            self.conexion.cursor_uno.execute(query)
            datos = self.conexion.cursor_uno.fetchall()

            for row_idx, row_data in enumerate(datos):
                self.table.insertRow(row_idx)
                
                # row_data = (id, fecha, hora, mascota, veterinario, motivo)
                
                # ID
                item_id = QTableWidgetItem(str(row_data[0]))
                item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 0, item_id)
                
                # Fecha
                item_fecha = QTableWidgetItem(str(row_data[1]))
                item_fecha.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 1, item_fecha)
                
                # Hora
                item_hora = QTableWidgetItem(str(row_data[2]))
                item_hora.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 2, item_hora)
                
                # Mascota
                item_mascota = QTableWidgetItem(str(row_data[3]))
                item_mascota.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 3, item_mascota)
                
                # Veterinario
                item_vet = QTableWidgetItem(f"Dr. {row_data[4]}")
                item_vet.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 4, item_vet)

                # Motivo (Con tooltip para texto largo)
                motivo_texto = str(row_data[5])
                item_motivo = QTableWidgetItem(motivo_texto)
                item_motivo.setToolTip(motivo_texto) 
                self.table.setItem(row_idx, 5, item_motivo)

        except Exception as e:
            print(f"Error cargando tabla de consultas: {e}")
            # Fallback simple si falla el JOIN complejo
            print("Intentando carga simple...")
            try:
                query_simple = "SELECT id_consulta, fecha, hora, fk_mascota, fk_veterinario, motivo FROM consulta"
                self.conexion.cursor_uno.execute(query_simple)
                datos = self.conexion.cursor_uno.fetchall()
                for row_idx, row_data in enumerate(datos):
                    self.table.insertRow(row_idx)
                    for col_idx, val in enumerate(row_data):
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))
            except:
                pass

    def volver_al_menu(self):
        try:
            from UI_ADMIN_main import MainWindow as AdminMenu 
            self.menu = AdminMenu(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = VentanaRevisarConsulta()
    window.show()
    sys.exit(app.exec())