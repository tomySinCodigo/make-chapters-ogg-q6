import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Mostrar Imagen en QLabel")
        self.setGeometry(100, 100, 800, 600)

        # Crear un QLabel para mostrar la imagen
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar la imagen
        pol = QSizePolicy(QSizePolicy.Policy.Ignored , QSizePolicy.Policy.Ignored)
        self.label.setSizePolicy(pol)
        # Cargar la imagen
        self.pixmap = QPixmap("U:/UTAG/PIX/Pix28/illust_105796671_20230307_081257.png")  # Cambia esto a tu ruta
        self.label.setPixmap(self.pixmap)

        # Ajustar la imagen al tamaño del QLabel
        self.label.setScaledContents(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    # def resizeEvent(self, event):
    #     # Redimensionar la imagen al cambiar el tamaño de la ventana
    #     self.label.setPixmap(self.pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    #     super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
