from pathlib import Path
import os


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
    
    def getDirs(self):
        return self.d.get('dirs')
    
    def getFiles(self):
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
    


if __name__ == '__main__':
    from pprint import pprint
    r1 = 'T:/TAG/EJECUTABLES/RECURSOS/pro_plex/modelos'
    sf = SearchFiles(r1)
    # res = sf.getFiles()
    # res = sf.bySuffix(['.jpg', '.png'], ex=['ava'])
    res = sf.getImages()
    print(f'TIPO:: {type(res)}')
    pprint(res)
    # print(f'TIPO:: {type(next(res))}')
    # print(next(res))