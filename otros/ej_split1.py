import sys
from PySide6.QtWidgets import QApplication, QSplitter, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Ejemplo de QSplitter con QTimer")
        self.setGeometry(100, 100, 600, 400)

        # Crear un QSplitter
        self.splitter = QSplitter(self)

        # Agregar widgets al splitter
        self.text_edit1 = QTextEdit("Texto 1")
        self.text_edit2 = QTextEdit("Texto 2")
        self.splitter.addWidget(self.text_edit1)
        self.splitter.addWidget(self.text_edit2)

        # Conectar la señal splitterMoved a un slot
        self.splitter.splitterMoved.connect(self.on_splitter_moved)

        # Crear un QTimer
        self.timer = QTimer()
        self.timer.setSingleShot(True)  # Asegurarse de que el temporizador se ejecute solo una vez
        self.timer.timeout.connect(self.on_timer_timeout)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)

    def on_splitter_moved(self, pos, index):
        # Reiniciar el temporizador cada vez que se mueve el separador
        self.timer.start(300)  # Esperar 300 ms después de que el usuario deja de mover el separador

    def on_timer_timeout(self):
        # Acción a ejecutar una vez que el temporizador se agota
        print("El separador ha dejado de moverse.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

