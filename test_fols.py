from qwidgets.funciones import SearchFiles
from pprint import pprint
import os
from pathlib import Path

r1 = 'T:/TAG/RECURSOS/personajes2'
def uno():
    sf = SearchFiles(path=r1)
    folder = sf.getDirs()
    print("===")
    pprint(folder)

def allFiles(path_dir:str) -> list:
    files = []
    def getFiles(path:str):
        with os.scandir(path) as fs:
            for f in fs:
                if f.is_file():
                    files.append(Path(f).as_posix())
                elif f.is_dir():
                    getFiles(f.path)
    getFiles(path_dir)
    return files

def getImageWall(folder:str):
    sf = SearchFiles(folder)
    images = sf.getImages()
    return images


li = allFiles(r1)
pprint(li)