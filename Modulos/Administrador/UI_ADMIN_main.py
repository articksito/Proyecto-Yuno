import sys
import os

# --- CONFIGURACIÓN DE RUTAS PARA IMPORTACIONES ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QMessageBox,
                             QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QBrush, QPen

from db_connection import Conexion

# --- WIDGET PERSONALIZADO PARA LA GRÁFICA ---
class GraficaCitas(QWidget):
    def __init__(self, data_dict):
        super().__init__()
        self.data = self.procesar_datos(data_dict)
        
        # Colores actualizados
        self.colors = {
            "Confirmada": QColor("#26C6DA"),  # Cian
            "Completada": QColor("#AB47BC"),  # Violeta
            "Cancelada": QColor("#EC407A"),   # Rosa Fuerte
            "Pendiente": QColor("#FF80AB")    # Rosa Claro
        }
        self.setMinimumHeight(350)

    def procesar_datos(self, data_raw):
        """Une claves similares y limpia datos"""
        clean_data = {
            "Confirmada": 0,
            "Completada": 0,
            "Cancelada": 0,
            "Pendiente": 0
        }
        
        if not data_raw:
            return clean_data

        for estado, cantidad in data_raw.items():
            est_norm = str(estado).strip().capitalize()
            
            if "Completad" in est_norm:
                clean_data["Completada"] += cantidad
            elif "Confirmad" in est_norm:
                clean_data["Confirmada"] += cantidad
            elif "Cancelad" in est_norm:
                clean_data["Cancelada"] += cantidad
            elif "Pendiente" in est_norm:
                clean_data["Pendiente"] += cantidad
        
        return clean_data

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("transparent"))

        # Configuración
        margin_left = 60
        margin_bottom = 50
        margin_top = 40
        bar_width_ratio = 0.5
        
        w = self.width()
        h = self.height()
        draw_w = w - margin_left - 40
        draw_h = h - margin_bottom - margin_top

        max_val = max(self.data.values()) if self.data.values() else 1
        max_val = int(max_val * 1.2)
        if max_val == 0: max_val = 1

        # Ejes
        pen_axis = QPen(QColor("#888"), 2)
        painter.setPen(pen_axis)
        painter.drawLine(margin_left, margin_top, margin_left, h - margin_bottom)
        painter.drawLine(margin_left, h - margin_bottom, w - 20, h - margin_bottom)

        # Grid
        pen_grid = QPen(QColor("#DDD"), 1, Qt.PenStyle.DotLine)
        painter.setPen(pen_grid)
        steps = 5
        for i in range(steps + 1):
            val = i * (max_val / steps)
            y_pos = (h - margin_bottom) - (val / max_val) * draw_h
            painter.drawLine(margin_left, int(y_pos), w - 20, int(y_pos))

        # Barras
        categories = ["Confirmada", "Pendiente", "Completada", "Cancelada"]
        num_bars = len(categories)
        section_width = draw_w / num_bars
        bar_width = section_width * bar_width_ratio
        spacing = (section_width - bar_width) / 2

        font_val = QFont("Segoe UI", 11, QFont.Weight.Bold)
        font_lbl = QFont("Segoe UI", 10)

        for i, estado in enumerate(categories):
            valor = self.data.get(estado, 0)
            bar_h = (valor / max_val) * draw_h
            x = margin_left + (i * section_width) + spacing
            y = (h - margin_bottom) - bar_h
            rect = QRectF(x, y, bar_width, bar_h)
            
            color = self.colors.get(estado, QColor("#999"))
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 6, 6) 
            
            painter.setPen(QColor("#333"))
            painter.setFont(font_val)
            if valor > 0:
                painter.drawText(QRectF(x, y - 25, bar_width, 20), Qt.AlignmentFlag.AlignCenter, str(valor))
            
            painter.setPen(QColor("#555"))
            painter.setFont(font_lbl)
            painter.drawText(QRectF(x - 15, h - margin_bottom + 10, bar_width + 30, 20), 
                           Qt.AlignmentFlag.AlignCenter, estado)


