import sys
import os
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QMessageBox, QComboBox, QDateEdit, QTimeEdit)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont, QPixmap, QIntValidator

# Intentamos importar la conexión nueva, si falla usamos la genérica o mock
try:
    from db_conexionNew import Conexion
except ImportError:
    class Conexion:
        def consultar_registro(self, *args, **kwargs): return None
        def editar_registro(self, *args, **kwargs): return False

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle(f"Sistema Veterinario Yuno - Modificar Cita ({self.nombre_usuario})")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)
        
        # Conexión Base de Datos
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")
        
        # Variable para saber qué ID estamos editando
        self.current_cita_id = None

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
            
            /* Botón Logout / Volver */
            QPushButton.action-btn {
                border: 2px solid white; border-radius: 15px; padding: 10px; 
                margin-top: 10px; font-size: 14px; color: white; font-weight: bold; 
                background-color: transparent;
            }
            QPushButton.action-btn:hover { background-color: rgba(255, 255, 255, 0.2); }

            /* --- INPUTS Y FORMULARIO (COLOR ROSA) --- */
            QLineEdit, QComboBox, QDateEdit, QTimeEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 16px;
                color: #333;
                height: 40px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus {
                background-color: rgba(241, 131, 227, 0.5); 
            }
            QLineEdit:disabled, QComboBox:disabled, QDateEdit:disabled, QTimeEdit:disabled {
                background-color: #F0F0F0; color: #999;
            }
            QComboBox::drop-down, QDateEdit::drop-down { border: 0px; }
            
            /* --- PANEL DERECHO (INFO) --- */
            QFrame#InfoBoard {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 12px;
            }
        """)

        self.setup_sidebar()
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- SETUP SIDEBAR (RECEPCIONISTA) ---
    # ==========================================

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # --- LOGO ---
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
        self.sidebar_layout.addSpacing(20)

        # --- MENÚS ---
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])
        
        self.sidebar_layout.addStretch()

        # Botón Volver
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setProperty("class", "action-btn")
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
            btn.clicked.connect(lambda checked=False, c=title, o=opt: self.navegar(c, o))
            layout.addWidget(btn)
        
        frame.hide()
        self.sidebar_layout.addWidget(frame)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def return_to_menu(self):
        try:
            from UI_REP_main import MainWindow as MenuPrincipal
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except ImportError:
            self.close()

    def navegar(self, categoria, opcion):
        # Evitar recargar la misma ventana
        if categoria == "Citas" and opcion == "Modificar": return

        ventana_map = {
            "Citas": {
                "Agendar": "UI_REP_Crear_cita",
                "Visualizar": "UI_REP_Revisar_Cita",
                "Modificar": "UI_REP_Modificar_cita"
            },
            "Mascotas": {
                "Registrar": "UI_REP_Registrar_mascota",
                "Visualizar": "UI_Revisar_Mascota",
                "Modificar": "UI_REP_Modificar_Mascota"
            },
            "Clientes": {
                "Registrar": "UI_REP_Registra_cliente",
                "Visualizar": "UI_Revisar_cliente", 
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

    # ==========================================
    # --- PANEL CENTRAL ---
    # ==========================================

    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(40, 40, 20, 40)

        # 1. Header
        header = QHBoxLayout()
        lbl_header = QLabel("Modificar Cita")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        header.addWidget(lbl_header)
        header.addStretch()
        self.white_layout.addLayout(header)
        self.white_layout.addSpacing(10)

        # 2. Barra de Búsqueda
        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        # 3. Contenedor Dividido
        content_split = QHBoxLayout()
        content_split.setSpacing(40)

        self.setup_form_left(content_split)
        self.setup_info_right(content_split)

        self.white_layout.addLayout(content_split)
        self.white_layout.addStretch()

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_search = QLabel("ID Cita:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        
        self.inp_search_id = QLineEdit()
        self.inp_search_id.setPlaceholderText("Ej: 402")
        self.inp_search_id.setFixedWidth(200)
        self.inp_search_id.setValidator(QIntValidator())
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
        btn_search.clicked.connect(self.buscar_cita)
        
        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.inp_search_id)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_container)

    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        label_style = "font-size: 18px; font-weight: 500; color: #444;"

        # --- Campos de Cita ---
        
        # Fecha
        self.inp_fecha = QDateEdit()
        self.inp_fecha.setCalendarPopup(True)
        self.inp_fecha.setDisplayFormat("yyyy-MM-dd")
        self.inp_fecha.setDate(QDate.currentDate())
        
        # Hora
        self.inp_hora = QTimeEdit()
        self.inp_hora.setDisplayFormat("HH:mm")
        self.inp_hora.setTime(QTime.currentTime())
        
        # Motivo
        self.inp_motivo = QLineEdit()
        self.inp_motivo.setPlaceholderText("Razón de la cita...")
        
        # Estado
        self.inp_estado = QComboBox()
        self.inp_estado.addItems(["Pendiente", "Confirmada", "Cancelada", "Realizada"])
        
        # ID Relacionados (Solo lectura usualmente al editar, o editables con cuidado)
        # Para este ejemplo los dejaremos como informativos en el formulario
        self.inp_id_mascota = QLineEdit()
        self.inp_id_mascota.setPlaceholderText("ID Mascota")
        self.inp_id_mascota.setReadOnly(True) # Normalmente no cambiamos la mascota de una cita ya creada

        # Conectar señales para actualización en tiempo real
        self.inp_fecha.dateChanged.connect(self.update_preview)
        self.inp_hora.timeChanged.connect(self.update_preview)
        self.inp_motivo.textChanged.connect(self.update_preview)
        self.inp_estado.currentTextChanged.connect(self.update_preview)

        # Agregar al Grid
        self.add_form_row(grid, 0, "Fecha:", self.inp_fecha, label_style)
        self.add_form_row(grid, 1, "Hora:", self.inp_hora, label_style)
        self.add_form_row(grid, 2, "Motivo:", self.inp_motivo, label_style)
        self.add_form_row(grid, 3, "Estado:", self.inp_estado, label_style)
        self.add_form_row(grid, 4, "ID Mascota:", self.inp_id_mascota, label_style)

        form_widget.setEnabled(False)
        self.form_widget = form_widget

        parent_layout.addWidget(form_widget, stretch=3)

    def add_form_row(self, grid, row, label_text, widget, style):
        lbl = QLabel(label_text)
        lbl.setStyleSheet(style)
        grid.addWidget(lbl, row, 0)
        grid.addWidget(widget, row, 1)

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
            background-color: #7CEBFC; 
            border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: none;
        """)
        head_lay = QHBoxLayout(header)
        lbl_tit = QLabel("Vista Previa")
        lbl_tit.setStyleSheet("color: #444; font-weight: bold; font-size: 16px; border: none; background: transparent;")
        head_lay.addWidget(lbl_tit, alignment=Qt.AlignmentFlag.AlignCenter)
        board_lay.addWidget(header)

        # Contenido
        content = QWidget()
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(20, 30, 20, 30)
        content_lay.setSpacing(10)
        content_lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- IMAGEN CITA ---
        self.lbl_pic = QLabel("📅") # Fallback emoji
        self.lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_pic.setStyleSheet("background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        
        # Cargar icono 'cita.png'
        ruta_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "cita.png")
        
        if os.path.exists(ruta_icon):
            pixmap = QPixmap(ruta_icon)
            if not pixmap.isNull():
                self.lbl_pic.setPixmap(pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                self.lbl_pic.setText("")
            else:
                self.lbl_pic.setStyleSheet(self.lbl_pic.styleSheet() + "font-size: 40px;")
        else:
            self.lbl_pic.setStyleSheet(self.lbl_pic.styleSheet() + "font-size: 40px;")
        
        content_lay.addWidget(self.lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Datos Preview
        self.prev_motivo = QLabel("Motivo Cita")
        self.prev_motivo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_motivo.setWordWrap(True)
        self.prev_motivo.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.prev_fecha = QLabel("AAAA-MM-DD | 00:00")
        self.prev_fecha.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_fecha.setStyleSheet("font-size: 16px; color: #666;")

        self.prev_estado = QLabel("PENDIENTE")
        self.prev_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_estado.setStyleSheet("""
            font-size: 14px; font-weight: bold; color: #555; 
            background: #eee; padding: 5px 10px; border-radius: 10px; margin-top: 5px;
        """)

        content_lay.addWidget(self.prev_motivo)
        content_lay.addWidget(self.prev_fecha)
        content_lay.addWidget(self.prev_estado)
        
        content_lay.addStretch() 
        
        # Botón Guardar
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_guardar.setFixedSize(250, 50)
        self.btn_guardar.setEnabled(False) 
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #7CEBFC; 
                color: #444; 
                font-size: 18px; 
                font-weight: bold; 
                border-radius: 25px;
                border: 1px solid #5CD0E3;
            }
            QPushButton:hover { background-color: #5CD0E3; }
            QPushButton:disabled { background-color: #f0f0f0; color: #aaa; border: 1px solid #ddd; }
        """)
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(self.btn_guardar)
        btn_container.addStretch()
        
        content_lay.addLayout(btn_container)
        content_lay.addSpacing(10)

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    # ==========================================
    # --- LÓGICA ---
    # ==========================================

    def update_preview(self):
        fec = self.inp_fecha.date().toString("yyyy-MM-dd")
        hor = self.inp_hora.time().toString("HH:mm")
        mot = self.inp_motivo.text()
        est = self.inp_estado.currentText()

        self.prev_motivo.setText(mot if mot else "Motivo Cita")
        self.prev_fecha.setText(f"{fec} | {hor}")
        self.prev_estado.setText(est.upper())
        
        # Color dinámico según estado
        color_map = {
            "Pendiente": "#FFF3CD", # Amarillo claro
            "Confirmada": "#D4EDDA", # Verde claro
            "Cancelada": "#F8D7DA", # Rojo claro
            "Realizada": "#CCE5FF"  # Azul claro
        }
        bg = color_map.get(est, "#eee")
        self.prev_estado.setStyleSheet(f"font-size: 14px; font-weight: bold; color: #555; background: {bg}; padding: 5px 10px; border-radius: 10px; margin-top: 5px;")

    def buscar_cita(self):
        cid = self.inp_search_id.text().strip()
        if not cid:
            return QMessageBox.warning(self, "Aviso", "Ingresa un ID de Cita.")

        try:
            # Consultamos fecha, hora, motivo, estado, fk_mascota
            columnas = ['fecha', 'hora', 'motivo', 'estado', 'fk_mascota']
            res = self.conexion.consultar_registro('cita', 'id_cita', cid, columnas)
            
            if res:
                self.current_cita_id = cid
                
                # Asignar valores
                # Nota: Dependiendo de tu BD, 'fecha' puede venir como str o date object.
                fecha_str = str(res[0])
                hora_str = str(res[1])
                
                self.inp_fecha.setDate(QDate.fromString(fecha_str, "yyyy-MM-dd"))
                # Si la hora viene con segundos "HH:mm:ss", tomamos solo HH:mm si es necesario, 
                # pero QTime.fromString suele ser flexible o especificamos formato.
                # Intentamos formato completo o corto
                t = QTime.fromString(hora_str, "HH:mm:ss")
                if not t.isValid(): t = QTime.fromString(hora_str, "HH:mm")
                self.inp_hora.setTime(t)
                
                self.inp_motivo.setText(str(res[2]))
                self.inp_estado.setCurrentText(str(res[3]))
                self.inp_id_mascota.setText(str(res[4]))
                
                self.form_widget.setEnabled(True)
                self.btn_guardar.setEnabled(True)
                self.update_preview()
                
                QMessageBox.information(self, "Éxito", "Cita encontrada.")
            else:
                QMessageBox.warning(self, "Error", "Cita no encontrada.")
                self.limpiar_form()
                self.form_widget.setEnabled(False)
                self.btn_guardar.setEnabled(False)
                self.current_cita_id = None

        except Exception as e:
            QMessageBox.critical(self, "Error BD", str(e))

    def guardar_cambios(self):
        if not self.current_cita_id: 
            return QMessageBox.warning(self, "Aviso", "Busca una cita primero.")
        
        mot = self.inp_motivo.text().strip()
        if not mot:
            return QMessageBox.warning(self, "Aviso", "El motivo es obligatorio.")

        datos = {
            "fecha": self.inp_fecha.date().toString("yyyy-MM-dd"),
            "hora": self.inp_hora.time().toString("HH:mm"),
            "motivo": mot,
            "estado": self.inp_estado.currentText()
        }

        try:
            if self.conexion.editar_registro(self.current_cita_id, datos, 'cita', 'id_cita'):
                QMessageBox.information(self, "Éxito", "Cita modificada correctamente.")
                self.inp_search_id.clear()
                self.limpiar_form()
                self.form_widget.setEnabled(False)
                self.btn_guardar.setEnabled(False)
                self.current_cita_id = None
                self.update_preview()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la cita.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def limpiar_form(self):
        self.inp_motivo.clear()
        self.inp_id_mascota.clear()
        self.inp_fecha.setDate(QDate.currentDate())
        self.inp_hora.setTime(QTime.currentTime())
        self.inp_estado.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())