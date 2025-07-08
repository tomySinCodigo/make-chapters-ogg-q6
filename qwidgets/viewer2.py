import os
os.environ['QT_LOGGING_RULES'] = '*=false'
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


class Title(QLabel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configTitle()
        
    def __configTitle(self):
        self.mod = 10
        self.mg = 0
        self.h = 12
        self.w = 20
        self.x = 0
        self.y = 0
        self.pos = 'so'
        
        self.setFixedHeight(self.h)

    def setText(
        self, text:str, fg:str='rgba(255,255,255,120)', bg:str='rgba(10,5,12,200)',
        size:int=7, bold:bool=True, name:str='Consolas',
        align:str='c'
    ):
        _ = "\u3164"
        mg = f'{_}' * self.mg
        text = f'{mg}{text}{mg}'
        super().setText(text)
        self.setFont(size, bold, name)
        self.setColors(fg, bg)
        self.setAlign(coord=align)

        fom = self.fontMetrics()
        w = fom.horizontalAdvance(str(text))+4
        self.setFixedWidth(w)

    def moveUpdate(self):
        if not self.parent() or not self.parent().isVisible():
            return
            
        try:
            gm = self.parent().geometry()
            wp, hp = gm.width(), gm.height()
            
            # Verificar que las dimensiones sean válidas
            if wp <= 0 or hp <= 0:
                return
                
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
        except:
            # Ignorar errores durante transiciones de maximizar/minimizar
            pass

    def setColors(self, fg:str='white', bg:str='blue'):
        self.setStyleSheet(f'color:{fg};background:{bg};')

    def setFont(self, size:int=7, bold:bool=True, name:str=None):
        fo = QFont()
        if name:  # Corregido: era "if not name"
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


class Overlay(QLabel):  # Corregido: solo hereda de QLabel
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)  # Corregido: super() normal
        self.__configOverlay()
    
    def __configOverlay(self):
        self.setScaledContents(True)

    def setText(
        self, text:str, fg:str='rgba(255,255,255,80)', bg:str='rgba(0,0,0,160)',
        size:int=12, bold:bool=True, name:str='Consolas',
        align:str='nc', mg:int=0
    ):
        text = f'{" "*mg}{text}{" "*mg}'
        super().setText(text)
        self.setFont(size, bold, name)
        self.setColors(fg, bg)
        self.setAlign(coord=align)

    def setColors(self, fg:str='white', bg:str='blue'):
        self.setStyleSheet(f'color:{fg};background:{bg};')

    def setFont(self, size:int=7, bold:bool=True, name:str=None):
        fo = QFont()
        if name:
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


class Viewer(QLabel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configViewer()

    def __configViewer(self):
        self.reloadVariables()
        pol = QSizePolicy(QSizePolicy.Policy.Ignored , QSizePolicy.Policy.Ignored)
        self.setSizePolicy(pol)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_op = Overlay(self)
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
        # Verificar que el evento y el widget estén en estado válido
        if not event or not event.size().isValid():
            return
        
        super().resizeEvent(event)
        
        # Verificar que el widget esté completamente inicializado
        if hasattr(self, 'lb_op') and self.lb_op and self.lb_op.isVisible():
            sz = event.size()
            # Verificar que el tamaño sea válido y no esté en transición
            if sz.width() > 0 and sz.height() > 0 and self.isVisible():
                try:
                    self.lb_op.setGeometry(0, 0, sz.width(), sz.height())
                except:
                    # Ignorar errores durante transiciones de maximizar/minimizar
                    pass

    def enterEvent(self, event):
        if self.OPACITY and hasattr(self, 'lb_op'):
            self.lb_op.hide()
        if hasattr(self, 'gviewer'):
            self.gviewer.setPaused(False)

    def leaveEvent(self, event):
        if self.OPACITY and hasattr(self, 'lb_op'):
            self.lb_op.show()
        if hasattr(self, 'gviewer'):
            self.gviewer.setPaused(True)

    def showOverlay(self, b:bool=True):
        if hasattr(self, 'lb_op'):
            self.lb_op.show() if b else self.lb_op.hide()
            self.OPACITY = b

    def opConfig(self, text:str, **kw):
        """text:str,
        fg:str='white', bg:str='rgba(10,5,10,160)',
        size:int=12, bold:bool=True, name:str='Consolas',
        align:str='c', mg:int=0"""
        if hasattr(self, 'lb_op'):
            self.lb_op.setText(text, **kw)

    def setOverlay(
        self, text:str='', show:bool=True, **kw
    ):
        """text:str,
        fg:str='white', bg:str='rgba(10,5,10,160)',
        size:int=12, bold:bool=True, name:str='Consolas',
        align:str='c', mg:int=0"""
        self.opConfig(text, **kw)
        self.showOverlay(show)


class Card(Viewer):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configCard()

    def __configCard(self):
        self.lb_title = Title(self)
        self.lb_title.pos = 'sw'
        self.lb_num = Title(self)
        self.lb_num.pos = 'se'

    def setTitle(self, text:str, **kw):
        """text: str,
            fg: str = 'white',
            bg: str = 'blue',
            size: int = 7,
            bold: bool = True,
            name: str = 'Consolas',
            align: str = 'c'"""
        self.lb_title.setText(text, **kw)

    def setNum(self, text:str, **kw):
        self.lb_num.mg = 0
        self.lb_num.setText(text, **kw)

    def resizeEvent(self, event):
        # Verificar que el evento sea válido
        if not event or not event.size().isValid():
            return
            
        super().resizeEvent(event)
        
        # Verificar que los widgets estén inicializados y visibles antes de actualizarlos
        if hasattr(self, 'lb_title') and self.lb_title and self.isVisible():
            try:
                self.lb_title.moveUpdate()
            except:
                pass
        if hasattr(self, 'lb_num') and self.lb_num and self.isVisible():
            try:
                self.lb_num.moveUpdate()
            except:
                pass


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self._configVentanaPrincipal()

    def _configVentanaPrincipal(self):
        self.setWindowTitle("Mi Ventana")
        self.setGeometry(100, 40, 280, 200)
        
        # Configurar flags de ventana para mejor manejo de maximize/minimize
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.Window)
        
        icon = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYBAMAAAASWSDLAAAAD1B" \
        "MVEUAAACoqKioqKioqKioqKjGKhJaAAAABHRSTlMAARAfdZsTCQAAACNJR" \
        "EFUeJxjcEECDORxnJUggIAMNZTh4LgosFDGcRZgIs3bAP2FROGW0Q0XAAA" \
        "AAElFTkSuQmCC"
        self.setWindowIcon(self.getQicon(str_b64=icon))
        
        central_widget = QWidget(self)
        vly = QVBoxLayout(central_widget)
        vly.setContentsMargins(0,0,0,0)
        
        # Crear el widget Card
        self.wg = Card(parent=central_widget)
        
        # Verificar que el archivo de imagen exista antes de cargarlo
        image = r"otros/image1.jpg"
        try:
            self.wg.setImage(image_file=image)
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            # Continuar sin imagen si hay error
        
        self.wg.setTitle(text='mi titulo uno', align='w')
        self.wg.setNum('05', bg='black')

        vly.addWidget(self.wg)
        self.setCentralWidget(central_widget)

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