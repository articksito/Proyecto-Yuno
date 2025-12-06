import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPixmap, QIntValidator, QDoubleValidator, QPainter, QColor

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
        def insertar_datos(self, *args): return 999

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.ventana = None
        
        try:
            self.conexion1 = Conexion()
        except:
            print("Error conectando a BD")

        self.setWindowTitle(f"Sistema Veterinario Yuno - Registrar Mascota ({self.nombre_usuario})")
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
            
            /* Inputs y ComboBox (Estilo Rosa Translúcido) */
            QLineEdit, QComboBox {
                background-color: rgba(241, 131, 227, 0.35); 
                border: none; border-radius: 10px; padding: 5px 15px; 
                font-size: 16px; color: #333; height: 40px;
            }
            QLineEdit:focus, QComboBox:focus { background-color: rgba(241, 131, 227, 0.5); }
            QComboBox::drop-down { border: 0px; }

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

        # 1. Barra Lateral
        self.setup_sidebar()
        
        # 2. Panel Principal
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- PANEL PRINCIPAL ---
    # ==========================================
    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # 1. Header
        header = QHBoxLayout()
        lbl_header = QLabel("Registrar Nueva Mascota")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        header.addWidget(lbl_header)
        header.addStretch()
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

        # 3. Botón Guardar Inferior
        self.setup_save_button()

    # ==========================================
    # --- IZQUIERDA: FORMULARIO ---
    # ==========================================
    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)
        
        lbl_style = "font-size: 16px; font-weight: 500; color: #444;"
        
        # Campos
        self.inp_nom = QLineEdit()
        self.inp_nom.setPlaceholderText("Nombre de la mascota")
        
        self.inp_eda = QLineEdit()
        self.inp_eda.setPlaceholderText("Ej: 4")
        self.inp_eda.setValidator(QIntValidator())
        
        self.inp_pes = QLineEdit()
        self.inp_pes.setPlaceholderText("Kg")
        self.inp_pes.setValidator(QDoubleValidator())
        
        self.inp_esp = QComboBox()
        self.inp_esp.addItems(["Perro", "Gato", "Ave", "Roedor", "Reptil", "Otro"])
        
        self.inp_raz = QLineEdit()
        self.inp_raz.setPlaceholderText("Raza o Cruza")
        
        self.inp_cli = QLineEdit()
        self.inp_cli.setPlaceholderText("ID del Cliente (Dueño)")
        self.inp_cli.setValidator(QIntValidator())

        # Conexiones Preview
        for x in [self.inp_nom, self.inp_eda, self.inp_pes, self.inp_raz, self.inp_cli]: 
            x.textChanged.connect(self.update_preview)
        self.inp_esp.currentTextChanged.connect(self.update_preview)

        # Agregar al Grid
        self.add_row(grid, 0, "Nombre:", self.inp_nom, lbl_style)
        self.add_row(grid, 1, "Edad (Años):", self.inp_eda, lbl_style)
        self.add_row(grid, 2, "Peso (Kg):", self.inp_pes, lbl_style)
        self.add_row(grid, 3, "Especie:", self.inp_esp, lbl_style)
        self.add_row(grid, 4, "Raza:", self.inp_raz, lbl_style)
        self.add_row(grid, 5, "ID Dueño:", self.inp_cli, lbl_style)
        
        grid.setRowStretch(6, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def add_row(self, grid, row, text, widget, style):
        lbl = QLabel(text)
        lbl.setStyleSheet(style)
        grid.addWidget(lbl, row, 0)
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
        lbl_tit = QLabel("Vista Previa")
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

        # --- ICONO PETS.PNG ---
        self.lbl_pic = QLabel()
        self.lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_pic.setStyleSheet("background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        
        ruta_icon = os.path.join(current_dir, "icons", "pets.png")
        
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
                self.lbl_pic.setText("🐾")
        else:
            self.lbl_pic.setText("🐾")

        content_lay.addWidget(self.lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Labels Preview
        self.lbl_prev_nom = QLabel("Nombre Mascota")
        self.lbl_prev_nom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_nom.setWordWrap(True)
        self.lbl_prev_nom.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.lbl_prev_detalles = QLabel("Especie | Raza")
        self.lbl_prev_detalles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_detalles.setStyleSheet("font-size: 16px; color: #555; margin-top: 5px;")
        
        self.lbl_prev_dueno = QLabel("Dueño ID: --")
        self.lbl_prev_dueno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prev_dueno.setStyleSheet("font-size: 14px; font-weight: bold; color: #888; margin-top: 10px;")

        content_lay.addWidget(self.lbl_prev_nom)
        content_lay.addWidget(self.lbl_prev_detalles)
        content_lay.addWidget(self.lbl_prev_dueno)
        content_lay.addStretch()

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    # ==========================================
    # --- LOGICA Y BOTON ---
    # ==========================================
    def setup_save_button(self):
        btn = QPushButton("Registrar Mascota")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(250, 55)
        btn.setStyleSheet("""
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
        btn.clicked.connect(self.guardar_datos)
        
        l = QHBoxLayout()
        l.addStretch()
        l.addWidget(btn)
        l.addStretch()
        self.white_layout.addLayout(l)

    def update_preview(self):
        nom = self.inp_nom.text()
        esp = self.inp_esp.currentText()
        raz = self.inp_raz.text()
        eda = self.inp_eda.text()
        cli = self.inp_cli.text()

        self.lbl_prev_nom.setText(nom if nom else "Nombre Mascota")
        
        detalles = f"{esp}"
        if raz: detalles += f" - {raz}"
        if eda: detalles += f" | {eda} años"
        self.lbl_prev_detalles.setText(detalles)
        
        self.lbl_prev_dueno.setText(f"Dueño ID: {cli}" if cli else "Dueño ID: --")

    def guardar_datos(self):
        nom = self.inp_nom.text().strip()
        cli = self.inp_cli.text().strip()
        
        if not nom or not cli:
            QMessageBox.warning(self, "Aviso", "El Nombre y el ID del Dueño son obligatorios.")
            return
        
        try:
            # Datos: nombre, edad, peso, especie, raza, fk_cliente
            eda = int(self.inp_eda.text()) if self.inp_eda.text() else 0
            pes = float(self.inp_pes.text()) if self.inp_pes.text() else 0.0
            esp = self.inp_esp.currentText()
            raz = self.inp_raz.text().strip()
            fk_cli = int(cli)

            datos = (nom, eda, pes, esp, raz, fk_cli)
            campos = ('nombre', 'edad', 'peso', 'especie', 'raza', 'fk_cliente')
            
            nid = self.conexion1.insertar_datos('mascota', datos, campos)
            
            if nid: 
                QMessageBox.information(self, "Éxito", f"Mascota registrada correctamente.\nID Mascota: {nid}")
                self.limpiar()
            else: 
                QMessageBox.warning(self, "Error", "No se pudo insertar en la base de datos.")
        
        except ValueError:
             QMessageBox.warning(self, "Error de Datos", "Revise que Edad, Peso e ID Dueño sean números válidos.")
        except Exception as e: 
            QMessageBox.critical(self, "Error BD", str(e))

    def limpiar(self):
        self.inp_nom.clear()
        self.inp_eda.clear()
        self.inp_pes.clear()
        self.inp_raz.clear()
        self.inp_cli.clear()
        self.inp_esp.setCurrentIndex(0)
        self.update_preview()

    # ==========================================
    # --- NAVEGACION SIMPLIFICADA ---
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
        self.setup_accordion_group("Citas", ["Agendar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Mascotas", ["Registrar", "Visualizar", "Modificar"])
        self.setup_accordion_group("Clientes", ["Registrar", "Visualizar", "Modificar"])
        
        self.sidebar_layout.addStretch()
        
        # Botón Volver
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setStyleSheet("""
            QPushButton {
                border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 10px;
                color: white; font-weight: bold; background-color: transparent; font-size: 14px;
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
        layout.setSpacing(2)
        
        for opt in options:
            btn = QPushButton(opt)
            btn.setProperty("class", "sub-btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, c=title, o=opt: self.abrir_ventana(c, o))
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
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al volver: {e}")

    def abrir_ventana(self, categoria, opcion):
        if categoria == "Mascotas" and opcion == "Registrar": return 

        try:
            target_window = None
            
            if categoria == "Citas":
                if opcion == "Agendar":
                    from UI_REP_Crear_cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_REP_Revisar_Cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
            
            elif categoria == "Mascotas":
                if opcion == "Visualizar":
                    from UI_Revisar_Mascota import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_Mascota import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
            
            elif categoria == "Clientes":
                if opcion == "Registrar":
                    from UI_REP_Registra_cliente import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    from UI_Revisar_cliente import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cliente import MainWindow as Win
                    target_window = Win(self.nombre_usuario)

            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close()

        except ImportError as e:
             QMessageBox.warning(self, "Error", f"Falta archivo: {e}")
        except Exception as e:
             QMessageBox.critical(self, "Error", f"Error al abrir: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())