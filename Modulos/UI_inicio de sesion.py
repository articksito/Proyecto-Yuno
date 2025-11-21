from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush
import sys

from db_connection import Conexion

from UI_Veterinario import VeterinarioMenu
from UI_Recepcionista import MainWindow as Recepcionista


# ---------------------------
#     LOGO BASE64 (PENPOT)
# ---------------------------
logo_base64 = b"""
iVBORw0KGgoAAAANSUhEUgAAAVYAAAF7CAYAAACJnaNrAAAAAXNSR0IArs4c6QAAIABJREFUeAHsvfmbY1d576ucpJN0EhpC4253l+ZZqirVpJJqVGmoUqkmqeahJ7cnPDYe2hO2cdrY2MYjGNsBTgIhONwACYkDCSThXghcwj3hwAkknHDDeU7Ok/xw/417Pqv2Km8LbWlLe2uq2noePZq29l57rff9rnd+bTbrYc1Ac2fgl2w226/abLbftNls77bZbCdtNtv1NpvNbrPZ3DabzW+z2cI2m61PeQ7YbLZB5Tlis9l4jtpstqTy5L38Xh7Hf+T/ORfn5Nxcg2txTa7NGBgLY7Ie1gxYM2DNQEfPAGD1LpvN9j6bzdZjs9m8NpstooBjQgWKAhyPHTuWPHb8ePL48ePJEydOJE+cOJk8eZLn6eTJ06eTpw+e9uTp0/bkabs9aVeevBff8b1yHP8R/z15UpyLc3JursG1yq9vs9kYE6DMGBkrY2bs3AP3Yj2sGbBmwJqBls3ALyvgc9pms3lsNluvzWaLq4ELIDt+fB8sAT4A0e12J92BQDIQiCaj0V989vb2jsZiseGBgYGhwcHBwaGhoQGeIyMj/fF4vI/n2NhYhKf8zG/yOP7DfzkH56p0Da7NGBgLY2JsADpjrQC+3BP3xj1yrwAu9249rBmwZsCaAUMz8Cs2m+09ijodstlsQxJA98HzuJAykR7tbncyEAi8AzpUjkKARFgBc2Q3z5z8zeuyz4Jt2AXS3J8QtN7HzE7zw8b6xRz7lL2kB6ALGfVTjCkUgKwDKBEA2QpvXnECWfZG55kb7suvLPtY+xHOuUvap0uFkG8AgEwUuXgV0xkqWaSwBvIQALLZURwH4AI6Wg3sH4m140j2etL46PfUfwPKF8MX91wnAxalKlcAAAAASUVORK5CYII=
"""


# ---------------------------
#      WIDGET PRINCIPAL
# ---------------------------
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de sesión")
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        # Fondo degradado
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#FC7CE2"))
        gradient.setColorAt(1.0, QColor("#7CEBFC"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Layout principal
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        title = QLabel("Bienvenido")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Campo usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setFixedWidth(250)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border-radius: 8px;
                border: 2px solid #ddd;
                padding: 8px;
                background: white;
            }
        """)

        # Campo contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(250)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border-radius: 8px;
                border: 2px solid #ddd;
                padding: 8px;
                background: white;
            }
        """)

        # Botón
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.setFixedWidth(200)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #5f2c82;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #49a09d;
            }
        """)
        self.login_button.clicked.connect(self.login)

        # Mensaje de estado
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: white; font-size: 13px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Añadir widgets al layout
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addWidget(self.login_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def login(self):
        conexion = Conexion()

        username = self.username_input.text()
        password = self.password_input.text()

        if conexion.Validacion_usuario(username) and conexion.Validacion_contrasena(password):
            self.animate_success()
            
            rol = conexion.Validacion_Perfil(username)
            
            if rol == "ADMIN":
                print("Perfil Admin")

            elif rol == "VET":
                self.vet = VeterinarioMenu("Isaid")
                self.vet.show()
                self.close()
            elif rol == "REP":
                self.rep = Recepcionista(conexion.Nombre_Usuario(username))
                self.rep.show()
                self.close()
        else:
            self.status_label.setText("❌ Usuario o contraseña incorrectos")
            QMessageBox.warning(self, "Error", "Credenciales inválidas")

    def animate_success(self):
        """Animación del botón al iniciar sesión correctamente"""
        anim = QPropertyAnimation(self.login_button, b"geometry")
        anim.setDuration(400)
        anim.setEasingCurve(QEasingCurve.Type.OutBounce)
        anim.setStartValue(self.login_button.geometry())
        anim.setEndValue(self.login_button.geometry().adjusted(0, -10, 0, -10))
        anim.start()
        self.anim = anim  # evitar que se destruya



# ---------------------------
#        EJECUCIÓN
# ---------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
