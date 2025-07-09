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
        self.gb_child.setRowCol(1, 4)
        self.gb_child.columnsEquals()
        self.split.addWidget(self.gb_parent)
        self.split.addWidget(self.gb_child)
        self.split.setSizes([150, 480])
        self.gb_parent.vh.setVisible(False)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.gb_parent.heightAuto)
        self.gb_parent.cellClicked.connect(self.itemChoice)
        # self.gb_child.cellClicked.connect(self.itemChoiceChild)

    def getDirs(self, dir=str) -> list:
        sf = SearchFiles(path=dir)
        return sf.getDirs()
    
    def getFiles(self, dir:str, **kw) -> list:
        sf = SearchFiles(path=dir)
        return sf.getImages(**kw)
    
    def resizeEvent(self, event):
        self.timer.start(400)
    
    def testUno(self):
        sf = SearchFiles(path='T:/TAG/RECURSOS/personajes2')
        data = sf.getCovers()
        self.gb_parent.setCovers(data=data, cols=2)

    def itemChoice(self, row:int, col:int):
        select = self.gb_parent.selectCard(row, col)
        if select:
            data = select.data
            dir = data.get('dir')
            sf = SearchFiles(path=dir)
            images = sf.getImages()
            dirs = sf.getDirs()

            if data.get('dirname')=='00':
                ...
            else:
                pprint(data)
                # else:
                #     images = sf.getImages()
                #     extra = []
                #     for dir in sf.getDirs():
                #         sf_sub = SearchFiles(dir)
                #         data = sf_sub.getImageByDir()
                #         if data:
                #             extra.append(data)
                #     images.extend(extra)
                #     if images:
                #         self.gb_child.setImages(files=images, cols=4)
                extra = []
                for dir in dirs:
                    sf_sub = SearchFiles(path=dir)
                    data_cover = sf_sub.getImageByDir()
                    if data_cover:
                        extra.append(data_cover)
                images.extend(extra)
            if images:
                self.gb_child.setImages(files=images, cols=4)
            

            # name, path = select
            # parent = Path(path).parent.as_posix()
            # print(name, path)

            # sf = SearchFiles(path=parent)
            # if name == '00':
            #     images = []
            #     # parent = Path(path).parent.as_posix()
            #     # sf = SearchFiles(parent)
            #     images = sf.getFiles()
            #     dirs = sf.getDirs()
            #     for dir in dirs:
            #         sf_sub = SearchFiles(path=dir)
            #         imgs = sf_sub.getImages()
            #         images.extend(imgs)
            #         extra = ()
            #         for subdir in sf_sub.getDirs():
            #             sf_sub2 = SearchFiles(subdir)
            #             data = sf_sub2.getImageByDir()
            #             if data:
            #                 extra.append(data)
            #         images.extend(extra)
            #     self.gb_child.setImages(files=images, cols=4)
            # else:
            #     images = sf.getImages()
            #     extra = []
            #     for dir in sf.getDirs():
            #         sf_sub = SearchFiles(dir)
            #         data = sf_sub.getImageByDir()
            #         if data:
            #             extra.append(data)
            #     images.extend(extra)
            #     if images:
            #         self.gb_child.setImages(files=images, cols=4)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    vn = TestSelectS()
    vn.test2Galleries()
    vn.testUno()
    vn.setGeometry(100, 50, 950, 600)
    vn.show()
    sys.exit(app.exec())