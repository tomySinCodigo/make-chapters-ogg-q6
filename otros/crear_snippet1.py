import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QFrame, QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QByteArray


class FrameContent(QFrame):
    def __init__(self):
        super().__init__()
        self._configFrameContent()

    def _configFrameContent(self):
        vly = QVBoxLayout()
        self.btn = QPushButton("Mi Boton")
        self.btn.clicked.connect(self.accionUno)
        vly.addWidget(self.btn)
        self.setLayout(vly)

    
    def accionUno(self):
        print("accion uno")


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self._configVentanaPrincipal()

    def _configVentanaPrincipal(self):
        self.setWindowTitle("Mi Ventana")
        self.setGeometry(100, 40, 450, 120)

        self.fm_contenido = FrameContent()
        self.setCentralWidget(self.fm_contenido)

        # icono "textarea-icon16.png" 16px
        icon = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYBAMAAAASWSDLAAAAD1B" \
        "MVEUAAACoqKioqKioqKioqKjGKhJaAAAABHRSTlMAARAfdZsTCQAAACNJR" \
        "EFUeJxjcEECDORxnJUggIAMNZTh4LgosFDGcRZgIs3bAP2FROGW0Q0XAAA" \
        "AAElFTkSuQmCC"
        self.setWindowIcon(self.getQicon(str_b64=icon))

    def getQicon(self, str_b64:str):
        pix = QPixmap()
        pix.loadFromData(QByteArray.fromBase64(str(str_b64).encode('utf-8')))
        qicon = QIcon()
        qicon.addPixmap(pix)
        return qicon


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vn = VentanaPrincipal()
    vn.show()
    sys.exit(app.exec())