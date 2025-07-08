import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QByteArray, QTimer
from qwidgets.viewer import Viewer, Card
from qwidgets.funciones import SearchFiles
from qwidgets.gallery_base import GalleryBase
from pprint import pprint


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self._configVentanaPrincipal()

    def _configVentanaPrincipal(self):
        self.setWindowTitle("Mi Ventana")
        self.setGeometry(100, 40, 280, 200)
        # icono "textarea-icon16.png" 16px
        icon = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYBAMAAAASWSDLAAAAD1B" \
        "MVEUAAACoqKioqKioqKioqKjGKhJaAAAABHRSTlMAARAfdZsTCQAAACNJR" \
        "EFUeJxjcEECDORxnJUggIAMNZTh4LgosFDGcRZgIs3bAP2FROGW0Q0XAAA" \
        "AAElFTkSuQmCC"
        self.setWindowIcon(self.getQicon(str_b64=icon))
        self.central_widget = QWidget(self)

        self.vly = QVBoxLayout(self.central_widget)
        self.vly.setContentsMargins(0,0,0,0)
        self.setCentralWidget(self.central_widget)
        self.setLayout(self.vly)

    def setMiWidget(self, wg):
        self.wg = wg
        self.vly.addWidget(self.wg)

    def getQicon(self, str_b64:str):
        pix = QPixmap()
        pix.loadFromData(QByteArray.fromBase64(str(str_b64).encode('utf-8')))
        qicon = QIcon()
        qicon.addPixmap(pix)
        return qicon


class TestViewer(VentanaPrincipal):
    def __init__(self):
        super().__init__()
        self.__configTest()

    def __configTest(self):
        image = 'D:/TEMPORAL/Desktop VARIOS/salida/eg G20.gif'
        # image = 'D:/TEMPORAL/Desktop VARIOS/salida/eg 32.jpg'
        wg = Card()
        wg.setImage(image_file=image)
        self.setMiWidget(wg)
        wg.setTitle(text='mi titulo')
        wg.setNum(15)
        wg.setOverlay()


class TestGallery(VentanaPrincipal):
    def __init__(self):
        super().__init__()
        self.__configTestGallery()

    def __configTestGallery(self):
        self.setGeometry(100,50,400,600)
        self.gb = GalleryBase()
        self.setMiWidget(self.gb)
        self.gb.setRowCol(rows=1, cols=3)
        self.gb.columnsEquals()

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.gb.heightAuto)

    def testMod(self):
        r1 = 'T:/TAG/EJECUTABLES/RECURSOS/pro_plex/modelos'
        sf = SearchFiles(path=r1)
        images = sf.getImages()
        self.gb.setImages(images=images, cols=3)
        self.gb.cellClicked.connect(self.selectCardViewer)

    def resizeEvent(self, event):
        return self.timer.start(400)
    
    def selectCardViewer(self, row, col):
        select = self.gb.selectCard(row, col)
        if select:
            name, path = select
            print('name:: ', name, path)

    def testPs(self):
        ruta = 'T:/TAG/EJECUTABLES/RECURSOS/pro_plex/ps'
        sf = SearchFiles(path=ruta)
        images = sf.getImages()
        self.gb.AR = 6/4
        self.gb.setImages(images=images)
        self.gb.cellClicked.connect(self.selectCardViewer)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # vn = VentanaPrincipal()
    # vn = TestViewer()
    vn = TestGallery()
    # vn.testMod()
    vn.testPs()
    vn.show()
    sys.exit(app.exec())