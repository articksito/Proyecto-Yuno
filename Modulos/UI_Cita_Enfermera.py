import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# Intentamos importar la conexión, si falla no crashea la UI visualmente
try:
    from db_connection import Conexion
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Veterinario Yuno - Revisar Cita (Enfermería)")
        self.resize(1280, 720)
        
        # Inicializar conexión si existe
        if DB_AVAILABLE:
            self.conexion1 = Conexion()

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
            /* Estilo Botones Menú Principal */
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
            /* Estilo Sub-botones */
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

        # --- 1. BARRA LATERAL (Adaptada a Enfermería) ---
        self.setup_sidebar()

        # --- 2. PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header con Botón "X" de regreso
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Revisar Cita")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_close_view = QPushButton("✕")
        btn_close_view.setFixedSize(40, 40)
        btn_close_view.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close_view.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0; border-radius: 20px; font-size: 20px; color: #666; border: none;
            }
            QPushButton:hover { background-color: #ffcccc; color: #cc0000; }
        """)
        # CONEXIÓN IMPORTANTE: Regresar al menú en lugar de cerrar app
        btn_close_view.clicked.connect(self.regresar_menu)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close_view)

        self.white_layout.addLayout(header_layout)
        self.white_layout.addStretch(1)

        # Barra de Búsqueda
        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        # Contenedor Horizontal para Datos + Panel Info
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        # A. Formulario Izquierda
        self.setup_details_form(content_layout)

        # B. Panel Motivo Derecha
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addStretch(2)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        # --- LOGO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ruta_logo = "logo.png"  # Ajusta ruta si es necesario (ej: Modulos/FILES/logo.png)
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")

        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)
        
        # --- MENÚ DE ENFERMERÍA (Coincide con tu Menu Principal) ---
        self.setup_accordion_group("Citas", ["Visualizar"])
        self.setup_accordion_group("Mascotas", ["Visualizar"])
        self.setup_accordion_group("Inventario", ["Farmacia", "Hospitalización"])
        self.setup_accordion_group("Expediente", ["Diagnóstico"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Volver al Menú")
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
        layout_options.setSpacing(5)
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            # Si quisieras navegar desde aquí, conectas self.regresar_menu o abres otra
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_search = QLabel("ID Cita:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Ingresa el ID...")
        self.inp_search.setFixedWidth(300)
        self.inp_search.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd; border-radius: 10px; padding: 8px 15px;
                font-size: 16px; color: #333; background-color: #F9F9F9;
            }
        """)
        
        btn_search = QPushButton("Buscar")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setFixedSize(120, 40)
        btn_search.setStyleSheet("""
            QPushButton {
                background-color: #7CEBFC; color: #333; font-weight: bold; font-size: 16px;
                border-radius: 10px; border: 1px solid #5CD0E3;
            }
            QPushButton:hover { background-color: #5CD0E3; }
        """)
        btn_search.clicked.connect(self.buscar_cita)
        
        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.inp_search)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        
        self.white_layout.addWidget(search_container)

    def setup_details_form(self, parent_layout):
        form_widget = QWidget()
        grid_layout = QGridLayout(form_widget)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        readonly_style = """
            QLineEdit {
                background-color: #F0F0F0; border: 1px solid #DDD; border-radius: 10px;
                padding: 5px 15px; font-size: 18px; color: #555; height: 45px;
            }
        """
        label_style = "font-size: 20px; color: black; font-weight: 400;"

        def add_row(row, label_text, attr_name):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            inp = QLineEdit()
            inp.setReadOnly(True)
            inp.setText("---")
            inp.setStyleSheet(readonly_style)
            setattr(self, attr_name, inp)
            grid_layout.addWidget(lbl, row, 0)
            grid_layout.addWidget(inp, row, 1)

        add_row(0, "Fecha:", "inp_fecha")
        add_row(1, "Hora:", "inp_hora")
        add_row(2, "Estado:", "inp_estado")
        add_row(3, "Mascota:", "inp_mascota")
        add_row(4, "Cliente:", "inp_cliente")
        add_row(5, "Veterinario:", "inp_vet")

        grid_layout.setRowStretch(6, 1)
        parent_layout.addWidget(form_widget, stretch=2)

    def setup_info_board(self, parent_layout):
        board_container = QFrame()
        board_container.setFixedWidth(350)
        board_container.setStyleSheet("QFrame { background-color: white; border: 1px solid #DDD; border-radius: 10px; }")
        
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7CEBFC, stop:1 rgba(252, 124, 226, 0.8));
            border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom: none;
        """)
        header_layout = QVBoxLayout(header_frame)
        lbl_info_title = QLabel("Motivo de la Cita")
        lbl_info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info_title.setStyleSheet("color: white; font-size: 20px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(lbl_info_title)

        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        self.lbl_motivo_text = QLabel("Ingrese un ID para ver los detalles...")
        self.lbl_motivo_text.setWordWrap(True)
        self.lbl_motivo_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.lbl_motivo_text.setStyleSheet("color: #555; font-size: 18px; border: none; line-height: 1.5;")
        
        content_layout.addWidget(self.lbl_motivo_text)
        content_layout.addStretch()
        
        board_layout.addWidget(header_frame)
        board_layout.addWidget(content_frame)

        parent_layout.addWidget(board_container, stretch=1)

    def buscar_cita(self):
        id_cita = self.inp_search.text().strip()
        
        if not id_cita:
            QMessageBox.warning(self, "Aviso", "Ingresa un ID de cita.")
            return

        if not DB_AVAILABLE:
            QMessageBox.critical(self, "Error BD", "No se pudo conectar a la base de datos.")
            return

        print(f"Consultando cita ID: {id_cita}")
        try:
            # Columnas a consultar
            columnas = [
                "cita.fecha", "cita.hora", "cita.motivo", "cita.estado",
                "mascota.nombre", "cliente.nombre", "cliente.apellido",
                "usuario.nombre", "usuario.apellido"
            ]
            
            joins = """
                JOIN mascota ON cita.fk_mascota = mascota.id_mascota
                JOIN cliente ON mascota.fk_cliente = cliente.id_cliente
                JOIN veterinario ON cita.fk_veterinario = veterinario.id_veterinario
                JOIN usuario ON veterinario.fk_usuario = usuario.id_usuario
            """
            
            registro = self.conexion1.consultar_registro(
                tabla='cita', 
                id_columna='cita.id_cita', 
                id_valor=id_cita, 
                columnas=columnas,
                joins=joins
            )
            
            if registro:
                self.inp_fecha.setText(str(registro[0]))
                self.inp_hora.setText(str(registro[1]))
                self.lbl_motivo_text.setText(str(registro[2]))
                self.inp_estado.setText(str(registro[3]))
                
                self.inp_mascota.setText(str(registro[4]))
                self.inp_cliente.setText(f"{registro[5]} {registro[6]}")
                
                nombre_vet = str(registro[7])
                if len(registro) > 8:
                    nombre_vet += f" {registro[8]}"
                self.inp_vet.setText(f"Dr. {nombre_vet}")
                
                QMessageBox.information(self, "Encontrado", "Cita cargada exitosamente.")
            else:
                self.limpiar_datos()
                QMessageBox.warning(self, "No encontrado", "No existe cita con ese ID.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar: {e}")

    def limpiar_datos(self):
        self.inp_fecha.setText("---")
        self.inp_hora.setText("---")
        self.inp_estado.setText("---")
        self.inp_mascota.setText("---")
        self.inp_cliente.setText("---")
        self.inp_vet.setText("---")
        self.lbl_motivo_text.setText("---")

    # --- FUNCIÓN CLAVE PARA VOLVER AL MENÚ ---
    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import MainWindow as MenuEnfermera
            self.menu = MenuEnfermera()
            self.menu.show()
            self.close()
        except ImportError:
            QMessageBox.warning(self, "Error", "No se encuentra el archivo del Menú Enfermera.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())