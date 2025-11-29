import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QTreeWidget, QTreeWidgetItem, QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# --- AJUSTE DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) 
if current_dir not in sys.path: sys.path.append(current_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)

# Intentar importar conexión
try:
    from db_connection import Conexion
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    class Conexion:
        def Select_users(self, table): return []
        def insertar_datos(self, *args): pass

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Enfermero"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.setWindowTitle(f"Sistema Veterinario Yuno - Farmacia ({self.nombre_usuario})")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)

        if DB_AVAILABLE:
            self.conexion1 = Conexion()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS ---
        self.setStyleSheet("""
            QMainWindow { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); 
            }
            QWidget#Sidebar { 
                background-color: transparent; 
            }
            
            /* 1. PANEL BLANCO (Contenedor general) */
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

            /* 2. LA TABLA ROSA (Lo que pediste) */
            QTreeWidget { 
                background-color: rgba(241, 131, 227, 0.35); /* Rosa translúcido */
                border: 1px solid #DDD; 
                border-radius: 10px; 
                font-family: 'Segoe UI'; 
                font-size: 14px; 
                color: #333; /* Letra Gris Oscuro */
                font-weight: 500;
            }
            /* Items dentro de la tabla */
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background-color: #b67cfc;
                color: white;
            }
            QHeaderView::section { 
                background-color: #b67cfc; 
                color: white; 
                padding: 5px; 
                border: none; 
                font-weight: bold; 
            }

            /* Inputs (Campos de texto) - Rosa muy suave */
            QLineEdit { 
                background-color: rgba(241, 131, 227, 0.15); 
                border: 1px solid #DDD; 
                border-radius: 10px; 
                padding: 5px 15px; 
                font-size: 16px; 
                color: #333; 
                height: 40px; 
            }
            QLineEdit:focus { 
                border: 2px solid #b67cfc; 
                background-color: white; 
            }

            /* Botones Menú Lateral */
            QPushButton.menu-btn { 
                text-align: left; padding-left: 20px; 
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; 
                color: white; font-weight: bold; font-size: 18px; 
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px; 
            }
            QPushButton.menu-btn:hover { 
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; 
            }
            QPushButton.sub-btn { 
                text-align: left; padding-left: 40px; 
                border-radius: 10px; color: #F0F0F0; font-size: 16px;
                background-color: rgba(0, 0, 0, 0.05); height: 35px; margin: 2px 10px; 
            }
            QPushButton.sub-btn:hover { 
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; 
            }
        """)

        self.setup_sidebar()

        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(40, 30, 40, 30)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Gestión de Farmacia")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # Contenido
        content_layout = QHBoxLayout()
        
        # Lado Izquierdo: Formulario
        form_container = QFrame()
        form_container.setStyleSheet("background: transparent;") 
        form_layout = QVBoxLayout(form_container)
        self.setup_form(form_layout)
        
        # Lado Derecho: Tabla + Búsqueda
        table_container = QFrame()
        table_container.setStyleSheet("background: transparent;")
        table_layout = QVBoxLayout(table_container)
        self.setup_search_bar(table_layout) 
        self.setup_table(table_layout)

        content_layout.addWidget(form_container, stretch=1)
        content_layout.addSpacing(30)
        content_layout.addWidget(table_container, stretch=2)

        self.white_layout.addLayout(content_layout)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)
        
        self.cargar_tabla()

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_logo = os.path.join(parent_dir, "FILES", "logo_yuno.png")
        
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

        self.setup_accordion_group("Citas", ["Visualizar"])
        self.setup_accordion_group("Mascotas", ["Visualizar"])
        self.setup_accordion_group("Inventario", ["Farmacia", "Hospitalización"])
        self.setup_accordion_group("Expediente", ["Diagnóstico"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Volver al Menú")
        btn_logout.setStyleSheet("QPushButton { text-align: center; border: 2px solid white; border-radius: 15px; padding: 10px; font-size: 14px; color: white; font-weight: bold; background-color: transparent; } QPushButton:hover { background-color: rgba(255,255,255,0.2); }")
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

    def setup_search_bar(self, layout):
        search_frame = QFrame()
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(0, 0, 0, 10)

        self.inp_search_id = QLineEdit()
        self.inp_search_id.setPlaceholderText("Buscar por ID...")
        
        btn_search = QPushButton("Buscar")
        btn_search.setFixedSize(100, 40)
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("QPushButton { background-color: #7CEBFC; color: #333; border-radius: 10px; font-weight: bold; border: 1px solid #5CD0E3; } QPushButton:hover { background-color: #5CD0E3; }")
        btn_search.clicked.connect(self.buscar_medicamento_id)

        search_layout.addWidget(self.inp_search_id)
        search_layout.addWidget(btn_search)
        layout.addWidget(search_frame)

    def setup_form(self, layout):
        lbl_titulo = QLabel("Registrar Medicamento")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px; color: #5f2c82;")
        layout.addWidget(lbl_titulo)

        self.inp_nombre = QLineEdit(); self.inp_nombre.setPlaceholderText("Nombre Medicina")
        self.inp_tipo = QLineEdit(); self.inp_tipo.setPlaceholderText("Tipo (ej. Antibiótico)")
        self.inp_comp = QLineEdit(); self.inp_comp.setPlaceholderText("Composición (mg)")
        self.inp_dosis = QLineEdit(); self.inp_dosis.setPlaceholderText("Dosis Recomendada")
        self.inp_via = QLineEdit(); self.inp_via.setPlaceholderText("Vía Admin. (ej. Oral)")

        style_lbl = "font-size: 16px; color: #333; margin-top: 10px; font-weight: bold;"
        
        layout.addWidget(QLabel("Nombre:", styleSheet=style_lbl)); layout.addWidget(self.inp_nombre)
        layout.addWidget(QLabel("Tipo:", styleSheet=style_lbl)); layout.addWidget(self.inp_tipo)
        layout.addWidget(QLabel("Composición:", styleSheet=style_lbl)); layout.addWidget(self.inp_comp)
        layout.addWidget(QLabel("Dosis:", styleSheet=style_lbl)); layout.addWidget(self.inp_dosis)
        layout.addWidget(QLabel("Vía Admin:", styleSheet=style_lbl)); layout.addWidget(self.inp_via)
        
        layout.addStretch()
        
        btn_add = QPushButton("Agregar al Inventario")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFixedHeight(50)
        btn_add.setStyleSheet("QPushButton { background-color: #b67cfc; color: white; font-size: 18px; font-weight: bold; border-radius: 25px; } QPushButton:hover { background-color: #a060e8; }")
        btn_add.clicked.connect(self.agregar_medicamento)
        layout.addWidget(btn_add)

    def setup_table(self, layout):
        # La tabla tomará el color rosa definido en el Stylesheet
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["ID", "Nombre", "Tipo", "Comp.", "Dosis", "Vía"])
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tree)
        
        btn_refresh = QPushButton("🔄 Mostrar Todos")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setStyleSheet("background: transparent; color: #333; font-weight: bold; text-align: right; margin-top: 5px;")
        btn_refresh.clicked.connect(self.cargar_tabla)
        layout.addWidget(btn_refresh)

    # --- LÓGICA ---
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
        if not id_med: return QMessageBox.warning(self, "Aviso", "Ingresa un ID.")
        
        if not DB_AVAILABLE: return

        try:
            self.tree.clear()
            todos = self.conexion1.Select_users(table='medicamento')
            enc = False
            for fila in todos:
                if str(fila[0]) == id_med:
                    self.tree.addTopLevelItem(QTreeWidgetItem([str(x) for x in fila]))
                    enc = True
                    break
            if enc: QMessageBox.information(self, "Éxito", "Encontrado.")
            else: 
                QMessageBox.warning(self, "Aviso", "No existe.")
                self.cargar_tabla()
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def limpiar_form(self):
        for w in [self.inp_nombre, self.inp_tipo, self.inp_comp, self.inp_dosis, self.inp_via]: w.clear()

    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import EnfermeroMain
            self.menu = EnfermeroMain(self.nombre_usuario) 
            self.menu.show(); self.close()
        except ImportError: QMessageBox.warning(self, "Error", "No se encuentra el menú.")

    def abrir_ventana(self, categoria, opcion):
        if categoria == "Inventario" and opcion == "Farmacia": return
        try:
            target = None
            if categoria == "Citas": from UI_Cita_Enfermera import MainWindow as Win; target = Win(self.nombre_usuario)
            elif categoria == "Mascotas": from UI_Revisar_Mascota_Enfermera import MainWindow as Win; target = Win(self.nombre_usuario)
            elif categoria == "Inventario" and opcion == "Hospitalización": from UI_Hospitalizacion import MainWindow as Win; target = Win(self.nombre_usuario)
            elif categoria == "Expediente": from UI_Diagnostico import MainWindow as Win; target = Win(self.nombre_usuario)

            if target: self.ventana = target; self.ventana.show(); self.close()
        except Exception as e: QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("TEST USER")
    window.show()
    sys.exit(app.exec())