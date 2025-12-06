import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, 
                             QMessageBox, QFrame, QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor

# --- AJUSTE DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) 
if current_dir not in sys.path: sys.path.append(current_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)

# Intentar importar conexión
try:
    from db_conexionNew import Conexion
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Enfermero"):
        super().__init__()
        
        self.nombre_usuario = nombre_usuario
        self.setWindowTitle(f"Sistema Veterinario Yuno - Hospitalización ({self.nombre_usuario})")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)

        if DB_AVAILABLE:
            self.conexion = Conexion()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES (Iguales a ADMIN_Agregar_medicina) ---
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel { 
                background-color: white; 
                border-top-left-radius: 30px; 
                border-bottom-left-radius: 30px; 
                margin: 20px 20px 20px 0px; 
            }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            
            /* Inputs y TextEdit */
            QLineEdit, QTextEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none; border-radius: 10px; 
                padding: 10px; font-size: 16px; color: #333;
            }
            QLineEdit:focus, QTextEdit:focus { background-color: rgba(241, 131, 227, 0.5); }
            
            /* Botones Menú Lateral */
            QPushButton.menu-btn { 
                text-align: left; padding-left: 20px; 
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; 
                color: white; font-family: 'Segoe UI', sans-serif; 
                font-weight: bold; font-size: 18px; 
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px; 
            }
            QPushButton.menu-btn:hover { 
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; 
            }
            QPushButton.sub-btn { 
                text-align: left; font-family: 'Segoe UI', sans-serif; font-size: 16px; 
                font-weight: normal; padding-left: 40px; border-radius: 10px; 
                color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05); 
                height: 35px; margin-bottom: 2px; margin-left: 10px; margin-right: 10px; border: none;
            }
            QPushButton.sub-btn:hover { 
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; 
            }
            
            /* Botón Logout / Volver */
            QPushButton.logout-btn { 
                text-align: center; border: 2px solid white; 
                border-radius: 15px; padding: 10px; margin-top: 20px; 
                font-size: 14px; color: white; font-weight: bold; 
                background-color: transparent; 
            }
            QPushButton.logout-btn:hover { background-color: rgba(255,255,255,0.2); }

            /* Tarjeta Derecha */
            QFrame#InfoBoard {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 12px;
            }
        """)

        # --- Sidebar ---
        self.setup_sidebar()

        # --- PANEL BLANCO ---
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # =========================================================================
    #  SETUP INTERFAZ
    # =========================================================================
    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        # LOGO
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_logo = os.path.join(parent_dir, "FILES", "logo_yuno.png")
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

        # Menús (Lógica de Enfermera)
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

        frame_options = QFrame()
        layout_options = QVBoxLayout(frame_options)
        layout_options.setContentsMargins(0, 0, 0, 10)
        layout_options.setSpacing(2)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.abrir_ventana(t, o))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(40, 40, 20, 40)

        # 1. Header
        header = QHBoxLayout()
        lbl_header = QLabel("Internar Paciente")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-size: 16px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #E0E0E0; color: #333; }
        """)
        btn_back.clicked.connect(self.regresar_menu)

        header.addWidget(lbl_header)
        header.addStretch()
        header.addWidget(btn_back)
        self.white_layout.addLayout(header)
        self.white_layout.addSpacing(30)

        # 2. Contenedor Dividido (Izquierda: Formulario, Derecha: Tarjeta)
        content_split = QHBoxLayout()
        content_split.setSpacing(40)

        # A. Izquierda (Búsqueda y Observaciones)
        self.setup_form_left(content_split)

        # B. Derecha (Tarjeta de Info e Icono)
        self.setup_info_right(content_split)

        self.white_layout.addLayout(content_split)
        self.white_layout.addStretch()

    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        vbox = QVBoxLayout(form_widget)
        vbox.setContentsMargins(0,0,0,0)
        vbox.setSpacing(15)

        # --- Sección Búsqueda ---
        lbl_search = QLabel("ID de la Consulta:")
        lbl_search.setStyleSheet("font-size: 16px; font-weight: 500; color: #444;")
        
        search_row = QHBoxLayout()
        self.inp_id_consulta = QLineEdit()
        self.inp_id_consulta.setPlaceholderText("Ej. 102")
        
        btn_buscar = QPushButton("Buscar")
        btn_buscar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_buscar.setFixedSize(100, 42)
        # Botón estilo Admin (Azulito)
        btn_buscar.setStyleSheet("""
            QPushButton { background-color: #7CEBFC; color: #444; border-radius: 10px; font-weight: bold; border: 1px solid #5CD0E3; }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_buscar.clicked.connect(self.buscar_datos_consulta)

        search_row.addWidget(self.inp_id_consulta)
        search_row.addWidget(btn_buscar)

        # --- Sección Observaciones ---
        lbl_obs = QLabel("Motivo / Observaciones:")
        lbl_obs.setStyleSheet("font-size: 16px; font-weight: 500; color: #444; margin-top: 10px;")
        
        self.inp_obs = QTextEdit()
        self.inp_obs.setPlaceholderText("Describa estado del paciente, medicación y razones de internamiento...")
        self.inp_obs.setMinimumHeight(200)

        vbox.addWidget(lbl_search)
        vbox.addLayout(search_row)
        vbox.addWidget(lbl_obs)
        vbox.addWidget(self.inp_obs)
        vbox.addStretch()

        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_right(self, parent_layout):
        board = QFrame()
        board.setObjectName("InfoBoard")
        board.setMaximumWidth(400)
        
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)

        # Header Board (AZUL)
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("""
            background-color: #7CEBFC; 
            border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: none;
        """)
        head_lay = QHBoxLayout(header)
        lbl_tit = QLabel("Detalles del Paciente")
        lbl_tit.setStyleSheet("color: #444; font-weight: bold; font-size: 16px; border: none; background: transparent;")
        head_lay.addWidget(lbl_tit, alignment=Qt.AlignmentFlag.AlignCenter)
        board_lay.addWidget(header)

        # Contenido
        content = QWidget()
        content.setStyleSheet("background: white; border: none; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;")
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(20, 30, 20, 30)
        content_lay.setSpacing(10)
        content_lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- ICONO HOSPITALIZACION.PNG (COLOREADO) ---
        self.lbl_pic = QLabel()
        self.lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_pic.setStyleSheet("background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        
        # Ruta del icono solicitado
        ruta_icon = os.path.join(current_dir, "icons", "hospitalizacion.png")
        
        if os.path.exists(ruta_icon):
            pixmap = QPixmap(ruta_icon)
            if not pixmap.isNull():
                scaled_size = 50
                final_pixmap = QPixmap(scaled_size, scaled_size)
                final_pixmap.fill(Qt.GlobalColor.transparent)
                
                painter = QPainter(final_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
                
                target_rect = QRect(0, 0, scaled_size, scaled_size)
                painter.drawPixmap(target_rect, pixmap)
                
                # Pintar de Azul (#7CEBFC)
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                painter.fillRect(target_rect, QColor("#7CEBFC")) 
                painter.end()
                
                self.lbl_pic.setPixmap(final_pixmap)
            else:
                self.lbl_pic.setText("🏥")
        else:
            self.lbl_pic.setText("🏥") # Fallback emoji

        content_lay.addWidget(self.lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- ETIQUETAS DE DATOS ---
        self.lbl_mascota = QLabel("Nombre Mascota")
        self.lbl_mascota.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_mascota.setWordWrap(True)
        self.lbl_mascota.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.lbl_consulta_info = QLabel("Consulta: -- | Consultorio: --")
        self.lbl_consulta_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_consulta_info.setStyleSheet("font-size: 16px; color: #555; margin-top: 5px;")

        self.lbl_veterinario = QLabel("Veterinario: --")
        self.lbl_veterinario.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_veterinario.setStyleSheet("font-size: 14px; font-weight: bold; color: #888; margin-top: 10px;")

        content_lay.addWidget(self.lbl_mascota)
        content_lay.addWidget(self.lbl_consulta_info)
        content_lay.addWidget(self.lbl_veterinario)
        content_lay.addStretch()

        # --- BOTÓN DE ACCIÓN (CONFIRMAR) ---
        btn_internar = QPushButton("Confirmar Internamiento")
        btn_internar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_internar.setFixedSize(250, 50)
        btn_internar.setStyleSheet("""
            QPushButton {
                background-color: #7CEBFC; 
                color: #444; 
                font-size: 18px; 
                font-weight: bold; 
                border-radius: 25px;
                border: 1px solid #5CD0E3;
            }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_internar.clicked.connect(self.internar_mascota)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_internar)
        btn_container.addStretch()
        
        content_lay.addLayout(btn_container)
        content_lay.addSpacing(10)

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    # =========================================================================
    #  LOGICA DE BASE DE DATOS
    # =========================================================================
    def buscar_datos_consulta(self):
        id_consulta_input = self.inp_id_consulta.text().strip()
        if not id_consulta_input:
            QMessageBox.warning(self, "Aviso", "Ingrese un ID de consulta.")
            return

        if not DB_AVAILABLE:
            QMessageBox.critical(self, "Error", "Sin conexión a BD.")
            return

        try:
            # 1. Obtener la Consulta
            consulta = self.conexion.consultar_registro('consulta', 'id_consulta', id_consulta_input)
            
            if consulta:
                consultorio = str(consulta[1])
                fk_vet = consulta[4]
                fk_mascota = consulta[5]

                nombre_vet = "Desc."
                if fk_vet:
                    vet_data = self.conexion.consultar_registro('usuario', 'id_usuario', fk_vet, columnas=['nombre', 'apellido'])
                    if vet_data:
                        nombre_vet = f"{vet_data[0]} {vet_data[1]}"

                # 3. Obtener NOMBRE de la Mascota
                nombre_mascota = "Desconocida"
                if fk_mascota:
                    mascota_data = self.conexion.consultar_registro('mascota', 'id_mascota', fk_mascota, columnas=['nombre'])
                    if mascota_data:
                        nombre_mascota = str(mascota_data[0])

                # Actualizar Tarjeta Derecha
                self.lbl_mascota.setText(nombre_mascota)
                self.lbl_consulta_info.setText(f"Consulta: {id_consulta_input} | Sala: {consultorio}")
                self.lbl_veterinario.setText(f"Vet: {nombre_vet}")
            else:
                QMessageBox.warning(self, "No encontrado", "No se encontró una consulta con ese ID.")
                self.limpiar_card()
                
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"Error al buscar consulta: {e}")

    def limpiar_card(self):
        self.lbl_mascota.setText("Nombre Mascota")
        self.lbl_consulta_info.setText("Consulta: -- | Consultorio: --")
        self.lbl_veterinario.setText("Veterinario: --")

    def internar_mascota(self):
        id_consulta = self.inp_id_consulta.text()
        obs = self.inp_obs.toPlainText()

        if not id_consulta or not obs:
            QMessageBox.warning(self, "Alerta", "Debe buscar una consulta y escribir observaciones.")
            return

        if self.lbl_mascota.text() == "Nombre Mascota":
             QMessageBox.warning(self, "Alerta", "Primero realice la búsqueda de la consulta.")
             return

        if not DB_AVAILABLE: return

        try:
            datos = (obs, int(id_consulta))
            columnas = ('observaciones', 'fk_consulta')
            self.conexion.insertar_datos('hospitalizacion', datos, columnas)
            
            QMessageBox.information(self, "Éxito", "Paciente internado correctamente.")
            
            # Reset
            self.inp_id_consulta.clear()
            self.inp_obs.clear()
            self.limpiar_card()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al internar: {e}")

    # --- NAVEGACIÓN ---
    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import EnfermeroMain
            self.menu = EnfermeroMain(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            QMessageBox.warning(self, "Error", "No se encuentra el menú de enfermera.")
        except Exception as e:
            self.close()

    def abrir_ventana(self, categoria, opcion):
        try:
            target_window = None
            if categoria == "Citas" and opcion == "Visualizar":
                from UI_Cita_Enfermera import MainWindow as Win
                target_window = Win(self.nombre_usuario) 
            elif categoria == "Mascotas" and opcion == "Visualizar":
                from UI_Revisar_Mascota_Enfermera import MainWindow as Win
                target_window = Win(self.nombre_usuario) 
            elif categoria == "Inventario":
                if opcion == "Farmacia":
                    from UI_Farmacia import MainWindow as Win
                    target_window = Win(self.nombre_usuario) 
            elif categoria == "Expediente" and opcion == "Diagnóstico":
                from UI_Diagnostico import MainWindow as Win
                target_window = Win(self.nombre_usuario) 

            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close() 
        except Exception as e:
            print(f"Error navegando: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("TEST USER")
    window.show()
    sys.exit(app.exec())