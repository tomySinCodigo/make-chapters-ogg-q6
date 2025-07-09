import os
import logging
from pathlib import Path
from random import randint


class SearchFiles:
    """obtener archivos de `path` (imagenes)"""
    def __init__(self, path:str) -> None:
        self.path = Path(path).as_posix()
        self.d = self._getAll(self.path)

    def error(self, err, msg:str="") -> None:
        if msg:
            msg = f'[{self.__class__.__name__}]{msg} -- '
        logging.error(f'{msg}{err}')

    def _getAll(self, path:str) -> dict:
        """obten todos los archivos: {dirs:[...], files:[...]}"""
        d = {'dirs':[], 'files':[]}
        try:
            with os.scandir(path) as files:
                for file in files:
                    _ = 'files' if file.is_file() else 'dirs'
                    d[_].append(Path(file).as_posix())
        except FileNotFoundError as efile:
            self.error(f'getAll, {efile}')
        except Exception as e:
            self.error(e)
            raise
        finally:
            return d
    
    def getDirs(self) -> list:
        """obten solo los directorios"""
        return self.d.get('dirs')
    
    def getFiles(self) -> list:
        """obten solo los archivos"""
        return self.d.get('files')
    
    def bySuffix(self, suffixes:list=[], ex:list=[]) -> list:
        suffixes = [s.lower() for s in suffixes]
        files = [f for f in self.getFiles() \
                 if Path(f).suffix.lower() in suffixes]
        res = [file for file in files \
            if not any(pal.lower() in file.lower() for pal in ex)]
        return res
    
    def getImages(self, suffixes:list=['.jpg', '.png', '.gif', '.jpeg'], ex:list=[]) -> list:
        """obten imagenes suffixes:[formatos] ex:[excluye]"""
        return self.bySuffix(suffixes=suffixes, ex=ex)
    
    def getImageByDir(self, **kwargs) -> str:
        """obten un cover (imagen) por directorio"""
        images = self.getImages(**kwargs)
        img = Path(images[randint(0, len(images)-1)]) if images else None
        if img:
            return {
                'path':img.as_posix(),
                'dir':img.parent.as_posix(),
                'dirname':img.parent.stem,
                'name':img.stem
            }
        else:
            return None
    
    def getCovers(self) -> list[dict]:
        """obten una lista de diccionarios (1 cover por directorio)"""
        covers = []
        for dir in self.getDirs():
            sf = SearchFiles(dir)
            images = {Path(img).stem:img for img in sf.getImages()}
            dirname = Path(dir).stem
            d = {
                'dir':dir,
                'dirname':dirname,
                'images':images
            }
            if dirname in images.keys():
                d['cover'] = images[dirname]
            elif 'cover' in images.keys():
                d['cover'] = images['cover']
            elif 'portada' in images.keys():
                d['cover'] = images['portada']
            else:
                img = sf.getImageByDir()
                if img:
                    d['cover'] = img.get('path')
                else:
                    d['cover'] = 'defo.png'
            covers.append(d)
        return covers


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

    # obten imagen (cover) de cada carpeta
    # print(sf.getImageByDir())
    # r1 = 'T:/TAG/RECURSOS/personajes2'
    # sf = SearchFiles(r1)
    # pprint(sf.getCovers())
