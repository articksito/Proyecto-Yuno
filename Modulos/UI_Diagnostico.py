import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# --- RUTA DEL ARCHIVO TXT ---
# Asegúrate que esta ruta sea correcta en tu PC
RUTA_ARCHIVO = '/home/owner_jose/Proyecto-Yuno/diagnostico.txt'

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

        # --- ESTILOS ---
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FC7CE2, stop:1 #7CEBFC); }
            QWidget#WhitePanel { background-color: white; border-top-left-radius: 30px; border-bottom-left-radius: 30px; margin: 20px 20px 20px 0px; }
            QWidget#Sidebar { background-color: transparent; }
            QTextEdit {
                background-color: #f9f9f9; border: 2px dashed #b67cfc; border-radius: 15px; padding: 20px; font-size: 16px; color: #333; font-family: 'Consolas', monospace;
            }
            /* Sidebar Styles */
            QPushButton.menu-btn { text-align: left; padding-left: 20px; border: none; background-color: transparent; color: white; font-family: 'Segoe UI'; font-weight: bold; font-size: 24px; height: 50px; margin-top: 10px; }
            QPushButton.menu-btn:hover { color: #EEE; }
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
        
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-weight: bold; border: none;")
        btn_back.clicked.connect(self.close)

        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_back)
        self.white_layout.addLayout(header_layout)
        
        self.white_layout.addWidget(QLabel("Escriba el nuevo diagnóstico para agregar al expediente:"))
        
        # Area de Texto
        self.txt_diagnostico = QTextEdit()
        self.txt_diagnostico.setPlaceholderText("Escriba aquí los detalles del diagnóstico...")
        self.white_layout.addWidget(self.txt_diagnostico)

        # Botón Guardar
        btn_save = QPushButton("GUARDAR EN EXPEDIENTE (.TXT)")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedHeight(60)
        btn_save.setStyleSheet("""
            QPushButton { background-color: #b67cfc; color: white; font-size: 20px; font-weight: bold; border-radius: 30px; }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_save.clicked.connect(self.guardar_diagnostico)
        
        self.white_layout.addSpacing(20)
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
            # Intenta crear el archivo si no existe
            with open(RUTA_ARCHIVO, 'a+') as f:
                f.write(texto_formateado)
                
            QMessageBox.information(self, "Guardado", "Diagnóstico agregado correctamente.")
            self.txt_diagnostico.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error de Archivo", f"No se pudo escribir en el archivo:\n{e}")

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(20, 50, 20, 50)
        
        lbl_logo = QLabel("YUNO VET\nEXPEDIENTES")
        lbl_logo.setStyleSheet("color: white; font-size: 30px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(lbl_logo)
        
        btn = QPushButton("Citas")
        btn.setProperty("class", "menu-btn")
        layout.addWidget(btn)
        layout.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())