import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QLabel, QPushButton

# Clase que hereda de QFrame
class MiFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuración del layout
        layout = QVBoxLayout()

        # Agregando widgets básicos
        self.label = QLabel("¡Hola, bienvenido a mi aplicación!")
        self.boton = QPushButton("Haz clic aquí")
        
        # Conectar el botón a una función
        self.boton.clicked.connect(self.on_button_click)

        # Añadir widgets al layout
        layout.addWidget(self.label)
        layout.addWidget(self.boton)

        # Establecer el layout en el frame
        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText("¡Botón clicado!")

# Clase de la ventana principal
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ejemplo de PySide")
        self.setGeometry(100, 100, 600, 200)

        # Crear una instancia de MiFrame
        self.frame = MiFrame()
        self.setCentralWidget(self.frame)

# Código principal para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
