import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, 
                             QMessageBox, QFrame, QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# --- AJUSTE DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) 
if current_dir not in sys.path: sys.path.append(current_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)

# Intentar importar conexión
try:
    from db_connection import Conexion
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
            self.conexion1 = Conexion()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS ---
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QWidget#Sidebar { background-color: transparent; }
            QLabel { font-family: 'Segoe UI'; color: #333; font-size: 16px; font-weight: bold; }
            
            /* Inputs */
            QLineEdit, QTextEdit {
                background-color: rgba(241, 131, 227, 0.15); 
                border: 1px solid #DDD; border-radius: 10px; 
                padding: 10px; font-size: 16px; color: #333;
            }
            QLineEdit:focus, QTextEdit:focus { border: 1px solid #b67cfc; background-color: white; }
            
            /* GroupBox para detalles */
            QGroupBox {
                border: 1px solid #DDD;
                border-radius: 10px;
                margin-top: 20px;
                font-size: 14px;
                font-weight: bold;
                color: #5f2c82;
            }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 10px; }

            /* Botones Menú Lateral (Estilo Unificado) */
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
                height: 35px; margin-bottom: 2px; margin-left: 10px; margin-right: 10px; 
            }
            QPushButton.sub-btn:hover { 
                color: white; background-color: rgba(255, 255, 255, 0.3); font-weight: bold; 
            }
            
            /* Botón Buscar */
            QPushButton#BtnBuscar {
                background-color: #7CEBFC; color: #333; border-radius: 10px; 
                font-weight: bold; border: 1px solid #5CD0E3;
            }
            QPushButton#BtnBuscar:hover { background-color: #5CD0E3; }
        """)

        # --- Sidebar ---
        self.setup_sidebar()

        # --- PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(80, 40, 80, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Internar Paciente")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)

        # --- SECCION DE BUSQUEDA ---
        search_layout = QHBoxLayout()
        self.white_layout.addWidget(QLabel("ID de la Consulta:"))
        
        self.inp_id_consulta = QLineEdit()
        self.inp_id_consulta.setPlaceholderText("Ej. 102")
        self.inp_id_consulta.setFixedWidth(200)
        
        btn_buscar = QPushButton("Buscar")
        btn_buscar.setObjectName("BtnBuscar")
        btn_buscar.setFixedSize(100, 42)
        btn_buscar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_buscar.clicked.connect(self.buscar_datos_consulta)

        search_layout.addWidget(self.inp_id_consulta)
        search_layout.addWidget(btn_buscar)
        search_layout.addStretch()
        self.white_layout.addLayout(search_layout)

        # --- DETALLES DE LA CONSULTA (Resultado Búsqueda) ---
        self.group_detalles = QGroupBox("Datos Completos de la Consulta")
        self.group_detalles.setVisible(False) # Oculto hasta buscar
        detalles_layout = QFormLayout(self.group_detalles)
        detalles_layout.setSpacing(10)

        # Labels para mostrar info (TODOS los campos)
        # Campos: id_consulta, consultorio, motivo, metodo_pago, fk_veterinario, fk_mascota
        self.lbl_id_res = QLabel("-")
        self.lbl_consultorio = QLabel("-")
        self.lbl_motivo = QLabel("-")
        self.lbl_veterinario = QLabel("-")
        self.lbl_mascota = QLabel("-")
        
        # Estilo simple para los valores
        style_val = "font-weight: normal; color: #555; padding: 2px;"
        for lbl in [self.lbl_id_res, self.lbl_consultorio, self.lbl_motivo, self.lbl_veterinario, self.lbl_mascota]:
            lbl.setStyleSheet(style_val)

        # Agregamos al layout en orden
        detalles_layout.addRow("ID Consulta:", self.lbl_id_res)
        detalles_layout.addRow("Consultorio:", self.lbl_consultorio)
        detalles_layout.addRow("Motivo:", self.lbl_motivo)
        detalles_layout.addRow("Veterinario:", self.lbl_veterinario)
        detalles_layout.addRow("Mascota:", self.lbl_mascota)

        self.white_layout.addWidget(self.group_detalles)
        self.white_layout.addSpacing(20)

        # --- FORMULARIO INTERNAMIENTO ---
        self.white_layout.addWidget(QLabel("Observaciones / Motivo de Internamiento:"))
        self.inp_obs = QTextEdit()
        self.inp_obs.setPlaceholderText("Describa el estado del paciente, medicación requerida y razones para internarlo...")
        self.white_layout.addWidget(self.inp_obs)

        self.white_layout.addSpacing(20)

        # Botón Confirmar
        btn_internar = QPushButton("CONFIRMAR INTERNAMIENTO")
        btn_internar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_internar.setFixedHeight(60)
        btn_internar.setStyleSheet("""
            QPushButton { background-color: #b67cfc; color: white; font-size: 20px; font-weight: bold; border-radius: 15px; }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_internar.clicked.connect(self.internar_mascota)
        self.white_layout.addWidget(btn_internar)
        self.white_layout.addStretch()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    # =========================================================================
    #  LOGICA BASE DE DATOS
    # =========================================================================
    def buscar_datos_consulta(self):
        """
        Busca y muestra TODA la información de la consulta, incluyendo
        los nombres del veterinario y la mascota (usando JOIN o subconsultas).
        """
        id_consulta_input = self.inp_id_consulta.text().strip()
        if not id_consulta_input:
            QMessageBox.warning(self, "Aviso", "Ingrese un ID de consulta.")
            return

        if not DB_AVAILABLE:
            QMessageBox.critical(self, "Error", "Sin conexión a BD.")
            return

        try:
            # 1. Obtener la Consulta Específica (usamos consultar_registro)
            # Retorna tupla: (id, consultorio, motivo, pago, fk_vet, fk_mascota)
            consulta = self.conexion1.consultar_registro('consulta', 'id_consulta', id_consulta_input)
            
            if consulta:
                # Extraer datos básicos
                id_c = str(consulta[0])
                consultorio = str(consulta[1])
                motivo = str(consulta[2])
                fk_vet = consulta[4]
                fk_mascota = consulta[5]

                # 2. Obtener NOMBRE del Veterinario
                nombre_vet = "Desconocido"
                if fk_vet:
                    # Asumimos que la tabla de usuarios contiene al veterinario
                    # Consultamos 'usuario' por 'id_usuario' y traemos 'nombre' y 'apellido'
                    vet_data = self.conexion1.consultar_registro('usuario', 'id_usuario', fk_vet, columnas=['nombre', 'apellido'])
                    if vet_data:
                        nombre_vet = f"{vet_data[0]} {vet_data[1]}"
                    else:
                        nombre_vet = f"ID: {fk_vet} (No encontrado)"

                # 3. Obtener NOMBRE de la Mascota
                nombre_mascota = "Desconocida"
                if fk_mascota:
                    # Consultamos 'mascota' por 'id_mascota' y traemos 'nombre'
                    mascota_data = self.conexion1.consultar_registro('mascota', 'id_mascota', fk_mascota, columnas=['nombre'])
                    if mascota_data:
                        nombre_mascota = str(mascota_data[0])
                    else:
                        nombre_mascota = f"ID: {fk_mascota} (No encontrada)"

                # Asignar a Labels
                self.lbl_id_res.setText(id_c)
                self.lbl_consultorio.setText(consultorio)
                self.lbl_motivo.setText(motivo)
                self.lbl_veterinario.setText(nombre_vet)
                self.lbl_mascota.setText(nombre_mascota)
                
                self.group_detalles.setVisible(True)
            else:
                QMessageBox.warning(self, "No encontrado", "No se encontró una consulta con ese ID.")
                self.group_detalles.setVisible(False)
                self.limpiar_labels()
                
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"Error al buscar consulta: {e}")

    def limpiar_labels(self):
        self.lbl_id_res.setText("-")
        self.lbl_consultorio.setText("-")
        self.lbl_motivo.setText("-")
        self.lbl_veterinario.setText("-")
        self.lbl_mascota.setText("-")

    def internar_mascota(self):
        id_consulta = self.inp_id_consulta.text()
        obs = self.inp_obs.toPlainText()

        if not id_consulta or not obs:
            QMessageBox.warning(self, "Alerta", "Todos los campos son obligatorios (ID Consulta y Observaciones).")
            return

        if not DB_AVAILABLE:
            QMessageBox.critical(self, "Error", "No hay conexión a la base de datos.")
            return

        try:
            # Insertar en tabla hospitalizacion
            datos = (obs, int(id_consulta))
            columnas = ('observaciones', 'fk_consulta')
            self.conexion1.insertar_datos('hospitalizacion', datos, columnas)
            
            QMessageBox.information(self, "Éxito", "Paciente internado correctamente.")
            self.inp_id_consulta.clear()
            self.inp_obs.clear()
            self.group_detalles.setVisible(False)
            self.limpiar_labels()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al internar: {e}")

    # --- BARRA LATERAL ---
    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(10)

        # --- LOGO ROBUSTO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ruta_logo = os.path.join(parent_dir, "FILES", "logo_yuno.png")
        
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                lbl_logo.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        else:
            lbl_logo.setText("YUNO VET")
            lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        
        self.sidebar_layout.addWidget(lbl_logo)
        self.sidebar_layout.addSpacing(20)

        # Menús
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
        if frame.isVisible():
            frame.hide()
        else:
            frame.show()

    # --- NAVEGACIÓN ---
    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import EnfermeroMain
            self.menu = EnfermeroMain(self.nombre_usuario)
            self.menu.show()
            self.close()
        except ImportError:
            QMessageBox.warning(self, "Error", "No se encuentra el menú de enfermera.")

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
                elif opcion == "Hospitalización":
                    pass 
            
            elif categoria == "Expediente" and opcion == "Diagnóstico":
                from UI_Diagnostico import MainWindow as Win
                target_window = Win(self.nombre_usuario) 

            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close() 
            
        except ImportError as e:
            QMessageBox.warning(self, "Error", f"No se encuentra el archivo de destino.\n{e}")
        except Exception as e:
            print(f"Error navegando: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("TEST USER")
    window.show()
    sys.exit(app.exec())