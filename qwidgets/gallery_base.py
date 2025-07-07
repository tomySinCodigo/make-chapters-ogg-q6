from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QSlider
from pathlib import Path
from qwidgets.viewer import Card


class CardViewer(Card):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configCardViewer()

    def __configCardViewer(self):
        self.STEM = None
        self.PATH = None
        self.DATA = None

    def setImage(self, image_file):
        path = Path(image_file)
        self.PATH = path.as_posix()
        self.STEM = path.stem
        super().setImage(image_file)

    def setData(self, dc:dict) -> None:
        self.DATA = dc
        if 'name' in dc.keys():
            self.STEM = dc.get('name')
        if 'path' in dc.keys():
            self.PATH = dc.get('path')



class GalleryBase(QTableWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configGalleryBase()

    def __configGalleryBase(self):
        self.hh = self.horizontalHeader()
        self.vh = self.verticalHeader()
        self.hh.setVisible(False)
        self.vh.setVisible(True)
        self.AR = 4/6

    def setRowCol(self, rows:int, cols:int):
        self.clearContents()
        self.setRowCount(rows)
        self.setColumnCount(cols)

    def columnsEquals(self):
        self.hh.setSectionResizeMode(QHeaderView.Stretch)

    def heightAuto(self):
        h = int(self.hh.sectionSize(0)/self.AR)
        for irow in range(self.rowCount()):
            self.setRowHeight(irow, h)

    def getIndexes(self, n:int, cols:int=3) -> list:
        return [(irow, icol) \
            for irow, _ in enumerate(range(0,n,cols)) \
            for icol in range(cols)]
    
    def setImages(self, images:list, cols:int=3):
        indexes = self.getIndexes(len(images), cols=cols)
        print('indexes:: ', indexes)
        print(indexes[-1][0])
        self.setRowCol(rows=indexes[-1][0]+1, cols=cols)
        self.columnsEquals()

        for i, img in enumerate(images):
            cv = CardViewer()
            cv.setImage(image_file=img)
            item = QTableWidgetItem(str(i))
            ix = indexes[i]
            self.setItem(ix[0], ix[1], item)
            self.setCellWidget(ix[0], ix[1], cv)
            # print('rc: ', ix[0], ix[1], img)
            cv.setNum(i, bg='black', fg='white')
            cv.setOverlay(
                text=Path(img).stem,
                bg='rgba(0,0,0,120)',
                fg='tgba(255,255,255, 210)'
            )
            cv.setTitle(Path(img).stem)
        self.heightAuto()

    def selectCard(self, row=None, col=None):
        wg = self.cellWidget(row, col)
        if wg:
            name, path = wg.STEM, wg.PATH
            return name, path
        
    def setWalls(self, data:list, cols:int=3) -> None:
        indexes = self.getIndexes(len(data), cols=cols)
        self.setRowCol(rows=indexes[-1][0], cols=cols)
        self.columnsEquals()

        for index, d in enumerate(data):
            cv = CardViewer()
            cv.setImage(image_file=d.get('wall'))
            item = QTableWidgetItem(str(index))
            ix = indexes[index]
            self.setItem(ix[0], ix[1], item)
            self.setCellWidget(ix[0], ix[1], cv)
            cv.setNum(index, bg='black', fg='white')
            cv.setOverlay(
                text=d.get('name'),
                bg='rgba(0,0,0,120)',
                fg='tgba(255,255,255, 210)'
            )
            cv.setTitle(text=d.get('name'))
            cv.setData(dc=d)
        self.heightAuto()