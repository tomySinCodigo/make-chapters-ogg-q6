import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton, QFrame, QHBoxLayout, QListWidget, QSplitter
from PySide6.QtCore import Qt, QTimer
from gallery.gallery_base import GalleryBase
from funciones import SearchFiles
from pathlib import Path


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self._configVentanaPrincipal()

    def _configVentanaPrincipal(self):
        self.setWindowTitle("Mi Ventana")
        self.setGeometry(550, 40, 800, 450)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.accion_redimension)

        central_widget = QWidget(self)

        vly = QVBoxLayout(central_widget)
        self.splitter = QSplitter(central_widget, orientation=Qt.Horizontal)
        self.splitter.splitterMoved.connect(self.onSplitMoved)
        fm = QListWidget(central_widget)
        self.wg = GalleryBase(central_widget)
        # self.test_wg()
        self.test_btn()
        self.btn.clicked.connect(self.setImages)
        self.splitter.addWidget(fm)
        self.splitter.addWidget(self.wg)

        vly.addWidget(self.splitter)
        self.setCentralWidget(central_widget)
        self.setLayout(vly)

    def test_wg(self):
        self.wg.setDim(rows=5, cols=3)
        self.wg.widthColumnsEquals()
        # self.wg.heightAuto()

    def test_btn(self):
        self.btn = QPushButton(self, text="A")
        self.btn.setFixedWidth(30)
        self.btn.move(2, 4)

    def accion_redimension(self):
        print("redimensionado")
        self.wg.heightAuto()

    def onSplitMoved(self, pos, index):
        self.timer.start(400)

    def resizeEvent(self, event):
        self.timer.start(300)

    def setImages(self):
        path = 'T:/TAG/EJECUTABLES/RECURSOS/pro_plex/modelos'
        sf = SearchFiles(path)
        images = sf.getImages()
        self.wg.setImages(images=images, cols=3)


app = QApplication(sys.argv)
vn = VentanaPrincipal()
vn.show()
sys.exit(app.exec())