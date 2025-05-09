import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget,
    QFrame, QLabel, QPushButton
)
from PySide6.QtGui import QIcon, QPixmap, QMovie
from PySide6.QtCore import QByteArray, QSize, Qt, QUrl


class GifViewer(QMovie):
    def __init__(
        self, img:str,
        play_focus:bool=True,
        speed:int=100, **kw
    ):
        super(GifViewer, self).__init__(img, speed=speed, **kw)
        self.PLAY_FOCUS = play_focus
        self.__configGifViewer()

    def __configGifViewer(self):
        self.jumpToFrame(0)
        self.start()
        self.setPaused(True)

    def togglePlay(self):
        self.setPaused(True if self.state()==2 else False)

    def isGif(self) -> bool:
        return self.fileName().endswith('.gif')
    
    def enterEvent(self, event):
        if self.PLAY_FOCUS:
            self.setPaused(False)
            print("enter gifo")

    def leaveEvent(self, event):
        if self.PLAY_FOCUS:
            self.setPaused(True)


class Viewer(QLabel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        bg = "yellow"
        self.setStyleSheet(f'background-color:{bg};')
        self.__configViewer()

    def __configViewer(self):
        self.reloadVariables()
        pol = QSizePolicy(QSizePolicy.Policy.Ignored , QSizePolicy.Policy.Ignored)
        self.setSizePolicy(pol)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_op = QLabel(self)
        self.lb_op.setStyleSheet("background-color:rgba(10,5,10,88);")
        # self.lb_op.hide()
        self.lb_op.setScaledContents(True)
        self.setScaledContents(True)

    def reloadVariables(self):
        self.IMAGE = None
        self.OPACITY = True
        self.VERTICAL = True
        self.INFO = {}

    def _setImageSimple(self, img_file:str):
        self.pix = QPixmap(img_file)
        self.setPixmap(self.pix)

    def _setImageGif(self, img_file:str):
        self.gviewer = GifViewer(img_file)
        self.setMovie(self.gviewer)

    def setImage(self, image_file:str):
        self.IMAGE = QUrl.fromLocalFile(image_file).toLocalFile()
        if image_file.endswith('.gif'):
            self._setImageGif(image_file)
        else:
            self._setImageSimple(image_file)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        sz = event.size()
        self.lb_op.setGeometry(0,0,sz.width(),sz.height())

    def enterEvent(self, event):
        if self.OPACITY:
            self.lb_op.hide()
        if hasattr(self, 'gviewer'):
            self.gviewer.setPaused(False)

    def leaveEvent(self, event):
        if self.OPACITY:
            self.lb_op.show()
        if hasattr(self, 'gviewer'):
            self.gviewer.setPaused(True)

    def setOverlay(self, b:bool=True):
        self.lb_op.hide() if b else self.lb_op.show()
        self.OPACITY = b


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
        central_widget = QWidget(self)

        image = r"otros/image1.jpg"
        # image = r"otros/image2.gif"
        vly = QVBoxLayout(central_widget)
        self.wg = Viewer(parent=central_widget)
        self.wg.setImage(image_file=image)

        vly.addWidget(self.wg)
        self.setCentralWidget(central_widget)
        self.setLayout(vly)


    def getQicon(self, str_b64:str):
        pix = QPixmap()
        pix.loadFromData(QByteArray.fromBase64(str(str_b64).encode('utf-8')))
        qicon = QIcon()
        qicon.addPixmap(pix)
        return qicon
    
    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     self.wg.resizeImage()
        # print(self.geometry())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vn = VentanaPrincipal()
    vn.show()
    sys.exit(app.exec())