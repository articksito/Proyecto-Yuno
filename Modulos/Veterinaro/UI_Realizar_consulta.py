import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QComboBox, QTextEdit, QMessageBox)
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
except ImportError:
    class Conexion:
        def insertar_datos(self, *args): return 101

class VentanaConsulta(QMainWindow):
    def __init__(self, nombre_usuario="Veterinario"):
        super().__init__()
        
        self.nombre_usuario = nombre_usuario
        self.ventana = None
        
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error BD: {e}")

        self.setWindowTitle(f"Sistema Veterinario Yuno - Nueva Consulta ({self.nombre_usuario})")
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
            
            /* Inputs y TextEdit (Estilo Rosa Translúcido) */
            QLineEdit, QComboBox, QTextEdit {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none; border-radius: 10px; 
                padding: 5px 15px; font-size: 16px; color: #333;
            }
            QLineEdit, QComboBox { height: 40px; }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus { 
                background-color: rgba(241, 131, 227, 0.5); 
            }
            QComboBox::drop-down { border: 0px; }
            
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
        lbl_header = QLabel("Realizar Consulta")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        # Botón Volver (Estilo simple en header)
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

        self.setup_form_left(content_split)
        self.setup_info_right(content_split)

        self.white_layout.addLayout(content_split)
        self.white_layout.addStretch(1)

    # ==========================================
    # --- IZQUIERDA: FORMULARIO ---
    # ==========================================
    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        # Usamos QVBoxLayout principal para poner el Grid arriba y el TextEdit abajo
        main_vbox = QVBoxLayout(form_widget)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(15)

        # Grid para datos cortos
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0,0,0,0)

        style_lbl = "font-size: 16px; font-weight: 500; color: #444;"

        # Campos
        self.inp_vet = QLineEdit()
        self.inp_vet.setPlaceholderText("ID Médico")
        self.inp_vet.setValidator(QIntValidator())

        self.inp_mascota = QLineEdit()
        self.inp_mascota.setPlaceholderText("ID Paciente")
        self.inp_mascota.setValidator(QIntValidator())

        self.inp_cons = QComboBox()
        self.inp_cons.addItems(["Sala 1", "Sala 2", "Quirófano", "Triaje"])
        self.inp_cons.setEditable(True)

        self.inp_pago = QComboBox()
        self.inp_pago.addItems(["Efectivo", "Tarjeta", "Transferencia", "Seguro"])

        self.inp_cita = QLineEdit()
        self.inp_cita.setPlaceholderText("Opcional")
        self.inp_cita.setValidator(QIntValidator())

        # Conexiones Preview
        self.inp_vet.textChanged.connect(self.update_preview)
        self.inp_mascota.textChanged.connect(self.update_preview)
        self.inp_cons.currentTextChanged.connect(self.update_preview)
        self.inp_pago.currentTextChanged.connect(self.update_preview)

        # Agregar al Grid
        self.add_row(grid, 0, "ID Veterinario:", self.inp_vet, style_lbl)
        self.add_row(grid, 1, "ID Mascota:", self.inp_mascota, style_lbl)
        self.add_row(grid, 2, "Consultorio:", self.inp_cons, style_lbl)
        self.add_row(grid, 3, "Método Pago:", self.inp_pago, style_lbl)
        self.add_row(grid, 4, "ID Cita:", self.inp_cita, style_lbl)

        main_vbox.addWidget(grid_widget)

        # Motivo (TextEdit grande abajo)
        lbl_motivo = QLabel("Motivo / Diagnóstico:")
        lbl_motivo.setStyleSheet(style_lbl)
        self.txt_motivo = QTextEdit()
        self.txt_motivo.setPlaceholderText("Detalles de la consulta...")
        self.txt_motivo.setMinimumHeight(120)
        
        main_vbox.addWidget(lbl_motivo)
        main_vbox.addWidget(self.txt_motivo)

        parent_layout.addWidget(form_widget, stretch=3)

    def add_row(self, grid, row, text, widget, style):
        l = QLabel(text); l.setStyleSheet(style)
        grid.addWidget(l, row, 0)
        grid.addWidget(widget, row, 1)

    # ==========================================
    # --- DERECHA: TARJETA INFO ---
    # ==========================================
    def setup_info_right(self, parent_layout):
        board = QFrame()
        board.setObjectName("InfoBoard")
        board.setMaximumWidth(400)
        
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)

        # Header (Azul)
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("""
            background-color: #7CEBFC; 
            border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: none;
        """)
        head_lay = QHBoxLayout(header)
        lbl_tit = QLabel("Resumen Consulta")
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

        # --- ICONO CONSULTA.PNG ---
        self.lbl_pic = QLabel()
        self.lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_pic.setStyleSheet("background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        
        ruta_icon = os.path.join(current_dir, "icons", "consulta.png")
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
                
                # Pintar Azul
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                painter.fillRect(target_rect, QColor("#7CEBFC")) 
                painter.end()
                
                self.lbl_pic.setPixmap(final_pixmap)
            else:
                self.lbl_pic.setText("🩺")
        else:
            self.lbl_pic.setText("🩺")

        content_lay.addWidget(self.lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Etiquetas Preview
        self.prev_ids = QLabel("Pac: -- | Vet: --")
        self.prev_ids.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_ids.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.prev_cons = QLabel("Ubicación: --")
        self.prev_cons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_cons.setStyleSheet("font-size: 16px; color: #555; margin-top: 5px;")
        
        self.prev_pago = QLabel("Pago: --")
        self.prev_pago.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_pago.setStyleSheet("font-size: 14px; font-weight: bold; color: #888; margin-top: 10px;")

        content_lay.addWidget(self.prev_ids)
        content_lay.addWidget(self.prev_cons)
        content_lay.addWidget(self.prev_pago)
        content_lay.addStretch()

        # Botón Guardar (Dentro de la tarjeta)
        btn_save = QPushButton("Guardar Consulta")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedSize(250, 55)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #7CEBFC; 
                color: #444; 
                font-size: 20px; 
                font-weight: bold; 
                border-radius: 27px;
                border: 1px solid #5CD0E3;
            }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_save.clicked.connect(self.guardar_datos)
        
        btn_cont = QHBoxLayout()
        btn_cont.addStretch()
        btn_cont.addWidget(btn_save)
        btn_cont.addStretch()

        content_lay.addLayout(btn_cont)
        content_lay.addSpacing(10)

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    # ==========================================
    # --- LOGICA ---
    # ==========================================
    def update_preview(self):
        vet = self.inp_vet.text()
        pac = self.inp_mascota.text()
        cons = self.inp_cons.currentText()
        pago = self.inp_pago.currentText()
        
        self.prev_ids.setText(f"Pac: {pac if pac else '--'} | Vet: {vet if vet else '--'}")
        self.prev_cons.setText(f"Ubicación: {cons}")
        self.prev_pago.setText(f"Pago: {pago}")

    def guardar_datos(self):
        vet = self.inp_vet.text().strip()
        pac = self.inp_mascota.text().strip()
        cons = self.inp_cons.currentText()
        motivo = self.txt_motivo.toPlainText().strip()
        pago = self.inp_pago.currentText()
        cita = self.inp_cita.text().strip()

        if not vet or not pac or not motivo:
            QMessageBox.warning(self, "Aviso", "ID Veterinario, Mascota y Motivo son obligatorios.")
            return

        try:
            fk_vet = int(vet)
            fk_mas = int(pac)
            fk_cita = int(cita) if cita else None
            
            campos = ['consultorio', 'motivo', 'metodo_pago', 'fk_veterinario', 'fk_mascota']
            datos = [cons, motivo, pago, fk_vet, fk_mas]
            
            if fk_cita is not None:
                campos.append('fk_cita')
                datos.append(fk_cita)
            
            # Usando insertar_datos que devuelve ID
            nuevo_id = self.conexion.insertar_datos('consulta', tuple(datos), tuple(campos))
            
            if nuevo_id:
                QMessageBox.information(self, "Éxito", f"Consulta generada correctamente.\nID Consulta: {nuevo_id}")
                self.limpiar()
            else:
                QMessageBox.warning(self, "Error", "No se pudo generar el registro (ID devuelto nulo).")
                
        except ValueError:
            QMessageBox.warning(self, "Error", "Los IDs deben ser números enteros.")
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"Error al guardar:\n{e}")

    def limpiar(self):
        self.inp_vet.clear()
        self.inp_mascota.clear()
        self.inp_cita.clear()
        self.txt_motivo.clear()
        self.inp_cons.setCurrentIndex(0)
        self.inp_pago.setCurrentIndex(0)
        self.update_preview()

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

        # Menús (Veterinario)
        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro"])
        self.setup_accordion_group("Extra", ["Visualizar mascotas", "Visualizar medicamento", "Agregar notas para internar"])

        self.sidebar_layout.addStretch()

        # Botón Volver
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

    def volver_al_menu(self):
        try:
            from UI_Veterinario import VeterinarioMenu 
            self.menu = VeterinarioMenu(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            self.close()

    def router_ventanas(self, categoria, opcion):
        # Evitar reabrir actual
        if categoria == "Consultas" and opcion == "Crear Consulta": return

        try:
            target_window = None

            if categoria == "Consultas":
                if opcion == "Ver Registro":
                    from UI_Revisar_consulta import VentanaRevisarConsulta as Win
                    target_window = Win(self.nombre_usuario)

            elif categoria == "Recetas":
                if opcion == "Crear Receta":
                    from UI_Registrar_receta import VentanaReceta as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Ver Registro":
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
                    QMessageBox.information(self, "Proximamente", "Modulo en construcción")

            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close()

        except ImportError as e:
            QMessageBox.warning(self, "Error", f"No se encuentra el archivo: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error navegando: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaConsulta("TestVet")
    window.show()
    sys.exit(app.exec())