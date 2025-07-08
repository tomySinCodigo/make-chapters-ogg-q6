from PySide6.QtWidgets import QTableWidgetItem
from gallery.gallery_base import GalleryBase
from gallery.gallery_base import CardViewer
from PySide6.QtCore import Qt

class RowGallery(GalleryBase):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configRowGallery()

    def __configRowGallery(self):
        self.CARDS = []
        self.AR = 6/4
        self.setRowCount(1)
        # .setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def addImage(self, img:str):
        if img not in self.CARDS:
            self.CARDS.insert(0, img)
            self.setColumnCount(len(self.CARDS))
            self.reloadImages()

    def reloadImages(self):
        # self.clearContents()
        for ic, img in enumerate(self.CARDS):
            cv = CardViewer()
            cv.setImage(img)
            item = QTableWidgetItem(str(ic))
            self.setItem(0, ic, item)
            self.setCellWidget(0, ic, cv)
        self.heightAuto()




class GalleryChapters(GalleryBase):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configGalleryChapters()

    def __configGalleryChapters(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def setHeightRow(self, n:int):
        self.setCurrentCell(0, 0)
        for i in range(self.rowCount()):
            self.setRowHeight(i, n)

    def addImage(self, img:str):
        irow = self.currentRow()
        rgallery = self.cellWidget(irow, 0)
        if not rgallery:
            rgallery = RowGallery()
            print('nottt')
        rgallery.addImage(img)

        item = QTableWidgetItem('row gallery')
        self.setItem(irow, 0, item)
        self.setCellWidget(irow, 0, rgallery)
        # self.heightAuto()

