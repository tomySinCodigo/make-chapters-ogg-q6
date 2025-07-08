from pathlib import Path
import os
from random import randint


class SearchFiles:
    def __init__(self, path:str):
        self.path = Path(path).as_posix()
        self.d = self._getAll(self.path)

    def _getAll(self, path:str) -> dict:
        d = {'dirs':[], 'files':[]}
        with os.scandir(path) as files:
            for file in files:
                _ = 'files' if file.is_file() else 'dirs'
                d[_].append(Path(file).as_posix())
        return d
    
    def getDirs(self) -> list:
        return self.d.get('dirs')
    
    def getFiles(self) -> list:
        return self.d.get('files')
    
    def bySuffix(self, suffixes:list=[], ex:list=[]) -> list:
        suffixes = [s.lower() for s in suffixes]
        files = [f for f in self.getFiles() \
                 if Path(f).suffix.lower() in suffixes]
        res = [file for file in files \
            if not any(pal.lower() in file.lower() for pal in ex)]
        return res
    
    def getImages(self, suffixes:list=['.jpg', '.png', '.gif', '.jpeg'], ex:list=[]) -> list:
        # return {Path(path).stem:path for path in self.bySuffix(suffixes=suffixes, ex=ex)}
        return self.bySuffix(suffixes=suffixes, ex=ex)
    
    def getWalls(self) -> list:
        data = []
        folders = self.getDirs()
        for folder in folders:
            sf = SearchFiles(folder)
            images = {Path(img).stem:img for img in sf.getFiles()}
            name_folder = Path(folder).name.lower()
            d = {
                'name':name_folder,
                'path':folder,
                'images':images,
                'dir':folder
            }
            if name_folder in images.keys():
                d['wall'] = images[name_folder]
            elif 'portada' in images.keys():
                # sf = SearchFiles(folder)
                # imgs = {Path(img).stem:img for img in sf.getFiles()}
                d['wall'] = images['portada']
            else:
                d['wall'] = 'defo.png'
            data.append(d)
        return data
    
    def getOneImage(self, *args) -> str:
        images = self.getImages(*args)
        if images:
            return images[randint(0, len(images))-1]
        else:
            return []
        
    def getOneImageData(self, *args) -> dict:
        images = self.getImages(*args)
        if images:
            d = {}
            _ = Path(images[randint(0, len(images))-1])
            d['path'] = _.as_posix()
            d['parent'] = _.parent
            d['dirname'] = _.parent.stem
            d['name'] = _.stem
            return d
        else:
            return None
    


if __name__ == '__main__':
    from pprint import pprint
    # r1 = 'T:/TAG/EJECUTABLES/RECURSOS/pro_plex/modelos'
    # sf = SearchFiles(r1)
    # res = sf.getFiles()
    # res = sf.bySuffix(['.jpg', '.png'], ex=['ava'])
    # res = sf.getImages()
    # print(f'TIPO:: {type(res)}')
    # pprint(res)
    # print(f'TIPO:: {type(next(res))}')
    # print(next(res))

    # obten imagen (wall) de cada carpeta
    # r1 = 'T:/TAG/RECURSOS/personajes2'
    # rser = "T:/TAG/RECURSOS/personajes2/sono bisque doll/Marin Kitagawa"
    # sf = SearchFiles(rser)
    # print(sf.getOneImage())