import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QGridLayout, QDateEdit, QTimeEdit, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, QDate, QTime, QRect
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
    # Si falla, usamos una conexión dummy para que no se cierre la app
    print("¡Advertencia! No se encontró db_connection.py")
    class Conexion:
        def insertar_datos(self, *args): return 101

class MainWindow(QMainWindow):
    def __init__(self, nombre_usuario="Recepcionista"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.ventana = None
        try:
             self.conexion = Conexion()
        except:
             print("Error conectando a BD")

        self.setWindowTitle(f"Sistema Veterinario Yuno - Agendar Cita ({self.nombre_usuario})")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES UNIFICADOS ---
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
            
            /* --- INPUTS (Estilo Rosa Translúcido) --- */
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
            QComboBox::drop-down { border: 0px; }
            /* Ajustes para Date/Time Edit */
            QDateEdit::down-arrow, QTimeEdit::down-arrow {
                 image: none; border-width: 0px;
            }
            QDateEdit::drop-down, QTimeEdit::drop-down {
                 border-width: 0px;
            }

            /* --- BOTONES SIDEBAR --- */
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

        # 2. Panel Blanco Principal
        self.setup_white_panel()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # ==========================================
    # --- ESTRUCTURA DEL PANEL BLANCO ---
    # ==========================================
    def setup_white_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        # Márgenes para centrar el contenido
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # 1. Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Agendar Nueva Cita")
        lbl_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(30)

        # 2. Contenedor Dividido (Izquierda: Formulario, Derecha: Preview)
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # A. Formulario
        self.setup_form_left(content_layout)
        # B. Tarjeta de Información
        self.setup_info_right(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addStretch(1) 

        # 3. Botón de Acción Principal (Inferior)
        self.setup_save_button()

    # ==========================================
    # --- SECCIÓN IZQUIERDA: FORMULARIO ---
    # ==========================================
    def setup_form_left(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        style_lbl = "font-size: 16px; font-weight: 500; color: #444;"

        # Widgets
        self.inp_fecha = QDateEdit()
        self.inp_fecha.setCalendarPopup(True)
        self.inp_fecha.setDate(QDate.currentDate())
        
        self.inp_hora = QTimeEdit()
        self.inp_hora.setTime(QTime.currentTime())
        
        self.inp_motivo = QLineEdit()
        self.inp_motivo.setPlaceholderText("Ej: Vacunación anual")
        
        self.inp_mascota = QLineEdit()
        self.inp_mascota.setPlaceholderText("ID de la Mascota")
        self.inp_mascota.setValidator(QIntValidator())
        
        self.inp_vet = QLineEdit()
        self.inp_vet.setPlaceholderText("ID del Veterinario")
        self.inp_vet.setValidator(QIntValidator())
        
        self.inp_estado = QComboBox()
        self.inp_estado.addItems(["Pendiente", "Confirmada"])

        # Conexiones para Live Preview
        self.inp_fecha.dateChanged.connect(self.update_preview)
        self.inp_hora.timeChanged.connect(self.update_preview)
        self.inp_motivo.textChanged.connect(self.update_preview)
        self.inp_mascota.textChanged.connect(self.update_preview)
        self.inp_vet.textChanged.connect(self.update_preview)

        # Agregar al Grid
        self.add_row(grid, 0, "Fecha Cita:", self.inp_fecha, style_lbl)
        self.add_row(grid, 1, "Hora Cita:", self.inp_hora, style_lbl)
        self.add_row(grid, 2, "Motivo:", self.inp_motivo, style_lbl)
        self.add_row(grid, 3, "ID Mascota:", self.inp_mascota, style_lbl)
        self.add_row(grid, 4, "ID Veterinario:", self.inp_vet, style_lbl)
        self.add_row(grid, 5, "Estado Inicial:", self.inp_estado, style_lbl)

        grid.setRowStretch(6, 1)
        parent_layout.addWidget(form_widget, stretch=3)

    def add_row(self, grid, row, label_text, widget, style):
        lbl = QLabel(label_text)
        lbl.setStyleSheet(style)
        grid.addWidget(lbl, row, 0)
        grid.addWidget(widget, row, 1)

    # ==========================================
    # --- SECCIÓN DERECHA: TARJETA INFO ---
    # ==========================================
    def setup_info_right(self, parent_layout):
        board = QFrame()
        board.setObjectName("InfoBoard")
        board.setMaximumWidth(400)
        board_lay = QVBoxLayout(board)
        board_lay.setContentsMargins(0, 0, 0, 0)
        board_lay.setSpacing(0)

        # 1. Header Board (Azul Sólido)
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

        # 2. Contenido Board
        content = QWidget()
        content.setStyleSheet("background: white; border: none; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;")
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(20, 30, 20, 30)
        content_lay.setSpacing(10)
        content_lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- ICONO CITA.PNG (Coloreado) ---
        self.lbl_pic = QLabel()
        self.lbl_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_pic.setStyleSheet("background: #f0f0f0; border-radius: 40px; min-height: 80px; min-width: 80px;")
        
        ruta_icon = os.path.join(current_dir, "icons", "cita.png")
        
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
                self.lbl_pic.setText("📅")
        else:
            self.lbl_pic.setText("📅")

        content_lay.addWidget(self.lbl_pic, alignment=Qt.AlignmentFlag.AlignCenter)

        # Etiquetas Preview
        self.prev_fecha = QLabel("--/--/---- --:--")
        self.prev_fecha.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_fecha.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; margin-top: 10px;")
        
        self.prev_motivo = QLabel("Motivo: --")
        self.prev_motivo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_motivo.setWordWrap(True)
        self.prev_motivo.setStyleSheet("font-size: 16px; color: #555; margin-top: 5px; font-style: italic;")

        self.prev_ids = QLabel("ID Mascota: -- | ID Vet: --")
        self.prev_ids.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prev_ids.setStyleSheet("font-size: 14px; font-weight: bold; color: #888; margin-top: 15px;")

        content_lay.addWidget(self.prev_fecha)
        content_lay.addWidget(self.prev_motivo)
        content_lay.addWidget(self.prev_ids)
        content_lay.addStretch()

        board_lay.addWidget(content)
        parent_layout.addWidget(board, stretch=2)

    # ==========================================
    # --- BOTÓN PRINCIPAL Y LÓGICA ---
    # ==========================================
    def setup_save_button(self):
        btn = QPushButton("Confirmar Cita")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(250, 55)
        # Estilo Cian/Azul para acción principal
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
        btn.clicked.connect(self.guardar_cita)
        
        l = QHBoxLayout()
        l.addStretch()
        l.addWidget(btn)
        l.addStretch()
        self.white_layout.addLayout(l)

    def update_preview(self):
        fecha = self.inp_fecha.date().toString("dd/MM/yyyy")
        hora = self.inp_hora.time().toString("HH:mm")
        mot = self.inp_motivo.text()
        mas = self.inp_mascota.text()
        vet = self.inp_vet.text()
        
        self.prev_fecha.setText(f"{fecha} {hora}")
        self.prev_motivo.setText(f"{mot}" if mot else "Motivo: --")
        self.prev_ids.setText(f"Mascota: {mas if mas else '--'} | Vet: {vet if vet else '--'}")

    def guardar_cita(self):
        mot = self.inp_motivo.text().strip()
        mas = self.inp_mascota.text().strip()
        vet = self.inp_vet.text().strip()

        if not mot or not mas or not vet:
            return QMessageBox.warning(self, "Aviso", "Motivo, ID Mascota y ID Veterinario son obligatorios.")

        datos = (
            self.inp_fecha.date().toString("yyyy-MM-dd"),
            self.inp_hora.time().toString("HH:mm:ss"),
            self.inp_estado.currentText(),
            mot,
            int(mas),
            int(vet)
        )
        cols = ('fecha', 'hora', 'estado', 'motivo', 'fk_mascota', 'fk_veterinario')

        try:
            nid = self.conexion.insertar_datos('cita', datos, cols)
            if nid:
                QMessageBox.information(self, "Éxito", f"Cita agendada correctamente.\nID Cita: {nid}")
                self.limpiar()
            else:
                QMessageBox.warning(self, "Error", "No se pudo guardar la cita en la base de datos.")
        except Exception as e:
            QMessageBox.critical(self, "Error DB", str(e))

    def limpiar(self):
        self.inp_motivo.clear()
        self.inp_mascota.clear()
        self.inp_vet.clear()
        self.inp_fecha.setDate(QDate.currentDate())
        self.inp_hora.setTime(QTime.currentTime())
        self.inp_estado.setCurrentIndex(0)
        self.update_preview()

    # ==========================================
    # --- SIDEBAR & NAVEGACIÓN (Sin cambios mayores) ---
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
                lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
        else:
            lbl_logo.setText("YUNO VET"); lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 30px;")
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

    # ==========================================
    # --- NAVEGACIÓN (SIMPLIFICADA) ---
    # ==========================================

    def return_to_menu(self):
        """Regresa al menú principal de Recepción"""
        try:
            # Importación LOCAL para evitar choques
            from UI_REP_main import MainWindow as MenuPrincipal
            
            self.ventana = MenuPrincipal(self.nombre_usuario)
            self.ventana.show()
            self.close()
        except ImportError:
            QMessageBox.critical(self, "Error de Archivo", "No se encuentra el archivo 'UI_REP_main.py'.\nAsegúrate de que esté en la misma carpeta.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir el menú:\n{e}")

    def abrir_ventana(self, categoria, opcion):
        """Maneja la apertura de otras ventanas según el botón presionado"""
        
        # Ignorar si intentamos abrir la ventana actual
        if categoria == "Citas" and opcion == "Agendar":
            return

        try:
            target_window = None

            # --- SECCIÓN: CITAS ---
            if categoria == "Citas":
                if opcion == "Visualizar":
                    from UI_REP_Revisar_Cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_cita import MainWindow as Win
                    target_window = Win(self.nombre_usuario)

            # --- SECCIÓN: MASCOTAS ---
            elif categoria == "Mascotas":
                if opcion == "Registrar":
                    from UI_REP_Registrar_mascota import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Visualizar":
                    # Ojo: Verifica si el nombre de este archivo es correcto en tu carpeta
                    from UI_Revisar_Mascota import MainWindow as Win
                    target_window = Win(self.nombre_usuario)
                elif opcion == "Modificar":
                    from UI_REP_Modificar_Mascota import MainWindow as Win
                    target_window = Win(self.nombre_usuario)

            # --- SECCIÓN: CLIENTES ---
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

            # --- VALIDACIÓN FINAL ---
            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close()
            else:
                print(f"Ruta no programada: {categoria} -> {opcion}")

        except ImportError as e:
            # Este mensaje te dirá exactamente qué archivo falta
            QMessageBox.warning(self, "Falta Archivo", f"No se pudo encontrar el archivo para {categoria}/{opcion}.\n\nError: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Ocurrió un error al navegar:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())