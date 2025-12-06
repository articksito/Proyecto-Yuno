import sys
import os

# --- 1. CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if 'Veterinaro' in current_dir:
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
else:
    project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout, QTextEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QListWidget, QListWidgetItem,
                             QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QColor

# Importar conexión
from db_conexionNew import Conexion

class VentanaRevisarReceta(QMainWindow):
    def __init__(self, nombre_usuario='Veterinario'):
        super().__init__()
        
        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Sistema Veterinario Yuno - Historial de Recetas")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)

        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS VISUALES ---
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            
            /* Inputs Generales */
            QLineEdit { background-color: white; border: 2px solid #ddd; border-radius: 10px; padding: 8px; font-size: 16px; }
            QLineEdit[readOnly="true"] { background-color: #F0F0F0; color: #555; }
            
            /* Botones Sidebar */
            QPushButton.menu-btn { text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; color: white; font-weight: bold; font-size: 18px; background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px; }
            QPushButton.menu-btn:hover { background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; }
            
            QPushButton.sub-btn { text-align: left; padding-left: 40px; border-radius: 10px; color: #F0F0F0; font-size: 16px; background-color: rgba(0, 0, 0, 0.05); height: 35px; margin: 2px 10px; }
            QPushButton.sub-btn:hover { color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; }
            
            QPushButton.logout-btn { text-align: center; border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 20px; font-size: 14px; color: white; font-weight: bold; background-color: transparent; }
            QPushButton.logout-btn:hover { background-color: rgba(255, 255, 255, 0.2); }

            /* Tabla Principal */
            QTableWidget { background-color: white; border: 1px solid #E0E0E0; border-radius: 15px; gridline-color: transparent; font-size: 14px; selection-background-color: #E1BEE7; selection-color: #333; outline: 0; }
            QHeaderView::section { background-color: #7CEBFC; color: #444; font-weight: bold; border: none; padding: 12px; }
            
            /* GLOBAL: Lista limpia (se sobrescribe localmente si es necesario) */
            QListWidget { border: none; outline: 0; }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # --- SIDEBAR ---
    def setup_sidebar(self):
        self.sidebar = QWidget(); self.sidebar.setObjectName("Sidebar"); self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar); self.sidebar_layout.setContentsMargins(20, 50, 20, 50); self.sidebar_layout.setSpacing(5)

        lbl_logo = QLabel(); lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_logo = os.path.join(current_dir, "..", "FILES", "logo_yuno.png")
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull(): lbl_logo.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else: lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        else: lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        self.sidebar_layout.addWidget(lbl_logo); self.sidebar_layout.addSpacing(20)

        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro"])
        self.setup_accordion_group("Extra", ["Visualizar mascotas", "Visualizar medicamento", "Agregar notas para internar"])

        self.sidebar_layout.addStretch()
        btn_logout = QPushButton("Cerrar Sesión"); btn_logout.setProperty("class", "logout-btn"); btn_logout.setCursor(Qt.CursorShape.PointingHandCursor); btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)
        
        btn_back = QPushButton("Volver al Menú"); btn_back.setProperty("class", "logout-btn"); btn_back.setCursor(Qt.CursorShape.PointingHandCursor); btn_back.clicked.connect(self.volver_al_menu)
        self.sidebar_layout.addWidget(btn_back)

    def setup_accordion_group(self, title, options):
        btn_main = QPushButton(title); btn_main.setProperty("class", "menu-btn"); btn_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebar_layout.addWidget(btn_main)
        frame = QFrame(); layout = QVBoxLayout(frame); layout.setContentsMargins(0, 0, 0, 10); layout.setSpacing(2)
        for opt in options:
            btn = QPushButton(opt); btn.setProperty("class", "sub-btn"); btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, t=title, o=opt: self.router_ventanas(t, o))
            layout.addWidget(btn)
        frame.hide(); self.sidebar_layout.addWidget(frame)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def router_ventanas(self, categoria, opcion):
        if categoria == "Recetas" and opcion == "Ver Registro": return
        try:
            if categoria == "Consultas":
                if opcion == "Crear Consulta": from UI_Realizar_consulta import VentanaConsulta; self.ventana = VentanaConsulta(self.nombre_usuario)
                elif opcion == "Ver Registro": from UI_Revisar_consulta import VentanaRevisarConsulta; self.ventana = VentanaRevisarConsulta(self.nombre_usuario)
            elif categoria == "Recetas":
                if opcion == "Crear Receta": from UI_Registrar_receta import VentanaReceta; self.ventana = VentanaReceta(self.nombre_usuario)
            
            elif categoria == "Extra":
                if opcion == "Visualizar mascotas": from UI_RevisarMascota_Vete import VentanaRevisarMascota; self.ventana = VentanaRevisarMascota(self.nombre_usuario)
                elif opcion == "Visualizar medicamento": from UI_RevisarMedicamento import VentanaRevisarMedicamento; self.ventana = VentanaRevisarMedicamento(self.nombre_usuario)
                elif opcion == "Agregar notas para internar": QMessageBox.information(self, "Info", "Módulo de Notas.")
            
            if hasattr(self, 'ventana') and self.ventana: self.ventana.show(); self.close()
        except Exception as e: QMessageBox.critical(self, "Error", f"Error al navegar: {e}")

    # --- PANEL CENTRAL ---
    def setup_content_panel(self):
        self.white_panel = QWidget(); self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel); self.white_layout.setContentsMargins(50, 40, 50, 40)

        header_layout = QHBoxLayout()
        lbl_header = QLabel("Historial de Recetas"); lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        btn_refresh = QPushButton("↻ Actualizar"); btn_refresh.setFixedSize(120, 40); btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setStyleSheet("background-color: #7CEBFC; color: #444; border-radius: 10px; font-weight: bold; border: 1px solid #5CD0E3;")
        btn_refresh.clicked.connect(lambda: [self.txt_buscar.clear(), self.cargar_datos_tabla(), self.limpiar_panel_derecho()])
        
        header_layout.addWidget(lbl_header); header_layout.addStretch(); header_layout.addWidget(btn_refresh)
        self.white_layout.addLayout(header_layout); self.white_layout.addSpacing(20)

        # Buscador
        search_layout = QHBoxLayout()
        self.txt_buscar = QLineEdit(); self.txt_buscar.setPlaceholderText("🔍 Buscar por mascota..."); self.txt_buscar.setFixedSize(300, 40)
        self.txt_buscar.returnPressed.connect(self.realizar_busqueda)
        btn_buscar = QPushButton("Buscar"); btn_buscar.setFixedSize(100, 40); btn_buscar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_buscar.setStyleSheet("background-color: #E1BEE7; color: #4A148C; border-radius: 10px; font-weight: bold; border: none;")
        btn_buscar.clicked.connect(self.realizar_busqueda)
        search_layout.addWidget(self.txt_buscar); search_layout.addWidget(btn_buscar); search_layout.addStretch()
        self.white_layout.addLayout(search_layout); self.white_layout.addSpacing(20)

        # Contenido: Tabla (Izq) + Panel Info (Der)
        content_layout = QHBoxLayout()
        self.setup_table(content_layout)
        self.setup_info_board(content_layout) 
        
        self.white_layout.addLayout(content_layout)
        self.cargar_datos_tabla()

    def setup_table(self, layout):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Receta", "Fecha", "Mascota", "Indicaciones Generales"])
        self.table.setShowGrid(False); self.table.setAlternatingRowColors(True); self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed); self.table.setColumnWidth(0, 80) # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # Fecha
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) # Mascota
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Indicaciones
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.table.itemClicked.connect(self.cargar_detalle_medicinas)

        layout.addWidget(self.table, stretch=2)

    def setup_info_board(self, layout):
        # Panel derecho para mostrar las medicinas de la receta seleccionada
        board = QFrame(); board.setFixedWidth(350)
        # Borde exterior del contenedor
        board.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 10px;")
        vl = QVBoxLayout(board); vl.setContentsMargins(0,0,0,0); vl.setSpacing(0)

        # Header Indicaciones (AZUL #7CEBFC para unificar)
        h1 = QFrame(); h1.setFixedHeight(40)
        h1.setStyleSheet("background: #7CEBFC; border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom: none;")
        l1 = QLabel("📝 Indicaciones Completas", h1); l1.setAlignment(Qt.AlignmentFlag.AlignCenter); l1.setStyleSheet("font-weight: bold; color: #333; border: none;")
        vl1 = QVBoxLayout(h1); vl1.addWidget(l1)
        
        # Area de texto (Sin borde interno, fondo blanco o muy suave)
        self.txt_indicaciones = QTextEdit()
        self.txt_indicaciones.setReadOnly(True)
        self.txt_indicaciones.setStyleSheet("border: none; padding: 10px; background: white; color: #555;")
        self.txt_indicaciones.setMaximumHeight(100)

        # Header Medicinas (AZUL #7CEBFC)
        h2 = QFrame(); h2.setFixedHeight(40)
        h2.setStyleSheet("background: #7CEBFC; border: none;") # Mismo azul
        l2 = QLabel("💊 Medicamentos Recetados", h2); l2.setAlignment(Qt.AlignmentFlag.AlignCenter); l2.setStyleSheet("font-weight: bold; color: #333; border: none;")
        vl2 = QVBoxLayout(h2); vl2.addWidget(l2)

        # Lista (Sin borde interno)
        self.lista_meds = QListWidget()
        self.lista_meds.setStyleSheet("border: none; background: white; padding: 5px;")

        # Añadir separador visual simple entre secciones si se desea, o dejar limpio
        linea = QFrame(); linea.setFrameShape(QFrame.Shape.HLine); linea.setStyleSheet("color: #DDD;")

        vl.addWidget(h1)
        vl.addWidget(self.txt_indicaciones)
        vl.addWidget(linea) # Separador sutil
        vl.addWidget(h2)
        vl.addWidget(self.lista_meds)
        
        layout.addWidget(board, stretch=1)

    # --- LÓGICA ---
    def realizar_busqueda(self):
        texto = self.txt_buscar.text().strip()
        self.cargar_datos_tabla(filtro=texto)

    def cargar_datos_tabla(self, filtro=""):
        self.table.setRowCount(0)
        self.limpiar_panel_derecho()
        try:
            # Traemos datos básicos de la receta + mascota
            columnas = ('receta.id_receta', 'consulta.fecha', 'mascota.nombre', 'receta.indicaciones')
            orden = ('receta.id_receta',)
            joins = [('consulta', 'receta'), ('mascota', 'consulta')] 

            if filtro:
                datos = self.conexion.consultar_tabla(columnas, 'receta', joins=joins, filtro=filtro, campo_filtro='mascota.nombre', orden=orden)
            else:
                datos = self.conexion.consultar_tabla(columnas, 'receta', joins=joins, orden=orden)

            for i, row in enumerate(datos):
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(str(row[0]))) # ID
                self.table.setItem(i, 1, QTableWidgetItem(str(row[1]))) # Fecha
                self.table.setItem(i, 2, QTableWidgetItem(str(row[2]))) # Mascota
                
                item_ind = QTableWidgetItem(str(row[3]))
                item_ind.setToolTip("Click para ver detalles y medicinas")
                self.table.setItem(i, 3, item_ind) 

        except Exception as e: print(f"Error tabla: {e}")

    def cargar_detalle_medicinas(self, item):
        row = item.row()
        id_receta = self.table.item(row, 0).text()
        indicaciones = self.table.item(row, 3).text()
        
        self.txt_indicaciones.setText(indicaciones)
        self.lista_meds.clear()
        try:
            query_meds = """
                SELECT m.nombre, m.dosis_recomendada 
                FROM medicamento m
                JOIN receta_medicamento rm ON m.id_medicamento = rm.fk_medicamento
                WHERE rm.fk_receta = %s
            """
            self.conexion.cursor.execute(query_meds, (id_receta,))
            medicinas = self.conexion.cursor.fetchall()
            
            if medicinas:
                for med in medicinas:
                    nombre = med[0]
                    dosis = med[1]
                    list_item = QListWidgetItem(f"• {nombre}")
                    list_item.setToolTip(f"Dosis: {dosis}")
                    list_item.setFont(QFont("Segoe UI", 11))
                    self.lista_meds.addItem(list_item)
                    
                    # Sub-item más pequeño y gris para la dosis
                    sub_item = QListWidgetItem(f"   ↳ {dosis}")
                    sub_item.setForeground(QColor("#777"))
                    sub_item.setFont(QFont("Segoe UI", 9))
                    self.lista_meds.addItem(sub_item)
            else:
                self.lista_meds.addItem("Sin medicamentos registrados.")
                
        except Exception as e:
            print(f"Error cargando medicinas: {e}")
            self.lista_meds.addItem("Error al cargar.")

    def limpiar_panel_derecho(self):
        self.txt_indicaciones.clear()
        self.lista_meds.clear()

    def volver_al_menu(self):
        try:
            from UI_Veterinario import VeterinarioMenu 
            self.menu = VeterinarioMenu(self.nombre_usuario)
            self.menu.show(); self.close()
        except ImportError: self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaRevisarReceta('Veterinario')
    window.show()
    sys.exit(app.exec())