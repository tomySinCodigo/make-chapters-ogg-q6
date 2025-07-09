# gallery base

usa un temporizador para redimensionar las imagenes para que no rediemncione muchas veces

```python
self.timer = QTimer()
self.timer.setSingleShot(True)
self.timer.timeout.connect(self.accion_redimension)


def accion_redimension(self):
    print("redimensionado")
    self.wg.heightAuto()


def onSplitMoved(self, pos, index):
    self.timer.start(400)

def resizeEvent(self, event):
    self.timer.start(300)
```

para redimencionar el alto de las celdas ya no use `QHeaderView` es mas efectivo usar `setRowHeight` pero este necesita el indice de cada fila

```python
def heightAuto(self, ar:float=4/6):
    h = int(self.hh.sectionSize(0)/ar)
    for irow in range(self.rowCount()):
        self.setRowHeight(irow, h)
```

## Test select

obtiene las imagenes pero las que no encuentra en las carpetas usa 'defo.png' por default, pero esto provoca que la ruta obtenida no sea la correcta en `setImages`

obtiene las imagenes de cada folder y al seleccionar la imagen se obtiene las imagenes del subfolder, ademas al seleccionar la carpeta `00` obtiene todas las imagenes de las carpetas y subcarpetas

**funciones** 

al obtener los indices con `getIndexes` hace falta sumar +1 para obtener la cantidad correcta de filas


**gallery base**

- ahora obtiene un diccionario en lugar de un `path` (str)
- reemplazo de `cover` por `path` al no tener un cover retornaba None (setImages)

