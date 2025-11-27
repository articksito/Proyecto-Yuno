import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# Importar conexión
from db_connection import Conexion

class VentanaRevisarConsulta(QMainWindow):
    def __init__(self, nombre_usuario):
        super().__init__()
        
        # 1. Conexión a BD
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Sistema Veterinario Yuno - Historial Médico")
        self.resize(1280, 720)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS VISUALES ---
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC);
            }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel {
                background-color: white;
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                margin: 20px 20px 20px 0px; 
            }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            
            /* Botones Menú (Acordeón) */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px;
                color: white; font-family: 'Segoe UI', sans-serif; font-weight: bold; font-size: 18px;
                background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover {
                background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF;
            }
            /* Sub-botones */
            QPushButton.sub-btn {
                text-align: left; padding-left: 40px; border-radius: 10px;
                color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05);
                height: 35px; margin-bottom: 2px; margin-left: 10px; margin-right: 10px;
            }
            QPushButton.sub-btn:hover {
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold;
            }
            
            /* Inputs Solo Lectura */
            QLineEdit[readOnly="true"], QTextEdit[readOnly="true"] {
                background-color: #F0F0F0; border: 1px solid #DDD; border-radius: 10px;
                padding: 5px 15px; font-size: 16px; color: #555;
            }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

    # ============================================================
    #  BARRA LATERAL (SOLO VETERINARIO)
    # ============================================================
    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        # --- LOGO (LOGICA ROBUSTA AGREGADA) ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Lógica para encontrar la imagen subiendo niveles
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Sube a Modulos -> FILES -> logo_yuno.png
        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)

        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                lbl_logo.setText("YUNO VET\nCONSULTAS")
                lbl_logo.setStyleSheet("color: white; font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        else:
            # print(f"No se encontró el logo en: {ruta_logo}")
            lbl_logo.setText("YUNO VET\nCONSULTAS")
            lbl_logo.setStyleSheet("color: white; font-size: 28px; font-weight: bold; margin-bottom: 20px;")

        self.sidebar_layout.addWidget(lbl_logo)

        # --- MENÚS EXCLUSIVOS VETERINARIO ---
        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("""
            QPushButton { text-align: center; border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 20px; font-size: 14px; color: white; font-weight: bold; background-color: transparent; }
            QPushButton:hover { background-color: rgba(255,255,255,0.2); }
        """)
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)
        
        self.main_layout.addWidget(self.sidebar)

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
        if frame.isVisible(): frame.hide()
        else: frame.show()

    # ============================================================
    #  ENRUTADOR (Router) - SOLO LÓGICA VETERINARIO
    # ============================================================
    def router_ventanas(self, categoria, opcion):
        print(f"Navegando: {categoria} -> {opcion}")
        
        try:
            # --- CONSULTAS ---
            if categoria == "Consultas":
                if opcion == "Crear Consulta":
                    from UI_Realizar_consulta import VentanaConsulta 
                    self.v = VentanaConsulta(self.nombre_usuario)
                    self.v.show()
                    self.close()
                
                elif opcion == "Ver Registro":
                    # Ya estamos aquí
                    QMessageBox.information(self, "Navegación", "Ya estás en el Historial de Consultas.")

            elif categoria == "Recetas":
                if opcion == "Crear Receta":
                    from UI_Registrar_receta import VentanaReceta
                    self.v = VentanaReceta(self.nombre_usuario)
                    self.v.show()
                    self.close()
                    QMessageBox.information(self, "Navegación", "Ir a: Crear Receta")
                
                elif opcion == "Ver Registro":
                    from UI_Revisar_recetas import VentanaRevisarReceta
                    self.v = VentanaRevisarReceta(self.nombre_usuario)
                    self.v.show()
                    self.close()
                    QMessageBox.information(self, "Navegación", "Ir a: Historial Recetas")

        except ImportError as e:
             QMessageBox.warning(self, "Error", f"No se encontró el archivo: {e.name}")
        except Exception as e:
             QMessageBox.critical(self, "Error", f"Error al navegar: {e}")

    # ============================================================
    #  PANEL CENTRAL: BUSCADOR Y LECTURA DE DATOS
    # ============================================================
    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Historial de Consultas")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(40, 40)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("background-color: #f0f0f0; border-radius: 20px; font-size: 20px; color: #666; border: none;")
        btn_close.clicked.connect(self.volver_al_menu)
        
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close)
        self.white_layout.addLayout(header_layout)

        # Barra de Búsqueda
        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        # Contenedor de Datos
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        # Izquierda: Datos Técnicos
        self.setup_details_form(content_layout)

        # Derecha: Motivo (Texto Largo)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addStretch(2)

        self.main_layout.addWidget(self.white_panel)

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_search = QLabel("ID Consulta:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Ingrese ID...")
        self.inp_search.setFixedWidth(300)
        self.inp_search.setStyleSheet("border: 2px solid #ddd; border-radius: 10px; padding: 8px; font-size: 16px; background-color: white;")
        
        btn_search = QPushButton("Buscar")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setFixedSize(120, 40)
        btn_search.setStyleSheet("background-color: #7CEBFC; color: #333; font-weight: bold; border-radius: 10px; border: 1px solid #5CD0E3;")
        btn_search.clicked.connect(self.buscar_consulta)
        
        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.inp_search)
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        self.white_layout.addWidget(search_container)

    def setup_details_form(self, parent_layout):
        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(30)

        def add_row(row, label, attr_name):
            lbl = QLabel(label)
            lbl.setStyleSheet("font-size: 18px; font-weight: 500;")
            inp = QLineEdit()
            inp.setReadOnly(True)
            inp.setText("---")
            setattr(self, attr_name, inp)
            grid.addWidget(lbl, row, 0)
            grid.addWidget(inp, row, 1)

        # Campos de tu BD
        add_row(0, "Fecha:", "inp_fecha")
        add_row(1, "Hora:", "inp_hora")
        add_row(2, "Consultorio:", "inp_consultorio")
        add_row(3, "Método Pago:", "inp_pago")
        add_row(4, "ID Veterinario:", "inp_vet")
        add_row(5, "ID Mascota:", "inp_mascota")
        add_row(6, "ID Cita:", "inp_cita")

        parent_layout.addWidget(form_widget, stretch=2)

    def setup_info_board(self, parent_layout):
        board_container = QFrame()
        board_container.setFixedWidth(400)
        board_container.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 10px;")
        
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FC7CE2, stop:1 #7CEBFC); border-top-left-radius: 10px; border-top-right-radius: 10px;")
        hl = QVBoxLayout(header)
        lbl = QLabel("Motivo / Diagnóstico")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none; background: transparent;")
        hl.addWidget(lbl)

        self.txt_motivo_view = QTextEdit()
        self.txt_motivo_view.setReadOnly(True)
        self.txt_motivo_view.setStyleSheet("border: none; padding: 15px; font-size: 16px; color: #555;")
        self.txt_motivo_view.setText("Ingrese un ID para ver los detalles...")

        board_layout.addWidget(header)
        board_layout.addWidget(self.txt_motivo_view)

        parent_layout.addWidget(board_container, stretch=1)

    # ============================================================
    #  LÓGICA
    # ============================================================
    def volver_al_menu(self):
        try:
            from UI_Veterinario import VeterinarioMenu 
            self.menu = VeterinarioMenu(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            self.close()

    def buscar_consulta(self):
        id_consulta = self.inp_search.text().strip()

        if not id_consulta.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número.")
            return

        try:
            # Consulta directa a tu tabla
            sql = f"SELECT fecha, hora, consultorio, metodo_pago, fk_veterinario, fk_mascota, fk_cita, motivo FROM consulta WHERE id_consulta = {id_consulta}"
            
            # Ejecutamos query (adapta si usas otro metodo en Conexion)
            self.conexion.cursor_uno.execute(sql)
            resultado = self.conexion.cursor_uno.fetchone()

            if resultado:
                # resultado = (fecha, hora, consultorio, pago, vet, mascota, cita, motivo)
                self.inp_fecha.setText(str(resultado[0]))
                self.inp_hora.setText(str(resultado[1]))
                self.inp_consultorio.setText(str(resultado[2]))
                self.inp_pago.setText(str(resultado[3]))
                self.inp_vet.setText(str(resultado[4]))
                self.inp_mascota.setText(str(resultado[5]))
                
                cita_val = resultado[6]
                self.inp_cita.setText(str(cita_val) if cita_val else "Sin Cita")
                
                self.txt_motivo_view.setText(str(resultado[7]))
                
                QMessageBox.information(self, "Encontrado", "Consulta cargada correctamente.")
            else:
                self.limpiar_datos()
                QMessageBox.warning(self, "No Encontrado", "No existe una consulta con ese ID.")

        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"Error al buscar:\n{e}")

    def limpiar_datos(self):
        self.inp_fecha.setText("---")
        self.inp_hora.setText("---")
        self.inp_consultorio.setText("---")
        self.inp_pago.setText("---")
        self.inp_vet.setText("---")
        self.inp_mascota.setText("---")
        self.inp_cita.setText("---")
        self.txt_motivo_view.setText("---")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = VentanaRevisarConsulta('Isaid')
    window.show()
    sys.exit(app.exec())