class MainWindow(QMainWindow):
    def __init__(self, nombre="Administrador"):
        self.nombre = nombre
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Administrador")
        self.resize(1280, 720)

        # Conexión
        self.conexion = Conexion()
        if nombre == "Administrador" or nombre == "Admin":
             pass 
        
        self.stats_citas = self.obtener_stats_citas()

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
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
            QWidget#WhitePanel {
                background-color: white;
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                margin: 20px 20px 20px 0px; 
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
            }
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
            }
            QPushButton.sub-btn:hover {
                color: white;
                background-color: rgba(255, 255, 255, 0.3);
                font-weight: bold;
            }
        """)

        # --- 1. BARRA LATERAL ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Panel de Control")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        
        self.lbl_reloj_header = QLabel()
        self.lbl_reloj_header.setStyleSheet("font-size: 24px; color: #777; font-weight: 300;")
        header_layout.addWidget(self.lbl_reloj_header)
        
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # Contenido Central
        self.setup_central_board()
        self.white_layout.addStretch()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # --- LOGO ROBUSTO ---
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

        # --- MENU NUEVO ---
        
        # Cita
        self.setup_accordion_group("Cita", ["Visualizar"])
        
        # Consulta
        self.setup_accordion_group("Consulta", ["Visualizar"])
        
        # Mascota
        self.setup_accordion_group("Mascota", ["Visualizar"])
        
        # Cliente
        self.setup_accordion_group("Cliente", ["Visualizar"])
        
        # Hospitalizacion
        self.setup_accordion_group("Hospitalizacion", ["Visualizar"])
        
        # Medicamentos
        self.setup_accordion_group("Medicamentos", ["Visualizar", "Agregar"])
        
        # Usuarios
        self.setup_accordion_group("Usuarios", ["Agregar", "Modificar", "Visualizar"])
        
        # Especialidad
        self.setup_accordion_group("Especialidad", ["Agregar", "Modificar"])


        self.sidebar_layout.addStretch()

        # Botón Cerrar Sesión
        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("""
            QPushButton {
                text-align: center; border: 2px solid white; 
                border-radius: 15px; padding: 10px; margin-top: 20px;
                font-size: 14px; color: white; font-weight: bold;
                background-color: transparent;
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
        layout_options.setSpacing(5)
        
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
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def setup_central_board(self):
        board_container = QFrame()
        board_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 15px;
            }
        """)
        
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8));
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-bottom: none;
        """)
        header_layout = QVBoxLayout(header_frame)
        
        # Nombre del Admin
        lbl_welcome = QLabel(f"Bienvenido, {self.nombre}") # Usamos self.nombre que viene del login
        lbl_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_welcome.setStyleSheet("color: white; font-size: 24px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(lbl_welcome)

        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 15px; border-bottom-right-radius: 15px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(40, 30, 40, 40)
        
        content_layout.addStretch()

        lbl_chart_title = QLabel("Resumen de Citas")
        lbl_chart_title.setStyleSheet("font-size: 22px; color: #555; font-weight: bold; margin-bottom: 20px;")
        lbl_chart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.chart_widget = GraficaCitas(self.stats_citas)
        
        content_layout.addWidget(lbl_chart_title)
        content_layout.addWidget(self.chart_widget)
        
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)
        self.white_layout.addWidget(board_container)

    def obtener_stats_citas(self):
        """Consulta BD"""
        try:
            query = "SELECT estado, COUNT(*) FROM cita GROUP BY estado"
            self.conexion.cursor_uno.execute(query)
            resultados = self.conexion.cursor_uno.fetchall()
            stats = {row[0]: row[1] for row in resultados}
            defaults = ["Confirmada", "Completada", "Cancelada", "Pendiente"]
            for d in defaults:
                if d not in stats: stats[d] = 0
            return stats
        except Exception:
            return {"Confirmada": 0, "Completada": 0, "Cancelada": 0, "Pendiente": 0}

    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.lbl_reloj_header.setText(current_time)

    # ============================================================
    #        ENRUTADOR DE VENTANAS (NUEVO)
    # ============================================================
    def router_ventanas(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        try:
            # --- CITA ---
            if categoria == "Cita":
                if opcion == "Visualizar":
                    from UI_ADMIN_Revisar_cita import MainWindow as UI_Revisar_Cita
                    self.cita = UI_Revisar_Cita()
                    self.cita.show()
                    self.close()

            # --- CONSULTA ---
            elif categoria == "Consulta":
                if opcion == "Visualizar":
                    # self.abrir_visualizar_consulta()
                    pass

            # --- MASCOTA ---
            elif categoria == "Mascota":
                if opcion == "Visualizar":
                   from UI_ADMIN_Paciente import MainWindow as UI_ADMIN_Paciente
                   self.apaciente = UI_ADMIN_Paciente()
                   self.apaciente.show()
                   self.close()

            # --- CLIENTE ---
            elif categoria == "Cliente":
                if opcion == "Visualizar":
                    from UI_ADMIN_Modificar_cliente import MainWindow as UI_Modificar_cliente
                    self.cliente = UI_Modificar_cliente()
                    self.cliente.show()
                    self.close()

            # --- HOSPITALIZACION ---
            elif categoria == "Hospitalizacion":
                if opcion == "Visualizar":
                    # self.abrir_hospitalizacion()
                    pass

            # --- MEDICAMENTOS ---
            elif categoria == "Medicamentos":
                if opcion == "Visualizar":
                    pass # Seria lista de medicamentos
                elif opcion == "Agregar":
                    from UI_Agregar_Medicamento import MainWindow as AddMed
                    self.ventana = AddMed()
                    self.ventana.show()
                    self.close()

            # --- USUARIOS ---
            elif categoria == "Usuarios":
                if opcion == "Agregar":
                    # self.abrir_crear_usuario()
                    pass
                elif opcion == "Modificar":
                    # self.abrir_modificar_usuario()
                    pass
                elif opcion == "Visualizar":
                    # self.abrir_consultar_usuario()
                    pass

            # --- ESPECIALIDAD ---
            elif categoria == "Especialidad":
                if opcion == "Agregar":
                    # self.abrir_agregar_especialidad()
                    pass
                elif opcion == "Modificar":
                    # self.abrir_modificar_especialidad()
                    pass

        except ImportError as e:
            QMessageBox.warning(self, "Error", f"No se encontró la ventana: {e.name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())