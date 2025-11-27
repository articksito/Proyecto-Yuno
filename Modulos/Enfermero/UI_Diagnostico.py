import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir,'..'))
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# --- RUTA DEL ARCHIVO TXT ---
# Asegúrate que esta ruta sea correcta en tu PC
RUTA_ARCHIVO = 'diagnostico.txt' # Ruta relativa para evitar errores

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Veterinario Yuno - Diagnóstico")
        self.resize(1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ESTILOS GENERALES ---
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QWidget#Sidebar { background-color: transparent; }
            QLabel { font-family: 'Segoe UI'; color: #333; }
            
            QTextEdit {
                background-color: #f9f9f9; border: 2px dashed #b67cfc; border-radius: 15px; 
                padding: 20px; font-size: 16px; color: #333; font-family: 'Consolas', monospace;
            }
            
            /* Sidebar Styles */
            QPushButton.menu-btn {
                text-align: left; padding-left: 20px; border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px; color: white; font-family: 'Segoe UI', sans-serif;
                font-weight: bold; font-size: 18px; background-color: rgba(255, 255, 255, 0.1);
                height: 50px; margin-bottom: 5px;
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
        """)

        # --- Sidebar ---
        self.setup_sidebar()

        # --- PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(50, 40, 50, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_title = QLabel("Expediente / Diagnóstico")
        lbl_title.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver al Menú")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0; color: #555; border-radius: 20px; 
                padding: 10px 20px; font-weight: bold; border: none; font-size: 14px;
            }
            QPushButton:hover { background-color: #E0E0E0; color: #333; }
        """)
        # CONEXIÓN CORRECTA
        btn_back.clicked.connect(self.regresar_menu)

        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_back)
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(20)
        
        lbl_instruction = QLabel("Escriba el nuevo diagnóstico para agregar al expediente:")
        lbl_instruction.setStyleSheet("font-size: 16px; color: #666; font-weight: bold;")
        self.white_layout.addWidget(lbl_instruction)
        
        # Area de Texto
        self.txt_diagnostico = QTextEdit()
        self.txt_diagnostico.setPlaceholderText("Escriba aquí los detalles del diagnóstico, síntomas y tratamiento...")
        self.white_layout.addWidget(self.txt_diagnostico)

        self.white_layout.addSpacing(20)

        # Botón Guardar
        btn_save = QPushButton("GUARDAR EN EXPEDIENTE (.TXT)")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedHeight(60)
        btn_save.setStyleSheet("""
            QPushButton { background-color: #b67cfc; color: white; font-size: 20px; font-weight: bold; border-radius: 30px; }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_save.clicked.connect(self.guardar_diagnostico)
        
        self.white_layout.addWidget(btn_save)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def guardar_diagnostico(self):
        texto = self.txt_diagnostico.toPlainText()
        if not texto.strip():
            QMessageBox.warning(self, "Vacío", "No has escrito nada para guardar.")
            return
            
        try:
            texto_formateado = f"\n--- NUEVO DIAGNÓSTICO ---\n{texto}\n"
            with open(RUTA_ARCHIVO, 'a+') as f:
                f.write(texto_formateado)
                
            QMessageBox.information(self, "Guardado", "Diagnóstico agregado correctamente.")
            self.txt_diagnostico.clear()
        except FileNotFoundError:
             QMessageBox.critical(self, "Error de Ruta", f"No se encuentra el archivo:\n{RUTA_ARCHIVO}")
        except Exception as e:
            QMessageBox.critical(self, "Error de Archivo", f"No se pudo escribir en el archivo:\n{e}")

    # --- BARRA LATERAL ---
    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 50, 20, 50)
        self.sidebar_layout.setSpacing(5)

        # --- LOGO ---
        lbl_logo = QLabel()
        lbl_logo.setObjectName("Logo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 1. Obtener la ruta donde está guardado ESTE archivo .py (Enfermero)
        directorio_actual = os.path.dirname(os.path.abspath(__file__))

        ruta_logo = os.path.join(directorio_actual, "..", "FILES", "logo_yuno.png")
        ruta_logo = os.path.normpath(ruta_logo)

        # 3. Cargar imagen
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                lbl_logo.setPixmap(scaled_pixmap)
            else:
                # Si la imagen existe pero está corrupta
                lbl_logo.setText("YUNO VET")
                lbl_logo.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        else:
            # Si no encuentra la imagen
            print(f"No se encontró el logo en: {ruta_logo}")
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
        
        # AQUÍ ESTABA EL ERROR: Esta función no existía
        btn_logout.clicked.connect(self.regresar_menu)
        
        self.sidebar_layout.addWidget(btn_logout)

    # --- ESTA ES LA FUNCIÓN QUE FALTABA ---
    def regresar_menu(self):
        try:
            from UI_Menu_Enfermera import EnfermeroMain as MenuEnfermera
            self.menu = MenuEnfermera()
            self.menu.show()
            self.close()
        except ImportError:
            QMessageBox.warning(self, "Error", "No se encuentra el menú de enfermera.")

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
            
            # CONEXIÓN AL ROUTER
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

    # --- ROUTER DE NAVEGACIÓN ---
    def abrir_ventana(self, categoria, opcion):
        try:
            target_window = None

            # 1. CITAS
            if categoria == "Citas" and opcion == "Visualizar":
                from UI_Cita_Enfermera import MainWindow as Win
                target_window = Win()
            
            # 2. MASCOTAS
            elif categoria == "Mascotas" and opcion == "Visualizar":
                from UI_Revisar_Mascota_Enfermera import MainWindow as Win
                target_window = Win()
            
            # 3. INVENTARIO
            elif categoria == "Inventario":
                if opcion == "Farmacia":
                    from UI_Farmacia import MainWindow as Win
                    target_window = Win()
                elif opcion == "Hospitalización":
                    from UI_Hospitalizacion import MainWindow as Win
                    target_window = Win()
            
            # 4. EXPEDIENTE
            elif categoria == "Expediente" and opcion == "Diagnóstico":
                pass # Ya estamos aquí

            # 5. EJECUCIÓN
            if target_window:
                self.ventana = target_window
                self.ventana.show()
                self.close() 
            
        except ImportError as e:
            QMessageBox.warning(self, "Error", f"No se encuentra el archivo: {e.name}")
        except Exception as e:
            print(f"Error navegando: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())