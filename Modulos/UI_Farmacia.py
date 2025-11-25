import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, 
                             QTreeWidget, QTreeWidgetItem, QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from db_connection import Conexion

class MainWindow(QMainWindow):
    conexion1 = Conexion()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Veterinario Yuno - Farmacia")
        self.resize(1280, 720)

        # Widget central
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
            QLabel { font-family: 'Segoe UI', sans-serif; color: #333; }
            QLineEdit {
                background-color: rgba(241, 131, 227, 0.35); border: none; border-radius: 10px; padding: 5px 15px; font-size: 16px; color: #333; height: 40px;
            }
            QTreeWidget { border: 1px solid #DDD; border-radius: 10px; font-family: 'Segoe UI'; font-size: 14px; }
            QHeaderView::section { background-color: #b67cfc; color: white; padding: 5px; border: none; font-weight: bold; }
            
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
        self.white_layout.setContentsMargins(40, 30, 40, 30)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("Farmacia e Inventario")
        lbl_header.setStyleSheet("font-size: 36px; font-weight: bold; color: #333;")
        
        btn_back = QPushButton("↶ Volver")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("background-color: #F0F0F0; color: #555; border-radius: 20px; padding: 10px 20px; font-weight: bold; border: none;")
        btn_back.clicked.connect(self.close)

        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        header_layout.addWidget(btn_back)
        self.white_layout.addLayout(header_layout)

        # --- CONTENIDO DIVIDIDO ---
        content_layout = QHBoxLayout()
        
        # Lado Izquierdo: Formulario
        form_container = QFrame()
        form_layout = QVBoxLayout(form_container)
        self.setup_form(form_layout)
        
        # Lado Derecho: Tabla
        table_container = QFrame()
        table_layout = QVBoxLayout(table_container)
        self.setup_table(table_layout)

        content_layout.addWidget(form_container, stretch=1)
        content_layout.addSpacing(20)
        content_layout.addWidget(table_container, stretch=2)

        self.white_layout.addLayout(content_layout)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.white_panel)
        
        # Cargar datos al iniciar
        self.cargar_tabla()

    def setup_form(self, layout):
        lbl_titulo = QLabel("Registrar Medicamento")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(lbl_titulo)

        # Campos
        self.inp_nombre = QLineEdit(); self.inp_nombre.setPlaceholderText("Nombre Medicina")
        self.inp_tipo = QLineEdit(); self.inp_tipo.setPlaceholderText("Tipo (ej. Antibiótico)")
        self.inp_comp = QLineEdit(); self.inp_comp.setPlaceholderText("Composición (mg)")
        self.inp_dosis = QLineEdit(); self.inp_dosis.setPlaceholderText("Dosis Recomendada")
        self.inp_via = QLineEdit(); self.inp_via.setPlaceholderText("Vía Admin. (ej. Oral)")

        layout.addWidget(QLabel("Nombre:")); layout.addWidget(self.inp_nombre)
        layout.addWidget(QLabel("Tipo:")); layout.addWidget(self.inp_tipo)
        layout.addWidget(QLabel("Composición:")); layout.addWidget(self.inp_comp)
        layout.addWidget(QLabel("Dosis:")); layout.addWidget(self.inp_dosis)
        layout.addWidget(QLabel("Vía Admin:")); layout.addWidget(self.inp_via)
        
        layout.addStretch()
        
        btn_add = QPushButton("Agregar al Inventario")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setFixedHeight(50)
        btn_add.setStyleSheet("""
            QPushButton { background-color: #b67cfc; color: white; font-size: 18px; font-weight: bold; border-radius: 25px; }
            QPushButton:hover { background-color: #a060e8; }
        """)
        btn_add.clicked.connect(self.agregar_medicamento)
        layout.addWidget(btn_add)

    def setup_table(self, layout):
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["ID", "Nombre", "Tipo", "Comp.", "Dosis", "Vía"])
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tree)
        
        btn_refresh = QPushButton("🔄 Actualizar Tabla")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setStyleSheet("background: transparent; color: #555; font-weight: bold; text-align: right;")
        btn_refresh.clicked.connect(self.cargar_tabla)
        layout.addWidget(btn_refresh)

    def agregar_medicamento(self):
        nombre = self.inp_nombre.text()
        tipo = self.inp_tipo.text()
        comp = self.inp_comp.text()
        dosis = self.inp_dosis.text()
        via = self.inp_via.text()

        if not nombre or not tipo:
            QMessageBox.warning(self, "Error", "El nombre y tipo son obligatorios.")
            return

        try:
            datos = (nombre, tipo, comp, dosis, via)
            columnas = ('nombre', 'tipo', 'composicion', 'dosis_recomendada', 'via_administracion')
            self.conexion1.insertar_datos('medicamento', datos, columnas)
            QMessageBox.information(self, "Éxito", "Medicamento agregado correctamente.")
            self.limpiar_form()
            self.cargar_tabla()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {e}")

    def cargar_tabla(self):
        self.tree.clear()
        try:
            filas = self.conexion1.Select_users(table='medicamento')
            for fila in filas:
                item = QTreeWidgetItem([str(x) for x in fila])
                self.tree.addTopLevelItem(item)
        except Exception as e:
            print(f"Error cargando tabla: {e}")

    def limpiar_form(self):
        self.inp_nombre.clear()
        self.inp_tipo.clear()
        self.inp_comp.clear()
        self.inp_dosis.clear()
        self.inp_via.clear()

    def setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(300)
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(20, 50, 20, 50)
        
        lbl_logo = QLabel("YUNO VET\nFARMACIA")
        lbl_logo.setStyleSheet("color: white; font-size: 30px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(lbl_logo)
        
        # Botones decorativos
        btn = QPushButton("Inventario")
        btn.setProperty("class", "menu-btn")
        layout.addWidget(btn)
        layout.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())