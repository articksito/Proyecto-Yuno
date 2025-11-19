from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QApplication
)
from PyQt6.QtGui import QPalette, QLinearGradient, QColor, QBrush, QFont, QIcon
from PyQt6.QtCore import Qt
import sys


class VeterinarioMenu(QWidget):
    def __init__(self, nombre_usuario="Usuario"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Menú Veterinario")
        self.setFixedSize(1366, 768)
        self.setup_ui()

    # ============================================================
    # CONFIGURACIÓN PRINCIPAL
    # ============================================================
    def setup_ui(self):

        # ---------------------------
        # FONDO DEGRADADO PRINCIPAL
        # ---------------------------
        palette = QPalette()
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#8EE7FC"))
        gradient.setColorAt(1.0, QColor("#FC7CE2"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # ============================================================
        #   BARRA LATERAL
        # ============================================================
        sidebar = QFrame()
        sidebar.setFixedWidth(10)

        # ---- Panel blanco encima del sidebar ----
        panel_blanco = QFrame(sidebar)
        panel_blanco.setGeometry(0, 0, 90, self.height())

        # ---- Botón Logoff encima del panel blanco ----
        logoff_btn = QPushButton(panel_blanco)
        logoff_btn.setIcon(QIcon("logout_icon.png"))
        logoff_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logoff_btn.setStyleSheet("background: transparent; border: none;")

        # Layout del panel blanco
        panel_blanco_layout = QVBoxLayout()
        panel_blanco_layout.addStretch()
        panel_blanco_layout.addWidget(
            logoff_btn,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom
        )
        panel_blanco_layout.addSpacing(25)
        panel_blanco.setLayout(panel_blanco_layout)

        # ============================================================
        #            BARRA SUPERIOR
        # ============================================================
        barra_superior = QFrame()
        barra_superior.setFixedHeight(60)

        titulo_bienvenida = QLabel(f"Bienvenido {self.nombre_usuario}")
        titulo_bienvenida.setFont(QFont("Segoe UI", 17, QFont.Weight.Bold))
        titulo_bienvenida.setStyleSheet("color: white;")
        titulo_bienvenida.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_registrar = QPushButton("Registrar Paciente")
        btn_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_registrar.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 17px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover { color: #ffe6ff; }
        """)

        barra_superior_layout = QHBoxLayout()
        barra_superior_layout.addWidget(titulo_bienvenida)
        barra_superior_layout.addWidget(btn_registrar)
        barra_superior.setLayout(barra_superior_layout)

        # ============================================================
        # SECCIONES
        # ============================================================
        frame_citas = self.create_section_frame("Citas Pendientes")
        self.lista_citas = QListWidget()
        frame_citas.layout().addWidget(self.lista_citas)

        frame_pacientes = self.create_section_frame("Pacientes")
        self.lista_pacientes = QListWidget()
        frame_pacientes.layout().addWidget(self.lista_pacientes)

        frame_actividades = self.create_section_frame("Actividades Recientes")
        self.lista_actividades = QListWidget()
        frame_actividades.layout().addWidget(self.lista_actividades)

        # Layouts de contenido
        left_layout = QVBoxLayout()
        left_layout.addWidget(frame_citas)
        left_layout.addWidget(frame_actividades)

        right_layout = QVBoxLayout()
        right_layout.addWidget(frame_pacientes)

        content_layout = QHBoxLayout()
        content_layout.addLayout(left_layout, 1)
        content_layout.addSpacing(30)
        content_layout.addLayout(right_layout, 1)

        # ---------------------------
        # Layout Principal
        # ---------------------------
        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar)

        central_layout = QVBoxLayout()
        central_layout.addWidget(barra_superior)
        central_layout.addLayout(content_layout)

        main_layout.addLayout(central_layout)
        self.setLayout(main_layout)

    # ============================================================
    #   CREA UN MARCO DE SECCIÓN CON CABECERA
    # ============================================================
    def create_section_frame(self, titulo_texto):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255,255,255, 190);
                border: 1px solid #d0d0d0;
                border-radius: 8px;
            }
        """)

        header = QLabel(titulo_texto)
        header.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header.setFixedHeight(32)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                color: white;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7CEBFC,
                    stop:1 #FC7CE2
                );
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(header)
        frame.setLayout(layout)

        return frame


# -------------------------------------------------------------------
# EJECUCIÓN
# -------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VeterinarioMenu("Mick")
    ventana.show()
    sys.exit(app.exec())
