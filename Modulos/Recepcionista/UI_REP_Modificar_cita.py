import sys
import os
from datetime import datetime, date, time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QDateEdit, QTimeEdit, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont, QPixmap, QIntValidator

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- IMPORTACIONES ---
try:
    from db_connection import Conexion
    from UI_REP_main import MainWindow as MenuPrincipal 
except ImportError:
    class Conexion:
        def consultar_registro(self, *args): return None
        def editar_registro(self, *args): return True
    class MenuPrincipal(QMainWindow):
        def __init__(self, u): super().__init__(); self.show()

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.ventana = None
        self.cita_cargada = False

        self.setWindowTitle(f"Sistema Veterinario Yuno - Modificar Cita ({self.nombre_usuario})")
        
        # 1. TAMAÑO MÍNIMO (Evita el error de miniatura)
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES ---
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC);
            }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel {
                background-color: white;
                border-top-left-radius: 30px; border-bottom-left-radius: 30px;
                margin: 20px 20px 20px 0px; 
            }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            
            /* Botones del Menú Lateral */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px;
                color: white; font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF;
            }
            
            /* Botones del Submenú */
            QPushButton.sub-btn {
                text-align: left; padding-left: 40px; font-size: 16px;
                border-radius: 10px; color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05);
                height: 35px; margin: 2px 10px;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
            
            /* Inputs */
            QLineEdit:disabled, QDateEdit:disabled, QTimeEdit:disabled, QComboBox:disabled {
                background-color: #F0F0F0; color: #999; border: 1px solid #DDD;
            }
        """)

        # 1. Barra Lateral
        self.setup_sidebar()

        # 2. Panel Blanco
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Modificar Cita")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        # Botón Guardar Superior
    

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()

        self.white_layout.addLayout(header_layout)
        self.white_layout.addStretch(1)

        # Contenedor Formulario + Info
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Alineación Superior

        self.setup_edit_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addStretch(1) 
        
        # Botón Guardar Inferior
        self.setup_save_button()
        self.white_layout.addSpacing(20)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

        # Estado inicial
        self.set_form_enabled(False)

    # --- NAVEGACIÓN ---
    def return_to_menu(self):
        try:
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al volver al menú: {e}")
            self.close()

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        # Margen inferior 50 para alineación correcta del botón volver
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # Logo
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "FILES", "logo_yuno.png")
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                lbl_logo.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        else:
            lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        
        self.sidebar_layout.addWidget(lbl_logo)

        # Menús
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])
        
        self.sidebar_layout.addStretch()

        # Botón Volver
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setStyleSheet("""
            QPushButton {
                border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 10px;
                font-size: 14px; color: white; font-weight: bold; background-color: transparent;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.2); }
        """)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.return_to_menu)
        self.sidebar_layout.addWidget(btn_back)

    def setup_accordion_group(self, title, options):
        btn_main = QPushButton(title)
        btn_main.setProperty("class", "menu-btn")
        btn_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebar_layout.addWidget(btn_main)

        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 10)
        
        for opt in options:
            btn = QPushButton(opt)
            btn.setProperty("class", "sub-btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, c=title, o=opt: self.abrir_ventana(c, o))
            layout.addWidget(btn)

        frame.hide()
        self.sidebar_layout.addWidget(frame)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame))

    def abrir_ventana(self, categoria, opcion):
        if categoria == "Citas" and opcion == "Modificar": return

        # MAPEO DE RUTAS CORREGIDO (Coincide con tus nombres de archivo reales)
        ventana_map = {
            "Citas": {
                "Agendar": "UI_REP_Crear_cita",
                "Visualizar": "UI_REP_Revisar_Cita",
                "Modificar": "UI_REP_Modificar_cita"
            },
            "Mascotas": {
                "Registrar": "UI_REP_Registrar_mascota",
                "Visualizar": "UI_Revisar_Mascota",   # Sin REP
                "Modificar": "UI_REP_Modificar_Mascota"
            },
            "Clientes": {
                "Registrar": "UI_REP_Registra_cliente",
                "Visualizar": "UI_Revisar_cliente",   # Sin REP
                "Modificar": "UI_REP_Modificar_cliente"
            }
        }

        nombre_modulo = ventana_map.get(categoria, {}).get(opcion)

        if nombre_modulo:
            try:
                module = __import__(nombre_modulo, fromlist=['MainWindow'])
                self.ventana = module.MainWindow(self.nombre_usuario)
                self.ventana.show()
                self.close()
            except ImportError as e:
                QMessageBox.warning(self, "Error de Navegación", f"Falta el archivo: {nombre_modulo}.py\n{e}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al abrir ventana: {e}")
        else:
            print(f"Ruta no mapeada: {categoria} -> {opcion}")

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def setup_edit_form(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(30)
        grid.setContentsMargins(0, 0, 0, 0)

        style_input = "background-color: rgba(241, 131, 227, 0.35); border: none; border-radius: 10px; padding: 5px 15px; font-size: 18px; color: #333; height: 45px;"
        style_lbl = "font-size: 24px; color: black; font-weight: 400;"

        # 1. Búsqueda
        lbl_id = QLabel("ID Cita:"); lbl_id.setStyleSheet(style_lbl)
        self.inp_id = QLineEdit(); self.inp_id.setPlaceholderText("ID..."); self.inp_id.setStyleSheet(style_input)
        self.inp_id.setValidator(QIntValidator())
        
        btn_search = QPushButton("Buscar")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("background-color: #7CEBFC; border-radius: 10px; font-weight: bold; border: 1px solid #5CD0E3;")
        btn_search.setFixedSize(100, 45)
        btn_search.clicked.connect(self.buscar_cita)

        # 2. Campos
        self.inp_fecha = QDateEdit(); self.inp_fecha.setCalendarPopup(True); self.inp_fecha.setDate(QDate.currentDate()); self.inp_fecha.setStyleSheet(style_input)
        self.inp_hora = QTimeEdit(); self.inp_hora.setTime(QTime.currentTime()); self.inp_hora.setStyleSheet(style_input)
        self.inp_motivo = QLineEdit(); self.inp_motivo.setStyleSheet(style_input)
        
        self.inp_estado = QComboBox(); self.inp_estado.addItems(["Pendiente", "Confirmada", "Cancelada", "Completada"]); self.inp_estado.setStyleSheet(style_input.replace("QLineEdit", "QComboBox"))
        self.inp_mascota = QLineEdit(); self.inp_mascota.setPlaceholderText("ID Mascota"); self.inp_mascota.setStyleSheet(style_input); self.inp_mascota.setValidator(QIntValidator())
        self.inp_vet = QLineEdit(); self.inp_vet.setPlaceholderText("ID Veterinario"); self.inp_vet.setStyleSheet(style_input); self.inp_vet.setValidator(QIntValidator())

        # Grid
        grid.addWidget(lbl_id, 0, 0)
        grid.addWidget(self.inp_id, 0, 1); grid.addWidget(btn_search, 0, 2)

        self.add_row(grid, 1, "Fecha:", self.inp_fecha, style_lbl)
        self.add_row(grid, 2, "Hora:", self.inp_hora, style_lbl)
        self.add_row(grid, 3, "Motivo:", self.inp_motivo, style_lbl)
        self.add_row(grid, 4, "Estado:", self.inp_estado, style_lbl)
        self.add_row(grid, 5, "Mascota:", self.inp_mascota, style_lbl)
        self.add_row(grid, 6, "Veterinario:", self.inp_vet, style_lbl)

        grid.setRowStretch(7, 1)
        parent_layout.addWidget(form_widget, stretch=2)

    def add_row(self, grid, row, label, widget, style):
        l = QLabel(label); l.setStyleSheet(style)
        grid.addWidget(l, row, 0)
        grid.addWidget(widget, row, 1, 1, 2)

    def setup_info_board(self, parent_layout):
        board = QFrame(); board.setFixedWidth(350)
        board.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 10px;")
        vl = QVBoxLayout(board); vl.setContentsMargins(0,0,0,0); vl.setSpacing(0)

        h = QFrame(); h.setFixedHeight(60)
        h.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252,124,226,0.8)); border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom: none;")
        hl = QVBoxLayout(h); l = QLabel("Estado / Notas"); l.setAlignment(Qt.AlignmentFlag.AlignCenter); l.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background: transparent;")
        hl.addWidget(l)

        c = QFrame(); c.setStyleSheet("background: white; border-radius: 10px; border: none;")
        cl = QVBoxLayout(c); cl.setContentsMargins(20,20,20,20); cl.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.lbl_info = QLabel("Busca una cita para ver detalles aquí."); self.lbl_info.setWordWrap(True); self.lbl_info.setStyleSheet("color: #555; font-size: 14px;")
        cl.addWidget(self.lbl_info)

        vl.addWidget(h); vl.addWidget(c)
        parent_layout.addWidget(board, stretch=1)

    def setup_save_button(self):
        btn = QPushButton("Guardar Cambios")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(250, 60)
        btn.setStyleSheet("QPushButton { background-color: #b67cfc; color: white; font-size: 24px; font-weight: bold; border-radius: 30px; } QPushButton:hover { background-color: #a060e8; }")
        btn.clicked.connect(self.guardar_cambios)
        l = QHBoxLayout(); l.addStretch(); l.addWidget(btn); l.addStretch()
        self.white_layout.addLayout(l)

    def set_form_enabled(self, enabled):
        for w in [self.inp_fecha, self.inp_hora, self.inp_motivo, self.inp_estado, self.inp_mascota, self.inp_vet]:
            w.setEnabled(enabled)

    def buscar_cita(self):
        cid = self.inp_id.text().strip()
        self.cita_cargada = False
        self.set_form_enabled(False)

        if not cid: return QMessageBox.warning(self, "Aviso", "Ingresa un ID.")

        try:
            cols = ['fecha', 'hora', 'motivo', 'estado', 'fk_mascota', 'fk_veterinario']
            r = self.conexion1.consultar_registro('cita', 'id_cita', cid, cols)
            
            if r:
                if isinstance(r[0], (date, datetime)): self.inp_fecha.setDate(r[0])
                elif isinstance(r[0], str): self.inp_fecha.setDate(QDate.fromString(r[0], "yyyy-MM-dd"))
                
                if hasattr(r[1], 'hour'): self.inp_hora.setTime(QTime(r[1].hour, r[1].minute))
                elif isinstance(r[1], str): self.inp_hora.setTime(QTime.fromString(r[1], "HH:mm:ss"))

                self.inp_motivo.setText(str(r[2]))
                self.inp_estado.setCurrentText(str(r[3]))
                self.inp_mascota.setText(str(r[4]))
                self.inp_vet.setText(str(r[5]))
                
                self.lbl_info.setText(f"Editando Cita #{cid}\nEstado actual: {r[3]}")
                self.cita_cargada = True
                self.set_form_enabled(True)
                QMessageBox.information(self, "Éxito", "Cita cargada.")
            else:
                QMessageBox.warning(self, "Error", "Cita no encontrada.")
                self.lbl_info.setText("...")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def guardar_cambios(self):
        if not self.cita_cargada: return QMessageBox.warning(self, "Aviso", "Busca una cita primero.")
        
        cid = self.inp_id.text().strip()
        mas = self.inp_mascota.text().strip()
        vet = self.inp_vet.text().strip()

        if not mas or not vet: return QMessageBox.warning(self, "Aviso", "Mascota y Veterinario obligatorios.")

        d = {
            "fecha": self.inp_fecha.date().toString("yyyy-MM-dd"),
            "hora": self.inp_hora.time().toString("HH:mm:ss"),
            "motivo": self.inp_motivo.text().strip(),
            "estado": self.inp_estado.currentText(),
            "fk_mascota": int(mas),
            "fk_veterinario": int(vet)
        }

        try:
            if self.conexion1.editar_registro(cid, d, 'cita', 'id_cita'):
                QMessageBox.information(self, "Éxito", "Cita actualizada.")
                self.inp_id.clear(); self.set_form_enabled(False); self.lbl_info.setText("...")
                self.inp_motivo.clear(); self.inp_mascota.clear(); self.inp_vet.clear()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())