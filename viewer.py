import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget,
    QFrame, QLabel, QPushButton
)
from PySide6.QtGui import QIcon, QPixmap, QMovie, QFont 
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
        bg = "pink"
        self.setStyleSheet(f'background-color:{bg};')
        self.__configViewer()

    def __configViewer(self):
        self.reloadVariables()
        pol = QSizePolicy(QSizePolicy.Policy.Ignored , QSizePolicy.Policy.Ignored)
        self.setSizePolicy(pol)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.lb_op = QLabel(self)
        self.lb_op = Overlay(self)
        # self.lb_op.setStyleSheet("background-color:rgba(10,5,10,88);")
        # self.lb_op.hide()
        # self.lb_op.setScaledContents(True)
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

    def opConfig(self, text:str, **kw):
        self.lb_op.setText(text, **kw)


class Title(QLabel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configTitle()
        
    def __configTitle(self):
        self.mod = 10
        self.mg = 2
        self.h = 12
        self.w = 20
        self.x = 0
        self.y = 0
        self.pos = 'so'
        
        self.setFixedHeight(self.h)
        # words = len(self.text())

    def setText(
        self, text:str, fg:str='white', bg:str='blue',
        size:int=7, bold:bool=True, name:str='Consolas',
        align:str='c'
    ):
        text = f'{" "*self.mg}{text}{" "*self.mg}'
        super().setText(text)
        self.setFont(size, bold, name)
        self.setColors(fg, bg)
        self.setAlign(coord=align)

    def moveUpdate(self):
        gm = self.parent().geometry()
        wp, hp = gm.width(), gm.height()
        w , h = self.geometry().width(), self.geometry().height()
        x, y = self.x, self.y
        match self.pos:
            case 'ne': x = wp - (w + x)
            case 'sw' | 'bot':
                y = hp - (self.h + y)
                x = self.x
            case 'se':
                x = wp - (w + x)
                y = hp - (h + y)
        if self.pos in ('top', 'bot'):
            self.setFixedWidth(wp - x)
        self.move(x, y)

    def setColors(self, fg:str='white', bg:str='blue'):
        self.setStyleSheet(f'color:{fg};background:{bg};')

    def setFont(self, size:int=7, bold:bool=True, name:str=None):
        fo = QFont()
        if not name:
            fo.setFamily(name)
        fo.setPointSize(size)
        fo.setBold(bold)
        super().setFont(fo)

    def setAlign(self, coord:str='c'):
        match coord:
            case 'n':self.setAlignment(Qt.AlignTop)
            case 's':self.setAlignment(Qt.AlignBottom)
            case 'w':self.setAlignment(Qt.AlignLeft)
            case 'e':self.setAlignment(Qt.AlignRight)
            case 'nc':self.setAlignment(Qt.AlignLeading | Qt.AlignTop | Qt.AlignHCenter)
            case 'sc':self.setAlignment(Qt.AlignLeading | Qt.AlignBottom | Qt.AlignHCenter)
            case _:self.setAlignment(Qt.AlignCenter)


class Overlay(Title, QLabel):
    def __init__(self, *args, **kw):
        super(Title, self).__init__(*args, **kw)
        self.__configOverlay()
    
    def __configOverlay(self):
        self.setScaledContents(True)

    def setText(
        self, text:str, fg:str='white', bg:str='rgba(10,5,10,160)',
        size:int=12, bold:bool=True, name:str='Consolas',
        align:str='c', mg:int=0
    ):
        text = f'{" "*mg}{text}{" "*mg}'
        super(Title, self).setText(text)
        self.setFont(size, bold, name)
        self.setColors(fg, bg)
        self.setAlign(coord=align)


class Card(Viewer):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configCard()

    def __configCard(self):
        self.lb_title = Title(self)
        self.lb_title.pos = 'sw'
        self.lb_num = Title(self)
        self.lb_num.mg = 1
        self.lb_num.pos = 'sw'

        self.opConfig(text='ALICE BONG\nPURPLE BITCH\n', align='sc')

    def setTitle(self, text:str, **kw):
        """text: str,
            fg: str = 'white',
            bg: str = 'blue',
            size: int = 7,
            bold: bool = True,
            name: str = 'Consolas',
            align: str = 'c'"""
        self.lb_title.setText(text, **kw)
        self.lb_title.x = 20
        # self.lb_title.y = 14

    def setNum(self, text:str, **kw):
        self.lb_num.setText(text, **kw)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.lb_title.moveUpdate()
        self.lb_num.moveUpdate()


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
        vly.setContentsMargins(0,0,0,0)
        # self.wg = Viewer(parent=central_widget)
        self.wg = Card(parent=central_widget)
        self.wg.setImage(image_file=image)
        self.wg.setNum('05', bg='black')
        self.wg.setTitle(text='mi titulo uno', align='w')


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