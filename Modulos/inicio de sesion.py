import sys
import base64
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton
)
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QPixmap
from PyQt6.QtCore import Qt


# ---------------------------
#     LOGO BASE64 (PENPOT)
# ---------------------------
logo_base64 = b"""
iVBORw0KGgoAAAANSUhEUgAAAVYAAAF7CAYAAACJnaNrAAAAAXNSR0IArs4c6QAAIABJREFUeAHsvfmbY1d576ucpJN0EhpC4253l+ZZqirVpJJqVGmoUqkmqeahJ7cnPDYe2hO2cdrY2MYjGNsBTgIhONwACYkDCSThXghcwj3hwAkknHDDeU7Ok/xw/417Pqv2Km8LbWlLe2uq2noePZq29l57rff9rnd+bTbrYc1Ac2fgl2w226/abLbftNls77bZbCdtNtv1NpvNbrPZ3DabzW+z2cI2m61PeQ7YbLZB5Tlis9l4jtpstqTy5L38Xh7Hf+T/ORfn5Nxcg2txTa7NGBgLY7Ie1gxYM2DNQEfPAGD1LpvN9j6bzdZjs9m8NpstooBjQgWKAhyPHTuWPHb8ePL48ePJEydOJE+cOJk8eZLn6eTJ06eTpw+e9uTp0/bkabs9aVeevBff8b1yHP8R/z15UpyLc3JursG1yq9vs9kYE6DMGBkrY2bs3AP3Yj2sGbBmwJqBls3ALyvgc9pms3lsNluvzWaLq4ELIDt+fB8sAT4A0e12J92BQDIQiCaj0V989vb2jsZiseGBgYGhwcHBwaGhoQGeIyMj/fF4vI/n2NhYhKf8zG/yOP7DfzkH56p0Da7NGBgLY2JsADpjrQC+3BP3xj1yrwAu9249rBmwZsCaAUMz8Cs2m+09ijodstlsQxJA98HzuJAykR7tbncyEAi8AzpUjkKARFgBc2Q3z5z8zeuyz4Jt2AXS3J8QtN7HzE7zw8b6xRz7lL2kB6ALGfVTjCkUgKwDKBEA2QpvXnECWfZG55kb7suvLPtY+xHOuUvap0uFkG8AgEwUuXgV0xkqWaSwBvIQALLZURwH4AI6Wg3sH4m140j2etL46PfUfwPKF8MX91wnAxalKlcAAAAASUVORK5CYII=
"""


# ---------------------------
#      WIDGET PRINCIPAL
# ---------------------------
class LoginUI(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setFixedSize(400, 300)

        self.setup_ui()
        self.load_logo()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(15)

        # Titulo
        title = QLabel("BIENVENIDO")
        title.setStyleSheet("""
            color: white;
            font-size: 18px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Usuario
        user_label = QLabel("Usuario")
        user_label.setStyleSheet("color: rgba(0,0,0,.52); font-size: 16px;")
        user_input = QLineEdit()
        user_input.setFixedHeight(25)
        user_input.setStyleSheet("""
            background: white;
            border-radius: 8px;
            padding-left: 8px;
        """)

        main_layout.addWidget(user_label)
        main_layout.addWidget(user_input)

        # Contraseña
        pass_label = QLabel("Contraseña")
        pass_label.setStyleSheet("color: rgba(0,0,0,.52); font-size: 16px;")
        pass_input = QLineEdit()
        pass_input.setFixedHeight(25)
        pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        pass_input.setStyleSheet("""
            background: white;
            border-radius: 8px;
            padding-left: 8px;
        """)

        main_layout.addWidget(pass_label)
        main_layout.addWidget(pass_input)

        # Botón
        login_button = QPushButton("Iniciar sesión")
        login_button.setFixedHeight(30)
        login_button.setStyleSheet("""
            background: #5f2c82;
            color: white;
            border-radius: 19px;
            font-size: 16px;
        """)

        main_layout.addWidget(login_button)

        # Espacio del logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self.logo_label)

        self.setLayout(main_layout)

    # Cargar logo DESPUÉS de tener QApplication
    def load_logo(self):
        pix = QPixmap()
        pix.loadFromData(base64.b64decode(logo_base64))
        self.logo_label.setPixmap(pix.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio))

    # Fondo con gradiente
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.11, QColor(124, 235, 252))
        gradient.setColorAt(0.92, QColor(252, 124, 226))
        painter.fillRect(self.rect(), gradient)


# ---------------------------
#        EJECUCIÓN
# ---------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginUI()
    window.show()
    sys.exit(app.exec())
