import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from db_connection import Conexion

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Veterinario Yuno - Hospitalización")
        self.resize(1280, 720)

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
            QLabel { font-family: 'Segoe UI'; color: #333; font-size: 18px; }
            QLineEdit, QTextEdit {
                background-color: rgba(241, 131, 227, 0.35); border: none; border-radius: 10px; padding: 10px; font-size: 16px; color: #333;
            }
            /* Sidebar Styles */
            QPushButton.menu-btn { text-align: left; padding-left: 20px; border: none; background-color: transparent; color: white; font-family: 'Segoe UI'; font-weight: bold; font-size: 24px; height: 50px; margin-top: 10px; }
            QPushButton.menu-btn:hover { color: #EEE; }
            QPushButton.sub-btn { text-align: left; font-family: 'Segoe UI'; font-size: 18px; font-weight: normal; padding-left: 40px; border: none; color: #F0F0F0; background-color: transparent; height: 35px; }
            QPushButton.sub-btn:hover { color: white; font-weight: bold; }
        """)

        # --- Sidebar ---
        self.setup_sidebar()

        # --- PANEL BLANCO ---
        self.white_panel = QWidget()
        self.white_panel.setObjectName("WhitePanel")
        self.white_layout = QVBoxLayout(self.white_panel)
        self.white_layout.setContentsMargins(100, 40, 100, 40)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Internar Paciente")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-weight: bold; border: none;")
        btn_back.clicked.connect(self.close)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_back)
        self.white_layout.addLayout(header_layout)
        self.white_layout.addSpacing(30)

        # Formulario
        self.white_layout.addWidget(QLabel("ID de la Consulta:"))
        self.inp_id_consulta = QLineEdit()
        self.inp_id_consulta.setPlaceholderText("Ej. 102")
        self.white_layout.addWidget(self.inp_id_consulta)
        
        self.white_layout.addSpacing(20)

        self.white_layout.addWidget(QLabel("Observaciones / Motivo de Internamiento:"))
        self.inp_obs = QTextEdit()
        self.inp_obs.setPlaceholderText("Describa el estado del paciente y las razones para internarlo...")
        self.white_layout.addWidget(self.inp_obs)

        self.white_layout.addSpacing(40)

        # Botón
        btn_internar = QPushButton("CONFIRMAR INTERNAMIENTO")
        btn_internar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_internar.setFixedHeight(60)
        btn_internar.setStyleSheet("""
            QPushButton { background-color: #b67cfc; color: white; font-size: 22px; font-weight: bold; border-radius: 30px; }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_internar.clicked.connect(self.internar_mascota)
        self.white_layout.addWidget(btn_internar)
        self.white_layout.addStretch()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)

    def internar_mascota(self):
        id_consulta = self.inp_id_consulta.text()
        obs = self.inp_obs.toPlainText()

        if not id_consulta or not obs:
            QMessageBox.warning(self, "Alerta", "Todos los campos son obligatorios.")
            return

        try:
            datos = (obs, int(id_consulta))
            columnas = ('observaciones', 'fk_consulta')
            self.conexion1.insertar_datos('hospitalizacion', datos, columnas)
            QMessageBox.information(self, "Éxito", "Paciente internado correctamente.")
            self.inp_id_consulta.clear()
            self.inp_obs.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al internar: {e}")

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(20, 50, 20, 50)
        
        lbl_logo = QLabel("YUNO VET\nHOSPITAL")
        lbl_logo.setStyleSheet("color: white; font-size: 30px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(lbl_logo)
        
        # Opciones visuales (Para mantener consistencia)
        self.crear_boton_menu_simple(layout, "Citas")
        self.crear_boton_menu_simple(layout, "Mascotas")
        self.crear_boton_menu_simple(layout, "Clientes")
        layout.addStretch()

    def crear_boton_menu_simple(self, layout, texto):
        btn = QPushButton(texto)
        btn.setProperty("class", "menu-btn")
        layout.addWidget(btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())