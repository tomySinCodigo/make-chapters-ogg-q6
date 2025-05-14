from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QSlider
from viewer import Viewer, Card, Title
from pathlib import Path


class CardViewer(Viewer):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configCardViewer()

    def __configCardViewer(self):
        self.STEM = None
        self.PATH = None
        self.lb_title = Title(self)
        self.lb_title.pos = 'bot'
        self.lb_num = Title(self)
        self.lb_num.pos = 'nw'

    def setOverlay(self, text:str='', bg:str='rgba(0,0,0,180)', **kw):
        self.opConfig(text=text, bg=bg, **kw)

    def setNum(self, num:str|int, **kw):
        self.lb_num.setText(text=num, **kw)

    def setTitle(self, text:str, **kw):
        self.lb_title.setText(text=text, **kw)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.lb_title.moveUpdate()
        self.lb_num.moveUpdate()

    def setImage(self, image_file):
        super().setImage(image_file)
        self.STEM = Path(image_file).stem
        self.PATH = image_file


class Base(QTableWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configBase()

    def __configBase(self):
        self.hh = self.horizontalHeader()
        self.vh = self.verticalHeader()
        self.hh.setVisible(False)
        self.vh.setVisible(True)

    def setDim(self, rows:int, cols:int):
        self.clearContents()
        self.setRowCount(rows)
        self.setColumnCount(cols)

    def widthColumnsEquals(self):
        self.hh.setSectionResizeMode(QHeaderView.Stretch)

    def heightAuto(self, ar:float=4/6):
        h = int(self.hh.sectionSize(0)/ar)
        for irow in range(self.rowCount()):
            self.setRowHeight(irow, h)

    def _setImagesTest(self):
        self.clearContents()

        vi1 = CardViewer()
        vi1.setImage("otros/mod/uno.png")
        item = QTableWidgetItem("item uno")
        self.setItem(0, 0, item)
        self.setCellWidget(0, 0, vi1)
        vi1.setNum('001', bg='black', fg='white')
        vi1.setOverlay(text='iMAGE Uno')
        # vi1.lb_num.moveUpdate()
        vi1.setTitle('imagen uno')

        vi2 = Card()
        vi2.setImage("otros/mod/dos.jpg")
        item2 = QTableWidgetItem("item dos ab")
        self.setItem(0, 1, item2)
        self.setCellWidget(0, 1, vi2)
        self.heightAuto()
        # vi2.setOverlay()
        vi2.opConfig(text='TITLE')
        vi2.setTitle('Image NUM')
        vi2.setNum('003', bg='black')


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton, QFrame, QHBoxLayout, QListWidget, QSplitter
    from PySide6.QtCore import Qt, QTimer


    class VentanaPrincipal(QMainWindow):
        def __init__(self):
            super().__init__()
            self._configVentanaPrincipal()

        def _configVentanaPrincipal(self):
            self.setWindowTitle("Mi Ventana")
            self.setGeometry(800, 40, 500, 450)

            self.timer = QTimer()
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.accion_redimension)

            central_widget = QWidget(self)

            vly = QVBoxLayout(central_widget)
            self.splitter = QSplitter(central_widget, orientation=Qt.Horizontal)
            self.splitter.splitterMoved.connect(self.onSplitMoved)
            fm = QListWidget(central_widget)
            self.wg = Base(central_widget)
            self.test_wg()
            self.test_btn()
            self.btn.clicked.connect(self.wg._setImagesTest)
            self.splitter.addWidget(fm)
            self.splitter.addWidget(self.wg)

            vly.addWidget(self.splitter)
            self.setCentralWidget(central_widget)
            self.setLayout(vly)

        def test_wg(self):
            self.wg.setDim(rows=5, cols=2)
            self.wg.widthColumnsEquals()
            self.wg.heightAuto()

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


    app = QApplication(sys.argv)
    vn = VentanaPrincipal()
    vn.show()
    sys.exit(app.exec())