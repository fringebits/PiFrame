
import logging
import os
from .photo import Photo

class Folder:
    PhotoExtensions = ['.jpg', '.png']

    def __init__(self, basepath, recurse):
        self.basepath = basepath
        self.recurse = recurse
        self.Info()

    def Info(self):
        logging.debug(f"Folder: path={self.basepath}, recurse={self.recurse}")

    def Scan(self):
        files = self.ScanInternal(self.basepath, self.recurse)
        logging.debug(f"Imported {len(files)} from path={self.basepath}, recurse={self.recurse}")
        return files

    def ScanInternal(self, filepath, recurse):
        dirfiles = os.listdir(filepath)
        fullpaths = map(lambda name: os.path.join(filepath, name), dirfiles)
        dirs = []
        files = []
        for file in fullpaths:
            logging.debug(f"\t{file}")
            if os.path.isdir(file): dirs.append(file)
            if os.path.isfile(file):
                (name, ext) = os.path.splitext(file)
                if ("SYNOPHOTO_THUMB" not in name) and  (ext in self.PhotoExtensions):
                    files.append(Photo(file))

        if recurse == True:
            for path in dirs:
                files = files + self.ScanInternal(path, recurse)
            
        return files

class FolderImport:
    def __init__(self):
        self.folders = []

    def AddPath(self, path, recurse):
        logging.debug(f"FolderImport: path=[{path}], recurse={recurse}")
        self.folders.append(Folder(path, recurse))

    def Run(self):
        logging.debug(f"FolderImport, scanning for files")
        files = []

        for folder in self.folders:
            files = files + folder.Scan()

        logging.debug(f"FolderImport, imported {len(files)}")
        return files