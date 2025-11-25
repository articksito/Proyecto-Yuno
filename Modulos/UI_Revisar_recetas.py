import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit,
                             QMessageBox, QGridLayout, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from db_connection import Conexion

class VentanaRevisarReceta(QMainWindow):
    def __init__(self, nombre_usuario="Mick"):
        super().__init__()
        
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error Conexión: {e}")

        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Sistema Veterinario Yuno - Historial de Recetas")
        self.resize(1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#Sidebar { background-color: transparent; }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            QLineEdit[readOnly="true"], QTextEdit[readOnly="true"] { background-color: #F0F0F0; border: 1px solid #DDD; border-radius: 10px; padding: 5px 15px; font-size: 16px; color: #555; }
            QPushButton.menu-btn { text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; color: white; font-family: 'Segoe UI', sans-serif; font-weight: bold; font-size: 18px; background-color: rgba(255, 255, 255, 0.1); height: 50px; margin-bottom: 5px; }
            QPushButton.menu-btn:hover { background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; }
            QPushButton.sub-btn { text-align: left; padding-left: 40px; border-radius: 10px; color: #F0F0F0; background-color: rgba(0, 0, 0, 0.05); height: 35px; margin-bottom: 2px; margin-left: 10px; margin-right: 10px; }
            QPushButton.sub-btn:hover { color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        lbl_logo = QLabel("YUNO VET\nRECETAS")
        lbl_logo.setStyleSheet("color: white; font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(lbl_logo)

        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro"])

        self.sidebar_layout.addStretch()
        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("QPushButton { text-align: center; border: 2px solid white; border-radius: 15px; padding: 10px; margin-top: 20px; font-size: 14px; color: white; font-weight: bold; background-color: transparent; } QPushButton:hover { background-color: rgba(255,255,255,0.2); }")
        btn_logout.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_logout)
        self.main_layout.addWidget(self.sidebar)

    def setup_accordion_group(self, title, options):
        btn_main = QPushButton(title)
        btn_main.setProperty("class", "menu-btn")
        self.sidebar_layout.addWidget(btn_main)
        frame_options = QFrame()
        layout_options = QVBoxLayout(frame_options)
        layout_options.setContentsMargins(0, 0, 0, 10)
        layout_options.setSpacing(5)
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.clicked.connect(lambda checked=False, cat=title, opt=opt_text: self.router_ventanas(cat, opt))
            layout_options.addWidget(btn_sub)
        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    def router_ventanas(self, categoria, opcion):
        print(f"Navegando: {categoria} -> {opcion}")
        try:
            if categoria == "Consultas":
                if opcion == "Crear Consulta":
                    from UI_Realizar_consulta import VentanaConsulta
                    self.v = VentanaConsulta(self.nombre_usuario)
                    self.v.show()
                    self.close()
                elif opcion == "Ver Registro":
                    from UI_Revisar_consulta import VentanaRevisarConsulta
                    self.v = VentanaRevisarConsulta(self.nombre_usuario)
                    self.v.show()
                    self.close()
            elif categoria == "Recetas":
                if opcion == "Crear Receta":
                    from UI_Registrar_receta import VentanaReceta
                    self.v = VentanaReceta(self.nombre_usuario)
                    self.v.show()
                    self.close()
                elif opcion == "Ver Registro":
                    QMessageBox.information(self, "Sistema", "Ya estás en el Historial de Recetas.")
        except ImportError as e:
            QMessageBox.warning(self, "Error", f"Archivo no encontrado: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error de navegación: {e}")

    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 30, 50, 40)

        header_layout = QHBoxLayout()
        lbl_header = QLabel("Historial de Recetas")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(40, 40)
        btn_close.setStyleSheet("background-color: #f0f0f0; border-radius: 20px; font-size: 20px; color: #666; border: none;")
        btn_close.clicked.connect(self.volver_al_menu)
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_close)
        self.white_layout.addLayout(header_layout)

        self.setup_search_bar()
        self.white_layout.addSpacing(20)

        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        self.setup_details_form(content_layout)
        self.setup_info_board(content_layout)

        self.white_layout.addWidget(content_container)
        self.white_layout.addStretch(2)
        self.main_layout.addWidget(self.white_panel)

    def setup_search_bar(self):
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        lbl_search = QLabel("ID Receta:")
        lbl_search.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Ingrese ID...")
        self.inp_search.setFixedWidth(300)
        self.inp_search.setStyleSheet("border: 2px solid #ddd; border-radius: 10px; padding: 8px; font-size: 16px; background-color: white;")
        btn_search = QPushButton("Buscar")
        btn_search.setFixedSize(120, 40)
        btn_search.setStyleSheet("background-color: #7CEBFC; color: #333; font-weight: bold; border-radius: 10px; border: 1px solid #5CD0E3;")
        btn_search.clicked.connect(self.buscar_receta)
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
        
        # --- AQUI ESTA LA CORRECCION ---
        # Solo mostramos Fecha y Consulta, pues la mascota se infiere de la consulta
        lbl_fecha = QLabel("Fecha Emisión:")
        lbl_fecha.setStyleSheet("font-size: 18px; font-weight: 500;")
        self.inp_fecha = QLineEdit()
        self.inp_fecha.setReadOnly(True)
        self.inp_fecha.setText("---")

        lbl_consulta = QLabel("ID Consulta Asociada:")
        lbl_consulta.setStyleSheet("font-size: 18px; font-weight: 500;")
        self.inp_consulta = QLineEdit()
        self.inp_consulta.setReadOnly(True)
        self.inp_consulta.setText("---")

        grid.addWidget(lbl_fecha, 0, 0)
        grid.addWidget(self.inp_fecha, 0, 1)
        grid.addWidget(lbl_consulta, 1, 0)
        grid.addWidget(self.inp_consulta, 1, 1)
        
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
        lbl = QLabel("Indicaciones / Medicamentos")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none; background: transparent;")
        hl.addWidget(lbl)

        self.txt_indicaciones_view = QTextEdit()
        self.txt_indicaciones_view.setReadOnly(True)
        self.txt_indicaciones_view.setStyleSheet("border: none; padding: 15px; font-size: 16px; color: #555;")
        self.txt_indicaciones_view.setText("Ingrese un ID para ver los detalles...")

        board_layout.addWidget(header)
        board_layout.addWidget(self.txt_indicaciones_view)
        parent_layout.addWidget(board_container, stretch=1)

    def volver_al_menu(self):
        try:
            from UI_Veterinario import VeterinarioMenu 
            self.menu = VeterinarioMenu(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            self.close()

    def buscar_receta(self):
        id_receta = self.inp_search.text().strip()
        if not id_receta.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número.")
            return

        try:
            # SELECT corregido: solo columnas de receta
            sql = f"SELECT fecha, fk_consulta, indicaciones FROM receta WHERE id_receta = {id_receta}"
            
            self.conexion.cursor_uno.execute(sql)
            resultado = self.conexion.cursor_uno.fetchone()

            if resultado:
                # resultado = (fecha, fk_consulta, indicaciones)
                self.inp_fecha.setText(str(resultado[0]))
                self.inp_consulta.setText(str(resultado[1]))
                self.txt_indicaciones_view.setText(str(resultado[2]))
                QMessageBox.information(self, "Encontrado", "Receta cargada correctamente.")
            else:
                self.limpiar_datos()
                QMessageBox.warning(self, "No Encontrado", "No existe una receta con ese ID.")
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"Error al buscar:\n{e}")

    def limpiar_datos(self):
        self.inp_fecha.setText("---")
        self.inp_consulta.setText("---")
        self.txt_indicaciones_view.setText("---")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaRevisarReceta()
    window.show()
    sys.exit(app.exec())