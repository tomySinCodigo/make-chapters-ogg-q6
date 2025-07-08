import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Ventana con Imagen")
        self.setGeometry(100, 100, 300, 200)

        # Crear un QLabel para mostrar la imagen
        self.label = QLabel(self)
        self.setCentralWidget(self.label)

        # Cargar la imagen desde la ruta proporcionada
        self.pixmap = QPixmap(r"U:\INICIO DOS\PROGRAMas REc\NotaS\sqink hex\resources\img\purple\daf\1603572280897.png")
        self.label.setPixmap(self.pixmap)

        # Ajustar la imagen al tamaño de la ventana
        self.label.setScaledContents(True)

    # def resizeEvent(self, event):
    #     # Redimensionar la imagen al cambiar el tamaño de la ventana
    #     self.label.setPixmap(self.pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    #     super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
