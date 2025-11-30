import sys
import os

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QComboBox, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor

# Importar conexión
from db_connection import Conexion

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Admin"):
        super().__init__()
        
        self.nombre_usuario = nombre_usuario
        
        try:
            self.conexion1 = Conexion()
        except Exception as e:
            print(f"Error BD: {e}")

        self.setWindowTitle("Sistema Veterinario Yuno - Agregar Medicamento")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal (Horizontal)
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
            
            /* --- BOTONES DEL SIDEBAR --- */
            QPushButton.menu-btn {
                text-align: left;
                padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1);
                height: 50px;
                margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid white;
                color: #FFF;
            }
            QPushButton.sub-btn {
                text-align: left;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: normal;
                padding-left: 40px;
                border-radius: 10px;
                color: #F0F0F0;
                background-color: rgba(0, 0, 0, 0.05);
                height: 35px;
                margin-bottom: 2px;
                margin-left: 10px;
                margin-right: 10px;
                border: none;
            }
            QPushButton.sub-btn:hover {
                color: white;
                background-color: rgba(255, 255, 255, 0.3);
                font-weight: bold;
            }
            
            /* Botón Logout */
            QPushButton.logout-btn {
                text-align: center; border: 2px solid white; 
                border-radius: 15px; padding: 10px; margin-top: 20px;
                font-size: 14px; color: white; font-weight: bold;
                background-color: transparent;
            }
            QPushButton.logout-btn:hover { background-color: rgba(255, 255, 255, 0.2); }
            
            /* --- INPUTS Y COMBOBOX (ESTILO ROSA YUNO) --- */
            QLineEdit, QComboBox, QTextEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 16px;
                color: #333;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                background-color: rgba(241, 131, 227, 0.5); 
            }
            QComboBox::drop-down { border: 0px; }
            QComboBox { height: 40px; }
            QLineEdit { height: 40px; }
            
            /* --- PANEL DERECHO (VISTA PREVIA) --- */
            QFrame#InfoBoard {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 12px;
            }
        """)

        # --- 1. BARRA LATERAL ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO ---
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- SETUP SIDEBAR ---
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
        ruta_logo = os.path.normpath(ruta_logo)

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

        # --- MENÚS DESPLEGABLES ---
        self.setup_accordion_group("Cita", ["Visualizar"])
        self.setup_accordion_group("Consulta", ["Visualizar"])
        self.setup_accordion_group("Mascota", ["Visualizar", "Modificar"])
        self.setup_accordion_group("Cliente", ["Visualizar"])
        self.setup_accordion_group("Hospitalizacion", ["Visualizar"])
        self.setup_accordion_group("Medicamentos", ["Visualizar", "Agregar"])
        self.setup_accordion_group("Usuarios", ["Agregar", "Modificar", "Visualizar"])
        self.setup_accordion_group("Especialidad", ["Agregar", "Modificar"])

        self.sidebar_layout.addStretch()

        # Botón Cerrar Sesión
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
            # Conectar al navegador
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.navegar(cat, opt))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    # ==========================================
    # --- NAVEGACIÓN ---
    # ==========================================
    def navegar(self, categoria, opcion):
        print(f"Admin navegando a: {categoria} -> {opcion}")
        
        # Evitar recargar la misma ventana
        if categoria == "Medicamentos" and opcion == "Agregar":
             return

        try:
            if categoria == "Cita" and opcion == "Visualizar":
                from UI_ADMIN_Revisar_cita import MainWindow as UI_Revisar_Cita
                self.ventana = UI_Revisar_Cita(self.nombre_usuario)
                self.ventana.show()
                self.close()
            elif categoria == "Consulta" and opcion == "Visualizar":
                from UI_ADMIN_Revisar_consulta import VentanaRevisarConsulta
                self.ventana = VentanaRevisarConsulta(self.nombre_usuario)
                self.ventana.show()
                self.close()
            elif categoria == "Mascota":
                if opcion == "Visualizar":
                   from UI_ADMIN_Revisar_Paciente import MainWindow as UI_ADMIN_Paciente
                   self.ventana = UI_ADMIN_Paciente(self.nombre_usuario)
                   self.ventana.show()
                   self.close()
                elif opcion == "Modificar":
                   from UI_Admin_Modificar_Mascota import MainWindow as UI_Modificar_Mascota
                   self.ventana = UI_Modificar_Mascota(self.nombre_usuario)
                   self.ventana.show()
                   self.close()
            elif categoria == "Cliente" and opcion == "Visualizar":
                from UI_ADMIN_Visualizar_cliente import MainWindow as UI_Modificar_cliente
                self.ventana = UI_Modificar_cliente(self.nombre_usuario)
                self.ventana.show()
                self.close()
            elif categoria == "Hospitalizacion" and opcion == "Visualizar":
                from UI_ADMIN_RevisarHospitalizacion import VentanaRevisarHospitalizacion
                self.ventana = VentanaRevisarHospitalizacion(self.nombre_usuario)
                self.ventana.show()
                self.close()
            elif categoria == "Medicamentos" and opcion == "Visualizar":
                from UI_ADMIN_Revisar_medicina import VentanaRevisarMedicina
                self.ventana = VentanaRevisarMedicina(self.nombre_usuario)
                self.ventana.show()
                self.close()
            elif categoria == "Usuarios":
                if opcion == "Agregar":
                    from UI_ADMIN_Agregar_usuario import VentanaAgregarUsuario
                    self.ventana = VentanaAgregarUsuario(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_ADMIN_Modificar_usuario import VentanaModificarUsuario
                    self.ventana = VentanaModificarUsuario(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Visualizar":
                    from UI_ADMIN_Revisar_usuario import VentanaRevisarUsuario
                    self.ventana = VentanaRevisarUsuario(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
            elif categoria == "Especialidad":
                if opcion == "Agregar":
                    from UI_ADMIN_Agregar_Especialidad import VentanaAgregarEspecialidad
                    self.ventana = VentanaAgregarEspecialidad(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Modificar":
                    from UI_ADMIN_Modificar_especialidad import VentanaModificarEspecialidad
                    self.ventana = VentanaModificarEspecialidad(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

        except ImportError as e:
            QMessageBox.warning(self, "Error", f"Falta archivo: {e.name}")
        except Exception as e:
             QMessageBox.critical(self, "Error", f"Error al navegar: {e}")

    # ==========================================
    # --- PANEL CENTRAL (Agregar Medicina) ---
    # ==========================================

    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        # Margen aumentado a la izquierda para centrar mejor
        self.white_layout.setContentsMargins(40, 40, 20, 40)

        # 1. Header
        header = QHBoxLayout()
        lbl_header = QLabel("Agregar Medicamento")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton { background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-size: 16px; font-weight: bold; border: none; }
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

        # A. Izquierda: Formulario
        self.setup_form_left(content_split)

        # B. Derecha: Preview + Botón Guardar
        self.setup_info_right(content_split)

        self.white_layout.addLayout(content_split)
        self.white_layout.addStretch() # Empuja todo hacia arriba

    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        label_style = "font-size: 16px; font-weight: 500; color: #444;"

        # Campos
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setPlaceholderText("Ej: Amoxicilina")
        
        self.inp_tipo = QComboBox()
        self.inp_tipo.addItems(["Antibiótico", "Analgésico", "Antiinflamatorio", "Vacuna", "Desparasitante", "Otro"])
        
        self.inp_comp = QLineEdit()
        self.inp_comp.setPlaceholderText("Ej: 500mg")
        
        self.inp_dosis = QLineEdit()
        self.inp_dosis.setPlaceholderText("Ej: 10 mg/kg")
        
        self.inp_via = QComboBox()
        self.inp_via.addItems(["Oral", "Intravenosa", "Intramuscular", "Subcutánea", "Tópica"])

        # Conectar señales para Live Preview
        self.inp_nombre.textChanged.connect(self.update_preview)
        self.inp_tipo.currentTextChanged.connect(self.update_preview)
        self.inp_comp.textChanged.connect(self.update_preview)
        self.inp_dosis.textChanged.connect(self.update_preview)
        self.inp_via.currentTextChanged.connect(self.update_preview)

        # Agregar al Grid
        grid.addWidget(QLabel("Nombre:", styleSheet=label_style), 0, 0)
        grid.addWidget(self.inp_nombre, 0, 1)

        grid.addWidget(QLabel("Tipo:", styleSheet=label_style), 1, 0)
        grid.addWidget(self.inp_tipo, 1, 1)

        grid.addWidget(QLabel("Composición:", styleSheet=label_style), 2, 0)
        grid.addWidget(self.inp_comp, 2, 1)

        grid.addWidget(QLabel("Dosis Rec.:", styleSheet=label_style), 3, 0)
        grid.addWidget(self.inp_dosis, 3, 1)

        grid.addWidget(QLabel("Vía Admin.:", styleSheet=label_style), 4, 0)
        grid.addWidget(self.inp_via, 4, 1)

        # Empujar hacia arriba
        grid.setRowStretch(5, 1)

        parent_layout.addWidget(form_widget, stretch=3)

    def setup_info_right(self, parent_layout):
        board = QFrame()
        board.setObjectName("InfoBoard")
        board.setMaximumWidth(400)
        
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)
        
        # Estilo borde
        board.setStyleSheet("""
            QFrame#InfoBoard {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 12px;
            }
        """)

        # Header Board (AZUL SOLIDO)
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("""
            background-color: #7CEBFC; 
            border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: none;
        """)
        head_lay = QHBoxLayout(header)
        lbl_tit = QLabel("Vista Previa")
        # Color Gris Oscuro para texto sobre azul claro
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

        # --- ICONO MEDICINE.PNG ---
        self.lbl_pic = QLabel()
        self.lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_pic.setStyleSheet("background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        
        ruta_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "medicine.png")
        
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
                
                # Pintar de Azul
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                painter.fillRect(target_rect, QColor("#7CEBFC")) 
                painter.end()
                
                self.lbl_pic.setPixmap(final_pixmap)
            else:
                self.lbl_pic.setText("💊")
        else:
            self.lbl_pic.setText("💊")

        content_lay.addWidget(self.lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Etiquetas Preview
        self.prev_nombre = QLabel("Nombre Medicina")
        self.prev_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_nombre.setWordWrap(True)
        self.prev_nombre.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.prev_detalles = QLabel("Tipo | Composición")
        self.prev_detalles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_detalles.setStyleSheet("font-size: 16px; color: #555; margin-top: 5px;")

        self.prev_uso = QLabel("Dosis -- | Vía --")
        self.prev_uso.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_uso.setStyleSheet("font-size: 14px; font-weight: bold; color: #888; margin-top: 10px;")

        content_lay.addWidget(self.prev_nombre)
        content_lay.addWidget(self.prev_detalles)
        content_lay.addWidget(self.prev_uso)
        content_lay.addStretch()

        # --- BOTÓN GUARDAR (Dentro de la tarjeta) ---
        btn_save = QPushButton("Registrar Medicamento")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedSize(250, 50)
        # Estilo Azul para coincidir con el tema
        btn_save.setStyleSheet("""
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
        btn_save.clicked.connect(self.guardar_datos)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_save)
        btn_container.addStretch()
        
        content_lay.addLayout(btn_container)
        content_lay.addSpacing(10)

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    # ==========================================
    # --- LÓGICA ---
    # ==========================================

    def update_preview(self):
        nombre = self.inp_nombre.text()
        tipo = self.inp_tipo.currentText()
        comp = self.inp_comp.text()
        dosis = self.inp_dosis.text()
        via = self.inp_via.currentText()

        if nombre:
            self.prev_nombre.setText(nombre)
        else:
            self.prev_nombre.setText("Nombre Medicina")
        
        self.prev_detalles.setText(f"{tipo} | {comp if comp else '--'}")
        self.prev_uso.setText(f"Dosis: {dosis if dosis else '--'} | Vía: {via}")

    def volver_al_menu(self):
        try:
            from UI_ADMIN_main import MainWindow as AdminMenu 
            self.menu = AdminMenu(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            self.close()

    def guardar_datos(self):
        # 1. Recolectar
        nombre = self.inp_nombre.text().strip()
        tipo = self.inp_tipo.currentText()
        composicion = self.inp_comp.text().strip()
        dosis_recomendada = self.inp_dosis.text().strip()
        via_administracion = self.inp_via.currentText()

        # 2. Validar
        if not nombre:
            QMessageBox.warning(self, "Campos Vacíos", "El nombre del medicamento es obligatorio.")
            return

        # 3. Insertar
        campos = ('nombre', 'tipo', 'composicion', 'dosis_recomendada', 'via_administracion')
        datos = (nombre, tipo, composicion, dosis_recomendada, via_administracion)
        tabla = 'medicamento'

        try:
            nuevo_id = self.conexion1.insertar_datos(tabla, datos, campos)
            
            if nuevo_id:
                QMessageBox.information(self, "Éxito", f"Medicamento registrado correctamente.\nID Generado: {nuevo_id}")
                # Limpiar
                self.inp_nombre.clear()
                self.inp_comp.clear()
                self.inp_dosis.clear()
                self.inp_tipo.setCurrentIndex(0)
                self.inp_via.setCurrentIndex(0)
            else:
                 QMessageBox.warning(self, "Error", "No se pudo obtener el ID del nuevo medicamento.")

        except Exception as e:
            QMessageBox.critical(self, "Error Base de Datos", f"Error al guardar:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())