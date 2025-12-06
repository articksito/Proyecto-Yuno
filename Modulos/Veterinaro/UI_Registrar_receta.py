import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout, QTextEdit, QComboBox)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPixmap, QIntValidator, QPainter, QColor

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- IMPORTACIONES ---
try:
    from db_conexionNew import Conexion
except ImportError as a:
    print(f'Error en al iniciar en registrar receta: {a}')

class VentanaReceta(QMainWindow):
    def __init__(self, nombre_usuario='Veterinario'):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.ventana = None
        
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")

        self.setWindowTitle(f"Sistema Veterinario Yuno - Gestión de Recetas ({self.nombre_usuario})")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)

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
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel {
                background-color: white;
                border-top-left-radius: 30px; border-bottom-left-radius: 30px;
                margin: 20px 20px 20px 0px; 
            }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            
            /* Inputs y TextEdit */
            QLineEdit, QTextEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none; border-radius: 10px; 
                padding: 5px 15px; font-size: 16px; color: #333;
            }
            QLineEdit:focus, QTextEdit:focus { background-color: rgba(241, 131, 227, 0.5); }
            
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
                text-align: left; padding-left: 40px; font-size: 16px;
                border-radius: 10px; color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05);
                height: 35px; margin: 2px 10px; border: none;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
            
            /* Tarjeta Derecha */
            QFrame#InfoBoard {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 12px;
            }
        """)

        # 1. Sidebar
        self.setup_sidebar()

        # 2. Panel Blanco
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- SETUP PANEL BLANCO ---
    # ==========================================
    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # 1. Header
        header = QHBoxLayout()
        lbl_header = QLabel("Gestión de Recetas")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #E0E0E0; color: #333; }
        """)
        btn_back.clicked.connect(self.volver_al_menu)

        header.addWidget(lbl_header)
        header.addStretch()
        header.addWidget(btn_back)
        self.white_layout.addLayout(header)
        self.white_layout.addSpacing(30)

        # 2. Contenedor Dividido
        content_split = QHBoxLayout()
        content_split.setSpacing(40)
        content_split.setAlignment(Qt.AlignmentFlag.AlignTop)

        # A. Izquierda: Crear Nueva Receta
        self.setup_form_left(content_split)

        # B. Derecha: Agregar Medicamentos a la Receta
        self.setup_add_meds_right(content_split)

        self.white_layout.addLayout(content_split)
        self.white_layout.addStretch(1)

    # ==========================================
    # --- IZQUIERDA: CREAR RECETA (HEADER) ---
    # ==========================================
    def setup_form_left(self, parent_layout):
        left_container = QWidget()
        layout = QVBoxLayout(left_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # Titulo Sección
        lbl_title = QLabel("1. Crear Nueva Receta")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #b67cfc;")
        layout.addWidget(lbl_title)

        # Inputs
        lbl_id = QLabel("ID Consulta Asociada:")
        lbl_id.setStyleSheet("font-size: 16px; color: #444;")
        
        self.inp_consulta = QLineEdit()
        self.inp_consulta.setPlaceholderText("Ej: 105")
        self.inp_consulta.setValidator(QIntValidator())
        self.inp_consulta.setHeight = 40

        lbl_ind = QLabel("Indicaciones Generales:")
        lbl_ind.setStyleSheet("font-size: 16px; color: #444;")
        
        self.txt_indicaciones = QTextEdit()
        self.txt_indicaciones.setPlaceholderText("Reposo, dieta blanda, etc...")
        self.txt_indicaciones.setMinimumHeight(150)

        # Botón Crear
        btn_crear = QPushButton("Generar Receta")
        btn_crear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_crear.setFixedHeight(50)
        btn_crear.setStyleSheet("""
            QPushButton {
                background-color: #b67cfc; color: white;
                font-size: 18px; font-weight: bold; border-radius: 25px;
            }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_crear.clicked.connect(self.crear_receta)

        layout.addWidget(lbl_id)
        layout.addWidget(self.inp_consulta)
        layout.addWidget(lbl_ind)
        layout.addWidget(self.txt_indicaciones)
        layout.addSpacing(10)
        layout.addWidget(btn_crear)
        layout.addStretch()

        parent_layout.addWidget(left_container, stretch=3)

    # ==========================================
    # --- DERECHA: AGREGAR MEDICAMENTOS ---
    # ==========================================
    def setup_add_meds_right(self, parent_layout):
        board = QFrame()
        board.setObjectName("InfoBoard")
        board.setMaximumWidth(400)
        
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)

        # Header (Azul)
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            background-color: #7CEBFC; 
            border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: none;
        """)
        head_lay = QHBoxLayout(header)
        lbl_tit = QLabel("2. Agregar Medicamentos")
        lbl_tit.setStyleSheet("color: #444; font-weight: bold; font-size: 16px; border: none; background: transparent;")
        head_lay.addWidget(lbl_tit, alignment=Qt.AlignmentFlag.AlignCenter)
        board_lay.addWidget(header)

        # Contenido
        content = QWidget()
        content.setStyleSheet("background: white; border: none; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;")
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(20, 20, 20, 30)
        content_lay.setSpacing(15)
        content_lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- ICONO RECETA.PNG ---
        self.lbl_pic = QLabel()
        self.lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_pic.setStyleSheet("background: #f0f0f0; border-radius: 35px; min-height: 70px; min-width: 70px; max-height: 70px;")
        
        ruta_icon = os.path.join(current_dir, "icons", "receta.png")
        if os.path.exists(ruta_icon):
            pixmap = QPixmap(ruta_icon)
            if not pixmap.isNull():
                scaled_size = 45
                final_pixmap = QPixmap(scaled_size, scaled_size)
                final_pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(final_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
                target_rect = QRect(0, 0, scaled_size, scaled_size)
                painter.drawPixmap(target_rect, pixmap)
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                painter.fillRect(target_rect, QColor("#7CEBFC")) 
                painter.end()
                self.lbl_pic.setPixmap(final_pixmap)
            else:
                self.lbl_pic.setText("💊")
        else:
            self.lbl_pic.setText("💊")

        content_lay.addWidget(self.lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Campos para agregar medicamento
        lbl_rid = QLabel("ID Receta:")
        lbl_rid.setStyleSheet("font-weight: bold; color: #555;")
        self.inp_id_receta = QLineEdit()
        self.inp_id_receta.setPlaceholderText("ID generado...")
        self.inp_id_receta.setValidator(QIntValidator())
        self.inp_id_receta.setStyleSheet("background-color: #f0f8ff; border: 1px solid #7CEBFC;")

        lbl_mid = QLabel("ID Medicamento:")
        lbl_mid.setStyleSheet("font-weight: bold; color: #555;")
        self.inp_id_med = QLineEdit()
        self.inp_id_med.setPlaceholderText("ID del medicamento")
        self.inp_id_med.setValidator(QIntValidator())

        lbl_cant = QLabel("Cantidad:")
        lbl_cant.setStyleSheet("font-weight: bold; color: #555;")
        self.inp_cantidad = QLineEdit()
        self.inp_cantidad.setPlaceholderText("Ej: 2")
        self.inp_cantidad.setValidator(QIntValidator())

        # Botón Agregar
        btn_add = QPushButton("Agregar a la Receta")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFixedHeight(45)
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #7CEBFC; color: #444; 
                font-size: 16px; font-weight: bold; border-radius: 22px;
                border: 1px solid #5CD0E3;
            }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_add.clicked.connect(self.agregar_medicamento)

        content_lay.addWidget(lbl_rid)
        content_lay.addWidget(self.inp_id_receta)
        content_lay.addWidget(lbl_mid)
        content_lay.addWidget(self.inp_id_med)
        content_lay.addWidget(lbl_cant)
        content_lay.addWidget(self.inp_cantidad)
        content_lay.addSpacing(10)
        content_lay.addWidget(btn_add)
        content_lay.addStretch()

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    # ==========================================
    # --- LÓGICA ---
    # ==========================================
    def crear_receta(self):
        # 1. Crear Receta (Encabezado)
        id_consulta = self.inp_consulta.text().strip()
        indicaciones = self.txt_indicaciones.toPlainText().strip()

        if not id_consulta or not indicaciones:
            QMessageBox.warning(self, "Datos Incompletos", "ID Consulta e Indicaciones obligatorias.")
            return

        try:
            fk_consulta = int(id_consulta)
            
            # Insertar Receta
            campos = ('indicaciones', 'fk_consulta')
            datos = (indicaciones, fk_consulta)
            
            # Usamos insertar_datos (debe retornar ID)
            nuevo_id = self.conexion.insertar_datos('receta', datos, campos)
            
            if nuevo_id:
                QMessageBox.information(self, "Receta Creada", f"Receta creada con éxito.\nID RECETA: {nuevo_id}\n\nAhora agregue los medicamentos a la derecha.")
                # Autocompletar el ID en el panel derecho
                self.inp_id_receta.setText(str(nuevo_id))
                self.inp_consulta.clear()
                self.txt_indicaciones.clear()
                # Poner foco en medicamento
                self.inp_id_med.setFocus()
            else:
                QMessageBox.warning(self, "Error", "No se generó el ID de la receta.")

        except ValueError:
            QMessageBox.warning(self, "Error", "El ID Consulta debe ser un número.")
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"Error al crear receta:\n{e}")

    def agregar_medicamento(self):
        # 2. Agregar Medicamento a la Receta (Tabla Intermedia)
        id_receta = self.inp_id_receta.text().strip()
        id_med = self.inp_id_med.text().strip()
        cant = self.inp_cantidad.text().strip()

        if not id_receta or not id_med or not cant:
            QMessageBox.warning(self, "Aviso", "Todos los campos de medicamento son obligatorios.")
            return

        try:
            fk_receta = int(id_receta)
            fk_med = int(id_med)
            cantidad = int(cant)

            # Insertar en 'receta_medicamento'
            tabla = 'receta_medicamento'
            campos = ('fk_receta', 'fk_medicamento', 'cantidad')
            datos = (fk_receta, fk_med, cantidad)

            self.conexion.insertar_datos(tabla, datos, campos,retornar=False)

            QMessageBox.information(self, "Agregado", "Medicamento agregado correctamente.")
            
            # Limpiar solo med y cantidad para agregar otro rapido
            self.inp_id_med.clear()
            self.inp_cantidad.clear()
            self.inp_id_med.setFocus()

        except Exception as e:
             QMessageBox.critical(self, "Error", f"No se pudo agregar el medicamento.\nVerifique los IDs.\n{e}")

    def volver_al_menu(self):
        try:
            from UI_Veterinario import VeterinarioMenu 
            self.menu = VeterinarioMenu(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            self.close()

    # ==========================================
    # --- SIDEBAR & NAVEGACION ---
    # ==========================================
    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        # Logo
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_logo = os.path.join(project_root, "FILES", "logo_yuno.png")
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                lbl_logo.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_logo.setText("YUNO VET")
        else:
            lbl_logo.setText("YUNO VET")
        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # Menús
        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro"])
        self.setup_accordion_group("Extra", ["Visualizar mascotas", "Visualizar medicamento", "Agregar notas para internar"])

        self.sidebar_layout.addStretch()

        # Botón Logout
        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("""
            QPushButton {
                border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 10px;
                color: white; font-weight: bold; background-color: transparent; font-size: 14px;
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
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def router_ventanas(self, categoria, opcion):
        # Evitar reabrir actual
        if categoria == "Recetas" and opcion == "Crear Receta": return

        try:
            target_window = None

            if categoria == "Consultas":
                if opcion == "Crear Consulta":
                    from UI_Realizar_consulta import VentanaConsulta as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Ver Registro":
                    from UI_Revisar_consulta import VentanaRevisarConsulta as Win
                    target_window = Win(self.nombre_usuario)

            elif categoria == "Recetas":
                if opcion == "Ver Registro":
                    from UI_Revisar_recetas import VentanaRevisarReceta as Win
                    target_window = Win(self.nombre_usuario)

            elif categoria == "Extra":
                if opcion == "Visualizar mascotas":
                    from UI_RevisarMascota_Vete import VentanaRevisarMascota as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar medicamento":
                    from UI_RevisarMedicamento import VentanaRevisarMedicamento as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Agregar notas para internar":
                     QMessageBox.information(self, "Construcción", "Modulo en desarrollo")

            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close()

        except ImportError as e:
            QMessageBox.warning(self, "Error", f"Falta archivo: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error navegando: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaReceta("TestVet")
    window.show()
    sys.exit(app.exec())