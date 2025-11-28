import sys
import os

# --- 1. CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..')) 

if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QColor

from db_connection import Conexion

class VeterinarioMenu(QMainWindow):
    def __init__(self, nombre_usuario="Veterinario"):
        super().__init__()
        
        try:
            self.conexion = Conexion()
        except Exception as e:
            print(f"Error BD: {e}")

        self.nombre_usuario = nombre_usuario
        self.user_data = {
            "nombre": f"{self.nombre_usuario}",
            "puesto": "Médico Veterinario",
            "id": "MED-001"
        }

        self.setWindowTitle("Sistema Veterinario Yuno - Panel Médico")
        self.resize(1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
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
            QLabel { font-family: 'Segoe UI', sans-serif; }
            
            /* ESTILO TABLA (FONDO BLANCO PURO) */
            QTableWidget {
                border: 1px solid black;
                border-radius: 10px;
                background-color: white;
                gridline-color: black;
                font-size: 14px;
                color: black;
            }
            QHeaderView::section {
                background-color: #FC7CE2;
                color: white;
                padding: 5px;
                font-weight: bold;
                border: 1px solid black;
            }
            QTableWidget::item {
                padding: 5px;
                color: black;
                background-color: white;
                border-bottom: 1px solid black;
            }
            QTableWidget::item:selected {
                background-color: #e0e0e0;
                color: black;
            }
            
            /* ESTILO BOTONES SIDEBAR */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px; color: white; font-family: 'Segoe UI', sans-serif;
                font-weight: bold; font-size: 18px; background-color: rgba(255, 255, 255, 0.1);
                height: 50px; margin-bottom: 5px;
            }
            QPushButton.menu-btn:hover { background-color: rgba(255, 255, 255, 0.25); border: 1px solid white; color: #FFF; }

            QPushButton.sub-btn {
                text-align: left; padding-left: 40px; border-radius: 10px; color: #F0F0F0;
                font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: normal;
                background-color: rgba(0, 0, 0, 0.05); height: 35px; margin-bottom: 2px;
                margin-left: 10px; margin-right: 10px;
            }
            QPushButton.sub-btn:hover { color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; }
            
            QPushButton.logout-btn {
                text-align: center; border: 2px solid white; border-radius: 15px;
                padding: 10px; margin-top: 20px; font-size: 14px; color: white;
                font-weight: bold; background-color: transparent;
            }
            QPushButton.logout-btn:hover { background-color: rgba(255, 255, 255, 0.2); }
        """)

        self.setup_sidebar()
        self.setup_content_panel()

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

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
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")

        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # --- AQUI ESTAN LOS CAMBIOS DE MENU ---
        
        # 1. Consultas
        self.setup_accordion_group("Consultas", ["Crear Consulta", "Ver Registro"])
        
        # 2. Recetas (Agregada nueva opción)
        self.setup_accordion_group("Recetas", ["Crear Receta", "Ver Registro", "Agregar medicina a receta"])
        
        # 3. Extra (Nuevo Grupo)
        self.setup_accordion_group("Extra", ["Visualizar mascotas", "Visualizar medicamento", "Agregar notas para internar"])

        self.sidebar_layout.addStretch()

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setProperty("class", "logout-btn")
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
        layout_options.setSpacing(2) 
        
        for opt_text in options:
            btn_sub = QPushButton(opt_text)
            btn_sub.setProperty("class", "sub-btn")
            btn_sub.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_sub.clicked.connect(lambda checked, t=title, o=opt_text: self.router_ventanas(t, o))
            layout_options.addWidget(btn_sub)

        frame_options.hide()
        self.sidebar_layout.addWidget(frame_options)
        btn_main.clicked.connect(lambda: self.toggle_menu(frame_options))

    def toggle_menu(self, frame):
        if frame.isVisible(): frame.hide()
        else: frame.show()

    # ============================================================
    #  ENRUTADOR ACTUALIZADO
    # ============================================================
    def router_ventanas(self, categoria, opcion):
        print(f"Navegando a: {categoria} -> {opcion}")
        try:
            # --- CONSULTAS ---
            if categoria == "Consultas":
                if opcion == "Crear Consulta":
                    from UI_Realizar_consulta import VentanaConsulta
                    self.ventana = VentanaConsulta(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Ver Registro":
                    from UI_Revisar_consulta import VentanaRevisarConsulta
                    self.ventana = VentanaRevisarConsulta(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

            # --- RECETAS ---
            elif categoria == "Recetas":
                if opcion == "Crear Receta":
                    from UI_Registrar_receta import VentanaReceta 
                    self.ventana = VentanaReceta(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Ver Registro":
                    from UI_Revisar_recetas import VentanaRevisarReceta
                    self.ventana = VentanaRevisarReceta(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                elif opcion == "Agregar medicina a receta":
                    from UI_Agregar_MReceta import VentanaAgregarMedicamento
                    self.ventana=VentanaAgregarMedicamento(self.nombre_usuario)
                    self.ventana.show()
                    self.close()

            # --- EXTRA (NUEVO) ---
            elif categoria == "Extra":
                if opcion == "Visualizar mascotas":
                    from UI_RevisarMascota_Vete import VentanaRevisarMascota
                    self.ventana = VentanaRevisarMascota(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                
                elif opcion == "Visualizar medicamento":
                    from UI_RevisarMedicamento import VentanaRevisarMedicamento
                    self.ventana = VentanaRevisarMedicamento(self.nombre_usuario)
                    self.ventana.show()
                    self.close()
                
                elif opcion == "Agregar notas para internar":
                    # AQUI CONECTAS TU CLASE
                    QMessageBox.information(self, "Construcción", "Aquí iría Notas de Internación.")

        except ImportError as e:
            QMessageBox.warning(self, "Archivo Faltante", f"No se encontró el archivo: {e.name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir ventana:\n{e}")

    def setup_content_panel(self):
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        
        panel_layout = QHBoxLayout(self.white_panel)
        panel_layout.setContentsMargins(40, 40, 40, 40)
        panel_layout.setSpacing(40)

        # IZQUIERDA: Reloj
        left_container = QFrame()
        info_layout = QVBoxLayout(left_container)
        info_layout.setSpacing(15)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_title = QLabel("Bienvenid@")
        lbl_title.setStyleSheet("color: #888; font-size: 24px; letter-spacing: 2px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_name = QLabel(self.user_data['nombre'])
        lbl_name.setStyleSheet("color: #5f2c82; font-size: 56px; font-weight: bold;")
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_role = QLabel(self.user_data['puesto'])
        lbl_role.setStyleSheet("color: #FC7CE2; font-size: 20px; font-weight: 600;")
        lbl_role.setAlignment(Qt.AlignmentFlag.AlignCenter)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedWidth(120)
        line.setStyleSheet("background-color: #DDD; margin: 25px 0;")
        
        self.lbl_time = QLabel()
        self.lbl_time.setStyleSheet("color: #555; font-size: 80px; font-weight: 300; font-family: 'Segoe UI Light';")
        self.lbl_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        info_layout.addWidget(lbl_title)
        info_layout.addWidget(lbl_name)
        info_layout.addWidget(lbl_role)
        
        line_layout = QHBoxLayout()
        line_layout.addStretch()
        line_layout.addWidget(line)
        line_layout.addStretch()
        info_layout.addLayout(line_layout)
        info_layout.addWidget(self.lbl_time)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        # DERECHA: TABLA DE CITAS
        right_container = QFrame()
        list_layout = QVBoxLayout(right_container)
        list_layout.setContentsMargins(0, 0, 0, 0)

        lbl_info = QLabel("Pacientes en espera:")
        lbl_info.setStyleSheet("font-size: 18px; color: #666; font-weight: bold; margin-bottom: 10px;")
        list_layout.addWidget(lbl_info)

        # TABLA
        self.tabla_citas = QTableWidget()
        self.tabla_citas.setColumnCount(4)
        self.tabla_citas.setHorizontalHeaderLabels(["Paciente ID", "Fecha", "Hora", "Estado"])
        
        self.tabla_citas.setAlternatingRowColors(False) 
        self.tabla_citas.verticalHeader().setVisible(False)
        self.tabla_citas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_citas.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        header = self.tabla_citas.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        try:
            datos_citas = self.conexion.Select_users('cita') 
            if datos_citas:
                pendientes = [fila for fila in datos_citas if fila[3] == 'Pendiente']
                pendientes = pendientes[::-1][:15] 

                self.tabla_citas.setRowCount(len(pendientes))

                for row, fila in enumerate(pendientes):
                    self.tabla_citas.setItem(row, 0, QTableWidgetItem(str(fila[0])))
                    self.tabla_citas.setItem(row, 1, QTableWidgetItem(str(fila[1])))
                    self.tabla_citas.setItem(row, 2, QTableWidgetItem(str(fila[2])))
                    
                    item_estado = QTableWidgetItem(str(fila[3]))
                    item_estado.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                    self.tabla_citas.setItem(row, 3, item_estado)
            else:
                pass
                
        except Exception as e:
            print(f"Error Tabla Citas: {e}")

        list_layout.addWidget(self.tabla_citas)

        panel_layout.addWidget(left_container, 40)
        panel_layout.addWidget(right_container, 60)

        self.main_layout.addWidget(self.white_panel)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.lbl_time.setText(current_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = VeterinarioMenu()
    window.show()
    sys.exit(app.exec())