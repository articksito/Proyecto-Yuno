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
                             QTableWidgetItem, QHeaderView, QMessageBox, QAbstractItemView,
                             QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# IMPORTAMOS LA NUEVA CONEXIÓN
from db_conexionNew import Conexion

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Enfermero"):
        super().__init__()
        
        self.nombre_usuario = nombre_usuario
        self.setWindowTitle(f"Sistema Veterinario Yuno - Revisar Citas ({self.nombre_usuario})")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)
        
        # Conexión DB
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")

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
                font-family: 'Segoe UI', sans-serif;
                color: #333;
            }
            
            /* --- ESTILOS DEL SIDEBAR --- */
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
            
            /* Botón Logout */
            QPushButton.logout-btn {
                text-align: center; border: 2px solid white; 
                border-radius: 15px; padding: 10px; margin-top: 20px;
                font-size: 14px; color: white; font-weight: bold;
                background-color: transparent;
            }
            QPushButton.logout-btn:hover { background-color: rgba(255, 255, 255, 0.2); }

            /* --- ESTILO TABLA --- */
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
        """)

        # --- 1. BARRA LATERAL ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO ---
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- SIDEBAR (ENFERMERA) ---
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
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_logo = os.path.join(current_dir, "..", "FILES", "logo_yuno.png")
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                lbl_logo.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        else:
            lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")

        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)
        
        # MENÚ ESPECÍFICO
        self.setup_accordion_group("Citas", ["Visualizar"])
        self.setup_accordion_group("Mascotas", ["Visualizar"])
        self.setup_accordion_group("Inventario", ["Farmacia", "Hospitalización"])
        self.setup_accordion_group("Expediente", ["Diagnóstico"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Volver al Menú")
        btn_logout.setProperty("class", "logout-btn")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.regresar_menu)
        self.sidebar_layout.addWidget(btn_logout)

    def setup_accordion_group(self, title, options):
        btn_main = QPushButton(title)
        btn_main.setProperty("class", "menu-btn")
        btn_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebar_layout.addWidget(btn_main)

        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(2)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.abrir_ventana(t, o))
            layout.addWidget(btn_sub)

        frame.hide()
        self.sidebar_layout.addWidget(frame)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def abrir_ventana(self, categoria, opcion):
        if categoria == "Citas" and opcion == "Visualizar": return
        try:
            target = None
            if categoria == "Mascotas": 
                from UI_Revisar_Mascota_Enfermera import MainWindow as Win
                target = Win(self.nombre_usuario)
            elif categoria == "Inventario" and opcion == "Farmacia": 
                from UI_Farmacia import MainWindow as Win
                target = Win(self.nombre_usuario)
            elif categoria == "Inventario" and opcion == "Hospitalización": 
                from UI_Hospitalizacion import MainWindow as Win
                target = Win(self.nombre_usuario)
            elif categoria == "Expediente": 
                from UI_Diagnostico import MainWindow as Win
                target = Win(self.nombre_usuario)

            if target: 
                self.ventana = target
                self.ventana.show()
                self.close()
        except Exception as e: 
            QMessageBox.warning(self, "Error", str(e))

    # ==========================================
    # --- PANEL CENTRAL (TABLA) ---
    # ==========================================

    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Listado de Citas")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        # Barra de Búsqueda
        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("🔍 Buscar por mascota...")
        self.txt_buscar.setFixedSize(250, 40)
        self.txt_buscar.setStyleSheet("""
            QLineEdit { 
                border: 2px solid #ddd; border-radius: 10px; padding: 5px 10px; font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #7CEBFC; }
        """)
        self.txt_buscar.returnPressed.connect(self.buscar_cita)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.setFixedSize(80, 40)
        btn_buscar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_buscar.setStyleSheet("""
            QPushButton { background-color: #E1BEE7; color: #4A148C; border-radius: 10px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #D1C4E9; }
        """)
        btn_buscar.clicked.connect(self.buscar_cita)
        
        # Botón Volver
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-size: 16px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #E0E0E0; color: #333; }
        """)
        btn_back.clicked.connect(self.regresar_menu)

        # Botón Actualizar
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
        btn_refresh.clicked.connect(lambda: [self.txt_buscar.clear(), self.cargar_datos_tabla()])

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(self.txt_buscar)
        header_layout.addWidget(btn_buscar)
        header_layout.addSpacing(10)
        header_layout.addWidget(btn_refresh)
        header_layout.addSpacing(10)
        header_layout.addWidget(btn_back)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # Tabla
        self.setup_table()

        # Cargar datos
        self.cargar_datos_tabla()

        self.white_layout.addStretch()

    def setup_table(self):
        # Columns: ID, Fecha, Hora, Mascota, Cliente, Veterinario, Estado, Motivo
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Fecha", "Hora", "Mascota", "Dueño", "Veterinario", "Estado", "Motivo"])
        
        # Configuración visual
        self.table.setShowGrid(False) 
        self.table.setAlternatingRowColors(True) 
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus) 
        
        # Ajuste de cabeceras
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed) # ID
        self.table.setColumnWidth(0, 50)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # Fecha
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) # Hora
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # Mascota
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Dueño
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # Vet
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed) # Estado
        self.table.setColumnWidth(6, 100)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch) # Motivo
        
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(50)

        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.white_layout.addWidget(self.table)

    def buscar_cita(self):
        texto = self.txt_buscar.text().strip()
        self.cargar_datos_tabla(filtro=texto)

    def cargar_datos_tabla(self, filtro=""):
        """Obtiene datos de la BD y rellena la tabla"""
        self.table.setRowCount(0)
        
        try:
            columnas = (
                'cita.id_cita', 
                'cita.fecha', 
                'cita.hora', 
                'mascota.nombre', 
                'cliente.nombre', 'cliente.apellido', # Dueño
                'usuario.nombre', 
                'cita.estado', 
                'cita.motivo'
            )
            
            orden_por = ('cita.fecha', 'cita.hora')
            
            # CADENA DE JOINS:
            # 1. Cita -> Mascota
            # 2. Mascota -> Cliente
            # 3. Cita -> Veterinario
            # 4. Veterinario -> Usuario
            mis_joins = [
                ('mascota', 'cita'),
                ('cliente', 'mascota'),
                ('veterinario', 'cita'),
                ('usuario', 'veterinario')
            ]

            if filtro:
                datos = self.conexion.consultar_tabla(
                    columnas=columnas,
                    tabla='cita',
                    joins=mis_joins,
                    filtro=filtro,
                    campo_filtro='mascota.nombre',
                    orden=orden_por
                )
            else:
                datos = self.conexion.consultar_tabla(
                    columnas=columnas,
                    tabla='cita',
                    joins=mis_joins,
                    orden=orden_por
                )

            for row_idx, row_data in enumerate(datos):
                self.table.insertRow(row_idx)
                
                # row_data = (id, fecha, hora, mascota, n_cli, a_cli, n_vet, estado, motivo)
                
                # ID
                item = QTableWidgetItem(str(row_data[0]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 0, item)
                
                # Fecha
                item = QTableWidgetItem(str(row_data[1]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 1, item)

                # Hora
                item = QTableWidgetItem(str(row_data[2]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 2, item)

                # Mascota
                item = QTableWidgetItem(str(row_data[3]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 3, item)

                # Dueño (Concatenado)
                dueño = f"{row_data[4]} {row_data[5]}"
                item = QTableWidgetItem(dueño)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 4, item)

                # Veterinario (Dr. Nombre)
                vet = f"Dr. {row_data[6]}"
                item = QTableWidgetItem(vet)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 5, item)

                # Estado
                estado = str(row_data[7])
                item_est = QTableWidgetItem(estado)
                item_est.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if "confirmada" in estado.lower(): item_est.setForeground(Qt.GlobalColor.darkBlue)
                elif "cancelada" in estado.lower(): item_est.setForeground(Qt.GlobalColor.red)
                elif "completada" in estado.lower(): item_est.setForeground(Qt.GlobalColor.darkGreen)
                self.table.setItem(row_idx, 6, item_est)

                # Motivo (Tooltip)
                motivo = str(row_data[8])
                item_mot = QTableWidgetItem(motivo)
                item_mot.setToolTip(motivo)
                self.table.setItem(row_idx, 7, item_mot)

        except Exception as e:
            print(f"Error cargando tabla de citas: {e}")

    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import EnfermeroMain
            self.menu = EnfermeroMain(self.nombre_usuario) 
            self.menu.show(); self.close()
        except ImportError: QMessageBox.warning(self, "Error", "No se encuentra el menú.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("TEST USER")
    window.show()
    sys.exit(app.exec())