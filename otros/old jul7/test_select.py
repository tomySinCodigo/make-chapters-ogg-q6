import sys
from pprint import pprint
from pathlib import Path
from PySide6.QtWidgets import QApplication, QSplitter, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from qwidgets.gallery_base import GalleryBase
from qwidgets.funciones import SearchFiles


class TestSelectS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__configTest()

    def __configTest(self):
        self.setGeometry(400, 50, 600, 600)
        self.setWindowTitle("Mi Ventana")
        
        self.central_widget = QWidget()
        vly = QVBoxLayout(self.central_widget)
        self.split = QSplitter(self.central_widget, orientation=Qt.Horizontal)
        vly.addWidget(self.split)
        self.setCentralWidget(self.central_widget)
        self.setLayout(vly)

    def test2Galleries(self):
        self.gb_parent = GalleryBase()
        self.gb_parent.setRowCol(2, 1)
        self.gb_parent.columnsEquals()
        self.gb_child = GalleryBase()
        self.gb_child.setRowCol(1, 3)
        self.gb_child.columnsEquals()
        self.split.addWidget(self.gb_parent)
        self.split.addWidget(self.gb_child)
        self.split.setSizes([150, 480])
        self.gb_parent.vh.setVisible(False)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.gb_parent.heightAuto)

        sf = SearchFiles(path='T:/TAG/RECURSOS/personajes2')
        data = sf.getWalls()
        # pprint(data)
        # {'images': {'Esdeath': 'T:/TAG/RECURSOS/personajes2/akame ga kill/Esdeath.png',
        #      'akame ga kill': 'T:/TAG/RECURSOS/personajes2/akame ga kill/akame '
        #                       'ga kill.png'},
        # 'name': 'akame ga kill',
        # 'path': 'T:/TAG/RECURSOS/personajes2/akame ga kill',
        # 'wall': 'T:/TAG/RECURSOS/personajes2/akame ga kill/akame ga kill.png'}

        # walls = [d.get('wall') for d in data]
        # self.gb_parent.setImages(images=walls, cols=2)
        # usando setWalls
        self.gb_parent.setWalls(data=data, cols=2)
        self.gb_parent.cellClicked.connect(self.itemChoice)
        self.gb_child.cellClicked.connect(self.itemChoiceChild)


    def getDirs(self, folder:str) -> list:
        sf = SearchFiles(path=folder)
        return sf.getDirs()
    
    def getFiles(self, folder:str, **kw) -> list:
        sf = SearchFiles(path=folder)
        return sf.getImages(**kw)

    def resizeEvent(self, event):
        self.timer.start(400)

    def itemChoice(self, row:int, col:int):
        select = self.gb_parent.selectCard(row, col)
        if select:
            name, path = select
            print('name:: ', name, path)
            sf = SearchFiles(path=path)
            if name == '00':
                images = []
                parent = Path(path).parent.as_posix()
                sf = SearchFiles(parent)
                images = sf.getFiles()
                dirs = sf.getDirs()
                for folder in dirs:
                    _sf = SearchFiles(path=folder)
                    imgs = _sf.getImages()
                    images.extend(imgs)
                    extra = []
                    print('subfolder:: ', _sf.getDirs())
                    for subdir in _sf.getDirs():
                        sfsub = SearchFiles(subdir)
                        data = sfsub.getOneImageData()
                        if data:
                            extra.append(data)
                    images.extend(extra)
                # pprint(images)
                print(len(images))
                self.gb_child.setImages(images=images, cols=3)
            else:
                images = sf.getImages()
                extra = []
                print('subfolder:: ', sf.getDirs())
                for subdir in sf.getDirs():
                    sfsub = SearchFiles(subdir)
                    data = sfsub.getOneImageData()
                    if data:
                        extra.append(data)
                images.extend(extra)
                if images:
                    pprint(images)
                    self.gb_child.setImages(images=images, cols=3)
                else:
                    print("no hay images")

    def itemChoiceChild(self, row:int, col:int):
        select = self.gb_child.selectCard(row, col)
        if select:
            name, path = select
            print(name, path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vn = TestSelectS()
    vn.test2Galleries()
    vn.setGeometry(100, 50, 950, 600)
    vn.show()
    sys.exit(app.exec())