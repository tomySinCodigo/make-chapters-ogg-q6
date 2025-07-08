import sys
from PySide6.QtWidgets import QApplication, QSplitter, QTableWidget, QVBoxLayout, QWidget, QLabel, QTextEdit, QListWidget, QHeaderView
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("QSplitter con QTableWidget y Otros Widgets")
        self.setGeometry(100, 100, 800, 600)

        # Crear un QSplitter
        self.splitter = QSplitter(self)

        # Crear un QTableWidget
        self.table_widget = QTableWidget(2, 2)  # 2 filas y 2 columnas
        self.populate_table()

        # Crear un QTextEdit
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Escribe aquí...")

        # Crear un QListWidget
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(["Elemento 1", "Elemento 2", "Elemento 3", "Elemento 4"])

        # Agregar widgets al splitter
        self.splitter.addWidget(self.table_widget)
        self.splitter.addWidget(self.text_edit)
        self.splitter.addWidget(self.list_widget)

        # Conectar el evento de redimensionamiento
        self.splitter.splitterMoved.connect(self.adjust_row_height)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)

    def populate_table(self):
        # Llenar la tabla con imágenes
        for row in range(2):
            for column in range(2):
                label = QLabel()
                pixmap = QPixmap("D:/Bta/q proyectos/make-chapters-ogg/otros/mod/Ava Bonilla.jpg")  # Cambia esto a tu ruta
                label.setPixmap(pixmap)
                label.setScaledContents(True)  # Permitir que la imagen se escale
                self.table_widget.setCellWidget(row, column, label)

        # Establecer el modo de redimensionamiento de las columnas usando horizontalHeader()
        header_h = self.table_widget.horizontalHeader()
        header_h.setSectionResizeMode(QHeaderView.Stretch)  # Estira todas las columnas

        # Ajustar la altura de las filas inicialmente
        self.adjust_row_height()

    def adjust_row_height(self):
        # Ajustar la altura de las filas en función del ancho de las columnas
        for row in range(self.table_widget.rowCount()):
            column_width = self.table_widget.columnWidth(0)
            h = int(column_width/3) + column_width
            self.table_widget.setRowHeight(row, h)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

