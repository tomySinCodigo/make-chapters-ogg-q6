from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QSlider
from pathlib import Path
from qwidgets.viewer import Card


class CardViewer(Card):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__configCardViewer()

    def __configCardViewer(self):
        self.data = {}

    def setImage(self, image_file):
        path = Path(image_file)
        self.data['path'] = path.as_posix()
        self.data['stem'] = path.stem
        super().setImage(image_file)
        
    def set(self, kwargs):
        self.data.update(kwargs)

    def get(self, key:str) -> str|int|None:
        return self.data.get(key)
    
    def setData(self, dc:dict, image='image'):
        img = dc.get(image)
        dirname = dc.get('dirname')
        # if img:
        self.setImage(image_file=img)
        self.set(dc)
        self.setOverlay(
            text=dirname,
            bg='rgba(0,0,0,120)',
            fg='rgba(255,255,255, 210)'
        )
        self.setTitle(dirname)


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
        """limpia y agrega las cantidad de celdas indicadas"""
        self.clearContents()
        self.setRowCount(rows)
        self.setColumnCount(cols)

    def columnsEquals(self):
        """ajustar el ancho de las columnas (para que sean iguales)"""
        self.hh.setSectionResizeMode(QHeaderView.Stretch)

    def heightAuto(self):
        """ajusta la altura de la celda, segun AR"""
        h = int(self.hh.sectionSize(0)/self.AR)
        for irow in range(self.rowCount()):
            self.setRowHeight(irow, h)

    def getIndexes(self, n:int, cols:int=3) -> list:
        """obten una lista con indices de cada celda para n:items"""
        return [(irow, icol) \
            for irow, _ in enumerate(range(0,n,cols)) \
            for icol in range(cols)]
    
    def setImages(self, files:list|dict, cols:int=3):
        indexes = self.getIndexes(len(files), cols=cols)
        nrows = indexes[-1][0]+1
        self.setRowCol(rows=nrows, cols=cols)
        self.columnsEquals()
    
        for index, file in enumerate(files):
            if isinstance(file, dict):
                d = files.pop(index)
                files.insert(0, d)

        for index, file in enumerate(files):
            if isinstance(file, dict):
                image = file.get('path')
                name = file.get('dirname')
            else:
                image = file
                name = Path(file).stem
            cv = self._setImage(image, name)

            item = QTableWidgetItem(str(index))
            ix = indexes[index]
            self.setItem(ix[0], ix[1], item)
            self.setCellWidget(ix[0], ix[1], cv)
            cv.setNum(index, bg='black', fg='white')
        self.heightAuto()
        
    def _setImage(self, image:str, name:str):
        cv = CardViewer()
        cv.setImage(image_file=image)
        cv.setOverlay(
            text=name,
            bg='rgba(0,0,0,120)',
            fg='rgba(255,255,255, 210)'
        )
        cv.setTitle(name)
        return cv
    
    def _setImageData(self, dc:dict):
        cv = CardViewer()
        cv.setData(dc=dc, image='cover')
        return cv
    
    def selectCard(self, row:int=None, col:int=None) -> CardViewer:
        wg = self.cellWidget(row, col)
        if wg:
            # name, path = wg.get('stem'), wg.get('path')
            # print("wg::: ", wg.d)
            # return name, path
            return wg

    def setCovers(self, data:list, cols:int=3) -> None:
        indexes = self.getIndexes(len(data), cols=cols)
        self.setRowCol(rows=indexes[-1][0], cols=cols)
        self.columnsEquals()

        for index, d in enumerate(data):
            # img = d.get('cover')
            # name = d.get('dirname')
            # cv = self._setImage(image=img, name=name)
            cv = self._setImageData(dc=d)

            item = QTableWidgetItem(str(index))
            ix = indexes[index]
            self.setItem(ix[0], ix[1], item)
            self.setCellWidget(ix[0], ix[1], cv)
            # cv.set(path=d.get('path'))
        self.heightAuto()
